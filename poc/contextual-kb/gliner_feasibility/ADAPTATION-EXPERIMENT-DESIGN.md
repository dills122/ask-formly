# Small question-frame annotation and adaptation experiment

Status: proposed for user review; design only. No annotations, training, inference,
planner implementation, or new held-out evaluation performed by this document.

## Purpose and boundaries

Test whether modest supervised adaptation repairs the observed missing requested
aspects, lost objects, shared conditions, negation and unresolved references.
Improved API extraction alone is insufficient. This is a question-frame feasibility
study, not a complete retrieval-plan qualification or an A/B rematch.

A remains unchanged and is not retrained or run in this experiment. Preserve all
prior evidence and the existing protected-file manifests. No knowledge facts,
corpus, compiler, schema, database or index changes; no retrieval or answer work.
Training labels describe questions, never Formly answers or fact IDs. All new
files, environments, caches, weights, logs and results stay under
`poc/contextual-kb/gliner_feasibility/adaptation/`. Existing base checkpoint files
remain read-only. Do not reuse implementation from outside this POC.

## Hypothesis and controlled comparison

Use the current local GLiNER2 2.1.0 package and GLiNER2.5 base checkpoint revision
`54785d51df8d86a0d8f2eb212fec15871aad2c4d`, subject to the compatibility gate below.

- G0: unadapted checkpoint with the new frozen question-frame schema.
- G1/G2: the same checkpoint and schema, adapted with two predeclared seeds.
- Keep tokenization, descriptions, decoding, extraction tasks and validation the
  same. No custom repair rules, semantic fallback, proximity-based attachment,
  hidden retries, or answer inference.
- Preserve the original 12 development cases as an exposed diagnostic panel.
  They do not enter training or the fresh decision set. Earlier exposed A/B
  cases cannot be called new held-out evidence.

## What we label

Canonical annotations retain the exact question and Unicode-codepoint spans
`{text, start, end}`, with exclusive end offsets. IDs distinguish occurrences;
equal strings at different positions are not interchangeable. Preserve overlaps.

| Annotation | Rule |
| --- | --- |
| Requested aspect | One distinct requested piece of information, with a source-grounded target and request cue/action. Distinguish a described setup action from what the user asks. |
| Target | The object or outcome being asked about: value, control, wrapper registration, insertion location, etc. Include modifiers needed to distinguish it. |
| Request cue/action | Source wording expressing what is wanted, including a shared cue such as “what happens to”. It may serve multiple aspects. Do not invent an absent verb. |
| Condition | Full source phrase specifying when/under what setup an aspect applies; explicitly link to every affected aspect. |
| Negative constraint | Include the negator and its scope, e.g. “without removing its control”. `false` as a code value is a literal, not automatically negation. |
| Exact identifier | Whole explicit API/code name, including paths and generic expressions. Distinguish API names from user-defined names and generic domain nouns. Do not infer unmentioned solution APIs. |
| Literal | Exact supplied value/code fragment and its explicit identifier association where present. Preserve quotes, case, zero and false. |
| Scope | Explicit version and UI adapter, each attached to affected aspects. Never fill in a default version/adapter. |
| Reference | Mark reference text and its in-question antecedent when resolvable; otherwise mark unresolved and attach it to the affected aspect(s). A pronoun alone is not ambiguity. |
| Planning ambiguity | Clear versus needs clarification, grounded in unresolved text or genuinely competing readings. Lack of knowledge about the answer is not ambiguity. |

Comparison questions normally have one comparison aspect with both compared
targets, unless they explicitly ask for independent additional information.
Coordinated outcomes (“value and control”) are separate aspects when each needs
its own answer. A rationale records borderline decisions; alternatives must be
adjudicated before model outputs are seen.

Example, used only to explain the rubric: “When hidden, what happens to the value
and the control without persistence code?” has two aspects, value and control.
Both carry “When hidden” and “without persistence code”, and share “what happens
to”. No label asserts what Formly actually does.

### Proposed native prediction schema

Train one combined schema: explicit entities, repeated request records, and one
clear/needs-clarification classifier. Avoid adding broad intent/topic tasks in this
first study; they do not directly address the demonstrated failures.

Each natural-mode request record has one exact source `target_anchor` and lists
of source spans for `targets`, `request_cues`, `conditions`, `negative_constraints`,
`identifiers`, `literals`, `versions`, `ui_adapters`, `references`,
`resolved_antecedents`, and `unresolved_references`. The anchor is the first target
in source order, not necessarily a verb. Empty fields remain empty. Shared context
is repeated in every applicable record. Entities also carry the identifier subtype
and literal/reference spans. Explicit identifier–literal and reference–antecedent
relations are trained separately where pairing cannot be represented unambiguously
by record membership; endpoint roles are fixed across examples.

The canonical gold includes exact pairings, even if a native record loses them.
List co-membership does not earn pairing credit. Two aspects with the same anchor,
ellipsis, repeated identical strings and nested spans are mandatory compatibility
cases. If the native representation cannot express them faithfully, stop and
revise the design before bulk annotation. Do not simplify the gold to fit it.
No generated clarification prose or search-query adapter is trained here.

## Small dataset and annotation quality

Propose **210 new questions: 120 training, 30 development, 60 sealed evaluation**.
This is a feasibility sample, not a claim that 120 examples suffice for deployment.

- Group by scenario/template family before splitting. Paraphrases and minimal
  positive/negative pairs stay in one partition. Different punctuation or swapped
  API names do not make a family independent.
- Cover six primary strata: multi-aspect/shared context; negation/polarity;
  exact APIs/literals; version/adapter scope; references/ambiguity; ordinary clear
  questions and comparisons. Training has 20 per stratum, development 5 and
  evaluation 10. Cross-tag cases: evaluation must include at least 20 multi-aspect,
  15 negative constraints, 20 identifier/literal cases, 15 scoped cases, and 15
  genuine ambiguities. Include clear matched controls for the last group.
- Include natural wording variation, Unicode, repeated mentions, multiline code,
  generic expressions and unfamiliar user-defined names. Keep evaluation families
  distinct; do not select questions by whether the current model fails them.
- A 24-question pilot is part of the 120 training questions, not extra test data.
  Use it to stabilize annotation rules and check native representability.
- Independently annotate the pilot and every development/evaluation question.
  Double-annotate a stratified 24 of the remaining training questions, and audit
  the rest. Annotators work without model predictions. Retain disagreements and
  adjudications, including manual corrections to generated drafts.
- Before bulk annotation, pilot agreement targets: at least 90% agreement on
  aspect counts and ambiguity labels, and at least .90 span/attachment F1 between
  annotators. If missed, clarify guidelines and re-annotate the pilot; do not
  present adjudicated agreement as raw agreement.
- A separate evaluation custodian creates and seals evaluation text and gold.
  Training/implementation workers cannot read either. Run duplicate/family checks
  through the custodian, exposing only contamination findings. Freeze the final
  rubric and evaluation manifest before tuning. If genuine separation is
  unavailable, report the set as exposed and do not use it for the decision.

## Training procedure and feasibility gates

Official GLiNER2 documentation supports entity, classification, structured-record
and relation supervision, including explicit occurrence offsets. It also documents
LoRA training. These capabilities do not prove that the installed boundary model,
all selected heads, and this host support the proposed joint run correctly.

1. **Compatibility before bulk work:** inspect installed training signatures and
   parameter selection. On the 24 training pilot questions only, verify offset and
   native-label round trips, repeated records, negative examples, joint losses,
   gradient flow to each task, finite backward steps and saved/reloaded parity.
   Establish which task heads train with LoRA and which weights the saved artifact
   actually contains. If heads change, save them alongside the adapter and report
   it as adapter-plus-head adaptation. Do not claim the model is encoder-only LoRA.
2. **Bounded training:** propose encoder LoRA rank 8, alpha 16, dropout 0; encoder
   learning rate 1e-5 and task-head learning rate 5e-4 only for trainable heads.
   Batch 2 with accumulation 8 (effective 16), float32, maximum 8 epochs. Seeds
   1701 and 2903; fresh base weights for each. No full fine-tuning, model swap,
   augmentation search or additional hyperparameter sweep in this study.
3. **Local resource check:** establish device support on the pilot; CPU is the
   conservative starting point, four threads for comparable inference. Cap pilot
   training at 30 minutes and each full seed at four hours. A controller terminates
   overdue workers and retains logs. If infeasible, report infrastructure failure
   and revise the design; do not silently move to cloud or change hardware.
4. **Checkpoint selection:** evaluate each epoch on the 30 development questions.
   Select highest complete-frame count, breaking ties by fewer critical errors,
   then earlier epoch. Use a fixed extraction threshold .5, nested overlap policy,
   and classification argmax. Validate that these settings are supported by every
   chosen output path before freeze. No per-case thresholds or post-test changes.
5. **Freeze before evaluation:** both selected checkpoints, base revision, package
   lock, schema, descriptions, decoding, scorer, annotation guide, hardware,
   seeds and manifests. Save all attempted runs, failures and selection results.

The parameter values and budgets above are proposed experimental choices, not
library recommendations or verified throughput. Compatibility changes require a
documented protocol revision before full training or evaluation, not hidden fixes.

## How improvement is judged

Primary outcome: **complete question-frame success out of 60**, separately for
G0 and each seed. A case passes only if all requested aspects and their attached
context, negation, scope, exact strings and required relationships are correct,
without invented aspects. Genuine ambiguity must be recognized and grounded in
the relevant source span; clear questions must not be unnecessarily blocked.
Whole-question copying or correct record count alone earns no completeness credit.

Score automatic span/structure checks plus independent semantic review of blinded,
randomized outputs by two graders. Freeze adjudications before revealing arm
identities and timing. Report exact-span metrics and semantic completeness
separately; harmless boundary variation may pass semantics but still fail exact
span scoring. Necessary identifier/literal spelling and negator retention are strict.

Secondary measures: aspect precision/recall; exact typed API/literal precision and
recall; condition/negative/scope attachment precision and recall; paired-relation
accuracy; ambiguity precision/recall; invented aspects; per-stratum failures;
native invalid outputs and runtime errors. Use N/A for zero-denominator metrics.
Preserve the earlier definition of critical errors: polarity/condition inversion,
silent scope substitution, and necessary identifier/literal corruption. Missing
content still fails completeness even when it is not classified as critical.

**Proposed gate to justify further planner work — both seeds must satisfy all:**

- At least 48/60 complete frames, and at least 10 more complete cases than G0.
- Zero observed critical semantic errors and zero backend/invalid-output failures.
- At least .95 exact identifier/literal precision and .90 recall; at least .90
  precision and recall for condition/negation/scope attachments and ambiguity.
- Neither seed loses more than one complete case versus G0 in any primary stratum.
- Warm frame-processing p95 no more than 500 ms and no more than 1.5 times G0 on
  the same host. This is a proposed feasibility budget, not a change to the existing
  complete-planner latency contract.

Measure cold loading separately. After three development warmups, use five paired,
seeded passes over evaluation, rotating arm order, batch size one, no concurrent
work. Include parsing and validation in warm timing. Semantic scoring uses the
first predeclared pass; report output variation and any additional errors in all
passes. Repeats are not additional independent questions. Report paired win/loss
tables and family-clustered uncertainty intervals, not just percentages. Sixty
cases and zero observed critical errors do not establish a zero population risk.

If only entity metrics improve, retain an entity-only research finding; do not
promote the full frame. If only one seed passes, call adaptation unstable. A pass
authorizes a recommendation to design a retrieval-plan adapter and a new A
comparison; it does not establish usable search requests, retrieval quality or
answer accuracy. No automatic promotion or downstream implementation.

## Implementation order after design approval

| Step | Deliverable / acceptance | Verification | Depends on |
| --- | --- | --- | --- |
| 1 | Guide, canonical frame specification and 24 training pilot labels; reliable agreement | Independent annotation and guideline adjudication | Approved design |
| 2 | Native exporter/validator and compatibility harness; preserve difficult cases | TDD for offsets, repeats, shared context, negative/empty labels, leakage denial and serialization; real pilot backward/save/reload checks | 1 |
| 3 | Final grouped train/dev data and separately sealed evaluation set | Custodian contamination audit, annotation checks and manifests | 1–2 |
| 4 | Two bounded training runs and dev-selected artifacts | Loss/gradient logs, trainable-weight inventory, frozen-base hash, reload parity | 3 |
| 5 | Frozen scorer/runner and implementation review before evaluation access | Independent review of design adherence, scoring, isolation and manifests | 4 |
| 6 | Single sealed evaluation, adjudication and report | Reproducible counts, failure ledger, runtime distribution, protected hashes | 5 passes |

Checkpoint after step 2: stop if the target representation cannot be learned or
faithfully serialized. Checkpoint before step 6: no sealed access until review
passes. The existing GLiNER feasibility review flow has used 2 of its 3 review
instances; preserve that accounting and reserve the remaining review for the
implementation/evaluation gate. Do not silently reset the review budget.

Each implementation step should touch at most a small set of dedicated files
under `adaptation/`: annotation guide/data; exporter/validator/tests;
training runner/config; scoring/evaluation runner; evidence/report. Hash protected
data/A/prior artifacts before and after; no model process receives DB/corpus paths.

## Sources and limitations

- [Official training-data format](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/8-train_data.md): available task types and explicit-span supervision.
- [Official LoRA tutorial](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/10-lora_adapters.md): adapter training/configuration.
- [Official training tutorial](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/9-training.md): training workflow.
- [Prior observed failures](investigation/FINDINGS.md): motivation for this experiment.

Official main-branch documentation was consulted during design; installed-version
compatibility must be verified before implementation. The dataset size, schema,
hyperparameters, thresholds and gates are proposals. Nothing here claims that
task-specific training has already worked.
