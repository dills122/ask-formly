# Validation harness author explanation

## Scope and intent

This batch compares the frozen installed foundation5 (70facts/15documents) with an isolated proposed79-fact/17-document candidate. Changes are restricted to validation-v1. No build or inference was performed during harness preparation, and no installed DB, runtime, model, compiler, catalog or canonical source was edited.

## Approach

The candidate builder, evaluator, matched-plan replay and fixed-denominator summarizer are copied from the reviewed extensions-v2 harness. `assess.py`, `delivery.py`, `replay.py`, `summarize.py`, answer/grade schemas and `GRADER.md` remain byte-identical. The builder retains exclusive candidate paths, exact source/candidate hashes, source offset checks, five-table row preservation and actual runtime eligibility; it now requires79facts/17documents through an explicit count guard. Source curation confirms all needed evidence IDs already exist, so no catalog entries are appended.

The current experiment already uses the accepted CapitalizingPlanner and latest mcp_v1.create_server, including project/version context. Both arms use that same composition and differ only in the checked read-only DB path. Backend lookup, extraction, selection and closure remain inherited from the accepted implementation. `baseline-state.json` pins166 protected runtime/model/source files and the installed70DB hash. Freeze batch-owned draft inputs and code after independent review, before building.

The caller adds the previously reviewed invocation-only lookup allowlist and lookup_formly approval override from promotion-v4. The user authorized these lookups. Neither global configuration nor sandbox policy changes; settings-write tools are not enabled. This is necessary because the current server correctly advertises lookup as potentially state-writing when optional project IDs/settings are supplied. Test requests concern library questions only. `run_agent` additionally rejects output paths outside this batch or through aliases before creating directories.

## Questions and acceptance

Qualification has10fresh targeted questions V01–V10 and five unchanged regression/gap controls copied exactly from extensions-v2: E05,M03,Q20,Q21,Q24. The five development requests are separate and are excluded from qualification. Questions cover all nine proposed facts, including typing/runtime differences and limits that should remain explicit gaps. Exact message precedence and universal routed-error cleanup are not demanded.

Three repeats use1701/1702/1701, with arm order counterbalanced per batch. Require at least14/15 usable answers each repeat, all controls, no critical/delivery failures and no regression on baseline-supported cases. Support IDs are retrieval diagnostics, not the semantic grade. Missing and duplicate assessments remain in fixed denominators.45paired normalized-plan replays are packet diagnostics, not another45final answers. Independent answer audit remains required; no tuning during qualification.

## Verification

Ten standalone tests pass under the existing MCP environment: six batch tests plus four reused candidate-isolation fixtures. Initial new-module tests failed before implementation (`tdd-red.txt`), then passed. The added explicit size guard demonstrated a separate missing-function failure before implementation (`tdd-count-red.txt`). A canonical-path fixture initially used macOS's temporary-path alias and was corrected to resolve its temporary root, without weakening production checks. The extra valid-candidate-path assertion is supplementary, not claimed to demonstrate a newly discovered production bug. Final receipt: `test-output/tdd-final-green.txt`.

The tests verify correct/rejected DB arms, digest drift, non-overwrite, candidate-path redirection, exact count drift, invocation-only approval and output confinement. They do not establish actual retrieval/answer quality, nor claim execution of upstream Angular/Formly tests.

## Commands after independent review and freeze

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/validation-v1 -p 'test_*.py'
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/validation-v1/candidate.py
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/validation-v1/experiment.py agents --cases poc/contextual-kb/knowledge-expansion/validation-v1/qualification-cases.json --name qualification-1 --repeats 3 --batch-size 5
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py --implementation validation-v1 --root poc/contextual-kb/knowledge-expansion/validation-v1/test-output/qualification-1 --cases poc/contextual-kb/knowledge-expansion/validation-v1/qualification-cases.json --repeats 3 --arms baseline,candidate
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/validation-v1/replay.py --root poc/contextual-kb/knowledge-expansion/validation-v1/test-output/qualification-1 --cases poc/contextual-kb/knowledge-expansion/validation-v1/qualification-cases.json --repeats 3
```

No build/inference command above has been executed by the harness worker. Outputs are exclusive; retain any failed attempt and investigate rather than silently retrying. Parent owns the review/freeze/build/run/outcome sequence and current-project maintenance check.
