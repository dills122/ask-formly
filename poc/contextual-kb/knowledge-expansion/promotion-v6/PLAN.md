# Guarded arrays and premise-planner promotion

User authorized promotion, installed testing and independent review before commit/push. Install the unchanged qualified arrays-v1 85-fact/19-document database and condition_candidate_v2 planner as foundation7. No model change, no sealed evaluation access, no alteration of old candidate inputs/results.

## Change boundary

Six transactional targets: add canonical authored/array-operations.json and array-repeat-example.json; replace build/knowledge.sqlite; change only CodexPlanner import in mcp_foundation/service.py; update foundation.json identity, planner component, knowledge counts and pins; add the two authored pins to packaging/source-files.json. Normalization, retrieval, selection, compiler and catalog bytes remain unchanged. Three v2 planner files become additional runtime pins; 84 existing non-DB/non-service runtime pins remain unchanged. Parent also adds a default-service regression and maintenance-suite inclusion, and updates current documentation/checklist.

Preflight checks pinned qualification reviews/results, original arrays freezes, all 265 prior preservation pins, 28 revised-planner freeze entries, candidate input hashes, original authored bytes, catalog semantic equality, both DB hashes, all old rows in all five knowledge tables and 85/19 counts. It independently compiles proposed canonical inputs and compares all five knowledge tables before mutation. Answer qualification must be qualified with three rounds >=14/15 and no critical/delivery failures; independent semantic evidence must show 36/36 probes and 3/3 Q20. Prior arrays-only rejection is retained; acceptance comes from arrays-condition-v2.

Guarded apply snapshots all old authored documents, DB, catalog, runtime service and manifests and records recovery journal before file replacements. Postcheck verifies all new runtime/source pins, 261 unaffected prior preservation pins and installed canonical reproduction. Caught exceptions/interrupts restore targets/remove additions. This is atomic per file, not a crash-proof multi-file transaction. Stop active service/maintenance during apply; reconnect old MCP processes afterward. Power-loss/SIGKILL recovery requires inspecting the journal and restoring snapshots before service restart.

## Commands

From repository root, choose fresh exclusive output names:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v6 -p 'test_*.py'
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v6/promote.py --name preflight-review
# Only after review:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v6/promote.py --apply --name install-1
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v6/merged_run.py --approved-lookups --name stable-live
```

## Installed smoke gates

The cases.json bytes equal arrays-condition-v2/qualification-cases.json: A01–A10 plus five controls, one repeat, seed1701, three batches of five. Use the stable launcher, not candidate composition. Require all 15 usable, all controls pass, zero critical/delivery/assessment failures, Q20 supplied premise retained in prose and ledger, installed DB/model integrity, and exact v2 contract receipt. No retry or tuning. Reuse the frozen arrays assessor/grader by pointing admission/assess_run.py at implementation arrays-condition-v2, this promotion's run root and cases with repeats1/arms candidate; do not invoke its historical preservation assertions after promotion. Independent answer audit is mandatory before publishing. These are installation checks; prior three-repeat qualification remains distinct.

## Preparation evidence

TDD: copied guarded-replacement baseline produced three expected failures for new array addition names, service switch and semantic gate tests; implementation made all 14 tests pass. First preflight failed before mutation because new output parent was absent; output creation now creates missing parents and preflight-2 passed, with equal five-table canonical reproduction. No installed targets were changed during preparation. Review and installation remain pending.
