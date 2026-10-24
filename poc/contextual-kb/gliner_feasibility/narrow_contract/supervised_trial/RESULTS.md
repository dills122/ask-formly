# Six-role supervised feasibility results

Decision: supervised adaptation is worth continuing; neither candidate is
qualified for integration. Both fixed training seeds substantially improved exact
typed extraction on the separate development set. No threshold, checkpoint,
labels, or decoder rules were selected using these scores.

## What ran

62 training questions (22 clear pilot cases plus 40 new cases), 24 independently
authored development questions, six entity roles, two fixed seeds, 16 epochs and
128 optimizer updates per seed. All 86 questions passed native exact-span target
transport checks before optimization. The existing base model and descriptions
were used; the rejected repair rules and older adapted checkpoint were not used.

The development author did not see training examples or model predictions.
These are small synthetic development sets with related templates, not a human
benchmark or the older sealed evaluation. Four development questions are empty
negative cases. There are only five registration-name and four model-key mentions.

## Development results

| Metric | Untouched base | Seed 1701 | Seed 1702 |
|---|---:|---:|---:|
| Exact typed-span precision | 41.3% | 100% | 96.7% |
| Exact typed-span recall | 69.4% | 95.2% | 95.2% |
| Exact typed-span F1 | 51.8% | 97.5% | 95.9% |
| F1 after whole-envelope validation | 12.3% | 97.5% | 95.0% |
| Completely correct envelopes | 3/24 | 23/24 | 21/24 |
| Invalid envelopes | 13/24 | 0/24 | 1/24 |
| Total measured extraction time | 3.93 s | 4.61 s | 4.36 s |

Times are single sequential CPU passes, roughly 164/192/182 ms per question;
they exclude model loading and do not establish service latency under load.
Raw scores retain individually correct spans even in conflicting envelopes.
Accepted scores discard spans from an invalid envelope, as required by the
unchanged contract.

Both trained models recovered all 24 API references, five registration names,
four model keys, ten version tokens and seven adapter mentions. Seed 1702 also
added one wrong registration role. Both recovered nine of twelve values; seed
1702 added one wrong value. All 18 compound API boundaries were exact. Quoted
name/key/value recovery was 11/14. The opaque callback expression in V12 was
recovered as a whole value by both seeds.

The frozen continuation gate passes for both seeds: raw F1 gains of 45.7 and
44.1 percentage points, improved accepted F1, and no role-recall regression.
Qualification fails: value recall is 75%, quoted-value misses remain, and seed
1702 has an invalid role-conflict envelope and registration precision of 83.3%.

## Every remaining development failure

- **V20, both seeds:** omitted all three occurrences of `"Waiting"` supplied for
  `props.placeholder`, `props.description`, and the negated `props.label` use.
  All three API paths were found. The contract requires mentions even when the
  request says not to use them. This is not exclusively a negation failure:
  the two affirmative occurrences were also missed.
- **V07, seed 1702:** found both exact quoted occurrences of `'memberToken'`,
  but assigned both model-key and registration-name roles to the first one.
  The overlap makes the whole envelope invalid.
- **V24, seed 1702:** extracted the interior of a quoted behavioral statement
  as a value, although it was a claim about Formly, not a supplied configuration
  value. Seed 1701 correctly returned no mentions.

These observations identify failures, not proven internal causes. Repeated
surface text, local role assignment, and quoted claims versus supplied values
need stronger coverage. No rules or training changes were made after seeing them.

## Training and verification

Training-set raw F1 reached 99.75% for both seeds; each had 61/62 exact envelopes.
This is fit evidence only. Development gains, including reserved custom names,
show transfer within this limited test distribution; they do not prove general
Formly coverage, ambiguity handling, retrieval quality, or answer accuracy.

Eight data/assessment unit tests passed after recorded failing tests. Native
transport checks covered every labeled training/development span. Epoch-one
and final saves were compared against freshly loaded adapters using exact
outputs and parameter hashes. Frozen base parameters remained unchanged.
The full run completed successfully and verified its frozen inputs. Independent
data, harness and result review is recorded in `DATA-REVIEW.md` and `REVIEW.md`.

## Next decision

Keep the trained artifacts as experimental candidates. The next useful step is
a fresh, independently authored challenge set focused on repeated occurrences,
role contrasts, quoted claims and real v2-style questions, frozen before further
adaptation. Evaluate both existing candidates first. If the weakness repeats,
add separate training examples for those behaviors and rerun the fixed paired
experiment; do not relabel this development set or treat it as unseen again.
Ambiguous-input handling still needs a separate qualification step.

Do not integrate yet, choose a seed based on these 24 questions as if that were
independent validation, or expand back into broad records or repair-rule growth.
This experiment supports continuing the narrow supervised approach.

All new files remain in this trial directory. A, v2, data/DB and prior evidence
are unchanged; old sealed evaluation contents were not inspected. Full outputs
and scoring are in `test-output/scores.json`, with raw predictions, loss logs,
saved adapters and receipts alongside it. `protected-after.json` records the
final protected-file hash audit.
