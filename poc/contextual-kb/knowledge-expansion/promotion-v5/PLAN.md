# Guarded 79-fact promotion

User authorized promotion on 2026-10-25. Preparation only: installation and live smoke remain pending independent review.

Promote the exact qualified validation-v1 candidate as foundation6: 79 facts / 17 documents. Preserve all five accepted knowledge tables' rows, all original authored bytes, catalog, compiler, 85 non-DB runtime/model pins and sealed evaluation. Add only validation-contracts.json and validation-group-example.json to canonical authored inputs; replace installed DB and update foundation/source manifests. Catalog must be semantically unchanged and canonical catalog bytes remain untouched.

The command follows promotion-v4's guarded replacement. It checks review, both freezes, qualification decision, final checks, candidate manifest, current source and model pins, candidate source equivalence, count expectations and complete old-row preservation. It rebuilds the proposed canonical inputs before mutation and compares all five tables. It snapshots the old DB, all canonical authored files, catalog and manifests, writes a recovery journal, then replaces five authorized targets. Postcheck verifies pins and canonical rebuild equality. Caught exceptions/interrupts roll back changed files and remove both additions.

This is atomic per file, not a crash-proof multi-file transaction. Do not launch maintenance or new MCP connections during apply. Existing MCP processes must reconnect afterward. A power loss/SIGKILL requires inspecting the recovery journal and restoring snapshots before service restart.

## Commands

Run from the repository root; use a new output name for every invocation:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v5 -p 'test_*.py'
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v5/promote.py --name preflight-review
# After independent review:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v5/promote.py --apply --name install-1
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v5/merged_run.py --approved-lookups --name stable-live
```

All output directories are exclusive; never repin historical preconditions to bypass failure. Apply refuses an already promoted foundation. The copied merged_run wrapper enables and approves only lookup_formly for this explicitly authorized test; it does not change global configuration or bypass the sandbox.

## Smoke criteria

Use the 15 byte-identical visible validation-v1 qualification cases: V01–V10, E05, M03, Q20, Q21, Q24. One repeat, seed1701, three batches of five. Require 15/15 usable answers, all controls passed, zero critical/delivery failures. Missing answers fail; no retries or tuning. Use validation-v1 assessment and independent answer audit. This verifies installation, not unseen evaluation or whole-library accuracy. Existing three-repeat candidate qualification remains separate. Commit/push only after installation checks, live smoke and independent outcome review.
