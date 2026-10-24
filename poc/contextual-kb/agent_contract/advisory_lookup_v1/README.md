# Working foundation + advisory GLiNER lookup

This POC integration runs the retained GLiNER extractor alongside the accepted qualification_v3 question plan and the unchanged full-question retrieval path. GLiNER is enabled by default. No training, query expansion, evidence filtering or answer generation occurs.

## Use

The calling agent first follows [the foundation contract](../qualification_v3/CONTRACT.md) to produce its structured plan. Supply one JSON object with exactly `request` (original text) and `question_plan` (the foundation output). [example-input.json](example-input.json) is a saved first foundation response, not a hard-coded planner.

From the repository root:

```sh
poc/contextual-kb/.venv/bin/python -B \
  poc/contextual-kb/agent_contract/advisory_lookup_v1/cli.py \
  --input poc/contextual-kb/agent_contract/advisory_lookup_v1/example-input.json
```

This prints JSON. Add `--output <new-file.json>` to save without overwriting, or `--seed 1702` to use the other retained adapter. The default1701 is a stable administrative choice, not a claimed quality winner. `--without-gliner` is the foundation-only diagnostic control.

The existing retrieval and GLiNER POC virtual environments, local GLiNER base/adapters, read-only knowledge DB and copied offline embedding cache must be present. No downloads/installations are performed. The first request pays model-loading cost. Applications within this POC can reuse `AdvisoryLookup(index, extractor_factory)` across requests to load GLiNER once; create `ProcessExtractor(seed)` in that factory, call `verify_unchanged()` at the end of a verification session, and always `close()` the worker in a finally block. The worker uses the existing gliner_feasibility/env/.venv environment; the parent uses .venv for retrieval. This is a local Python/CLI integration, not a newly registered MCP server or hosted reasoning service.

## Output and authority

- `plan.question_plan` and `plan.search_requests`: unchanged authoritative foundation input and complete query texts.
- `plan.role_hints`: extracted exact spans with question index and role; every hint has `usable_as_filter: false`.
- `advisory`: available/degraded/disabled/not_needed status and explicit diagnostics. Unavailable extraction does not remove the search path.
- `extractions`: raw native results, errors and per-question times.
- `retrieval`: the actual full-question searches and existing merged fact IDs, at most8.
- `facts`: copies of the original candidate records with claims, conditions, limits and available catalog metadata. `evidence_status: candidate_only` means neither relevance nor full answer support has been certified.
- CLI `runtime`: selected adapter, model integrity checks and DB integrity check.

Role labels cover API references, registration names, model keys, values, version tokens and UI adapters. Structurally valid hints can still have wrong roles; consumers must not use them as filters or proof that a named API exists. Hints are not fed into retrieval at all. An invalid foundation plan fails explicitly; retrieval failures also propagate.

## Test

```sh
python3 -B -m unittest discover \
  -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'
```

Actual verification outputs live in test-output/live-native. The initial missing-torch run remains in test-output/live; see ENVIRONMENT-RECOVERY.md. verify_live.py is an exclusive first-run harness and intentionally refuses to overwrite that evidence. Both frozen seeds are tested against identical foundation-only retrieval. Fresh cases and previous realistic plans test integration invariants, not a newly measured90% annotation or answer-accuracy target. Existing model/data/DB files and all prior candidates remain unchanged; evaluation remains sealed.
