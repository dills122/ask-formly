# Targeted record-identity revision and compatibility protocol

User authorized this revision on the same 24 pilot cases, with one additional
independent review before full training. Review accounting: next instance 4 of 4.
No bulk annotation, evaluation access, A changes, DB work or full training.

## Revision selected before checks

Use the installed library's **anchorless record mode**, with its existing 32
learned instance queries. Records represent requested aspects; multiple records
may refer to the same target occurrence. Preserve all canonical gold spans and
pairings from pilot/adjudicated-v2.json. `target_anchor` remains a source field
for backward comparison but no longer controls native instance identity. Do not
create new heuristics that select different anchors case by case. No model weight
or architecture setting changes are needed to test the mode's representation.

Unlike latent mode (candidate-seeded), anchorless mode does not make record count
depend on a particular source candidate. It has a bounded capacity: 32 instance
hypotheses in the pinned checkpoint, whereas this pilot requires at most two.
That is capacity, not proof that predictions will identify the correct records.

Keep natural-mode failure evidence unchanged. New exporter calls the POC-local
pilot validator/exporter, changes only record metadata, and supplies explicit
empty head/tail placeholders for each absent relation type, so relation tasks
are represented on negative examples as well. Verify the library retains these
as zero-edge supervision rather than interpreting them as positive relations.

## TDD and checks

1. Write failing tests for mode metadata, unmodified gold, same-target records,
   explicit negative relation tasks and invalid-input rejection. Implement the
   minimal exporter and fixed-input/access checks; preserve red/green logs.
2. On all 24 cases, verify native serialization, strict training preprocessing,
   exact field occurrences/attachments and typed entities/relations where the
   library exposes targets. Reject truncation or discarded labels.
3. Exercise native anchorless instance formation and decoding with oracle field
   scores for all 24 gold record sets, including P04's same-target two requests,
   shared cues/conditions, nested and repeated occurrences. Retain a natural-mode
   collision control. Also exercise the dense path used by the installed model.
4. If representation passes, bounded actual compatibility smoke: local CPU4,
   float32, seed1701, encoder LoRA rank8/alpha16/dropout0; at most one pass of the
   same24 examples, batch1, at most24 optimizer steps and30 minutes total worker
   time. Disable random task/schema removal. Require finite joint losses and
   gradients; record active trainable parameter names and changed/frozen weights.
   Check per-task loss gradient paths to adapters on an applicable positive case,
   and retain all failures. Save adapter under this directory; fresh local base
   plus saved adapter must reproduce pre-save deterministic outputs/losses on
   the pilot. No task-head training is silently added: encoder-only LoRA leaves
   head weights frozen. If this limits learning it is a future design question.
5. Independent review4/4 of findings and implementation. No full training follows
   automatically even if compatibility passes. Report which checks actually ran.

All new evidence/cache/artifacts live here. Prior90 protected paths and all prior
pilot files are hashed. Load only fixed SHA-frozen pilot input; all other question
sets and knowledge files unavailable to model worker. Offline inference/training,
no retrieval calls, no outside-project implementation reuse. Standard library and
installed third-party packages are allowed. Audit hooks are defense in depth;
parent controller supplies the hard wall-clock bound.

## Sources and limits

Installed GLiNER2 2.1.0 `models/boundary/records.py` and `processing/records.py`
define anchorless mode, learned query count, Hungarian matching and decoding.
The official JSON tutorial links boundary documentation, but that linked URL
returned404 during this revision; installed source is the compatibility authority.
Official [JSON tutorial](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/3-json_extraction.md)
and [LoRA tutorial](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/10-lora_adapters.md)
provide the public API context. Success here means representational/training
plumbing compatibility, not generalization, complete plans or answer accuracy.
