# N1 isolated candidate

Baseline116/25, proposed124/27. See PLAN.md, source-decisions.json, source-notes.md and sources.md. Source notes and extra-evidence.json are new candidate inputs; canonical authored/catalog/reference/runtime/model/DB inputs remain unchanged.

From repo root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-radio-native-v1 -p 'test_*.py'
# Only after prebuild review and freeze; exclusive output directories:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-radio-native-v1/candidate.py
# Caller supplies exact tools/arguments, each output must be new:
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-radio-native-v1/harness.py candidate INPUT.json NEW-OUTPUT.json
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-radio-native-v1/results.py
python3 tools/project.py check
```

Freeze.json locks reviewed inputs before build; run-freeze.json locks actual database wiring before transport. Reproduction requires fresh isolated output directories; never delete retained qualification receipts to rerun. Model-free stdio server uses unchanged factory, read-only DB and offline guard. No production server inference or hosted calls; caller in this chat assesses evidence. Repeated exact packets reuse judgments, not independent generations. Promotion requires separate authorization.
