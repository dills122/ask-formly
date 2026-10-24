# GLiNER2 failure investigation and researcher reconciliation

Status: independently reviewed (instance 2 of 3). Review accepts the bounded investigation with no remaining correctness blocker; full planner implementation/comparison is not ready. Ten declared configurations on the 12 exposed development questions plus three diagnostic controls: **123 model calls**, no backend/span-validation errors. Original feasibility evidence, A, and locked data/DB remain unchanged. No full comparison, retrieval, plan adapter or training was performed.

## What the experiments established

GLiNER2 is operational and some failures respond to task framing. The researcher's narrower technical-entity schema is a better fit for explicit API extraction than our broad initial schema. It still cannot serve as a complete question understanding component in the tested configuration. Changing the threshold or record format did not repair the central missing-outcomes/context problem.

| Variant | Change | Observed effect | Limitation |
| --- | --- | --- | --- |
| E0 | Replay original full schema | Exactly reproduces all 12 original native outputs | Confirms stable initial failures |
| E1 | Remove descriptions, retain labels/tasks | Three exact API-slot hits; shorter calls | Six other/partial API-slot spans, both true ambiguities missed; no condition links |
| E2 | Original entities alone | props.placeholder and options.formState become identifiers | Requested phrases/conditions still incomplete; separating tasks is not a general cure |
| E3 | Original schema, threshold .2 | Four requires_context and five refers_to links appear | Several wrong links; more output is not better meaning; full phrase can become fragments |
| E4 | Short concrete entity labels | Picks some verbs, values and version text | Calls PrimeNG an action and generic nouns API names; no complete decomposition |
| E5 | Legacy structured records | D08 groups persist, options.formState and browser restart | D02 combines actions/subjects in one record; D01/D10 fail |
| E6 | Original ambiguity classifier alone | Isolates classification from extraction | Misses both genuine ambiguities and falsely flags five clear cases |
| E7 | Original schema, nested overlap | Retains extra nested spans | Does not recover missing asks or condition links |
| E8 | Natural records anchored on action | D02 has separate register/configure records | Objects/context vanish; D10 has no record; D08 loses useful fields seen in E5 |
| E9 | Researcher-inspired explicit slots + broad intent | Four of eight annotated API occurrences correctly typed; Formly v7 extracted | Three generic terms tagged as APIs, resetOnHide tagged error_message, other APIs missed; no ambiguity/condition/decomposition task in this schema |

API-slot counts are an exposed-development diagnostic: exact whole-text match in identifier/API name/formly_api slots against eight explicit API occurrences derived from the existing development questions. They exclude literals and partial names. E9 gets expressions, expressionProperties, props.placeholder and options.formState. It misses resetOnHide, FormControl, defaultValue and FormlyFieldConfig<MyProps>. Its three API nonmatches are renderer, wrapper and hook; resetOnHide under error_message is an additional role error. E0's zero API-slot score does not mean no API text appeared elsewhere: props.placeholder/options.formState were returned under other labels. This is not a complete-plan metric or a general accuracy claim. E5/E6/E8 have no API slot and should be N/A for that metric, not zero quality.

## Failure mechanisms, evidence and possible corrections

### 1. Semantic labels and task framing matter

The original schema used long descriptions for abstract requested_outcome/condition/requires_context labels. The library accepts and forwards them, but that does not make the encoder an instruction-following decomposer. E1/E2/E4/E9 show that descriptions, labels and task combinations materially change predictions. E9 recovers both expression API names where E0 returns no spans at all. This is a demonstrated narrow improvement, not proof that short labels are always better.

Correction supported now: use explicit typed slots for explicit mentions, keep extraction errors visible, and retain source spans/original question. Do not infer that an unmentioned solution API has been extracted. Choosing a universally best schema remains unproven; E9 changes labels, descriptions and classification together, so its improvement cannot be attributed to just one of those factors.

### 2. Lowering threshold can fragment phrases

D02 at .5 returns register a renderer with score .71996. At .2 it returns renderer (.62294) and register (.30698). The default flat overlap decoder maximizes the total score of non-overlapping candidates; .62294+.30698 exceeds .71996. An installed-library decoder replay over the union of observed candidates reproduces both outputs exactly. This is a sufficient mechanism for this observed change, not capture of the complete internal candidate set. A separate synthetic control illustrates the same effect.

Correction supported now: do not optimize for raw candidate count or assume lower thresholds monotonically improve phrase coverage. E7 nested decoding retains extra spans but does not fix the missing semantics. A longest-span policy or better span training could be tested later; neither was measured as a successful fix here.

### 3. Relation extraction works, but our condition relation is not learned reliably

C01 produces the expected John→Apple Inc. employment and John→San Francisco location links. C02 produces wrapper→field surrounds. C03, an explicit condition/outcome sentence, produces no condition_for link. The relation machinery is therefore functioning. E3 creates some relevant topic-context associations (options.formState→browser restart), but also renderer→wrapper as requires_context and wrapper→type as refers_to. The custom relations do not reliably bind the requested information to its conditions.

Possible correction: task-specific relationship annotations, with shared-condition and negative examples. A typed graph constraint can reject an invalid endpoint type but cannot manufacture a missing correct relation or prove its meaning. Training remains a hypothesis, not something done in this investigation.

### 4. Record identity can be fixed without fixing record content

The official JSON tutorial recommends natural anchored records for repeated instances. E8 applies that mode to E5's fields, with a required single action anchor. D02 changes from one merged record to two records. That addresses the instance-count problem, but the renderer/wrapper objects are missing. D08's good E5 grouping is lost in E8, which returns only persist. Structural correctness and semantic completeness need separate checks.

Possible correction: annotate complete per-request records, including anchor, subject and context; evaluate field retention alongside record count. Do not add proximity rules to hide missing model associations.

### 5. Negation and ambiguity are distinct unresolved tasks

D03 returns removing its control without the word without; copying that span preserves bytes while dropping polarity. Broad intent labels in E9 can identify compare/how_to but do not identify missing referents. E6's ambiguity-only classifier fails both D09/D12 and flags five clear questions. E9 intentionally has no ambiguity task, so it cannot be credited for resolving this problem.

Possible correction: explicitly labelled negative-constraint spans including the negator, contrastive examples of clear/ambiguous references, and a clarification record grounded in the unresolved source span. Do not treat a low confidence or broad intent label as a justified clarification.

## What we take from the supplied research

- Keep extraction, interpretation and downstream retrieval responsibilities explicit. Our existing experiment already stopped at extraction, so its failures were not caused by executing retrieval planning.
- The recommended base checkpoint is the one already used, pinned to revision 54785d51df8d86a0d8f2eb212fec15871aad2c4d. No model change was necessary to try the narrower schema.
- Tested the useful concrete suggestion: four explicit entity types plus broad multi-label intent in one call. The malformed pasted code was reconstructed from the installed public API; E9 is inspired by it, not an exact reproduction of missing code.
- A typed internal question frame can be useful within the question layer, provided every extracted field has provenance and no unsupported inferred concepts are presented as extraction. A typed schema alone does not solve omitted requested aspects.
- The proposed concept catalog, alias DB, FTS changes, retrieval/reranking and answer contracts are outside this locked question-layer experiment. They do not explain or repair observed extraction errors, and none were implemented.
- Intent classification is promising by inspection on simple how-to/comparison questions, but no independent intent gold was frozen for these cases. No intent accuracy number is claimed. The classification-specific Decide model was not evaluated; it would not by itself demonstrate missing span/relation capabilities.

## Per-question diagnostic ledger

| Case | Baseline problem | Best relevant observation and remaining gap |
| --- | --- | --- |
| D01 | No value/control asks, false ambiguity | Some configurations extract resetOnHide/false separately, but no faithful two-outcome decomposition with hiding condition; E9 mislabels resetOnHide |
| D02 | Incomplete configure request | E8 separates two action records; objects absent. E0 retains complete register phrase better than lower-threshold E3 |
| D03 | Missing requested outcome, negator dropped | No configuration demonstrates the complete keep-value-without-removing-control request |
| D04 | No comparison span or API names | E9 extracts both exact APIs and compare intent; useful explicit understanding improvement |
| D05 | Missing version/adapter; false ambiguity | E9 extracts props.placeholder and Formly v7 with how_to; PrimeNG not represented (UI adapter slot absent) |
| D06 | Default/model value relationship missing | No correct defaultValue comparison record; false often treated as negation instead of supplied value |
| D07 | Missing location ask, false ambiguity | E5/E8 extract render; this alone does not capture the requested insertion location |
| D08 | API/topic without persistence action/link | E5 groups persist+options.formState+browser restart; E9 correctly tags API; E8 loses context |
| D09 | Genuine referent ambiguity missed | No tested ambiguity schema succeeds; E9 broad intent is not clarification |
| D10 | Only answer target, missing control | E1 adds answer/control nouns but labels retain its control negative; E8 no records; shared condition not correctly attached to both |
| D11 | Missing exact generic expression | E9 misses it; some variants return partial MyProps/MyProps> or FormlyFieldConfig without the full generic expression |
| D12 | Ambiguous label without explanation | Baseline/E7 retain correct label; E1/E6 lose it. No unresolved-reference span supporting clarification |

## Recommendation

Keep GLiNER2 as a research candidate, with the narrower explicit-slot frame as the most useful lead. Do not promote a configuration or start a full A comparison yet. The observed improvements repair parts of extraction, not the complete question-layer contract.

The next substantial experiment I would design is a small supervised, question-specific extraction/record adaptation, using explicit annotations for requested outcomes, exact APIs, negative conditions, shared context and unresolved references. GLiNER2 documents training formats and LoRA adapters. Feasibility on this host and sufficient example coverage would need verification; success is not guaranteed. Keep that training data separate from the locked knowledge DB, and use new independent evaluation cases after training/configuration freeze. No training was performed here. More unstructured schema tweaking on these same twelve questions risks overfitting without answering generalization.

## Runtime, integrity and limits

All 123 calls completed locally with exact source-span validation. Original E0 native outputs exactly match the first feasibility run. Per-variant development medians range roughly 57–198 ms; E9 is 87 ms. No randomized pairing, warmup or production budget acceptance: these are diagnostic timings, not proof of speed superiority against A. Both phase manifests were written before model execution; phase1 code stayed unchanged for phase2. Frozen configuration files preserve the exact tests. Four new tests passed after a retained red stage; eight prior tests remain applicable and prior review evidence is preserved.

Integrity checks: 60 protected data/A/B entries, 17 prior probe/evidence files, 11 phase1 manifest entries and nine phase2 entries unchanged. Existing unrelated Git modifications were left alone. Python audit hooks and offline flags are defense in depth, not OS sandboxing; diagnostic signal alarms are not hard native deadlines. Loader warnings remain in logs. Preparatory source/path lookups and a pre-execution relative-path preparation command failed and were corrected without running model samples; no failed model outputs were discarded.

## Reproducing the analysis without model inference

From this directory, run `PYTHONDONTWRITEBYTECODE=1 ../env/.venv/bin/python analyze.py` to verify aggregates and integrity, and `PYTHONDONTWRITEBYTECODE=1 ../env/.venv/bin/python check_decoder.py` to replay the standalone decoder examples. Both are read-only. They were added during review to make the earlier inline analysis reproducible; they do not rewrite evidence or rerun models.

## Independent review disposition

[Independent review](evidence/independent-review.md) verified 12 tests, all four integrity manifests, baseline replay, aggregate calculations and both decoder replays. Accepted the reproducibility follow-up by adding the read-only analysis helpers; reviewer verified both. No remaining correction required to accept these findings. Training and complete planner work remain unimplemented proposals.

## Evidence

- [Phase plan](PLAN.md), [phase1 variants](phase1-variants.json), [phase2 decisions](PHASE1-ANALYSIS.md), [phase2 variants](phase2-variants.json), [controls](controls.json)
- [Phase1 raw](evidence/phase1-raw.jsonl), [phase2 raw](evidence/phase2-raw.jsonl), [aggregate summary](evidence/summary.json)
- [Observed-candidate decoder replay](evidence/decoder-observed-union.json), [synthetic decoder control](evidence/decoder-control.json)
- [Integrity](evidence/integrity-after.json), [phase1 freeze](evidence/phase1-freeze.json), [phase2 freeze](evidence/phase2-freeze.json)

Official sources: [relations](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/6-relation_extraction.md), [structured records](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/3-json_extraction.md), [training format](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/8-train_data.md), [LoRA](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/10-lora_adapters.md). Decoder mechanism verified in installed gliner2/inference/overlap.py resolve_overlaps; no third-party source edited.
