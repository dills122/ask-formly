# Fresh challenge and targeted adaptation results

Both saved models improved after targeted supervision. The paired replacement
gate nevertheless failed: seed1701 introduced an invalid overlap on an older
development case. Neither final candidate qualifies for integration. Preserve
both as experimental artifacts; do not select seed1702 on this exposed test and
present it as independently qualified.

## Experiment and scope

The independent reviewer authored and froze 24 new clear-input questions before
seeing training examples or prior outputs: eight repeated values, eight
same-string/different-role contrasts, eight quoted claims versus configuration
literals. The implementation author separately froze 36 training additions,
12 per family, before baseline inference. Reserved custom names differ. Shared
library syntax and related templates remain; this is synthetic targeted evidence,
not a representative traffic benchmark or old sealed evaluation.

Both previous epoch16 checkpoints were tested unchanged first. Both failed,
triggering exactly one predeclared continuation experiment: eight epochs on all
62 original training questions plus 36 additions, corresponding seeds1701/1702,
AdamW1e-4, serial accumulation8, final chunk2,104updates each. No decoder,
threshold, labels or schema changes. No repaired predictions became training
gold. All146 train/challenge/regression rows passed native exact-span transport
for both input checkpoints. Only training rows entered gradient updates.

The old24 development questions are exposed regression diagnostics. The new24
challenge questions are now exposed too; their post-adaptation scores are a
paired comparison, not a second independent holdout.

## Fresh challenge results

| Metric | 1701 before | 1701 after | 1702 before | 1702 after |
|---|---:|---:|---:|---:|
| Raw exact typed-span F1 | 88.6% | 94.3% | 86.8% | 95.4% |
| F1 after envelope validation | 74.6% | 87.6% | 53.8% | 88.4% |
| Completely correct envelopes | 9/24 | 14/24 | 5/24 | 17/24 |
| Invalid envelopes | 6 | 4 | 11 | 3 |
| Correct raw mentions | 113/119 | 116/119 | 112/119 | 115/119 |
| Extra raw mentions | 23 | 11 | 27 | 7 |

Raw scores count individually correct spans even when the whole output is invalid.
Accepted scores reject every span from an invalid envelope. After adaptation,
accepted precision/recall are96.9%/79.8% and99.0%/79.8%; losing whole conflicting
envelopes is still a material limitation.

| Challenge family: accepted F1 | 1701 before→after | 1702 before→after |
|---|---:|---:|
| Repeated literals | 74.4%→92.0% | 36.4%→92.0% |
| Same-string roles | 67.6%→82.1% | 49.2%→78.9% |
| Quoted claims versus literals | 86.4%→87.2% | 86.4%→97.4% |

Raw quoted-claim false positives fell from six each to four/one. Both final models
found all24 compound API paths exactly. Quoted-name/key/value recovery was33/34
and32/34, with remaining omissions distinct from extra overlapping spans.

## Regression outcome and frozen decision

On olddev24, seed1701 accepted F1 improved97.5%→98.4%, with23/24exact unchanged,
but invalid count rose0→1. It now recovers the three repeated V20 values, yet
adds an interior value span overlapping the correct escaped-string span in V10.
Seed1702 improved95.0%→100%,21→24exact, invalid1→0.

Both seeds pass the challenge gain, exact-count and family checks. The paired
improvement/replacement gate is **false**, because it also required no increase
in olddev invalid outputs for either seed. Aggregate improvement cannot erase
that failure. Qualification also fails: challenge invalid outputs remain,
quoted mentions are missed, and some per-role precision/recall is below90%.
No candidate was integrated or promoted.

## Remaining errors

Every residual case is recorded with exact missing/extra spans in
`test-output/final-failures.json`.

- Both omit `hide` in repeat-03 and configuration `key` in roles-03.
- Both omit the supplied label literal in roles-07; seed1702 also misses the
  label literal in roles-04 and emits a larger overlapping API span plus `text`
  as a value.
- Both add oversized version spans in repeat-02 and roles-06; seed1701 also
  does so in claims-03. Correct version tokens are present but invalidated by
  their overlapping extras.
- Seed1701 adds an oversized value in roles-05.
- Quoted behavioral-claim false positives remain in claims-03/05/07/08 for
  seed1701 and claims-07 for seed1702.
- Olddev V10 gains a nested interior-value duplicate for seed1701.

Training fit is96/98 and97/98 exact, raw F199.4% and99.8%; it is not qualification.
Full challenge extraction takes4.63/4.54seconds for24questions, approximately
193/189ms per question on this local CPU. These single sequential passes exclude
model loading and do not establish service latency or determinism under load.

## Verification and interpretation

Seven trial-specific tests passed after recorded RED runs. One initial baseline
attempt failed before inference due to a freeze-manifest reader mismatch; its
log remains preserved. The correction was tested and independently reviewed
before training. See EXECUTION-NOTES.md.

Both continuations completed all104updates. Epoch1 and epoch8 saves each reproduce
original outputs and parameter hashes after fresh reload. Frozen base weights
remain unchanged. The independent review checks full scoring, native transport,
training records, saved artifacts and all residual failures; see REVIEW.md.
Protected-file hashes are recorded in test-output/protected-after.json.

The narrow model is learning useful distinctions, especially repeated values
and occurrence roles. It still emits incompatible or oversized spans, and the
remaining failures vary by seed. More examples alone cannot be assumed to solve
this. The next bounded investigation should determine whether the library's
native decoding can enforce this contract's nonoverlap requirement without
losing correct mentions, compared fairly across both old and adapted candidates.
That would be a separately frozen experiment, not a retrospective change to
this trial. Keep ambiguity handling and realistic v2-output qualification as
explicit remaining work. Do not claim retrieval or answer-quality improvements.

All new work is inside challenge_adaptation. A, v2, data/DB and earlier evidence
remain unchanged; no older sealed evaluation contents were inspected. Full paired
scores and all raw predictions are retained in test-output/final-scores.json and
before-/after-1701/1702 directories.
