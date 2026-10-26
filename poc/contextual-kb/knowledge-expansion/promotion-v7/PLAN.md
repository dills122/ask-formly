# Guarded Material select promotion

The user authorized installing the exact reviewed93-fact Material select candidate, testing through the stable MCP, independent review, then commit/push and a new PR. Preparation does not perform installation. Models and sealed evaluation remain unchanged.

## Authorized boundary

Five transactional targets: add canonical authored/material-select-options.json and material-select-all.json; replace build/knowledge.sqlite with the exact qualified candidate; update foundation.json to foundation8 with93facts/21documents and the new DB hash; add the two authored source pins to packaging/source-files.json. All88 non-DB runtime/model pins, planner, normalization, retrieval, selector, compiler, catalog and original authored bytes remain unchanged. No new runtime pins are introduced.

Preflight checks the pinned final candidate review, both input freezes, candidate manifest/inputs, numeric qualification and45 replay completion, installed foundation/source pins and631 explicit preserved files. Both database hashes, full old-row preservation across five knowledge tables,93/21counts, source byte equality and unchanged catalog semantics are required. A disposable build from proposed canonical inputs must reproduce all five candidate tables before mutation.

Apply snapshots old authored inputs, DB, catalog and manifests before replacement and records a recovery journal. It checks all new foundation/source pins,628 unaffected preservation pins and canonical installed reproduction afterward. Caught errors/interrupts restore targets and remove new authored files. Replacement is atomic per file, not a crash-proof multi-file transaction: stop serving/maintenance during apply, and inspect/restore the recovery journal after power loss or SIGKILL before restarting. Existing MCP processes must reconnect after promotion.

## Commands

Use new exclusive output names from repository root:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v7 -p 'test_*.py'
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v7/promote.py --name preflight-review
# After independent preapply review:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v7/promote.py --apply --name install-1
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v7/merged_run.py --approved-lookups --name stable-live
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py --implementation material-select-v1 --root poc/contextual-kb/knowledge-expansion/promotion-v7/test-output/stable-live --cases poc/contextual-kb/knowledge-expansion/promotion-v7/cases.json --repeats 1 --arms candidate
```

Do not invoke historical candidate preservation assertions after authorized installation. Their pinned pre-promotion states remain unchanged evidence. Current documentation and installed-admission ledger updates occur separately after apply, with exact changed-file accounting; never refresh old freezes to hide differences.

## Installation smoke gate

cases.json is byte-identical to the15 visible material-select-v1 qualification cases: S01–S10, E05, A06, Q20, Q21 and Q24. One repeat, seed1701, three batches of five through stable launcher. Require15/15 usable, all controls passed, zero critical/delivery/assessment failures, supplied-premise Q20 prose/ledger intact, exact unchanged v2 planner contract receipts, and DB/model integrity. No retries or tuning. Retain failures and stop publication if gates fail. The unchanged one-pass admission assessor refuses retries; independent answer/citation audit remains required. Prior44/45candidate qualification stays separate from installation results.

Commit/push and PR creation follow passing local maintenance, installed smoke and independent outcome review. No model assets, DBs, raw runs, caches or sealed material enter public Git. Review instance1of3 for this promotion scope.

## Preparation evidence

Fifteen fixture tests pass after four observed RED errors (two new source additions plus new six-round/live/replay qualification contract). Read-only preflight-1 passed93facts/21documents, exact five-table reproduction, all88 non-DB runtime pins and628 unaffected preservation pins. No installed targets changed during preparation.
