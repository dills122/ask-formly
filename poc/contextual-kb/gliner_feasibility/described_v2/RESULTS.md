# Narrow entity descriptions on actual v2 questions

Descriptions improve extraction substantially, especially UI adapters, but do
not fix it. Neither model meets the predeclared 90% precision and recall gate
overall or across all categories. No training was performed.

## Controlled comparison

All 60 saved v2 question strings were unchanged, as were the 175 reference entity
occurrences. The five labels retained their names and meaning. The only candidate
change was adding descriptions via GLiNER2's entity-description API. No output
filtering, normalization, threshold changes or new model selection.

240 real inference calls: 60 questions × bare/described × base/prior adapter.
Zero inference or scorer failures. Both bare controls reproduced all 60 prior
outputs exactly, including spans and confidence values. This supports an effect
of descriptions in this run, not a general determinism guarantee.

This is an exposed development experiment with existing agent-authored labels,
not an independent held-out test. No annotation changes were made after results.
The adapter is the previously fixed final epoch8/seed1701 checkpoint, not a new
training run or selected best checkpoint. A and agent v2 were unchanged.

| Model / schema | Correct / predicted / expected spans | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Base, bare | 52 / 118 / 175 | 44.1% | 29.7% | 35.5% |
| Base, described | 94 / 208 / 175 | 45.2% | 53.7% | 49.1% |
| Prior adapter, bare | 51 / 121 / 175 | 42.1% | 29.1% | 34.5% |
| Prior adapter, described | 98 / 215 / 175 | 45.6% | 56.0% | 50.3% |

Base descriptions gained 43 correct occurrences and lost one; they also introduced
68 new false-positive spans while removing 20 old false positives. Adapter:
48 gained, one lost, 66 new false positives and 19 removed. Scores are exact
typed spans; partial paths and omitted quote delimiters count as mismatches.

## Where descriptions help and fail

| Base category | Bare correct / expected | Described correct / expected | Described precision |
|---|---:|---:|---:|
| API | 2/40 | 6/40 | 9.4% |
| Custom identifier | 11/28 | 15/28 | 83.3% |
| Literal | 1/40 | 6/40 | 30.0% |
| Version | 33/34 | 34/34 | 48.6% |
| UI adapter | 5/33 | 33/33 | 91.7% |

UI adapters meet the development category gate on these cases. Descriptions do
not solve exact API paths or literal boundaries. Version recall reaches 100%,
but precision worsens because extra overlapping spans remain: both v6 and
Formly v6 are frequently returned, despite the description requesting only the
version token. Descriptions guide the model; they are not enforced constraints.

Concrete base/described examples:
- H01/focused/1 now finds Material and retains postal-choice. It still labels
  Formly as API, emits both version boundaries, and labels zip as an unquoted
  literal rather than a custom identifier plus quoted literal.
- H13/focused/1 now recovers the numeric/boolean defaults and Material. It still
  misses type/key/defaultValue APIs and does not preserve quote boundaries for
  string keys.
- H16/focused/1 correctly moves hideExpression from literal to API.
- R04/focused/1 still misses both complete expressions[...] paths and emits
  Formly as API. The earlier incorrect path fragments disappear without the
  desired whole paths replacing them.

After deduplicating (type,text) within each parent request, base correct recovery
rises from 31/94 to 53/94; adapter from 30/94 to 53/94. These 94 atoms cover all
focused gold, unlike the prior original-versus-focused comparison's 93 shared
atoms. Thus the gain is not solely repeated Material/version context.
Unique false positives also increase: base 41 to 62; adapter 43 to 63.

No described output has a completely exact entity set, compared with five bare
outputs per model. This does NOT mean zero useful extractions: base has 94 exact
correct occurrences and adapter 98. Exact-set success additionally requires no
missing or extra spans; widespread extra Formly/version spans prevent that.

## Cost and limits

Base bare total 3.48 seconds versus described 9.35 seconds for 60 questions:
about 58 versus 156 ms per question. Adapter: 4.38 versus 10.85 seconds, about
73 versus 181 ms per question. Descriptions increased input size and measured
inference cost. Single CPU pass with alternating schema order; loading excluded,
no service latency or statistical significance claim.

Entity scores do not establish correct negation, condition attachment, value/API
pairings, retrieval quality, answer quality or usefulness of a complete plan.
H11 remains an upstream abstention with no v2 questions, not an extraction pass.

## Decision

Keep the agent v2 boundary. Descriptions are a useful input to a future narrow
extractor, especially for UI adapters, but this configuration is not ready for
integration. The small adapter advantage is descriptive and not evidence for
reusing the old broad-frame training objective.

Before more training, settle the narrow extraction representation: API path,
registration name, model key, value and scope should have explicit roles and
boundary rules. Then use the concrete missed spans and false positives here to
design a small supervised trial aligned with that contract. Do not train another
broad request-frame model, or assume descriptions alone enforce exact syntax.
No follow-up training, label split or postprocessor was implemented in this test.

## Evidence and verification

- labels.json and PROTOCOL.md: one frozen candidate and decision criteria.
- test-output/freeze.json: exact source, labels, code, old output and gold hashes.
- test-output/base.jsonl and adapted.jsonl: all 240 raw outputs and timings.
- test-output/*-schemas.json: serialized schemas confirm descriptions are present.
- test-output/scores.json: per-label/per-parent scores and control reproducibility.
- test-output/differences.json: every gained/lost correct span and changed false positive.
- Four new scorer tests pass after recorded RED/GREEN development.
- REVIEW.md: independent review.
- test-output/integrity.json: all 36,222 protected prior files plus 137 frozen
  agent/prior-experiment artifacts unchanged. Data/DB untouched; no sealed
  evaluation read, no retrieval or answer integration.

API was checked against installed gliner2 2.1.0 and the
[official schema source](https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/inference/schema.py).
The [official project documentation](https://github.com/fastino-ai/GLiNER2)
describes entity extraction with optional descriptions. No dependency upgrade.
