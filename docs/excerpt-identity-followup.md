# Excerpt guidance and dependency identity follow-up

This follows the [isolated answer-response experiment](answer-response-experiment.md). The candidate remains under `poc/contextual-kb/answer_response_v1/`; default runtime, facts, installed DB and recipe storage are unchanged. No promotion or release is implied.

The [recovery efficiency follow-up](recovery-efficiency-followup.md) preserves
these results and audits their cost increase, with subsequent isolated fixes and
a separate caller comparison.

## Changes

Initial lightweight citations now include `stored_excerpt: available|absent` for each evidence record. Available means a nonblank stored string, not a claim that every part of the requested behavior is demonstrated. The original evidence kind and pinned location remain visible. An absent excerpt means this record has no stored text; it does not mean the upstream implementation does not exist.

Detailed provenance preserves the original citation objects and adds separate availability metadata. It distinguishes authored-summary quotations from evidence excerpts. Guidance explains that changing the response format or refetching the same IDs cannot supply absent stored text. Fetching available excerpts, discovering different relevant facts and authorized inspection of pinned sources remain valid options. No source text was authored or added to the DB.

The candidate identity now verifies actual bytes against the existing non-DB runtime manifest pins, then hashes explicit candidate files, the checked local import closure and required runtime resources. The current map has 30 files, including `mcp_foundation/capitalization.py` and `mcp_v1/versions.json`. Source and minimal-stage identity agree at `answer-response-v1+ff1f4cdf1a26`. Missing required files or changed pinned files fail closed; unpinned candidate/resource changes affect the identity.

This identifies first-party source and declared runtime resources, not the entire execution environment. Python and third-party implementation bytes are excluded; expected package versions are expectations, not installed-version verification. DB bytes retain their separate Store hash check. Startup verification is not continuous monitoring of later filesystem changes.

## Review and preflight history

Review instance 2 and the native SDK smoke independently caught a missing runtime resource: the first 29-file stage produced the expected identity but could not construct VersionResolver because `versions.json` was absent. That stage, its failure logs and the reviewed source snapshot are preserved. The correction adds the resource explicitly, tests mutation and missing-file behavior, and exercises VersionResolver in a relocated subprocess.

Twenty focused tests now pass. Native minimal-stage SDK checks cover initialization/help identity agreement, lookup selection, answer/provenance rejoining, Material and unfiltered scope, full-format rejoining, and measured retry batches. Exact facts and original provenance remain unchanged. The 16-fact provenance probe now requires two batches because the new availability metadata also counts against the existing byte budgets; the added overhead is retained in measurements.

Final independent review, instance 3 of 3 for this candidate flow, verified the
resource correction and loaded first-party dependency coverage. It found no
actionable issues remaining and approved the bounded experiment at the frozen
build above. This does not promote the candidate or qualify the installed runtime.

## Fresh caller design

The baseline is the previous isolated answer candidate `be65e7da2161`, not the complete-evidence source16 server. Six questions were generated without reading runtime evidence or old answers: two ordinary requests and four source audits. Both arms receive the same question in fresh sessions with eight non-help calls, two help calls and six local commands available. Source-audit questions without an adapter retain that unspecified scope. An inherited prompt wrapper initially injected Material; it was corrected and the initial prompt freeze archived before any calls.

Questions, essential/optional rubric, prompts and stages are frozen before execution. Grading distinguishes legitimate first provenance requests and new evidence discovery from same-ID retries after explicit absence information, checks quote types and pinned locations, and checks for premature stopping. Masked grading precedes unmasking, although response schemas can reveal the arm. No quality resampling. These are bounded Codex controls, not Kiro IDE qualification or general rates.

## Fresh caller results

All twelve sessions completed without timeouts, failed MCP transport calls,
parser commands, wrong-server calls or budget excesses. Two updated-candidate
discovery calls returned `needs_refinement` (E04 and E05); these count toward
cost and are not hidden by the zero transport-failure count.

| Metric | Previous candidate | Updated candidate |
| --- | ---: | ---: |
| Total MCP calls | 35 | 39 |
| Help calls | 6 | 6 |
| `get_formly_provenance` calls | 10 | 7 |
| Explicit full-format fact fetches | 1 | 0 |
| Result text bytes | 293,639 | 308,408 |
| Serialized CLI result-envelope bytes | 317,102 | 333,057 |

The narrower recovery counters improved, but total calls rose by four and bytes
by about 5%. Ordinary requests used six versus nine calls; source audits used
29 versus 30. Envelope bytes are measurements of CLI result objects, not network
wire size or model token usage. The added metadata itself has a cost.

| Question | Previous / updated calls | Previous / updated envelope bytes |
| --- | ---: | ---: |
| E01 hide/reset | 4 / 5 | 37,619 / 42,563 |
| E02 inheritance/nested key | 2 / 4 | 24,759 / 33,683 |
| E03 hide source audit | 6 / 6 | 62,525 / 52,945 |
| E04 inheritance source audit | 10 / 10 | 83,742 / 71,572 |
| E05 validation/Material audit | 6 / 9 | 63,092 / 85,646 |
| E06 key/defaults source audit | 7 / 5 | 45,365 / 46,648 |

Independent grades were frozen before unmasking X as previous and Y as updated.
The updated candidate had six pass/bounded-pass outcomes; the previous candidate
had four and two partials. A bounded pass explicitly permits acknowledged source
gaps: it does not mean every requested implementation quotation was delivered.
Previous E02 failed to explain nested addressing; previous E05 discovered a
relevant Material fact but left it unfetched. Updated E05 retrieved its actual
K74 template fragment without claiming the entire matcher/message path was
verified. Some additional calls therefore recovered useful evidence. This
single paired sample does not establish that the metadata caused the improvement.

No caller made two provenance/full calls for the same fact. Nevertheless, updated
E04 requested provenance for an already-absent defaults record after explicitly
acknowledging the missing code. That part returned an authored summary and no
new implementation excerpt. It was bundled with a different fact yielding
guide/source excerpts, including evidence already seen under another fact.
The stop guidance is explicit but does not eliminate every unnecessary
reinspection. Initial provenance calls remain legitimate when needed for an
authored quotation or other detailed records, so absence alone is not a blanket
ban on fetching provenance.

Pinned URL checks passed. Authored notes were not relabelled as implementation.
The grader retained two minor presentation defects: updated E03 changed
punctuation inside an authored quotation; previous E01 grouped a default claim
under a different supporting link. No evidence of harmful premature stopping
was found in the updated arm. Schemas make the arm potentially recognizable;
the assessment is masked, not fully blind.

## Decision

The missing-excerpt contract and dependency identity fixes are complete for this
isolated candidate. Keep it isolated: the trial shows better bounded answer
coverage, fewer provenance/full-format calls, but greater overall cost. Further
work should assess discovery-refinement recovery and reuse of already-known
evidence across facts, with answer completeness scored alongside cost. Do not
interpret fewer provenance calls alone as an efficiency win or add facts merely
to hide these caller-flow issues. Recipe storage remains deferred.

## Preservation

Raw evidence lives in ignored `test-output/excerpt-identity-v1/`. Previous experiments remain intact. The existing 348 source checks pass; full maintenance remains blocked by the missing worktree compiler environment. That limitation is not reported as a qualified installed runtime.

All 144 protected paths, installed DB hash, 60 baseline stage files, 31 updated
stage files, 17 frozen inputs, 84 raw output files and twelve masked session
manifests verified unchanged. The retry collector initially assumed citation
objects rather than lists; a separate v2 corrected derived chronology only.
The original frozen collector, prompts, runtime and outputs remain preserved.
