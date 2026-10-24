# Entailment experiment and question-plan usability

Completed 2026-10-23. **Stop this NLI branch. Keep the frozen extractors and v2 as experimental components; role annotations are not approved as authoritative filters.** The text-first question plan is promising but not qualified: independent assessment found29/30 complete usable plans with one shared-condition omission.

This report is the post-run supplement to [the best-configuration inventory](../../../BEST-QUESTION-CONFIGURATIONS.md), written before inference and bound by the preparation receipt. That inventory remains unchanged so its reviewed hash stays valid. There is no new winning configuration or promoted replacement from this experiment.

## What was executed

- One public entailment model: `MoritzLaurer/deberta-v3-base-zeroshot-v2.0`, pinned revision `8e7e5af5983a0ddb1a5b45a38b129ab69e2258e8`, downloaded entirely into this POC. Existing environment: Transformers5.20.2, torch2.14.1, CPUfloat32/fourthreads. No package upgrade or model training.
- One fixed seven-hypothesis policy: six roles plus no-entity, exact occurrence marked in the complete question; absolute entailment support>=0.8 and runner-up margin>=0.2. No cross-role softmax, threshold search, prompt revisions or post-result retry. Abstention/no-entity preserves original output in the hypothetical candidate. Roles may change only at existing offsets; no missing-span recovery.
-24 new self-authored development questions in12 contrast pairs, independently reviewed before inference,25 gold mentions. No normalized duplicates against302 exposed old train/dev rows; conceptual overlap intentional. Fresh oracle has positive probes only; it does not measure negative rejection.
- Two existing30-question regression panels: shadow development and separately adjudicated legacy development, using preserved raw extraction caches. No claim of newly executed extraction on those cached panels; no retrospective change to original legacy results.
- All30 original requests and60 questions from unchanged v2 beta1, with both frozen epoch-6 extractors newly executed. This is cached v2 generation, not a new generation/repeatability trial. Each extractor ran84 new calls: fresh24 plus usability60,168total.
-326 unique occurrence-level NLI calls,2,282 premise/hypothesis pairs; shared scores cached across seeds/panels. Operational scoring completed before separate supplied-span oracle scoring. No gold entered the scoring API.

Ten TDD policy/accounting tests passed after the absent-module red run. Review1 found preparation/code/data ready and bound77 files, including model assets, code, data, sources and baseline dependencies. Review2 independently graded text before predictions, raw annotations before NLI results, then verified decisions/arithmetic and frozen artifacts. No third review or tuning loop was needed.

## Extraction and hypothetical NLI changes

Counts below are exact typed mentions and whole extraction sets, not answered questions.

| Panel | Seed | Baseline correct/gold | Baseline extras | Exact extraction cases | Useful NLI repairs | Lost correct mentions |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fresh24 |1701|25/25|2|23/24|0|0|
| Fresh24 |1702|23/25|0|22/24|0|0|
| Shadow30 |1701|28/30|1|27/30|0|0|
| Shadow30 |1702|29/30|0|29/30|0|0|
| Adjudicated30 |1701|57/65|4|20/30|0|1|
| Adjudicated30 |1702|56/65|2|22/30|0|1|

Both seeds fail the predeclared continuation gate. The harmful legacy change is VCAL-015: `'account.id'` changes from correct model_key to registration_name (entailment0.947811, margin0.220417). This is a wrong model decision, not an accounting error. Whole-case exact totals do not expose this additional loss because that case was already imperfect; mention-level regression reporting matters.

On actual v2 questions the alternative proposes13 harmful role changes across8questions per seed, independently reviewed. They include `v6` and `Material` becoming api_reference, a key and registration becoming API references, and `false` becoming an API reference. No helpful usability relabelings were found. All changes are hypothetical saved alternatives; original raw outputs and question text were never changed.

The policy mostly abstains:27/27 fresh occurrences for1701 and23/23 for1702. Supplied-span accepted-correct oracle roles are0/25fresh,1/30shadow,2/65adjudicated. **Zero accepted fresh oracle roles does not mean the extractor found zero mentions.** It means no supplied fresh gold span met the fixed NLI role-support/margin decision correctly. Fresh top-ranked role accuracy ignoring acceptance was16/25; corresponding shadow/adjudicated values18/30 and29/65. Those are posthoc descriptive diagnostics only, not an alternative selected policy. Most fresh abstentions came from insufficient separation between high role scores (23small-margin,2low-support). Lowering the threshold is not supported as a remedy by these observations.

No-entity oracle decisions reject only1/18shadow and1/36adjudicated negative probes. Abstention is not counted as correct rejection. This experiment rejects this specific model/hypothesis/policy configuration, not all possible NLI methods.

## Independent question-plan assessment

All30 original requests, including the intentionally empty H11 output, were assessed before predictions. **29/30 plans were judged fully usable under the preservation/focus rubric.** H07q1 omits that the selected value still occurs among the new options despite the original request explicitly applying conditions to both questions. H07q2 retains it. Broad search is possible, but q1 is incompletely scoped; retaining the original request elsewhere does not excuse the omission. H11's empty plan was judged appropriate from its original request. This new judgment remains separate from earlier v2 grades; none were rewritten.

The reviewer then inspected all120 question/seed annotation rows. Visible defects occur in8questions per seed:

- H01q1,H13q1,H14q1,H21q1..q4 label prose component-category `type` as api_reference under the reviewed shadow distinction.
- H15q1 labels SSN/ssn registration names as values. Seed1702 also produces malformed boundaries/overlap there.

R05q1's `Material` is correctly recognized as an adapter but explicitly negated. Using it as a positive adapter filter would be wrong. This is a scope/polarity hazard, not an entity-label error. Flat role lists also do not encode literal pairings, requested-versus-protected APIs or conditional existence.

None of the observed annotation defects prevents formulating a text query from the unchanged focused question. That finding depends on the diagnostic representation retaining complete question text and constraints and keeping role hints optional. It does not establish an implemented retrieval integration, measured retrieval gain, or a qualified automated filter. The usability panel has no independently authored exhaustive mention gold; the manual review is a visible-defect assessment, not a six-role precision/recall certification. No claim that all remaining52question annotations per seed are fully correct follows.

## Foundation and next decision

The strongest supported foundation remains the library-question agent and the two retained GLiNER extractors, with their documented limits. This bounded experiment supplies no reason to add the earlier verifier or this NLI alternative. Stop optimizing those branches.

The next useful question-layer work is a separately versioned candidate addressing shared-condition propagation and an explicit contract for advisory versus authoritative metadata. In particular, exact text, scope, negation and literal relationships must survive even when role extraction abstains or disagrees. Any such change would need a small targeted regression comparison while keeping v2 unchanged. No such implementation, retraining, baseline promotion or downstream change was performed here.

## Costs, preservation and evidence

New extraction execution totals:1701cold3.757s plus84calls16.021s;1702cold3.626s plus84calls17.826s. NLIcold0.473s and326unique occurrences50.928s. Shared memoization and mixed operational/oracle calls prevent these totals from being per-seed or production latency estimates. No SLA qualification or benefit-per-latency claim.

Before/after audits match:37,925 inherited protected entries plus37shadow,54full-training,85sealed-preparation and5diagnosis bindings;77reviewed input bindings and original v2 source hashes remain valid. Both baselines,A,v2,knowledge/data/DB and prior evidence remain unchanged. Sealed evaluation was not inspected or used for inference; preservation hashing only. No retrieval, DB search, answer assembly, application investigation or serving changes.

Evidence:

- `PROTOCOL.md`, `model-revision.json`, `data/`, `test-output/red.txt`, `test-output/green.txt`.
- `REVIEW-1.md`, `review-ready.json`: independent preparation gate.
- `test-output/run-v1/`: raw extractions, hypothetical outputs, oracle scores, summaries, costs, before/after and completion/freeze records.
- `REVIEW-2.md` and `test-output/usability-{text,annotation,nli-change}-review.json`: independent judgments and per-case evidence.
- `test-output/review-2-arithmetic.json`: independent recomputation; `author-arithmetic-check.json` is separately labelled author verification.
- `test-output/posthoc-score-diagnostic.json`: descriptive rank/margin analysis, no tuning.

Review2 verdict: Ready with non-blocking follow-ups to close/report this negative experiment; NLI not ready for continuation/adoption. All requested follow-ups are addressed here by recording the failed gate, role-filter hazards and frozen v2 limitation. This report supplements the inventory without invalidating its pre-run hash. No qualification, held-out generalization or final-answer accuracy claim is made.
