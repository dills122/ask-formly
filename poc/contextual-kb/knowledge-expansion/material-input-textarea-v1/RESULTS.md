# Material input and textarea comparison

Isolated candidate: **116 facts / 25 documents**, adding five records. Installed **111 facts / 24 documents** unchanged. Branch `codex/material-input-textarea` from merged PR12 at `e5027e7`. Candidate SHA256: `417e30ce3465b6d97bd0f013ef06db2fc35963236d983b6a4c9b88858c97bb09`.

| Arm | Initial support in each repeat | Completed usable answers in each repeat |
| --- | --- | --- |
| Installed 111 | 5/15, 5/15, 5/15 | 9/15, 9/15, 9/15 |
| Isolated 116 | 15/15, 15/15, 15/15 | 15/15, 15/15, 15/15 |

The baseline already contains the full K74 Material input implementation excerpt under custom-type-recipe-material/material-input-pattern. Four observed-ID fetches per repeat recovered Q01-Q04 using that excerpt. They receive full credit even though the new fact IDs do not exist in baseline. Therefore two input records improve structured access to existing evidence; the three textarea records add missing answerable coverage. Do not describe all five records as entirely new underlying source knowledge.

All candidate targeted questions and five controls were supported initially. Baseline Q05-Q10 remain incomplete after two discovery pages each. Controls cover hidden-value retention, datepicker constraints, multicheckbox identity and unsupported version/adapter stops. No baseline-supported regression, no plan repair, and no critical unsupported claim found by caller assessment; final independent semantic review pending.

90 lookups + 36 baseline discovery calls + 12 baseline fact fetches = **138 successful actual MCP tool calls**, zero tool/operational errors. Recovery used at most two pages of16 for each of six baseline textarea cases and one fetch of one observed ID for each of four baseline input cases; candidate needed none. Frozen original requests/plans stayed identical across arms. Structured packets and arguments were exactly equal across repeats within each arm. Thirty completed caller answers and thirty initial assessments were reused only after this equality check, not90 independent generations. Scores measure this bounded development set, not whole-library accuracy or autonomous planning.

K47/K51 pinned upstream file hashes matched the existing catalog. Source lint and18 inherited admission/audit tests passed; these are adaptation checks, not newly discovered production bugs. Full local maintenance passed. Candidate eight-table superset, quote offsets/hashes, foreign keys, exact6.3.12 scope and runtime eligibility passed. All321 protected baseline paths and installed DB hash remain unchanged; both runtimes/manifests and models unchanged. Evaluation sealed. No model-backed inference or browser compatibility testing was performed.

Prebuild independent review1: Ready. Final review2 pending. Numeric parsing/precision, aliases/registration, disabled/payload policy, CSS pixel geometry, hidden-container timing and hydration guarantees remain outside this batch. No promotion, commit or push.
