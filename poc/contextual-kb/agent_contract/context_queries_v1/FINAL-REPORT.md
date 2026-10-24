# Context-preserving queries: results and decision

**Keep the foundation alone as the working setup.** Supplemental queries produced a small retrieval gain, but lost a required fact on another request and did not reach the consistency target.

We tested 36 fresh development requests in three batches. The unchanged foundation generated 49 questions; a separate rewrite step generated one supplemental query for each. Four identical rewrites were skipped. Both arms used the same foundation outputs, existing retrieval engine and eight-result limit. No GLiNER model was run or trained.

## Retrieval comparison

Recall is the average fraction of labeled relevant facts retrieved across 30 catalog-supported requests. Those include four partially supported requests, scored only on their supported parts. These figures do not measure final-answer accuracy.

| Metric | Foundation alone | With supplemental queries |
|---|---:|---:|
| Recall, top eight | 89.39% | 89.94% |
| Precision, top eight | 25.42% | 25.42% |
| Requests with every required fact group | 26/30 | 26/30 |
| Requests with at least one relevant fact | 29/30 | 30/30 |
| Recall, top four | 85.83% | 85.83% |
| Queries executed | 49 | 94 |

Precision also uses the 30 supported requests, with eight result slots per request. The six unsupported requests each returned eight candidates in both arms; no abstention or answer generation was tested.

| Batch | Foundation recall | Supplemental recall |
|---|---:|---:|
| 1 | 92.50% | 90.83% |
| 2 | 91.67% | 91.67% |
| 3 | 84.00% | 87.33% |

The pooled supplemental score is within the requested tolerance around 90%, but batch 3 remains below the **89.25% minimum**. The candidate also fails the predeclared improvement criteria: its gain is only 0.56 percentage points, batch 1 regresses, and one request loses a required fact group. Small, related synthetic batches cannot establish population performance to within ±0.75 points.

## What helped and what hurt

**C30 improved:** moving the requested operation—combining supplied properties with missing defaults—before the long condition recovered the relevant `reverse-merged-defaults` fact. The original search found none of the three labeled relevant facts; the combined search found one and satisfied the minimum required group.

**C06 regressed:** the original questions about registering and using a custom field type already found the fact explaining the distinction between a model key and a registered type. Supplemental-query fusion and the eight-result cap displaced it. Relevant-fact coverage fell from five of six to four of six. The request's meaning was preserved, but its retrieved evidence was not.

These were the only requests whose top-eight recall changed. The equal 26/30 complete-group totals conceal one gain and one loss; paired scoring catches that loss.

## Meaning, cost and limitations

Prospective review found two semantic issues, retained without repair:

- C09's supplemental query moved “when the field is destroyed” next to “onInit returns an Observable,” introducing ambiguity about which event the timing describes.
- C11's foundation question retained “in IndexedDB” in prose but omitted that supplied channel from the mandatory condition ledger. The supplemental text preserved it.

All structural checks passed; there were no runtime errors or missing outputs. The cases were not filtered to remove these failures. Each stage passed semantic review on 35/36 requests; 34/36 passed both stages.

Retrieval took 0.329 seconds total for the foundation versus 0.620 seconds for the candidate, excluding the shared 0.908-second setup. The additional agent rewrite cost was not measured, so these are not total service timings. Seventeen harness tests passed before execution.

The four partial cases lack catalog evidence for the full Material implementation recipe, expression-generated initial defaults, initial hidden-field rendering lifecycle, or dotted-key parsing. Required-group coverage does not close those gaps.

## Decision

Contextual rewrites can help, but this candidate is not a consistent improvement and should not replace the foundation. More GLiNER training would not address the observed loss: the original queries already retrieved that fact, and combining results discarded it.

A further experiment should explicitly address evidence displacement and the remaining hide/default qualifications. Changing the result-merging policy would be a separately scoped integration task; it was not done here. These 36 requests are now diagnostic evidence, not a fresh set for tuning and requalification.

All work is in this new POC directory. Existing candidates, models and DB remain unchanged; evaluation stayed sealed. Raw results and the detailed technical report are frozen. The final independent verdict is recorded in [COMPLETED-REVIEW.md](COMPLETED-REVIEW.md).
