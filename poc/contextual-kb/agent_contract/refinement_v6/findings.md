# Findings

Frozen v5 stress identified5 failure patterns: omitted narrower support query, shared dependency lost on message lookup, nested outer condition missing, uncertain scope metadata null, exclusion text without ledger. v6 adds an explicit aspect/condition attachment audit inside the single response; no output schema change or semantic omission detector.

Native generation is necessary to evaluate the semantic change. TDD red was missing candidate module, green6 tests; this is transport/selection verification, not proof of semantic improvement. Existing v5 tests7 and aggregation tests8 passed.

Code graph indexed2026-10-16; relied-on v5/v3/preservation/scoring paths not_tracked. Full direct source used instead; no completeness claim. PreToolUse consecutive-read hook blocked one read/test command; reset and retry succeeded without file changes from blocked call.
