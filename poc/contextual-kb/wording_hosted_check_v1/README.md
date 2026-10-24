# Authorized full hosted check

Evidence-only follow-up for wording_candidate_v1, after explicit user approval to send saved Formly plans and retrieved facts to the hosted selector. No prior candidate was edited.

Read RESULTS.md and REVIEW.md. Two saved-plan full-pipeline runs and eight real calling-agent MCP requests completed with both frozen extractors and ten actual hosted selector calls. The known wording failure is exercised by saved replay; the fresh generated plans were already valid. No retries, fallback or data/model changes. Small exposed diagnostic sample, not sealed evaluation or general accuracy qualification.

Existing opt-in launcher remains:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/wording_candidate_v1/serve.py
```

No client configuration was changed. saved_replay.py and calling_agent.py reserve output directories and are retained as provenance, not repeatable commands against existing outputs. audit.py is a read-only verification pass that reserves its summary file. Raw generation, packet, selector and review evidence lives under test-output. Prior candidate manifests and protected chains are verified by the final preservation record.
