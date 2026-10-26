# Supplied-premise clarification candidate v2

This isolated candidate clarifies when a factual assertion supplied by the user
is a condition of a requested implication lookup. It preserves that assertion as
an unverified premise, including attribution and uncertainty, in each applicable
standalone question and a source-exact nonempty ledger binding. A mere API or
operation target remains requested information and does not acquire an artificial
noun-only binding. Existing local scope, independence, correction, shared-context
and support-caveat rules continue to apply.

The only generation change is an appended prospective section in CONTRACT.md.
Its illustrative contrasts use hide and defaultValue; they neither assert facts
about those APIs nor provide library answers. The frozen prior contract remains
the exact prefix. planner.py and plan.schema.json are byte-identical copies of
condition_candidate_v1. Their relative paths select this directory's contract and
schema. The one-shot generation process, model, effort, decoding, strict validator,
CapitalizingPlanner, capitalization handling and no-retry behavior are unchanged.
There is no new semantic classifier, inferred index, case folding or repair.

No existing candidate, installed runtime, knowledge source, DB, model, evaluation
or historical grade is changed. The candidate is not promoted. This work does not
establish whole-library compatibility or retrieval/answer quality.

## Offline verification and its limits

Run from the repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/condition_candidate_v2 -p test_planner.py -v
```

All 18 tests passed: 12 inherited v1 regressions run with the v2 candidate selected
and six additional tests covering runtime/schema identity, attributed and uncertain
premise fixtures, target-only fixtures, local applicability, missing declared
question excerpts and the validator's missing-both limitation. The inherited
historical failure fixture remains in v1 and is imported unchanged; no historical
question-specific example was added to the generation contract.

These fixture checks show what the existing validator accepts and rejects. They
do not run a hosted planner, prove semantic classification or demonstrate that
the new prompt fixes generation. A premise dropped from both prose and ledger
still passes validation, which the test suite deliberately records. Likewise,
exact-copy validation cannot prove attribution, appropriate attachment, or that
all source conditions have been declared. The contract-prefix assertion is a
preservation check, not semantic evidence.

This is a prompt-content-only change, so no artificial failing implementation test
was manufactured. Any future logic change requires a failing behavioral test
first. Live contrast checks and independent semantic review must assess generation
separately before any promotion; those are run and recorded by the coordinating
harness, not by this offline suite. The repository maintenance command remains
`python3 tools/project.py check`; the coordinating task owns its aggregate run.

Codebase-memory Tier 2 coverage at generation 2026-10-25T14:19:41Z reported the
four v1 evidence files as not tracked. Those files were read directly as the
coverage fallback; no graph completeness claim is made.
