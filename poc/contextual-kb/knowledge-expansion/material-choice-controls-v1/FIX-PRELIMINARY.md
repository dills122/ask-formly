# Preliminary audit-fix review

Review instance: 2 of 3. Recorded before reading REVIEW-RESPONSE.md or REVIEW-AUTHOR.md. Fresh reviewer context contains the neutral fix bootstrap and task instructions, not the implementation conversation.

Verified branch codex/material-choice-controls and HEAD eb53f184faccffc1de1ec349c0df1a29bd65091a. Scope is the untracked material-choice-controls-v1 directory; unrelated untracked paths are excluded.

No actionable defect identified in the three bounded fixes on direct source inspection:

- read_run records discovered IDs before fetch and requires recovery version/adapter and discovery request/plan to match the initial call. A genuinely unseen fetch is rejected.
- All lookup calls must exactly equal the shared lookup-calls.json list. Applying this check to both arms enforces identical initial arguments by transitivity; repeats also retain exact structured packet/argument equality.
- Initial packets are deep-copied before fetched evidence is appended. main validates separate initial and completed assessments and emits both score series.

All 17 batch tests passed with the bootstrap unittest command. New tests reproduce successful discovery/fetch, unchanged initial facts, unseen fetch rejection, changed initial request/version/plan rejection and recovery-version rejection. Existing tests cover answer citation/coverage and repeat-equality checks. Graph coverage reports results.py and test_audit.py not tracked; full direct reads supply the evidence instead.

Residual checks: reconcile author response, exercise separate initial citation validation and malformed discovery scope/plan directly, and preserve final semantic qualification as review instance 3. This pass makes no candidate-build, runtime comparison, universal Formly compatibility or promotion claim. No implementation files, installed DB or sealed evaluation were modified/opened.
