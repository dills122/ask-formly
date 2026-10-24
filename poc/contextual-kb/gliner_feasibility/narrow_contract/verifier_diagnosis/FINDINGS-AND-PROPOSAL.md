# Development-only verifier diagnosis and proposed next experiment

Status: investigation completed; next experiment proposed, not implemented. No training, new model predictions, decoder changes, annotation changes or sealed evaluation inspection. Original negative result and all frozen artifacts remain intact.

## Why no eligible conflicts

The pinned native boundary decoder loops over entity names and calls its overlap resolver separately for each role (models/boundary/engine.py::_decode_entities). Exact-span deduplication/flat interval selection therefore operates within a role, not globally across roles. A model-free reproduction calls the actual native entity decoder with two role candidates at the same span: both survive flat decoding, and our actual groups() function admits that span. No encoder or weights were loaded for this reproduction. Flat decoding does not make eligibility structurally impossible.

Actual cached development outputs have no cross-role same-offset groups at all, and zero groups blocked by partial overlap. No verifier operational scores were requested. This is observed for these30 questions, not proof that conflicts never occur elsewhere. Thresholding/proposal/null decisions may suppress alternate roles upstream; the saved final-output cache cannot determine which upstream mechanism removed a particular alternate. No causal claim about pre-decode scores is made.

Relative to the frozen gold inventories:

| Baseline seed | Exact correct mentions | Same-span wrong role | Partial span only | No overlapping proposal |
| --- | ---: | ---: | ---: | ---: |
|1701|60|1|0|10|
|1702|56|1|1|13|

Gold total71 per seed;1701 emits61 mentions,1702 emits58. These counts inherit the annotation issues below. Both single-role mistakes are [] classified as api_reference. The partial error is field instead of field.model.shipping.city. Missing mentions, a single wrong role and clipped spans do not enter the current resolver, which requires two already-proposed roles at identical offsets. Expanding training for that resolver cannot by itself change its eligibility contract. Do not disable flat decoding or lower baseline thresholds simply to manufacture opportunities.

## Role errors: three distinct issues

### Annotation ambiguity/inconsistency

The written contract distinguishes explicit configuration properties from prose about field types. Training T09 says “registered Formly type named ...” without an API mention on type; rb-train-014 and contrast-train-33 likewise use type as a concept. Calibration VCAL-010/011/012/013/015/017 labels type as api_reference in similar prose. Training also has19 positive type API occurrences, including explicit property examples and some less explicit phrasing. Thus this is a contextual contract/annotation consistency question, not missing knowledge of the word type.

Five1701 failures and two1702 failures involve those type occurrences. Do not silently remove them or recalculate a passing old result: the original71-gold result remains frozen. Independently adjudicate the distinction before creating a separately versioned future dataset. Inspect training and development under the same rule, rather than adjusting labels to current predictions. This diagnosis is an author finding, not a fresh independent annotation-review verdict.

### Genuine wrong-role generalization

There are unambiguous failures independent of type. For defaultValue, the expected API scores are approximately .006/.005 while value scores are .965/.984. For literal [], expected value scores are approximately .004/.004 while API scores are .938/.960. Both seeds therefore favor the wrong role strongly. Threshold adjustment within the frozen grid cannot make those choices correct.

Training contains26 exact defaultValue API positives and6 expressions API positives: these are not simply unseen spellings. It contains31 Material adapter positives,19 type API positives, no exact gold [] and no exact gold 'invoice-entry'. The latter absence suggests a coverage hypothesis, not proof of cause; generalization to unseen names is part of the requirement. More vocabulary entries alone do not explain or solve errors on already-seen APIs.

### Confidence and exclusivity

At(.5,.5),1701 failures split8 no passing role,2 wrong role,1 multiple role,1 boundary failure.1702 splits4 no-role,3 wrong-role,2 multiple-role. Ranking the six role scores alone puts the frozen expected role first on65/71 and67/71, versus59/71 and62/71 passing the actual boundary-plus-exclusive-role rule. This is a diagnostic calculation, not a new decoder or approved threshold. Argmax would force decisions and still leave wrong-role examples; it is not a safe fix.

The role contract is mutually exclusive but the current head uses six independent sigmoid/BCE decisions, requiring exactly one to clear an absolute threshold. This permits none/multiple outcomes by design. Official native attributes support both single-label softmax and multi-label sigmoid: https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/13-span_attributes.md . This supports a possible later controlled objective comparison, not a claim it would solve current errors or avoid shared-representation interference.

## Recommended next experiment: no-training contract and coverage check

Run this before spending another training budget. All models, baselines, A, v2, decoder settings and old evidence stay frozen; the sealed40-question set remains reserved.

1. Independent annotation adjudication: compare explicit property use against generic concepts across existing training/development examples. Record disputed IDs and a written rule. If corrections are approved, make separately versioned overlays; preserve the original result and never claim retrospective success. Apply the rule to positives and malformed probes consistently.
2. Independently author30 new development questions before any outputs:24 in12 contrast pairs, plus6 controls. Two pairs each for property/prose, property/literal, registration/value, key/value, adapter/registration and whole API path/opaque code value; controls include versions, ordinary requests and no-mention inputs. Use different wording and names; compare overlap against existing training/development. Annotate exhaustive inventories and independently review them. These are development cases, not held-out evidence.
3. Run both unchanged extractors. Count actual same-offset conflicts, partial spans, misses and single-role errors separately. Keep a synthetic duplicate-role case only as a plumbing assertion; it must not count as a learned repair opportunity. If actual conflicts remain absent, report that result rather than resampling to force them.
4. In a separate diagnostic path, score the existing frozen verifiers on EVERY emitted baseline span, including single-role spans. Do not edit outputs or automatically relabel/delete mentions. This tests whether the verifier recognizes real baseline mistakes and whether it would challenge correct baseline mentions. Record supported/unsupported span coverage and cost. Supplied gold/malformed probes remain a separate oracle panel and never generate operational candidates. This diagnostic widens inspection scope only; it is not a serving-policy change.
5. Report exact baseline/verifier agreements and disagreements, high-confidence shared mistakes, correct baseline mentions the verifier would reject, correct alternative roles on actual baseline errors, missing-span ceiling, and all30 cases for both seeds. Retain(.5,.5) as an explicitly diagnostic reference plus full score vectors; do not pick a new operating threshold from this inspection. Include the original development panel as exposed diagnostics.

Decision criteria before more training:
- All new annotation disputes must be resolved independently before outputs, with exact boundaries and no hidden exclusions.
- A future correction policy needs at least one real baseline error per seed with the correct alternative role available, zero losses of baseline-correct mentions, and no fabricated candidate spans. If inspection offers no such opportunity, do not claim repair benefit; reconsider whether this verifier belongs in the pipeline at all.
- If most errors remain absent/clipped candidates, a role-only verifier cannot recover them. Propose a separate candidate/boundary study; do not silently expand this task into it.
- Only after those checks justify a verifier, preregister a new two-seed comparison: existing seven independent BCE outputs versus separate complete-boundary BCE plus mutually-exclusive six-role cross-entropy on valid spans, with malformed spans teaching boundary rejection only. Use the same budgets and reviewed training inputs across arms, no baseline updates, and a newly declared development selection procedure. Keep a no-change control. This is a conditional future proposal, not permission to train now or to substitute argmax on old logits.
- Before a future evaluated adoption: require real operational improvement for both seeds, zero loss of baseline-correct mentions, retained malformed rejection, preserved first/final checkpoint checks and measured latency. Freeze policy before touching sealed evaluation. Current nine-pair calibration remains failed.

## Evidence and limits

Reproducible investigation: diagnose.py; output test-output/diagnosis.json and run.log. It uses cached development outputs and synthetic native decoding only. test-output/preservation.json verifies all54 full-run artifacts, all85 preparation artifacts and37,925 protected checks. Sealed files are byte-hashed for integrity, not inspected or parsed.

Graph service/coverage calls failed with Transport closed; findings use direct reads of the installed pinned source and local POC code. Native source path is gliner_feasibility/env/.venv/lib/python3.12/site-packages/gliner2/. Relevant functions: boundary/engine.py::_decode_entities, inference/overlap.py::resolve_overlaps, inference/runtime.py::_format_spans; POC verifier_evaluation/decisions.py::groups and runtime.py::Models.extract. No generalization, answer-accuracy or production-latency claim follows from this diagnostic.
