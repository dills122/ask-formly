# Material datepicker admission candidate

Five proposed facts cover separate module/type/wrapper registration, date-adapter responsibility, nested min/max/filter, calendar startView/touchUi/startAt, and callback arguments. See [plan](PLAN.md), [results](RESULTS.md), [draft](draft-authored/material-datepicker.json), [source decisions](source-decisions.json) and [source verification](source-verification.json). The installed99-fact foundation remains unchanged.

## Reproduce and audit

From repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-datepicker-v1 -p 'test_*.py'
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-datepicker-v1/results.py
```

The isolated builder `candidate.py` requires freeze.json, verifies protected inputs, copies canonical plus draft inputs, lints and builds with the unchanged schema2 compiler. It refuses existing candidate-inputs/build; it has already run in this checkout. Do not delete qualified outputs or point the builder at the installed path. For fresh reproduction copy this batch's source-only files into a fresh sibling experiment directory, retain the baseline/freeze and provisioned toolchain, then run the builder; verify exact manifest/content equality. Its catalog and origins remain the canonical pinned inputs.

`harness.py baseline|candidate INPUT.json OUTPUT.json` executes saved tool calls through the unchanged MCP factories under offline guard. Output and all sidecar paths must be fresh. databases.json pins each arm; the candidate hash comes from the build receipt. lookup-calls.json contains fixed requests/plans; test-output batch files are exact groups of5. Follow-up input files preserve actual scope/observed IDs. Raw transport, candidate inputs/DB, downloaded upstream and logs are private ignored artifacts. answers-*.json are the30 caller-written supported/gap answers with manual semantic judgments; results.py checks evidence accounting and exact repeat stability, not truth automatically. Independent final review audits semantic judgments.

Never read sealed evaluation or run historical promotion commands. No hosted model or agent CLI is invoked by this experiment server. Models and model-backed implementation remain frozen.
