# Question-layer A/B results

Completed 21 October 2026. **Recommend neither frozen candidate for promotion.**
A passed 17/30 held-out cases; B passed 18/30. Both miss the agreed 27/30
complete-plan floor and both produced critical semantic errors. A one-case
difference does not establish a quality winner. These are question-plan scores,
not retrieval coverage or final-answer accuracy.

## Gate and scope

The user-authorized fourth independent review returned **Ready**, with no
remaining actionable findings on the timeout recovery and hardware provenance
fixes. It independently passed 33 tests and verified all 22 public freeze entries.
Only then was the held-out set opened. The exact reviewed implementation remained
frozen through the comparison; no held-out tuning or retries occurred.

The run completed 30 questions × five paired passes × two arms = 300 samples.
Two independent graders assessed all 58 distinct anonymous plans. A third blind
adjudicator resolved 12 disagreements, including one completeness disagreement.
Grades were frozen before joining arm labels and timings. All 38 locked source/data/DB
file hashes matched before and after execution, and again after separate diagnostics.
No retrieval, evidence assessment, answer assembly, or data/DB changes were made.
All new implementation code is inside this POC, using its isolated dependencies.

## Measured results

| Metric | A: spaCy dependency projection | B: LlamaIndex question generator + local Qwen |
| --- | ---: | ---: |
| Complete first-pass plans | 17/30 | 18/30 |
| Complete on all five passes | 17/30 | 18/30 |
| Cases with critical error in any pass | 1 (h18) | 2 (h01, h14) |
| Focused atomic aspect coverage | 25/39 | 39/39 |
| Condition attachment | 39/40 | 31/40 |
| Relationship attachment | 24/27 | 22/27 |
| Exact identifier/literal role and text | 49/52 | 38/52 |
| Human-graded usable requests, first pass | 24/41 | 28/48 |
| Invented extra asks, first pass | 2 | 6 |
| Genuine ambiguities identified | 0/4 | 0/4 |
| Exact normalized output agreement over five passes | 30/30 | 30/30 |
| Warm median | 3.94 ms | 1.480 s |
| Warm nearest-rank p95 | 5.88 ms | 2.380 s |
| Warm maximum | 7.35 ms | 4.015 s |
| Timeout / explicit failure samples | 0/150 | 0/150 |
| Median / maximum plan size, UTF-8 JSON bytes | 814 / 1,650 | 817 / 2,443 |
| Median / maximum requests per sample | 1 / 2 | 1.5 / 4 |

Output sizes use Python JSON serialization with `ensure_ascii=False` and default separators.
The independent results audit recomputed the figures below and found no discrepancies.

All 300 outputs were structurally planned; schema acceptance did not establish
semantic correctness. Neither arm predicted ambiguity, so ambiguity precision
is N/A and recall is 0/4. Counts of conditions, relationships, and exact strings
are annotated per-aspect occurrences; they can earn preservation credit even
when decomposition fails. Aspect coverage recognizes the requested target;
it does not by itself imply retention of its conditions. Every repeated output
was identical within its case/arm, so the repeat run added stability evidence,
not 150 independent questions per arm. No worker recovery was needed.

Paired outcomes: 12 cases passed both arms, five passed A only, six passed B only,
and seven passed neither. The full paired IDs and per-case judgments are retained
in the evidence. This small purpose-built set does not establish population
superiority; both fail the prespecified gate regardless of the one-case difference.

## What failed

A preserves wording well and runs quickly, but trained syntax does not supply
semantic decomposition on its own. It left independent asks combined in h03,
h04, h05, h09 and h14. Its token projection also split the label literal
`"A & B"` into separate pieces (h18), a critical corruption. It failed to mark
unresolved references in all four ambiguous cases.

B recognized all annotated information targets, but rewriting lost required
conditions and exact strings. In h01, “replacing a model object with the same
fields array” changes the relationship between model replacement and retained
fields. In h14, it recast an `expressions` mapping as an assignment. Both were
adjudicated critical errors. It also added broader asks and failed all four
ambiguity cases. h18 failed exact preservation, but retained the label value
semantically and was not counted as critical literal-value corruption.

These results apply to these implementations, parser/model versions, prompt and
rubric. They do not show that every spaCy or LlamaIndex design will behave the same.

## Runtime and maintenance

Host: Apple M1 Max, 10 cores, 64 GiB, macOS 26.6.2, Python 3.13.14, Ollama 0.31.1.
A cold worker startup was 1.665 s; B startup was 2.269 s. B model preparation was
2.082 s separately, including 1.982 s of reported model loading. The model was
not resident at run start. Warm timing includes input transport and final plan
validation and excludes those startup/preparation costs. Server environment
settings unavailable through Ollama remain explicitly unknown, limiting exact
reproduction. No concurrent test or diagnostic workload was launched during
the paired run. Product latency acceptance is still undecided; the ten-second
deadline was an experiment bound, not an approved product budget.

A uses spaCy 3.8.16 and en_core_web_sm 3.8.0 for trained parsing. Its 114-line
adapter still owns four custom grammar rule families: selecting coordination,
projecting branches, retaining shared/comparison/disjunction context, and a
limited demonstrative-ambiguity check. These are custom rules, not spaCy-provided
question decomposition or coreference resolution.

B uses llama-index-core 0.14.25 and llama-index-llms-ollama 0.9.1 to prompt and parse
the standalone LLMQuestionGenerator. The local Qwen3-Coder 30B model supplies
semantic generation. The 125-line adapter owns a frozen prompt, tagged decoding,
and strict failure handling; there is no semantic repair pass. Pydantic 2.14.1
validates the common contract, not meaning. B additionally requires a local model
service; Ollama reported about 19.36 GB model residency. The shared isolated
Python environment occupies about 173 MB on disk (environment footprint, not
an independently attributable per-arm or full package-cache size).

The eight planner modules total 707 physical lines including comments/blank
lines, contract, process isolation, timing and experiment support. Both arms
have explicit bounded failures and no old-planner fallback. This comparison
uses neither the previous regex planner nor an answer pipeline.

## Evidence and next decision

- [Fourth independent review](../../test-output/question-ab-20261021/implementation-review-four.md)
- [Ready receipt](../../test-output/question-ab-20261021/review-receipt-four.json)
- [Frozen implementation manifest](planner_cases/implementation-freeze.json)
- [Raw 300 samples](../../test-output/question-ab-20261021/comparison-four/raw.jsonl)
- [Runtime metadata](../../test-output/question-ab-20261021/comparison-four/metadata.json)
- [Frozen grading hashes](../../test-output/question-ab-20261021/comparison-four/grades-freeze.json)
- [Final grades](../../test-output/question-ab-20261021/comparison-four/grades-final.json)
- [Blind adjudication](../../test-output/question-ab-20261021/comparison-four/adjudicated-disagreements.json)
- [Independent results audit](../../test-output/question-ab-20261021/comparison-four/results-audit.md)
- [Computed summary](../../test-output/question-ab-20261021/comparison-four/summary.json)
- [Full case ledger](../../test-output/question-ab-20261021/comparison-four/case-ledger.json)
- [48 exposed diagnostic outputs](../../test-output/question-ab-20261021/diagnostics-four.json)

The old 13 catalog and 11 obligation questions were each run through both arms
separately. Their fact-ID gold is not a plan-quality rubric, so no comparable
semantic score is assigned and they do not affect selection or qualified timing.

No arm was promoted. Any follow-up design needs a newly sealed held-out set and
separate evidence; the current set is now exposed. This result supersedes
pre-run status statements in the frozen implementation documents without
rewriting those historical artifacts.

## Per-case failure ledger

Passing cases remain in the machine-readable ledger; each failure appears below.

| Arm | Case | Reason |
| --- | --- | --- |
| A | h03 | One whole-question echo retains defaultValue and all server/edit/reset conditions, but does not separate initialization participation from the independent reset-value source ask. |
| A | h04 | One whole-question echo retains disabled-child validation and hidden-parent child rendering with correct condition attachments, but supplies no separate focused queries for those independent outcomes. |
| A | h05 | One verbatim whole-question request combines "display label" and "request-tracking metadata". Both require separate focused requests; the text preserves conditions and the non-display constraint but does not decompose them. |
| A | h06 | q1 focuses the initial-value lookup. q2 includes both "how its initial model value located" and "how can a change ... be observed", repeating the independent lookup ask inside the observation request. Nested-key scope and no-polling negation survive, but the observation aspect lacks a focused request under the required separation rule. |
| A | h09 | A single whole-question echo combines expression-driven description change and focus-conditioned clearing. The preserved "without changing the model" and "except while ... focus" earn retention credit but do not supply the required separate focused requests. |
| A | h10 | q1 names defaultValue but ends its alternative at defaultValue:. q2 retains empty string as existing model data, yet is only a fragment with no comparison and no binding of null to defaultValue. The required condition is not attached to a requested comparison. Exact credit is limited to defaultValue and empty string in their roles; neither query is usable. |
| A | h14 | The exact expressions mapping is retained, but a single whole-question echo combines "what triggers evaluation" and "which field property receives the result". Required independent focused searches are absent. |
| A | h17 | Both asks are present and the application registration mapping is repeated. q2 ends "receive props.precision:?", omitting its required value 3; q1 strands ": 3?" after the selection ask. This does not retain 3 as the precision value in the focused props request. Selection remains usable. |
| A | h18 | Both queries repeat both asks rather than focusing label and disabled separately. They split the one label literal into "A" and " B", corrupting the requested value and its one-label relationship. props/label and props/disabled/false remain (5/6 exact occurrences); false remains attached to disabled. |
| A | h19 | Neither q1 "field has a wrapper. Can it" nor q2 "field has a custom type. Can it" identifies the unresolved provider referent. The required explicit ambiguity is absent; planned status silently treats alternatives as requests. |
| A | h20 | The whole-question echo preserves move/removal wording but leaves "its key" unresolved without explicit ambiguity about the key owner. No conditional alternative is identified. |
| A | h21 | Repeats "the state" and "replace the form" as a planned search without identifying either unresolved meaning. Required state and replacement-target ambiguity is absent. |
| A | h22 | q1 "wrapper changes the label ... stop that" and q2 "type changes the description ... stop that" do not identify the unresolved prevention target. Neither is marked conditional, and no explicit ambiguity is recorded. |
| B | h01 | q2 faithfully retains model replacement and the same fields array. q1 "replacing a model object with the same fields array" changes the model-versus-fields relationship: the model is replaced with the fields array, rather than keeping fields while replacing model identity. Both outcome targets are named, but q1 cannot be credited with retained fields scope. |
| B | h07 | The readonly-versus-disabled validation comparison survives, but "neither field is hidden" is absent from the focused query. Full original context cannot restore the missing negative condition. |
| B | h11 | q1 faithfully asks the failure for an unregistered selected invoiceCell. q2 adds a separate broad investigation request; q3 and q4 repeat the diagnostic comparison and omit that a field selects the unregistered type. The explicit selection condition must travel to the focused comparison. |
| B | h12 | q1 retains the model flag true and no-overwrite constraint but omits expression result false. q2 retains "after the last edit" but omits both false-result and true-flag premises. These omissions leave only 2/5 conditions and 1/4 literal occurrences; neither complete disagreement scenario is independently preserved. |
| B | h14 | Evaluation trigger and receiving-property targets are separately named, but both queries omit expressions and both quoted literals. "props.required = model.qty === 0" changes the mapping representation; only props.required and model.qty are intact per aspect (4/10 exact occurrences). |
| B | h16 | q3 compares the exact paths, but all queries omit "used by an expression". q1/q2 ask their generic "purpose", adding broader requests. The two paths and reviewMode spelling remain intact in the comparison. |
| B | h17 | q1 preserves the quoted registration name but omits exact name and CurrencyChipType plus their application-registry mapping. q2 preserves CurrencyChipType, props.precision and 3 but omits the supplied registration name and mapping premise. Thus both requested targets exist but neither retains its required application registration context (4/7 exact occurrences). |
| B | h18 | Both targets and the false-to-disabled relationship survive. q1 says "label prop with value A & B": it omits exact props and the quoted literal "A & B" as supplied. q2 preserves props, disabled, and false. Label wording retains the text value semantically, so this exact-preservation failure is not scored as a polarity or literal-value corruption. |
| B | h19 | "Can a field ... provide validation messages" resolves the ambiguous it to field. No ambiguity identifies the competing field/wrapper/type providers. |
| B | h20 | "does the field key need to be changed" silently binds its to the child. Required ambiguity about removed group, moved child, or destination group is absent. |
| B | h21 | "keep the state when replacing a form in Formly" leaves both state and replacement target unresolved but does not explicitly identify either ambiguity. Planned status therefore fails the genuine-ambiguity requirement. |
| B | h22 | q1 "prevent a wrapper from changing the label" and q2 "stop a type from changing the description" select both possible targets. No explicit ambiguity states that "that" may refer to either or both. |
