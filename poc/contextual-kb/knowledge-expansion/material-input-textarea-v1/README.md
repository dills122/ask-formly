# Material input and textarea candidate

Isolated admission from installed111facts/24documents; proposes five facts for116/25. See PLAN.md, source-decisions.json, source-verification.json and draft-authored/ for scope. No promotion or publishing.

Commands from repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-input-textarea-v1 -p 'test_*.py'
# After review/freeze, once into new exclusive outputs:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-input-textarea-v1/candidate.py
# Caller prepares a tool-input file; every output must be new:
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-input-textarea-v1/harness.py candidate INPUT.json NEW-OUTPUT.json
# After answer review and repeated receipts:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-input-textarea-v1/results.py
python3 tools/project.py check
```

Builder never overwrites existing candidate inputs/DB. databases.json pins actualcandidatehash through run-freeze before MCPtesting. Same unchangedmodel-free factories, no models/hostedgeneration. Readonly and numeric/geometry claims stay bounded to inspected source. All rawdevelopment artifacts stay in ignoredtest-output; sealedarchives untouched. Replay needs a fresh isolated copy; retain originalreceipts.
