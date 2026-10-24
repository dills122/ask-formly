# Development-only GLiNER2 feasibility probe

Start with [FINDINGS.md](FINDINGS.md). This folder is an isolated experiment, not a third production planner. It does not create retrieval plans or integrate with A, MCP, retrieval or knowledge storage.

`env/pyproject.toml` and `env/uv.lock` isolate the GLiNER2 environment. `models/` contains the pinned local checkpoint and `.cache/` contains download/install caches; both are ignored. The existing A/B environment is untouched.

Run harness unit tests from this folder:

```sh
PYTHONDONTWRITEBYTECODE=1 env/.venv/bin/python -m unittest discover -s tests
```

The completed model probe is retained in `evidence/raw.jsonl`. `run.py` deliberately refuses to overwrite it. Do not delete or replace evidence to rerun. Any new trial needs separately specified inputs/configuration and output provenance; this bounded task does not authorize a full comparison. The fixed existing development fixture is the only accepted model input.

All model inference was local/offline. No cloud inference service or API key was used. Model identifiers and revision, runtime versions, raw outputs, warnings, and hash records are under `evidence/`. Read the limitations in the findings before interpreting latency or extraction counts.
