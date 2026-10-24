# Bounded retrieval repair — separate MCP candidate

This candidate retains the accepted foundation and frozen GLiNER advisory extraction. It keeps the original eight facts unless a separate semantic selector identifies missing requested support and an irrelevant slot it can replace. At most two replacements are allowed; observed runs used one per changed packet. Original MCP remains unchanged.

The diagnosed expression callback miss is recovered 3/3. On 81 structurally valid plan slots, there are no labeled relevant-fact or supported-group losses. One fresh foundation output failed its existing exact-copy validator, affecting three scheduled repetitions; the original overall qualification gate remains failed. This candidate is opt-in and is not presented as a default promotion or a fully qualified fresh end-to-end replacement. See RESULTS.md and independent REVIEW.md for completed evidence.

## Run the candidate

Use the already-installed POC MCP environment and authenticated Codex CLI. No new dependencies or model downloads are needed:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/retrieval_repair_v1/serve.py
```

In a local MCP client, keep the command pointing to mcp_v1/.venv/bin/python and change the server script argument to the absolute retrieval_repair_v1/serve.py path. The tool remains lookup_formly(request). Add `--seed 1702` as two arguments for the alternate frozen adapter. No global configuration is modified by this work.

The unchanged foundation planner and new selector each use hosted Codex gpt-6-astra/medium, fresh ephemeral sessions, no shell/web tools. The selector adds one provider call per nonempty request, including requests it leaves unchanged. Allow a client timeout of at least 480 seconds for both bounded provider calls plus model setup; concurrent calls serialize. --runtime-dir sets local planner/selector artifact location; --audit-dir optionally records complete tool responses. Logs contain supplied questions and model outputs. Original GLiNER worker logs remain in its existing excluded POC runtime-cache.

## Behavior

Original full-query retrieval executes first. Supplemental lexical 20/dense 20 acquisition uses exactly the same full questions and preserves the entire union of those candidates plus the original packet. No query rewrite, API keyword routing or GLiNER filter is added. The selector reads stored source quotes in addition to claims/conditions/limits and must retain every useful original fact, including corroborating context. Code validates membership, at most 2 atomic replacements, question references and verbatim evidence quotes. Semantic judgment remains model-based; structural checks do not prove relevance.

The unchanged plan and advisory output are returned. retrieval.foundation_ids preserves original selection; retrieval.queries/questions/query_count continue to describe original full-query retrieval. selection.queries separately records both deeper channel calls for each question. selection.ids is the final packet; facts and citations correspond exactly to it. selection.status is repaired, unchanged, fallback or not_needed. A failed/invalid optional selection retains the original packet with explicit diagnostics. Known IntegrityError stays fatal through the existing reusable-service guard.

No new knowledge, source freshness certification or final-answer authority is added. Existing source records remain candidate-only. Recovering callback context does not establish an absent props.required or validator recipe. No training, data/DB writes, baseline/foundation edits, sealed semantic reads, commits or publication.

## Tests and provenance

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/retrieval_repair_v1 -p 'test_*.py'
```

Original mcp_v1 and advisory_lookup_v1 tests remain applicable and unchanged. PROTOCOL.md and design-freeze.json preserve original criteria. ASSESSMENT-ADDENDUM.md corrects group-count accounting using per-group identity and explains the limited native diagnostic continuation despite the upstream failure. Original failed overall scores remain intact. experiment.py/native_check.py reserve output directories and never overwrite earlier runs.
