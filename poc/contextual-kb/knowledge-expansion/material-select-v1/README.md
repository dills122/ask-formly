# Material select knowledge batch

Preparation for an isolated 93-fact/21-document candidate against installed foundation7 (85/19). Read [PLAN.md](PLAN.md) for gates. Source mapping, independent prebuild review and frozen qualification cases precede build/inference. Nothing here promotes or edits the installed setup; models stay unchanged and evaluation sealed.

From the repository root, after source-mapping review and input freeze:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/material-select-v1 -p 'test_*.py'
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-select-v1/candidate.py
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-select-v1/experiment.py agents --cases poc/contextual-kb/knowledge-expansion/material-select-v1/qualification-cases.json --name qualification-1 --repeats 3 --batch-size 5
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py --implementation material-select-v1 --root poc/contextual-kb/knowledge-expansion/material-select-v1/test-output/qualification-1 --cases poc/contextual-kb/knowledge-expansion/material-select-v1/qualification-cases.json --repeats 3 --arms baseline,candidate
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-select-v1/evaluate.py --root poc/contextual-kb/knowledge-expansion/material-select-v1/test-output/qualification-1
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/material-select-v1/replay.py --root poc/contextual-kb/knowledge-expansion/material-select-v1/test-output/qualification-1 --cases poc/contextual-kb/knowledge-expansion/material-select-v1/qualification-cases.json --repeats 3
```

Every output is exclusive; never overwrite a failed or completed run. Hosted calls need authenticated provider access. The caller permits only lookup_formly. Both arms use the exact installed premise planner and unchanged strict normalization; only the DB differs. The schema and grader are copied unchanged from the reviewed arrays harness. Existing installed runtime pins are checked by launcher preflight and the batch preservation checks.

## Completed comparison

See [RESULTS.md](RESULTS.md) for the fixed comparison: candidate 44/45 usable answers versus baseline 15/45, all controls passing, and 45/45 saved-plan replays. The installed foundation7 remains unchanged; this candidate is not promoted. [Final independent review](REVIEW-FINAL.md): Ready for bounded isolated qualification.
