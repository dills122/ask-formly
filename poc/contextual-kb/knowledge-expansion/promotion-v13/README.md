# Foundation15 / discovery7 knowledge promotion

This checkpoint promotes the reviewed 192-fact, 36-document Formly 6.3.12 core/Material candidate. It adds 68 facts across nine documents to the previous 124-fact installation. Both runtime implementations and all model assets remain unchanged.

The [plan](PLAN.md), [guarded mechanism](MECHANISM.md), [smoke plan](SMOKE-PLAN.md), and [results](RESULTS.md) record the scope and checks. Source admission remains reproducible through the existing schema2 compiler; the promotion additionally reproduces the exact candidate DB bytes with the qualification interpreter.

After installation, verify with:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/promote.py --verify-installed
python3 tools/project.py check
```

The `--apply` command is a guarded one-time transition and refuses the already-promoted installation. Recovery snapshots and the before/after journal remain privately under `test-output/installed/before/`; ordinary exceptions or interrupts trigger rollback. The group of filesystem replacements is not crash-atomic.

Restart existing MCP processes after promotion so they reload both updated manifest pins and the installed DB. Client configuration is unchanged. Installed testing launches fresh processes through the stable launcher; already-running client sessions are not silently restarted.

Public Git keeps authored inputs, source provenance, admission mechanisms/tests, and concise qualification/review records. DBs, models, environments, raw run packets, recovery snapshots and sealed evaluation remain private. Historical failed runs and their separate grading errata are retained; targeted fixed-plan repeats do not imply whole-library accuracy.
