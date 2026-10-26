# Installed Material datepicker knowledge

Foundation11(model-backed) and model-free-discovery-3 share the qualified104-fact/23-document DB. Both runtime implementations and model assets remain unchanged. See [results](RESULTS.md), [plan](PLAN.md), [installed checklist](CHECKLIST.md) and [qualification](../material-datepicker-v1/RESULTS.md).

Use the [stable dual-mode launcher](../../mcp_runtime/README.md). Restart existing MCP processes after promotion to load the new manifest/DB pins. No client configuration is changed by this promotion. Both local connections already point to that launcher; restarting the hosting application may be needed.

Canonical authored inputs plus pinned catalog/compiler reproduce the exact installed candidate into a fresh isolated output. `promote.py --name FRESH` is historical pre-install verification for the99-to104 transition; `--apply` additionally installs. It requires provisioned private qualification artifacts and the exact99-fact baseline, and intentionally refuses an already promoted installation. It is not an installer or normal startup command.

Recovery snapshots/journal are under ignored `test-output/install-1/before`. Five coordinated targets: new authored/material-datepicker.json, knowledge.sqlite, both manifests and packaging/source-files.json. Ordinary exceptions/interrupts restore old bytes/remove new source. Writes are atomic per-file, not crash-atomic across all five. After abrupt interruption stop clients, inspect journal and restore the entire target set together; never change only a DB hash to bypass integrity checks.

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v9 -p 'test_*.py'
python3 tools/project.py check
```

`installed_smoke.py --mode model-free --name FRESH` replays15fixed lookups and one observed-ID fetch through the installed stable launcher and compares exact results to the qualified candidate. `--mode model-backed --seed 1701` or1702 performs bounded D09/C01/C04 checks, including the retained internal hosted calls. Raw receipts/assets/DBs/models remain private and ignored. Source-only CI does not qualify these asset-backed checks. Sealed evaluation is not used.
