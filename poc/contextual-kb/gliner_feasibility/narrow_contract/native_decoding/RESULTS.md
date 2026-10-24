# Native nonoverlapping decoding results

Native `overlap_policy="flat"` passes the frozen useful-without-loss gate on
both latest adapted models. It removes all observed invalid overlaps while
preserving every previously correct raw mention. Use flat as the candidate
setting for the next experiment. This is not a production or integration pass.
No serving configuration or earlier candidate was edited.

## What was compared

Both challenge_adaptation epoch8 adapters (seeds1701/1702), the same pinned base,
six described labels and threshold0.5. Each received challenge24 and olddev24
under both nested and flat:192 actual extraction calls. Policy order alternated
per question. All96 nested controls exactly matched the earlier saved outputs,
including confidences. Parameter hashes matched the saved adapters and stayed
unchanged after inference. No training, dependency changes, schema changes,
custom span repair or per-question policy selection occurred.

These are exposed synthetic diagnostic questions. They test the decoder change
on known failure cases, not fresh generalization, real v2 traffic, ambiguity
handling, retrieval or answer accuracy.

## Results

| Challenge24 | Seed1701 nested→flat | Seed1702 nested→flat |
|---|---:|---:|
| Completely correct envelopes | 14→17 | 17→19 |
| Invalid envelopes | 4→0 | 3→0 |
| Raw exact typed-span F1 | 94.3%→97.1% | 95.4%→97.5% |
| F1 after envelope validation | 87.6%→97.1% | 88.4%→97.5% |
| Correct raw mentions | 116→116 of119 | 115→115 of119 |
| False raw mentions | 11→4 | 7→2 |

On olddev24, seed1701 improves23→24 completely correct, invalid1→0;
seed1702 stays24/24 correct with zero invalids. Both reach100% exact typed-span
precision/recall on that exposed diagnostic set. Flat removes the quote-interior
duplicate in V10 that caused the latest adaptation regression.

Across both splits and seeds, flat removes13 false mentions, loses zero correct
mentions, adds zero false or correct mentions, and introduces zero invalid
outputs. The8 previously invalid model/question outputs become valid. Valid does
not mean completely correct: some retain independent omissions or false positives.
Accepted correct counts improve from312 to355 across the96model/question cases,
while raw correct count remains355. These totals count each model separately.

The frozen gate passes: both seeds lose zero correct raw mentions, reduce total
invalids, introduce zero invalids, and do not reduce accepted F1 on either split.
Exact lost/new/removed spans and overlap counts are retained in
`test-output/changes.json`; complete metrics and outputs are in `scores.json`
and the individual prediction files.

## What the library actually provides

Installed `gliner2/inference/overlap.py` maps flat/disallow to maximum-total-score
nonoverlapping span selection. The boundary decoder applies this resolver inside
each entity-label query, in `models/boundary/engine.py::_decode_content_entities`.
This is per-label resolution, not a guarantee of global mutual exclusion across
roles. Native filtering happened to remove all cross-role conflicts in these
cases too, by removing a conflicting span within its own label's candidates.
The downstream contract validator must remain in place.

The [official GLiNER2 API documentation](https://github.com/fastino-ai/GLiNER2)
describes the overlap-policy options. The pinned installed implementation,
frozen with this run, is the execution evidence. No library source was changed.
A score-based resolver can choose a wrong boundary on other examples; zero lost
correct mentions here is an observation, not a universal guarantee.

## Remaining limitations

Both still omit `hide` in repeat-03, configuration `key` in roles-03, and the
supplied label literal in roles-07. Seed1702 also misses a value in roles-04 and
emits the ordinary word `text` as a value. Quoted behavioral-claim false positives
remain: four for1701 (claims-03/05/07/08), one for1702 (claims-07). These semantic
errors do not overlap anything, so flat decoding does not remove them.

Both recover24/24 compound API boundaries. Quoted-name/key/value recovery remains
33/34 and32/34. All per-role precision/recall now meet90% on this challenge, and
invalids are zero, but the frozen critical-boundary/mention coverage requirement
still fails. Neither candidate meets full qualification. Do not select the better
seed from this exposed sample and describe it as independently validated.

Measured extraction totals across48questions: nested9.75/9.68seconds versus
flat9.64/9.57seconds. These single local CPU passes are roughly0.20seconds per
question, exclude loading, and do not establish a meaningful speed advantage or
service latency under load.

## Verification and next step

Five comparison tests passed after a recorded failing run. Independent review
checks the native policy path, full baseline identity, scoring and every removed
or retained error; see REVIEW.md. Protected-file hashes are recorded separately
in test-output/protected-after.json. A,v2,data/DB and prior evidence remain
unchanged. Older sealed evaluation contents were not inspected.

Carry native flat forward as the experimental decoder, retaining strict global
validation. The next useful qualification is a fresh independently authored mix
of realistic focused Formly questions, including quoted claims versus values,
ordinary-word API names and role contrasts. Test both frozen candidates before
any further tuning. This round resolves the observed overlap problem without
more training; it does not resolve the remaining semantic coverage problem.
