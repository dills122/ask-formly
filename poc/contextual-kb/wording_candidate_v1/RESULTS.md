# Results

The new bounded wording adapter resolves the saved F01 exact-copy failure without modifying the old validator or any previous candidate. Passive configuration wording is rendered as an equivalent active configuration question, preserving exact paths, relationship direction, source ledger and standalone information need. The raw output remains in provenance.

- TDD: seven policy tests and two service-boundary tests pass, with retained initial failing logs. Multiple negative subcases reject altered paths, direction, relation, negation, extra clauses, missing bound restrictions, malformed structures/indices and ungrounded source.
- Prior regression suites: retrieval repair 11, MCP 11, advisory 35, all pass. Total new plus prior: 66 test methods. Prior MCP ResourceWarning remains visible in its log.
- Fixed development replay: 84 slots accepted; 81 old passes unchanged; three repetitions of one distinct F01 plan repaired. This is structural acceptance only, not a fresh planner success rate. The old failed qualification remains frozen and unchanged.
- Local service/backend check: saved F01 raw output replayed with frozen extractor seeds 1701 and 1702. Both models available and parameter-preserved; original strict validation passes; actual retrieval receives canonical full questions; same eight fact IDs across both seeds, including conditional-disabled-target. The optional selector was an explicitly no-op test double. No new planner generation, hosted selection or calling-agent qualification is claimed.
- Independent review: see REVIEW.md and REVIEW-DECISION.json. Reviewer additionally replayed all 84 slots, exercised eight negative cases and checked preservation.

The planned hosted-selector smoke was rejected by automatic approval review for external transfer of the saved plan and retrieved data. It was not retried or bypassed. The local integration check isolates the changed deterministic adapter and makes no hosted integration claim. Existing default server unchanged; new launcher is opt-in.

All prior protected hashes and the preceding candidate's final freeze verified. Evaluation remains sealed. No data/model changes, new dependencies or training. General semantic equivalence, undeclared lost-condition detection and broad end-to-end qualification remain outside this bounded fix.
