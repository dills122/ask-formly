# Session orchestration and navigation

Ruflo is used for persistent swarm/task coordination; Codex collaboration workers perform repository work. Ruflo registration is not itself an executing agent or proof of completion. Test receipts and independent reviews establish completion.

Session swarm: `swarm-1792936251116-as7sfw`, hierarchical, maximum4agents. Repo-scoped task records:

- Admission mechanisms: `task-1792936317586-9jiv41`.
- Source inventory and candidate: `task-1792936318905-yixpjw`.
- Guarded64promotion: `task-1792936404078-tqkfsj`.

Ruflo's MCP service accepted and read back task/agent state. A local SQLite memory record is under ignored `test-output/ruflo-session.sqlite`, namespace `ask-formly-knowledge-admission`, key `session-2026-10-25`. This is coordination data, not knowledge seeded into the Formly DB. Swarm connectivity is not independently measured by Ruflo health; do not interpret registration counts as active worker processes.

Serena's ignored local project configuration now selects Python and TypeScript. A fresh worker successfully retrieved symbols from the Python compiler; the tool response is saved in `test-output/navigation-proof.json`. The older parent connection cached TypeScript-only state and needs reconnecting to use its updated language configuration. No shared AI Central targets were edited.

Codebase-memory was refreshed against this checkout, most recently at2026-10-25T14:19:41Z. Queries resolve the new admission symbols, and checked paths report matching metadata. The MCP session does not continuously watch this checkout (`not_session_project`); refresh at checkpoints and check exact-path coverage rather than claiming automatic synchronization. Ignored models, DBs and sealed evaluation are not analysis inputs.

The guide for continuing the work is `docs/knowledge-admission-session.md`; detailed local execution state is kept in ignored `.planning/knowledge-admission-session/` and `test-output/orchestration.json`. Keep generated coordination state out of public Git.
