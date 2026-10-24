# Record identity revision — compatibility findings

Status: independent review4/4 complete: ready with non-blocking follow-ups for
bounded identity/mechanical compatibility. See evidence/independent-review.md.
Same24 exposed training pilot questions; no evaluation cases opened.

## Change and result

The original target-based natural anchor cannot represent two requested operations
sharing a target occurrence. The revision uses native **anchorless records**: the
pinned model's32 learned instance queries supply record identity, while target text
is an ordinary record field. Canonical annotations are unchanged; no new
decomposition heuristic or conditional anchor-selection rule was introduced.

Explicit empty relation placeholders keep both `has_value` and `refers_to` tasks
present on every question. Strict target inspection confirms these become zero
positive edges when absent, and exact endpoint pairs when present.

| Check | Result |
| --- | --- |
| Pure exporter/input/access tests | 7 pass; failing import retained before implementation |
| Native semantic serialization and strict preprocessing | All24 preserve exact record-field attachments, typed entity occurrences and relation endpoint pairs |
| Native record decoder with gold candidates/assignment scores | All24 gold record sets represented, including P04's two requests about the same wrapper |
| Dense instance formation and field transport |32 valid hypotheses; all24 gold record sets decode exactly through native packed-to-ragged conversion |
| Natural-mode collision control | Still cannot reproduce the same-target two-record gold |
| Per-task gradient check | Entity, record, relation and classification losses each produce finite nonzero encoder-adapter gradients on fixed positive P02 |
| Bounded joint smoke |24 optimizer steps, one per pilot question, with finite joint losses/gradients and all expected auxiliary losses present |
| Trainable/frozen state | Encoder LoRA only;144 adapter tensors changed, zero frozen parameter tensors changed |
| Adapter save/reload | Identical decoded outputs including confidences on all24 questions after fresh-base reload |
| Integrity |137 protected file hashes unchanged: A/data/prior artifacts/model and complete prior pilot evidence |

Seven unit tests plus three native acceptance tests pass; the training acceptance
test separately passes. No tests were skipped. First native attempt exposed a
helper error treating the checkpoint's dictionary configuration as an object;
the fixed API access and both logs are retained. No optimizer ran in that failed
attempt. The sole optimization run completed successfully. Loader/deprecation
warnings remain in the evidence; package/model versions remain unchanged.

## What the checks prove

The **specific representation blocker is removed**. Two records can contain the
same target span with different requested operations. Shared-action/two-target,
shared conditions, negation, nested identifiers and repeated occurrences from the
same24 cases survive transport and oracle representation checks. The gold is not
rewritten to fit the library.

The oracle uses actual native RecordHead instance formation and decode_group,
but supplies gold candidates and assignment scores. This proves representational
capacity, not learned prediction quality. Dense-path checks also transport supplied gold field assignments through native
PackedRecordDecodeOutput and packed_record_group_to_ragged into decode_group.
This still bypasses learned public prediction selection. The dense joint loss
is exercised in the actual model smoke.

The smoke uses installed ExtractorTrainer setup (including freeze/LoRA injection),
then a transparent PyTorch AdamW loop for exactly24 updates. It does not exercise
the complete ExtractorTrainer.train scheduling/checkpoint-selection workflow.
It is one compatibility pass, not the planned120-question, two-seed experiment.
No semantic accuracy grades, model selection, held-out improvement or A comparison
can be inferred from its losses or outputs.

## Settings and evidence

GLiNER2 2.1.0, same GLiNER2.5 checkpoint revision
54785d51df8d86a0d8f2eb212fec15871aad2c4d. CPU4 threads, float32, seed1701;
encoder LoRA rank8/alpha16/dropout0, AdamW1e-5, weight decay.01, batch1,
gradient clipping1.0. Random task/schema removal disabled; full gold proposal
injection for training compatibility. No change to native32 instance capacity.
Inference uses threshold.5 and nested overlap. Base task-head weights stay frozen;
nonzero gradients through a head do not imply its own parameters were trained.

Smoke worker elapsed30.36 seconds; controller elapsed39.15 seconds including
process imports/startup, well within the30-minute bound. These are single-run
compatibility timings, not a training throughput or planner latency benchmark.
Saved adapter artifacts total approximately5.34 MB including metadata.

- [Protocol](PLAN.md), [code/input freeze](evidence/smoke-freeze.json)
- [Native checks](evidence/05-native-second.txt), [training log](evidence/07-training-attempt.txt)
- [Training report](smoke-run/report.json), [task/step losses](smoke-run/steps.jsonl), [trainable inventory](smoke-run/trainable.json)
- [Pre-save outputs](smoke-run/before-reload.json), [reloaded outputs](smoke-run/after-reload.json)
- [Protected integrity](evidence/integrity-after.json), [review artifact manifest](evidence/review-freeze.json)

No model process reads knowledge, other question sets or data/DB files. The
controller's hash checks read protected bytes only. All outputs/cache are inside
this POC. Audit hooks are defense in depth, not OS sandboxing.

## Next decision

The completed independent review supports carrying anchorless records into
the annotation/adaptation experiment design. Full training is still not performed
or automatically authorized by these checks. Before full execution, freeze the
native record mode and negative relation supervision in that protocol, prepare
the approved grouped training/development data and separately sealed evaluation
set, and implement/review the real training/evaluation workflow. Keeping base
task heads frozen is the configuration tested here; any adapter-plus-head change
needs separate compatibility verification. The original24 questions are now
training-exposed and must never serve as held-out evidence.

## Additional checks requested during review

The original smoke captured pre-first-save outputs but omitted losses. That
historical omission cannot be repaired retrospectively. The supplement checks
the narrower property of reserializing the already saved adapter, with zero
optimizer updates. Initial loss parity failed despite equal parameters and
outputs. A diagnostic isolated Python random sampling in native preprocessing:
resetting only PyTorch produced different batches; resetting Python too produced
identical batches. No tolerances were relaxed.

The seeded second attempt achieved exact batch, loss, parameter and output
parity but failed when serializing mappingproxy metadata for evidence. The third
attempt permits string serialization of non-JSON metadata only; equality is
still tested on the complete in-memory fingerprints before serialization. Failed
attempts remain preserved alongside the final report. This is checkpoint
transport evidence, not an accuracy result or a full trainer workflow test.

Supplemental evidence: `evidence/rng-diagnostic.json`,
`reload-supplement/report.json`, `reload-supplement-v2/report.json`,
`reload-supplement-v3/report.json`, and
`evidence/11-supplement-seeded-serialization.txt`. The original review freeze is
historical; `evidence/review-final-freeze.json` covers the supplemented sources.
