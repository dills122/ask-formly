# Guarded 70-fact promotion

User authorized promotion on 2026-10-25. Status: installed; all15 smoke cases passed, independent outcome review Ready.

Promote the exact qualified extensions-v2 candidate as foundation5: 70 facts / 15 documents. Preserve all five accepted knowledge tables' rows, all original authored bytes, catalog, compiler, runtime/model pins and sealed evaluation. Add only extensions-presets.json and extension-addons-material.json to canonical authored inputs; replace installed DB and update foundation/source manifests. Catalog comparison confirms no additional catalog changes are needed.

The narrowly pinned command follows promotion-v3's reviewed guarded replacement. It checks review/freeze/manifest hashes, current source and model pins, candidate source equivalence, count expectations and complete old-row preservation. It rebuilds the proposed canonical inputs before mutation and compares all five tables. It snapshots the old DB, all canonical authored files, catalog and manifests, writes a recovery journal, then replaces five authorized targets. Postcheck verifies pins and canonical rebuild equality. Caught exceptions/interrupts roll back all changed files and remove both additions.

This is atomic per file, not a crash-proof multi-file transaction. Do not launch maintenance or new MCP connections during apply. Existing MCP processes must reconnect afterward. A power loss/SIGKILL requires inspection of the recovery journal and restoration from snapshots before service restart.

## Commands

Run from the repository root:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v4 -p test_promote.py
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v4/promote.py --name preflight-new
# After independent review:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v4/promote.py --apply --name install-1
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v4/run.py --cases poc/contextual-kb/knowledge-expansion/promotion-v4/cases.json --name stable-live --repeats 1 --batch-size 5
```

All output directories are exclusive; never repin historical preconditions to bypass a failure. Apply refuses an already promoted foundation.

## Smoke criteria

The 15 unchanged visible extensions-v2 qualification cases cover all six additions and five regression/gap controls: X01–X10, E05, M03, Q20, Q21, Q24. One repeat, seed1701, three batches of five. Require 15/15 usable answers, all controls passed, zero critical/delivery failures. Preserve missing answers as failures, no retries or tuning. Use existing extensions-v2 assessor and independent answer audit. This verifies installation, not unseen evaluation or whole-library accuracy. Existing three-repeat qualification remains recorded separately.
