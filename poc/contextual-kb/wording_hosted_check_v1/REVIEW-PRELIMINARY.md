# Preliminary independent review

Review instance: 1 of 3. Author explanation not yet read. The reviewer received the neutral bootstrap and task scope, not implementation conversation.

Scope: new hosted evidence directory and frozen dependencies needed to verify it. HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516, broadly dirty main; unrelated repository changes excluded. Graph lookup returned no symbols and all eight checked POC paths were not_tracked; direct source inspection used.

The plan correctly separates deterministic saved-plan normalization from fresh caller/foundation generation. The launcher creates the real Selector unless explicitly overridden; saved_replay overrides only the planner, and calling_agent invokes the unchanged launcher. Selector calls Codex with tool-disabled generation, captures events/decision/receipt, and strict repair bounds replacements to two of eight existing slots.

Pending verification before verdict:
- Real caller batches still active; completion, errors, exactly-once calls, final answer support and gap honesty remain open.
- Independently match selector events to decisions and packet repair, rather than relying only on receipt labels.
- Verify final protected hashes and existing freeze manifests; evaluation content must remain unopened.
- Check the audit's baseline replay, citations and delivered packet equality against actual retained outputs. Citation-ID membership alone cannot prove answer support, so manual answer/fact comparison is necessary.
- The harness freeze currently covers plan, saved replay and caller only; audit/report were expected later and must be bounded in final evidence.

No actionable defect established at this point. This is not a readiness verdict.
