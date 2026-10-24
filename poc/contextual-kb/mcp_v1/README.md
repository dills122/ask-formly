# Local Formly MCP foundation

This self-contained POC exposes one stdio tool, `lookup_formly(request)`. It runs the unchanged qualification_v3 question-planning contract, both supported frozen GLiNER adapters as advisory extraction (one selected per server), and the unchanged full-question retrieval path. The default adapter is seed1701; seed1702 is an alternative, not a separately advertised quality tier. The corpus remains the bounded46-fact Formly6.3.12 core/Material sample.

## Start it

Prerequisites: the existing POC DB, offline embedding cache, GLiNER base/checkpoints and GLiNER environment; an authenticated `codex` CLI on PATH. The qualified CLI version is0.164.0-alpha.11.1. The planner is explicitly `gpt-6-astra` with medium reasoning and a fresh ephemeral session per request. Model aliases can evolve; historical foundation qualification did not pin the generation revision. No existing environment or global MCP config needs modification.

New MCP environment setup, from repository root (already installed for this checkout):

```sh
UV_CACHE_DIR=poc/contextual-kb/mcp_v1/.uv-cache uv venv --python poc/contextual-kb/.venv/bin/python poc/contextual-kb/mcp_v1/.venv
UV_CACHE_DIR=poc/contextual-kb/mcp_v1/.uv-cache uv pip sync --python poc/contextual-kb/mcp_v1/.venv/bin/python poc/contextual-kb/mcp_v1/requirements.lock
```

Run as a stdio server:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_v1/server.py
```

It waits for MCP protocol input; it is not an interactive terminal question prompt. In an MCP client configure an equivalent entry (absolute paths below describe this checkout):

```json
{
  "mcpServers": {
    "formly": {
      "command": "/Users/dsteele/repos/ask-formly/poc/contextual-kb/mcp_v1/.venv/bin/python",
      "args": ["-B", "/Users/dsteele/repos/ask-formly/poc/contextual-kb/mcp_v1/server.py"]
    }
  }
}
```

Clients differ in config syntax. Allow at least240seconds per call (planner timeout180seconds); serialized concurrent batches need a larger client timeout. `--seed 1702` selects the other frozen adapter. `--audit-dir <new-directory>` optionally records full calls; planner diagnostics are saved under `runtime/planner`, configurable with `--planner-runs`. No registration into your global client configuration is performed by this work.

Tool input example:

```json
{"request":"In Formly, when a field is hidden with resetOnHide: false, what happens to its model value and FormControl?"}
```

A calling agent should forward the whole request, read the derived questions and returned facts, check which facts support which requested aspects, and explain supported behavior with citations. It should state when support is missing, limited to an older version or outside Formly library scope. It should not inspect an application on behalf of this tool.

## Returned data and limits

- `plan`: unchanged foundation plan/full search queries plus optional advisory spans. GLiNER spans are never retrieval filters.
- `facts`, `retrieval`: original candidate records and existing query/fact selections. `evidence_status: candidate_only` remains explicit.
- `citations`: separate fact-ID mapping to the stored authored-source quote/offset/hash and linked stored evidence. This preserves stored provenance; it does not revalidate external source freshness or prove semantic support.
- `knowledge_scope`: current bounded6.3.12/core/Material coverage, separate from the user's requested version and adapter.
- `advisory`, `runtime`, `generation`: diagnostics, adapter/model integrity and DB checks, planner settings and timing.

The local server does not generate the final answer; the calling agent does. Each request sends its text to the authenticated Codex planner and consumes model usage. Provider credentials remain in the existing login, not this POC. Request/output logs are retained locally for reproducibility and may contain user-provided text. No retries, fallback plans, web search, shell/app investigation, training, database writes or knowledge expansion occur. Invalid plans fail explicitly. Ordinary extractor unavailability returns degraded diagnostics with full retrieval; known integrity drift fails and remains fatal for that server instance.

The server serializes requests and retains the index and extractor between calls. Shutdown closes resources. This qualifies local stdio use, not remote hosting, arbitrary parallel scale or complete Formly coverage.

## Verification

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/mcp_v1 -p 'test_*.py'
python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'
```

See PROTOCOL.md, cases.json and test-output/qualification for the fixed fresh development trial. `qualify.py` and `smoke.py` intentionally refuse to overwrite prior runs. Frozen evaluation remains sealed. Results and review are recorded separately; parity must not be interpreted as annotation or answer accuracy.
