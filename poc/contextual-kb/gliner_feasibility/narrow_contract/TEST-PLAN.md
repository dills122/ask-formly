# Proposed qualification before narrow training

This is a plan, not executed results. Existing v2/A evidence stays frozen.
Changing the taxonomy means old five-label F1 is not directly comparable to new
six-role F1. Do not relabel only candidate successes or compare unmatched gold.

## 1. Qualify the contract on a small annotation pilot

Use 24 development questions, four in each family below, drawn from saved actual
v2 outputs where possible. Select and freeze question IDs before new predictions.
Include the existing failures H01, H13, H16 and R04.
Two independent annotators label all 24 under CONTRACT.md before seeing predictions.
Retain initial agreement, disputes and adjudication. Any guide revision applies
to all 24 and requires reannotation before freezing; no tuning to model output.

Families:
1. Whole paths and API candidates: bracket/dot syntax, repeated paths, hypothetical
   APIs, library name as a negative example.
2. Registration names versus model keys: named type/wrapper, supplied key,
   identical spelling in different roles, business-purpose-only negative.
3. Values and boundaries: '0'/0, 'false'/false, empty string/null, quoted or
   escaped punctuation. Preserve quoted instruction text as data when supplied.
4. Scope: version tokens, adapter names, comparisons, negated scope. Scoring
   mentions never grants an active-scope or attachment pass.
5. Context preservation: exclusions, multi-field settings, repeated values,
   corrections. Detect omissions without pretending flat spans solve relations.
6. No mention and ambiguity: generic grounded Formly question, business name
   alone, unclear role, unclear value boundary. Keep these in denominators.

If saved outputs lack coverage (e.g. escaping), add explicitly marked developer
diagnostics; never pretend they are actual v2 outputs. No app investigation.
Proceed only after every gold decision is adjudicated and no systematic
boundary/role disagreement remains unresolved. Report initial agreement; do not
invent an agreement score after adjudication.

## 2. Test the future validator with TDD

Write failing tests first, then implement only generic representation checks:
- Exact offsets, Unicode, valid role enum, source ordering, bounds and no overlap.
- Full paths and internal quotes; outer formatting backticks excluded.
- Typed distinctions: '0' vs 0 and 'false' vs false remain different raw spans.
- Repeated occurrences remain separate; duplicate records rejected.
- question/id copy preserved; output shape and schema version validated.
- Missing/null/malformed result => extraction_error, zero-recall failure in scores.
- Empty successful output is valid but loses recall if gold has required mentions.
- needs_review never counts as a correct extraction; report abstention coverage.
- No automatic repair that invents spans, role labels or property/value links.

Passing these tests proves serialization and validation, not model accuracy.

## 3. Freeze and run a small schema-only comparison before training

Start with the same pinned base model; avoid another checkpoint sweep.
One bare six-role schema and one described six-role schema, same model, question
set, gold, threshold 0.5 and overlap setting. Specify exact descriptions before
prediction. Keep raw overlapping predictions for evaluation: a schema/overlap
violation is a failure, not an invitation to silently discard false positives.
Any later overlap policy experiment must be separately declared.

Do not automatically reuse the old adapter: it learned a different role system.
No training in this first run. Labels and full output records remain inspectable.

## 4. Measure the actual hard problems

Report exact kind+offset precision/recall/F1 for each of the six roles and micro
overall; whole-API-path exact match; quoted-name/key/value boundary errors;
no-mention false-positive rate; invalid output/error and review/abstention rates.
Report exact-set question success, with/without gold mentions separately.
Keep all failures in denominators; correct empty output cannot dominate scores.

Per-parent unique (kind,raw) metrics supplement occurrence scores so repeated
versions/adapters do not inflate the result. Show gained/lost correct spans and
new/removed false positives for the two schemas. Measure per-question and
per-parent latency including validation; model load separately.

Proposed progression gate: >=90% precision AND recall overall and for each
nonempty role; 100% structural validity; no observed string/boolean/number
conflation, instruction execution or dropped complete API paths in designated
critical fixtures. Report denominators and uncertainty: a tiny perfect sample
does not establish production reliability. If the gate fails, state exactly
which roles and errors justify narrowly targeted training, rather than widening
the task. Semantic relations and final answer quality are not scored.

## 5. Independent evidence before a readiness claim

After contract and candidate are frozen, prepare fresh question families with
independent labels; keep them sealed during any training/tuning. Keep entire
paraphrase families and parent requests in one split. Use new registration names,
model keys and API-path combinations, not superficial copies of pilot questions.
Freeze sample size and per-role coverage before running; do not choose them from
candidate outcomes. Old sealed evaluations remain sealed.

Compare on the identical new contract/gold, not historical five-label headline
scores. Independent review checks annotation leakage, scorer correctness, raw
failures and scope integrity before a full comparison or readiness claim.
No training dataset size or run budget is approved by this document.
