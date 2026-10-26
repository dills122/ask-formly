# Material choice-controls candidate

This isolated batch starts from merged PR11, installed 104 facts/23 documents. It proposes seven exact 6.3.12 Material facts (111/24 candidate): checkbox registration, indeterminate display, label/marker; multicheckbox map, array and disabled options; toggle forwarded properties. Nothing is promoted.

See PLAN.md for criteria, source-verification.json for pinned upstream hashes, source-decisions.json for source accounting and draft-authored/ for reviewed authoring. Existing production implementations and compiler are reused unchanged. Table-row source quotes are provenance anchors; pinned implementations establish the detailed contracts. Toggle registration module recipe and browser compatibility are deferred.

Commands from repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-choice-controls-v1 -p 'test_*.py'
# After prebuild review and freeze, exactly once into new directories:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-choice-controls-v1/candidate.py
# Each call file is caller-authored; output paths must be new:
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-choice-controls-v1/harness.py candidate INPUT.json NEW-OUTPUT.json
# After judgments and receipts:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-choice-controls-v1/results.py
python3 tools/project.py check
```

A completed build refuses to overwrite candidate-inputs/ or candidate-build/. Reproduction uses a fresh isolated copy and retains original receipts. databases.json pins the exact candidate hash separately before MCP testing. No installed launcher configuration changes. Development receipts stay under ignored test-output/. Evaluation and historical qualification archives stay sealed.
