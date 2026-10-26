# Model-free candidate: bounded feasibility results

The isolated server accepts caller-supplied plans and returns SQLite evidence without
server-side inference. Installed foundation9 remains unchanged; candidate not promoted.

## Retrieval comparison

Fixed45saved Material-select development plans:15requests repeated3times,13requests
with required factIDs. Same93-fact knowledge; no new facts, aliases or companion rules.

| Retrieval | Required fact occurrences found | Requests with all required IDs | Mean facts returned |
| --- | --- | --- | --- |
| Saved hybrid/selector packets (8slots) | 54/54 | 39/39 | 7.47 |
| Basic lexical (8slots) | 51/54 | 36/39 | 4.47 |
| Improved lexical (8slots) | 54/54 | 39/39 | 4.58 |
| Improved lexical (16slots) | 54/54 | 39/39 | 4.58 |

All54required occurrences retained with improved retrieval; basic lost3. These are
repeated known plans, not45independent unseen questions, semantic answer scores or
whole-library accuracy. Historical hybrid was not rerun. Nonrequired fact changes
remain visible perID in comparison-1/results.json; equivalence is not claimed.

## External caller

User authorized Codex as the harness. Clean caller-2 completed6requests in82.54seconds:
five supported evidence packets and one unsupportedFormly7response. Each original
request arrived verbatim with a caller-generated plan. No MCP-internal model calls.
Raw delivered structured packets exactly match saved audits; text/structured parity
also passes transport tests. All display citations resolve to returned fact IDs.

Two qualifications matter: M03/M04miss the predefined public-registration-type fact
ID, while a returned example contains registration/use support. Independent semantic
review must distinguish that from complete identity coverage. Also citation strings
include source suffixes, rather than bare machine IDs. This is a feasibility smoke,
not completed answer qualification. No caller repair-loop or live follow-up was
exercised. Kiro/Claude remains untested; shared MCP compatibility is not proof of
identical caller behavior.

caller-1was interrupted and marked invalid because its prompt included expected
checks. It contributes no quality evidence. A RED/GREEN test now prevents expectation
leakage; caller-2only received IDs and original requests. Both attempts remain saved.

## Offline and preservation checks

12tests pass, including actual stdio, source-condition validation, scope conflicts,
late API names, AND/OR behavior, whole-record truncation, read-only SQL, malformed
plans and denied network/process/model attempts. Tests use empty caches/PATH and no
inference credentials in the server. The guard is Python test instrumentation,
not an OS security sandbox. No clean-machine installation claim is made.

`python3 -B tools/project.py check` passed. All769frozen baseline file pins and the
installedDB hash remain unchanged. Models and sealed evaluation untouched.

## Next contract decision

The supplied repair-loop research fits this architecture: return specific structured
validation feedback and let the caller issue a corrected call, with at most2repairs.
That behavior is not implemented or tested here. Current errors are ordinary MCP
execution errors; missingplan uses disclosed rawsearch. Decide whether a new revision
should instead return PLAN_REQUIRED. Do not silently change this frozen candidate.
See REVIEW.md for independent findings/verdict and README.md for candidate setup.
