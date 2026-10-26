# Preliminary independent review

Review instance: 1 of 3. Recorded before reading REVIEW-AUTHOR.md.

Scope verified: branch codex/material-choice-controls, HEAD eb53f184faccffc1de1ec349c0df1a29bd65091a; batch untracked, unrelated untracked files excluded. No candidate build performed.

- P1: results.py:36-45 ignores discover_formly_candidates packets when tracking observed IDs, so a valid fetch of an ID first delivered by discovery is rejected. This blocks the expressly planned discovery recovery path.
- P2: results.py:28-30 compares each arm to its own mutable saved call plan, but does not compare initial lookup plans with lookup-calls.json or with the other arm. Different initial arguments can pass the audit although the experiment requires identical full-question plans.
- P2: results.py:40-45 mutates initial facts with fetched facts and reports only final usability. The promised separate initial versus completed evidence support measurement is absent.

Seven proposed claims inspected against local K48/K49/K52/K62 upstream sources; no substantive claim defect found. K13/K48/K49/K52/K62 local hashes match source-verification.json. All 13 batch unit tests pass; they do not exercise read_run. Graph coverage returned no entries for this new scope, so conclusions rely on direct full-file inspection.
