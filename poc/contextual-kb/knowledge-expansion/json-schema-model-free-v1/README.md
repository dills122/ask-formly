# JSON Schema data-only comparison through model-free MCP

This experiment compares the installed93-fact DB with the already-built99-fact JSON Schema candidate. Both are read-only; both MCP runtimes and model assets remain unchanged. Do not invoke a production DB build or install this candidate from this directory.

`PLAN.md` freezes the15visible development cases, identical full-request plans, three repetitions and acceptance criteria. `server.py` injects only the approved DB into the existing model-free service factories. `harness.py` transports caller-supplied MCP calls with complete receipts under the offline guard. No server model/CLI call and no application investigation occur. This is real SDKstdio testing, not a new app-native connection test.

The initial run caught a caller scope omission; see `CORRECTION.md`. Original raw results remain in test-output/r1,r2,r3 and remain unqualified. The reviewed full new run uses test-output/corrected/r1,r2,r3. Both are preserved, never merged or cherry-picked. The new helper copies actual resolved scope to fetch arguments.

The caller authored30answers after reading packets. Repeats retain the same answer only when fresh full records/citations are identical. Ninety observation slots are not90independent generations or unseen evaluations. Source-derived criteria were visible to the author; final separate-context semantic review mitigates but does not eliminate that limitation.

Run experiment helper tests:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/json-schema-model-free-v1 -p 'test_*.py'
```

`audit.py` verifies per-case request/plan/scope continuity, seen fetchIDs, delivered citations against the selectedDB, complete observations, guard activation and preservation. It does not grade meaning. `assessment.py` applies the frozen numeric gate to independently supplied semantic judgments. A positive decision needs BOTH semantic gate and mechanical audit to pass.

`replay_corrected.py` deliberately refuses an existing corrected directory. Do not delete its output to rerun it. Further experiments require a separately reviewed scope/output location. No installed promotion, commit or push is authorized by this experiment.
