# v4 ledger candidate results

## Outcome

The original missing exclusion was repaired in all3 diagnostic runs. Scenario and dependency diagnostics also passed all3 runs under explicit rules. All48 generated question texts remained useful. However, conditional-existence follow-ups still lost their condition in the ledger: both relevant cases failed that requirement in all3 runs. The full candidate gate fails. v4 is a separate tested development candidate; no replacement or production promotion occurred.

## What changed

- Ledger policy now explicitly requires scope, scenario transitions, controlling dependencies, prerequisites, exclusions and uncertain scenario alternatives; bare API/operation names are not automatically conditions.
- Source-first inventory and final exclusion check require meaningful verbatim source excerpts in the ledger and every assigned question. A text-only paraphrase is insufficient.
- The candidate selects a new prompt and reuses unchanged v3 validation and advisory-hint transport. Schema, derivation rules and output section stay unchanged. No regex detector, postprocessor, repair loop, training or downstream integration was added.

## Test evidence

Four exposed diagnostics plus12 independently authored fresh development requests; two batches of8, each3 fresh-context native-agent repeats:48 first-submitted responses,78 question occurrences and160 binding occurrences. Inputs/rubrics frozen before generation; raw outputs frozen before independent review. No feedback, repairs, retries or same-panel tuning.

| Measure | Result |
| --- | --- |
| Structural validation | 48/48 |
| Useful question text, independent review | 48/48 |
| Equivalent question meaning across repeats | 16/16 cases |
| Exact canonical JSON equality across repeats | 1/16 cases |
| Original missing no-substitution exclusion repaired | 3/3 diagnostic runs |
| Strict complete-ledger compliance | 41/48 responses;13/16 cases pass all3 |
| If F07 context attachment ambiguity accepted | 42/48 responses;14/16 cases pass all3 |
| Fresh cases alone | 36/36 useful text;32/36 strict compliance |
| New wrapper/compatibility tests | 7/7, including72 saved v3 structures |
| Unchanged v3 unit tests | 13/13 |

## Failures retained

**D12 and F01, all three runs each:** the no-substitution exclusion is correctly carried, but the contingency that meaning is requested only if the option exists is paraphrased in question text and omitted from the ledger. Both frozen rubrics explicitly require it. This is a new omission relative to the desired complete contract, not lost question meaning. D12 overall passes0/3 ledger-completeness checks even though the original specific symptom is fixed3/3. No claim of guaranteed omission prevention is justified.

**F07, run1:** the ledger attaches prior visible-to-hidden context to the later control-on-showing question. The reviewer strictly followed the rubric’s local attachment and failed this entry. Pre-generation data-review permits prior hiding as transition context; a reasonable permissive reading passes it. Report41 strict versus42 permissive, preserve the original grades, and clarify this history-versus-requested-outcome boundary before any further candidate. The six existence-contingency failures remain under either interpretation.

D16/D17/D22 passed3/3 each, including the newly explicit hiding-scenario and controlling-dependency requirements and locally scoped no-polling exclusion. Quoted and retracted restrictions did not produce text-semantic failures. F09 correctly supports an empty ledger without inventing conditions; F10 correctly produces no library questions.

## Independent review and decision

Review1of3: implementation/evidence **Ready** as a bounded experiment; full candidate gate **Not ready**. All48 texts and all bindings reviewed independently, raw reconstruction and hashes checked, candidate7 and original v3 thirteen tests rerun. No blocking runtime-code defect was found. Findings accepted, with the documented F07 sensitivity. No replacement review or fixes on this panel.

Keep the useful question-derivation foundation. The next narrow improvement, if pursued, should explicitly cover eligibility gates for conditional follow-up questions and clarify prerequisite-history attachment; it should use fresh tests. This experiment does not justify further extractor training or expanding retrieval/DB work.

## Limits and costs

This is prompt-level behavioral evidence, not mechanical semantic validation. Native agents used instruction packets, uncontrolled provider revision/temperature/seed and shared context within each8-request batch. Synthetic development cases and correlated repeats are not a production accuracy estimate. Context-separated authors/generators/reviewer are not independent model vendors. No current v3 comparison arm, retrieval usefulness measurement, final-answer test, latency/SLA qualification or sealed evaluation was run. Historical v3 scores are not directly comparable to this smaller, differently graded panel.

The prompt grew from7,712 to10,843 UTF-8 bytes (about41%); latency impact was not measured. The validator still accepts omitted undeclared conditions; a regression test explicitly preserves that limitation rather than disguising it.

## Preservation

All writes stayed in refinement_v4. Both extractors,A,v2,v3,data/DB and downstream code are unchanged. Evaluation stayed sealed: byte hashing for preservation only, no case inspection. The31 prior manifests cover38,248 hash entries (not necessarily unique); inputs15 and raw files6 verified. All final evidence is frozen separately.

## Artifacts

- [Ledger rules](LEDGER-RULES.md)
- [Candidate contract](CONTRACT.md)
- [Independent review](REVIEW-1.md)
- [All requests and question texts](test-output/all-questions.md)
- [Semantic grades](test-output/semantic-review.json)
- [Aggregate measurements](test-output/aggregate.json)
- [Protocol](PROTOCOL.md)
