# Findings
- Scope: new mcp_v1 only, reuse code solely within contextual-kb.
- Graph index October16 does not track POC paths; exact source reads used after coverage checks.
- Foundation build_messages selects unchanged qualification_v3/CONTRACT.md; build_plan performs frozen validation. Current CLI receives a pre-generated plan.
- Codex CLI 0.164.0-alpha.11.1 offers exec --ephemeral --ignore-user-config --output-schema --json and read-only sandbox. Authentication remains with existing Codex login; no credentials read/copied.
- References: https://learn.chatgpt.com/docs/non-interactive-mode ; https://developers.openai.com/codex/config-reference/ ; https://github.com/modelcontextprotocol/python-sdk/tree/v1.x . Verify installed API and pin dependency before implementation.
