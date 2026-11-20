"""Our own repeatable prompt matrix for the live model-free flow.

Not sealed evaluation. planner_cases/sealed/, evaluation/ and qualification/
stay separate and untouched by this file. This is an informal, iterable dev
harness: our own test prompts, run through the exact composition the real
launcher serves for model-free mode --

    mcp_runtime.launcher.start_model_free
      -> parity_v1.serve_discovery.create_discovery_server
         -> model_free_repair_v1.serve.create_server
            -> model_free_v1.candidate.Store / Service

-- and scored against fact IDs picked by hand from the installed, un-sealed
authored knowledge (poc/contextual-kb/authored/, same facts the DB is built
from). It answers one question: for a question a developer would plausibly
ask, does the real flow actually surface the fact that answers it, and at
which stage (first page, or only after discovery)?

Read-only against the installed DB; no model-backed/hosted calls. Add cases
to cases.json and re-run any time retrieval, the question-layer or the
repair/discovery wrapping changes.

Usage, from poc/contextual-kb: .venv/bin/python -B prompt_matrix/run.py
"""
import asyncio
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
POC = HERE.parent
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
sys.path.insert(0, str(POC / 'model_free_repair_v1'))
sys.path.insert(0, str(POC / 'parity_v1'))

from candidate import Service, Store  # noqa: E402
from feedback import RepairService  # noqa: E402
from discovery import discover  # noqa: E402


def make_plan(request, adapter, questions=None, formly_version='6.3.12'):
    if questions is None:
        questions = [dict(question=request, reason='Identify the fact(s) answering this question')]
    else:
        questions = [dict(question=q['question'], reason='Identify the fact(s) answering this question')
                     for q in questions]
    return dict(
        formly_questions=questions,
        library_constraints=dict(formly_version=formly_version, ui_adapter=adapter),
        condition_bindings=[],
    )


def build_service():
    # Use mcp_runtime/launcher.py's own pin, not model_free_v1/baseline-state.json's:
    # the latter is stale against the installed DB (confirmed when building this
    # harness) and would raise IntegrityError here even though the real launcher
    # starts fine. See prompt_matrix/README.md.
    sha = json.loads((POC / 'mcp_runtime/model-free.json').read_text())['files']['build/knowledge.sqlite']
    store = Store(POC / 'build/knowledge.sqlite', sha)
    settings = HERE / 'test-output/settings.sqlite'
    settings.parent.mkdir(parents=True, exist_ok=True)
    return RepairService(Service(store, settings)), store


async def run_status_case(service, case):
    """A case that expects a specific packet status (no_evidence/unsupported_scope/...),
    not a delivered fact -- e.g. a question genuinely outside the corpus, or an
    explicitly unsupported Formly version."""
    plan = make_plan(case['request'], case['adapter'], formly_version=case.get('formly_version', '6.3.12'))
    started = time.perf_counter()
    packet, error = await service.lookup(case['request'], plan=plan)
    seconds = round(time.perf_counter() - started, 4)
    outcome = dict(id=case['id'], status=packet.get('status'), is_error=error, seconds=seconds)
    outcome['result'] = 'status_match' if packet.get('status') == case['expect_status'] else 'status_mismatch'
    if outcome['result'] == 'status_mismatch':
        outcome['detail'] = packet
    return outcome


async def run_multi_question_case(service, case):
    """A plan with more than one formly_question, exercising the real per-question
    interleaving/depth split (model_free_v1/candidate.py) instead of the single-
    question path every other case uses."""
    plan = make_plan(case['request'], case['adapter'], questions=case['questions'])
    started = time.perf_counter()
    packet, error = await service.lookup(case['request'], plan=plan)
    seconds = round(time.perf_counter() - started, 4)
    outcome = dict(id=case['id'], status=packet.get('status'), is_error=error, seconds=seconds)

    if packet.get('status') not in ('ok', 'no_evidence'):
        outcome['result'] = 'blocked_before_retrieval'
        outcome['detail'] = packet
        return outcome

    page, _ = await discover(service, case['request'], plan=plan)
    candidates = {c['id'] for c in page.get('candidates', [])}
    outcome['discovery_candidates'] = sorted(candidates)
    sub_results = []
    for i, q in enumerate(case['questions']):
        expected = set(q['expected_fact_ids'])
        delivered = set(packet['questions'][i]['fact_ids'])
        if expected & delivered:
            sub_results.append('direct_hit')
        elif expected & candidates:
            sub_results.append('discoverable_only')
        else:
            sub_results.append('missed')
    outcome['sub_results'] = sub_results
    # Worst sub-result stands for the whole case.
    outcome['result'] = ('missed' if 'missed' in sub_results
                          else 'discoverable_only' if 'discoverable_only' in sub_results
                          else 'direct_hit')
    return outcome


async def run_case(service, case):
    if 'expect_status' in case:
        return await run_status_case(service, case)
    if 'questions' in case:
        return await run_multi_question_case(service, case)
    plan = make_plan(case['request'], case['adapter'])
    started = time.perf_counter()
    packet, error = await service.lookup(case['request'], plan=plan)
    seconds = round(time.perf_counter() - started, 4)
    outcome = dict(id=case['id'], status=packet.get('status'), is_error=error, seconds=seconds)
    expected = set(case['expected_fact_ids'])

    if packet.get('status') not in ('ok', 'no_evidence'):
        outcome['result'] = 'blocked_before_retrieval'
        outcome['detail'] = packet
        return outcome

    delivered = {f['id'] for f in packet.get('facts', [])}
    outcome['delivered'] = sorted(delivered)
    if expected & delivered:
        outcome['result'] = 'direct_hit'
        return outcome

    # Not on the first page: would a real calling agent find it via discovery?
    page, _ = await discover(service, case['request'], plan=plan)
    candidates = {c['id'] for c in page.get('candidates', [])}
    outcome['discovery_candidates'] = sorted(candidates)
    outcome['result'] = 'discoverable_only' if expected & candidates else 'missed'
    return outcome


async def main():
    cases = json.loads((HERE / 'cases.json').read_text())
    service, store = build_service()
    try:
        results = [await run_case(service, case) for case in cases]
    finally:
        store.close()

    out_dir = HERE / 'test-output'
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'results.json').write_text(json.dumps(results, indent=2))

    counts = {}
    for r in results:
        counts[r['result']] = counts.get(r['result'], 0) + 1
    print(json.dumps(dict(total=len(results), **counts), indent=2))
    clean = ('direct_hit', 'status_match')
    for r in results:
        if r['result'] not in clean:
            extra = f" ({r.get('status')})" if r.get('status') else ''
            print(f"  {r['id']}: {r['result']}{extra}")
    failing = counts.get('missed', 0) + counts.get('blocked_before_retrieval', 0) + counts.get('status_mismatch', 0)
    return 0 if failing == 0 else 1


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
