# Refined Formly question contract

Use CONTRACT.md as the recommended v2 instruction for the next agent-layer
experiments. It retains the two-field JSON shape and the library-only boundary.
The tested baseline remains intact in BASELINE.md and the parent directory.

V2 asks for separate searchable operations/outcomes, carries context into each
question, preserves comparisons and conditional alternatives, honors corrections,
and standardizes explicit core-only ui_adapter to "none". Unknown remains null.
It does not inspect applications, answer questions, call retrieval, or run GLiNER2.

To package a request with the tested v2 instruction, from the repository root:

    python3 -B poc/contextual-kb/agent_contract/refinement_v2/prompt.py --request 'I need a new custom Formly field and want to use it in a form.'

This prints system/user messages; it does not call a model. Feed them to the calling
agent. Validate the returned JSON using the unchanged parent contract.py validate
command. The parent contract.py prompt command still uses v1; use this folder's
prompt.py for v2. No MCP or retrieval integration was changed.

Tests:

    python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v2 -p 'test_*.py' -v

Read RESULTS.md for the240-response comparison, including remaining variability
and increased number of questions. Cases/rubric and all raw outputs remain available.
