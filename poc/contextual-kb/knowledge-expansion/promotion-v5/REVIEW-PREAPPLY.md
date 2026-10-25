# Independent preapply review

Review instance: 1 of 3. HEAD a3240d33bed5ae82aa779a0004f80c8894924a97, branch codex/knowledge-admission-70. Scope: untracked promotion-v5, validation-v1 qualification/publication context, and tools/project.py plus tools/test_project.py source-suite wiring. Reviewer changed only review artifacts and isolated preflight output; no apply, hosted calls, model writes or sealed reads.

## Findings

No actionable findings. Preliminary source/test inspection preceded REVIEW-AUTHOR.md. Initial checks focused on exact candidate authorization pins, accepted-source preservation, rollback, fixture-only CI imports, and distinguishing the installation smoke from prior qualification. The task bootstrap necessarily disclosed the intended transition and prior qualification result before the blind pass; author rationale was read afterward.

## Plan Review

The plan implements the explicitly authorized foundation5-to-foundation6 transition: two additional canonical authored files, the exact qualified DB, and two updated manifests. Old authored bytes, catalog bytes, compiler/schema/runtime and 85 non-DB foundation pins remain unchanged. Five-table old-row preservation and canonical rebuild equality gate application. Snapshot and journal precede writes; postchecks validate installed bytes and reproduce from canonical inputs. The documented ordinary-error/interruption rollback matches code and injected-failure fixtures. Power loss/SIGKILL is accurately excluded from atomicity guarantees.

One installed smoke repeat of 15 answers, seed1701, is separate from the earlier candidate qualification of 45 answers across three repeats. The plan requires all 15 usable, all controls, zero critical/delivery failures and independent outcome audit before publication. That later gate remains pending. Public Git must exclude test-output, candidate DB/input products, environments, models and private archives.

## Author-Claim Reconciliation

| Claim | Evidence | Status |
| --- | --- | --- |
| Promotion guard is narrow adaptation of prior migration | Exact v4/v5 diff and full guard source | Confirmed; only addition names, batch, foundation IDs and counts change. |
| Stable caller implementation is reused | Byte comparisons of run.py, merged_run.py and test_merged_run.py | Confirmed. |
| Candidate and prior qualification are pinned | promotion-spec.json, prior REVIEW-FINAL.md, independent preflight | Confirmed; exact candidate hash 226c377ecb4a8a220c5c6db541156c3dcad71045d73b21a5d205fbf164b7715b. |
| Candidate preserves accepted data and reproduces | Independent preflight receipt | Confirmed:17 documents,79 facts,46 evidence,122 fact_evidence,70 fact_links; all five tables reproduce. |
| Cases remain fixed | Byte comparison against validation-v1/qualification-cases.json | Confirmed; copied three-repeat metadata is historical candidate criteria, while PLAN.md explicitly defines one installation smoke repeat. |
| Source-only checks avoid heavy harness imports | tests and transitive candidate/evaluate imports | Confirmed for the newly selected fixture suites. |

## Verification Performed

Independently executed successfully:

- `python3 -B -m unittest discover -s tools -p test_project.py`:4 tests.
- `poc/contextual-kb/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/validation-v1 -p test_candidate.py`:4 tests.
- `python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/validation-v1 -p test_evaluate.py`:6 tests.
- `python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v5 -p 'test_*.py'`:12 tests, including rollback, interruption, partial-write failure, drift/path rejection and narrow lookup authorization.
- Compiler-environment `promote.py --name preflight-independent-review-1`:checked-only, canonical reproduction equal,85 runtime/model pins verified.

Installed DB remained a5fbfd098fe59b3f80090d3cf1551700542d82cee77aaa7c4ccc2d5023d84929 after preflight. Reviewed promote.py SHA-256:18c4412fa2c7458f881228dae7c9830057970e1de4d9a0fcfa8978f1c694bb72; promotion-spec.json:47c1da684e743d2f42578864dfefb65998fa7f3d2dcc7360720d31a1ec7e5fd1.

Graph lookup returned no source_checks symbol; coverage marked tools excluded and new promotion/validation files untracked (generation2026-10-25T14:19:41Z). Relevant exact source was read directly; no absence or completeness claim relies on graph metadata.

## Open Questions And Residual Risks

Installed outcome, full maintenance suite,15actual smoke answers, final documentation and public staged-file boundary are not yet available. Prior candidate independent review is accepted as retained qualification evidence; this instance did not repeat all90earlier answers or45replays. This review does not establish unseen/whole-library accuracy or universal adapter compatibility.

## Verdict

**Ready** for the authorized guarded apply. Publication readiness remains contingent on the planned postinstall checks and outcome review in this same review instance.

## Recommended Next Actions

Serialize maintenance, apply once under an exclusive output name, reconnect runtime, run local checks and one15-case smoke without retries, then provide raw delivery/answer outcomes and final publication file list for this instance's final audit.
