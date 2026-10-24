# GLiNER2 on actual v2 agent outputs

Focused questions help modestly, but this extraction configuration is not ready
to become a dependable next layer. The prior adapter did not outperform the base
model overall. No model, prompt, threshold, data, or DB was changed to obtain this result.

## What actually ran

30 original requests and all 60 question strings from saved v2 run beta1, with no
rewriting, reasons, global constraints, gold labels, retrieval, or answers passed
to GLiNER2. H11 yielded no focused questions: agent abstention, not an extractor
success. All 360 calls completed; zero inference errors and zero invalid outputs.

Each input ran against the pinned local base and the existing final epoch-8
adapter from seed 1701, under both the prior full-frame schema and a five-label
entity-only schema. Threshold 0.5, nested spans, CPU float32, four threads.
The adapter was fixed in advance, not selected from these results. Its earlier
training-data limitations remain. This is a development feasibility result, not
a sealed evaluation or proof about GLiNER2's potential after suitable adaptation.

Blind agent-authored reference labels cover 111 original and 175 focused entity
occurrences. Three independent annotation workers split the cases; this was
single annotation per case, not three-way agreement or expert-human gold.
Offsets were validated and selected cases inspected. Labels preserve the old
pilot's convention that quoted literals include delimiters. Exact API paths
must be whole paths, not fragments. This deliberately measures the requested
representation; quote/boundary disagreements can lower scores without losing
all of the underlying information.

## Exact typed-span results

| Model / schema | Original precision / recall / F1 | Focused precision / recall / F1 |
|---|---|---|
| Base / full frame | 30.9% / 26.1% / 28.3% | 39.3% / 27.4% / 32.3% |
| Base / entities | 33.7% / 25.2% / 28.9% | 44.1% / 29.7% / 35.5% |
| Prior adapter / full frame | 25.2% / 23.4% / 24.3% | 34.2% / 29.7% / 31.8% |
| Prior adapter / entities | 32.1% / 24.3% / 27.7% | 42.1% / 29.1% / 34.5% |

The two input arms have different entity distributions and repeated shared
context. A second comparison therefore counts each shared (type, exact text)
only once per original request. Across 93 shared atoms:

| Model / schema | Original recovered | Focused recovered |
|---|---:|---:|
| Base / full frame | 26/93 | 26/93 |
| Base / entities | 24/93 | 31/93 |
| Prior adapter / full frame | 23/93 | 29/93 |
| Prior adapter / entities | 23/93 | 30/93 |

This checks common retained entities only, not whether the agent preserved every
original condition. Focused extraction has multiple chances per parent. For
base/entity-only, eight parents improve on this measure, one worsens, and the
others tie (including parents with no shared entities). There is no significance
claim or repeated-run stability claim from this single inference pass.

## What failed

Base/entity-only is the strongest overall focused cell, but its exact recalls
are still: APIs 2/40 (5.0%), custom identifiers 11/28 (39.3%), literals 1/40
(2.5%), versions 33/34 (97.1%), UI adapters 5/33 (15.2%).

Concrete raw-output examples:

- H01/focused/1: finds custom name postal-choice and v6, but misses key zip,
  Material, and the explicit type/key properties. Also emits Formly v6 alongside
  v6 as overlapping version spans.
- H13/focused/1: emits text as a literal without its quotes and finds v6, but
  misses the explicit 0/false pairings and defaultValue properties. This is
  not solely a quote-boundary problem.
- H16/focused/1: tags Formly as api and hideExpression as literal.
- R04/focused/1: tags Formly as api and props.required / props.disabled as
  custom identifiers; it fails to return the exact expressions[...] API paths.

Focused wording did not resolve label meaning, boundary choice, or exact API-path
recognition. Splitting the semantic request and reliably tagging its entities
are distinct tasks. These results do not invalidate the agent's question quality.

Full-frame output remained sparse: base emitted two request records in 90 calls
(one original, one focused); adapter emitted one (original only). All three have
empty targets/request_cues and null target_anchor. These are observed incomplete
records, not three correct frames. Both full-frame models classified 76 inputs
needs_clarification and 14 clear; no status accuracy is claimed without status
gold. There is no frame, relation, condition-attachment, negation, retrieval, or
answer accuracy claim from entity scores.

## Timing

Observed base/entity-only inference total: 2.05 seconds for 30 originals and
3.37 seconds for 60 focused questions (about 68 ms/original and 56 ms/focused
question). Focused total per original request averages 112 ms, including H11's
zero questions. Base/full: 4.10 and 7.46 seconds. Adapter/entities: 2.53 and
4.22 seconds; adapter/full: 4.71 and 8.67 seconds. Model load was about 3.6 seconds
per model, excluded from inference totals. Single sequential CPU pass, no warmup
discard or timing repetitions: descriptive measurements, not service latency SLOs.

## Decision

Keep v2's focused-question boundary. Do not wire this GLiNER configuration into
retrieval yet, and do not reuse the old broad-frame adapter as a proven extractor.
The next bounded experiment should test descriptive, narrowly defined entity
labels against these exposed development failures, especially API paths,
registration names, model keys, versions, adapters and literal boundaries.
Keep frame decomposition with the agent. If schema descriptions are insufficient,
adapt to this narrower task using reviewed labels; don't restart broad-frame
training. This is a recommendation only; no such new experiment was run here.

## Verification and artifacts

Eight scoring tests pass after RED/GREEN development. Independent review found
missing/malformed-result handling and reporting gaps; these were corrected before
final reporting. All actual results were complete/valid, so the fixes did not
change observed precision/recall. Raw outputs remain unmodified.

- PROTOCOL.md, ANNOTATION.md: fixed setup and label semantics.
- inputs.json, input-freeze.json: exact source questions and source/checkpoint hashes.
- gold-1.json through gold-3.json: blind reference labels and ambiguity notes.
- test-output/*-*.jsonl: all predictions, timings, errors.
- test-output/scores.json: per-label, per-parent, shared-atom counts and diagnostics.
- test-output/protected-check.json: 36,222 prior protected files unchanged.
- REVIEW.md: independent harness review and resolution.

Everything added is under this POC experiment. A, pilot, saved v2 evidence,
knowledge data and DB remain unchanged; no old sealed evaluation content was read.
