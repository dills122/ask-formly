# Frozen v3 repeated fresh-request results

## Outcome

The focused library questions held up on this bounded development panel: all72 responses passed independent text-semantic review, and all24 requests retained equivalent search meaning across their three runs. The condition ledger did not fully comply. v3 remains unchanged; no promotion or sealed qualification was performed.

## Measurements

| Measure | Result |
| --- | --- |
| Fresh requests / batches / repeats | 24 / 3 of8 / 3 per batch |
| Retained responses / question occurrences | 72 / 99 |
| Structural validation | 72/72 |
| Independently useful question text | 72/72 |
| Equivalent question meaning across3 runs | 24/24 requests |
| Identical canonical JSON across3 runs | 2/24 requests (empty plans S08,S24) |
| Primary strict condition-ledger compliance | 65/72 responses;21/24 requests pass all3 |
| Alternative interpretation of two borderline categories | 71/72 responses;23/24 requests pass all3 |
| Harness tests / unchanged candidate tests | 8/8 and13/13 |

The strict aggregate combines structure, text semantics and ledger completeness. A ledger failure here does not mean the Formly question became unusable. Conversely, correct text does not establish a complete ledger. All24 requests produced the same question count across runs; that count alone was not used to infer semantic stability.

| Batch | Text semantics | Primary strict compliance | Alternative interpretation |
| --- | --- | --- | --- |
| 1 | 24/24 | 24/24 | 24/24 |
| 2 | 24/24 | 20/24 | 23/24 |
| 3 | 24/24 | 21/24 | 24/24 |

## Findings and interpretation

- **Clear failure — S12, run3:** both questions preserved the instruction not to substitute another API, but the condition ledger omitted that exclusion. Runs1/2 included it. This alone fails the predeclared all24/all3 gate.
- **Stricter audit findings — S16, all3 runs:** hiding remained in the model-value comparison question but not the condition ledger.
- **Stricter audit findings — S17, all3 runs:** dependence on `model.needsPermit` remained in the question but not the ledger.
- The frozen rubric did not explicitly enumerate separate bindings for the last two categories. Classifying them as requested operations instead of additional auditable conditions changes65/72 to71/72. Both readings are retained;65 is not an interpretation-free accuracy score.
- S22 attaches “without polling” to observation. The reviewer accepted this natural reading, supported by the request’s restatement, despite the rubric grouping it as shared. The rubric remains unchanged.

The reviewer found no blocking harness or integrity defect and rated the bounded evidence **Ready with non-blocking follow-ups**. The candidate failed the stricter complete-contract gate under either interpretation. No retry, output repair, candidate tuning, training or replacement review followed.

## What this establishes

These are genuinely generated outputs from nine separate fresh-context native test agents, each receiving only the frozen contract and its8 requests. There was no output feedback between runs. The independent reviewer assessed all72 responses and191 declared bindings. Exact bytes and author/test provenance are retained; independent file review cannot prove absence of unseen attempts, so native orchestration provenance is reported separately from hash-verifiable artifacts.

This supports continuing with v3 as a development foundation for deriving Formly questions. It does not establish universal determinism, production readiness, retrieval quality or final-answer accuracy. Provider model revision,temperature and seed were uncontrolled; this was an instruction-packet experiment, not a pinned deployed API or latency/load benchmark. The24 authored requests target known categories, are synthetic rather than sampled user traffic, and their repeats are correlated. No new v2 comparison was run.

## Recommendation

Retain this unchanged candidate as the question-text foundation. Before another candidate, precisely define which requested dependencies/circumstances require ledger entries, then address the unambiguous missing-exclusion audit. Do not discard useful question text or start more extractor training because of these metadata findings. Any new candidate needs fresh cases; this panel is now exposed diagnostic evidence.

## Preservation and artifacts

All work is confined to this new POC directory. Both frozen extractors, A, v2, v3, data/DB, retrieval and answer assembly remain unchanged. Evaluation stayed sealed: manifest byte hashing only, no case inspection. Final protection audit checks30 inherited manifests covering38,202 entries (not necessarily unique). Inputs13 and raw files9 also retain their frozen hashes.

- [Independent review](REVIEW-1.md)
- [All requests and repeated question text](test-output/all-questions.md)
- [Raw output manifest](test-output/raw-freeze.json)
- [Independent semantic grades](test-output/semantic-review.json)
- [Semantic stability grades](test-output/stability-review.json)
- [Aggregate measurements](test-output/aggregate.json)
- [Protocol](PROTOCOL.md)
