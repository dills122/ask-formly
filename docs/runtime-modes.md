# Choosing an MCP runtime

Ask-formly keeps two ways to use the same reviewed Formly knowledge. The default is
**model-free inside the MCP server**. The earlier **model-backed** implementation
remains available as an explicit option.

| Responsibility | Model-free default | Model-backed option |
| --- | --- | --- |
| Turn the request into Formly library questions | Calling agent | Internal hosted planner |
| Retrieve stored evidence | Lexical and exact-symbol retrieval | Lexical/dense retrieval with advisory GLiNER extraction |
| Decide which evidence is relevant | Calling agent, with discovery and fact-fetch tools | Existing hosted selector, then calling agent |
| Explain the answer and its limits | Calling agent | Calling agent |
| Internal model/provider calls | None | Local models plus hosted Codex CLI calls |

Choose model-free when your agent harness must own all AI calls, including the
workplace use case that motivated this change. Model-free does not mean the calling
agent is offline. Choose model-backed only where its local inference and internal
hosted calls are permitted. There is no automatic fallback between modes.

## How the default round trip works

1. The agent preserves the original request and derives scoped Formly questions.
2. `lookup_formly` validates the supplied plan and returns candidate facts with citations.
3. If the plan needs repair, the same agent fixes it and calls again. The server
   does not launch another agent or call a CLI to repair it.
4. If evidence is incomplete, the agent uses `discover_formly_candidates`, selects
   relevant IDs and calls `get_formly_facts` for full evidence and citations.
5. The agent answers from supported evidence and identifies remaining knowledge gaps.

Unsupported release/adapter coverage is a stop, not permission to silently change
scope. A structurally valid plan does not prove every part of the request survived.
The caller remains responsible for meaning, relevance and final answer quality.

## Setup and current readiness

Use the [mode selection and setup guide](../poc/contextual-kb/mcp_runtime/README.md)
for commands and separate client examples. Existing client entries are not
rewritten automatically. Examples use placeholder checkout paths; the live local
configuration, provider credentials, models and DB are not published.

Both modes use the same 111-fact, 24-document knowledge set with exact Formly 6.3.12
core/Material coverage. The [knowledge pipeline](knowledge-pipeline.md) is shared;
changing modes neither rebuilds the DB nor expands its coverage. This remains a
provisioned POC, not a verified fresh-machine installer.

Both launcher modes passed real stdio smoke checks and independent review. A
separate native Codex pilot exercised all three model-free tools. Other harnesses
remain unqualified. See the [verification record](../poc/contextual-kb/mcp_runtime/RESULTS.md)
and [bounded comparison history](history/model-free-transition.md). These results
do not establish whole-library accuracy, broad model parity or production readiness.

After knowledge promotions, use the stable launcher commands in the setup guide. Original experimental direct-entry scripts retain their historical DB pins and are not current installed entry points. Restart/reconnect clients after promotion.
