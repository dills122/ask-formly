# Annotation pilot and native compatibility findings

Status: independently reviewed (instance 3 of 3). Pilot findings accepted;
full training is not ready because the proposed representation gate fails.
Only the 24 training pilot questions were created/used.

## Annotation result

Two independent agent annotators labeled all 24 questions before model predictions.
They agreed on all aspect counts (31 total aspects) and on two questions needing
clarification. Initial exact role/span/attachment F1 was 0.801603, below .90.
Clarifying general span and attachment rules and independently re-annotating
raised raw agreement to 0.981053. Three remaining disagreements were adjudicated.
The real tokenizer check then exposed one common substring-selection error,
corrected in separately frozen `adjudicated-v2.json`.

This supports using the clarified guide for further research annotation, with
manual occurrence checks. High agreement alone did not catch shared labeling
errors. These are agent-produced annotations; no human annotation agreement or
model accuracy is claimed. All raw versions, disagreements and corrections remain
in [ADJUDICATION.md](ADJUDICATION.md) and evidence/agreement*.json.

## What passed and what failed

| Check | Observed result |
| --- | --- |
| New exporter/validator/access/analysis unit tests | 13/13 pass; retained red runs preceded implementation |
| Native InputExample validation and semantic round trip | All 24 examples pass after allowing documented/default classification serialization normalization |
| Real pinned model's training processor | All 24 corrected examples preserve request-record count and every record-field occurrence/attachment, with stochastic schema removal disabled |
| Distinct-anchor native record formation/decoding control | Two distinct supplied anchors can produce two records |
| Two requests sharing the same exact target anchor | Fails: real RecordHead instance formation plus perfect supplied decoding scores produces one record, while gold requires two |
| Final combined acceptance suite | 17 tests: 16 pass, one explicit compatibility failure; no skips |
| Protected files/model checkpoint | 90 hashes checked, none changed |
| Optimizer steps, full training, sealed evaluation | None |

The first native round-trip test was overstrict about serialization: the library
canonicalizes one classification label to a list and omits default false flags.
The corrected test checks those semantics explicitly; source annotations remain
unchanged. The first real preprocessing run passed 23 questions and exposed P20's
mislocated `disable` annotation; the corrected rerun passes all 24. Logs preserve
both failures and the model-loader warnings. No failed model runs were discarded.

## Structural blocker

P04 asks: `For the wrapper, explain registration and removal.` Both independent
annotators retained two requested operations about the same target occurrence.
The approved proposal makes that target the natural-mode anchor. The installed
library's `RecordHead.forward_group` creates one instance per anchor candidate;
`decode_group` fills fields of that instance. Supplying both action candidates
with high scores fills one record rather than creating two. The test exercises
actual instance formation, not just a manually assigned record count.

This is a mismatch between our proposed record identity and this native mode,
not evidence that GLiNER2 as a whole cannot understand the question. More examples
or a lower confidence threshold cannot make this exact representation lossless.
We did not replace distinct asks with a merged gold record to obtain a pass.

## Training compatibility status

The pinned package/model load locally on CPU, strict training preprocessing works,
and PEFT is installed. Installed `ExtractorTrainer._setup_lora` freezes all model
parameters before injecting the selected adapters. Consequently encoder-only
LoRA does not automatically train task heads; claims of separate task-head
adaptation would require an explicit, verified configuration and save format.

Per the design's stop gate, no optimizer, joint-loss/backward, gradient-flow,
adapter save/reload or learning-quality checks were executed after the
representation incompatibility was established. Those remain unverified, not
passing. We loaded the checkpoint for preprocessing; no learned predictions or
trained model artifact were produced. Wall-clock preprocessing checks are not
training throughput or question-layer latency benchmarks.

The exporter is a pilot transport helper, not a complete fixed-schema training
pipeline. In particular, empty relation lists omit relation tasks; a future
training design needs explicit negative relation-task supervision. No lossless
entity/relation target-graph or joint-loss claim follows from the record-field
preprocessing check. The unit access hook is defense in depth, not OS isolation.

## Recommendation before full training

Revise record identity and test it on these same exposed training pilot cases
before spending effort on bulk annotation/training. Candidate directions are
an aspect-specific anchor that can distinguish operations on a shared object,
or the library's latent/anchorless record modes. Neither has been tested here;
simply switching to action anchors must also handle shared-action/multiple-object
questions. Keep the canonical gold and exact attachment requirements unchanged.

This requires a targeted design revision and a new compatibility gate, not a
silent implementation change. A remains the unchanged baseline. No complete-plan,
retrieval, or answer-quality comparison is supported by this pilot.

## Reproduction

From this directory, using `PYTHONDONTWRITEBYTECODE=1` and offline HF flags:

```sh
../../env/.venv/bin/python -m unittest test_contract test_analysis
../../env/.venv/bin/python -m unittest test_native_contract
../../env/.venv/bin/python -m unittest test_preprocessing
```

The second command intentionally returns failure for the unmet compatibility
requirement. The third does not write evidence unless PILOT_WRITE_EVIDENCE=1;
that option refuses to overwrite retained output. Use the existing local model.
No evaluation fixture or DB is needed. Review the result rather than treating a
shell command's final `cat`/`tail` status as a unittest exit code; the bounded final
controller retained returncode=1 in acceptance-v2-runtime.json.

Evidence: [final acceptance log](evidence/08-acceptance-v2.txt),
[preprocessed fields](evidence/preprocessing-v2.json),
[annotation freeze](evidence/annotation-freeze-v2.json),
[code freeze](evidence/code-freeze-v2.json),
[integrity](evidence/integrity-after.json), [environment](evidence/environment.json).

Official sources: [training data](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/8-train_data.md),
[record modes](https://github.com/fastino-ai/GLiNER2/blob/main/docs/boundary_architecture.md),
[LoRA configuration](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/10-lora_adapters.md).
Installed source hashes for the specific mechanisms are retained in environment.json.

## Review disposition

[Independent review](evidence/independent-review.md) reproduced the 16/17 result,
both agreement reports and 105 current code/annotation/protected hashes. Accept
P1: the record identity blocks full training. No additional blocker to accepting
the pilot findings was identified. No architectural fix was made during review.
The next design/compatibility phase needs user authorization and an explicitly
revised review allowance; the current three-instance allowance is exhausted.
