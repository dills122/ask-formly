# Author explanation

Intent: remove source-target collision as a native request-record identity limit,
preserving all pilot gold, then check training mechanics before broader work.

Plan trace: new anchorless exporter and explicit negative relation tasks; TDD
red/green;24 native transports plus per-field/typed entity/relation target checks;
24 oracle record sets; natural-mode negative control; actual encoder-adapter
gradient checks;24 joint updates; save/fresh-base reload output parity; integrity.
No outside POC code reuse, no knowledge reads, no A execution, no evaluation.

Files: revision.py reuses POC-local frozen pilot contract and changes metadata plus
absent relation slots; compatibility.py validates actual target tensors and exercises
native record formation/decoding; training_smoke.py uses installed trainer setup
and a deliberately transparent bounded optimizer loop; tests encode acceptance.
PLAN defines this new targeted protocol; evidence and smoke-run retain all results.

Choices: anchorless mode removes the requirement to choose a unique literal target
or verb per ask. Keep target_anchor as an ordinary field for unchanged canonical
gold. No branch-per-question anchor rules. Use existing32 native learned instance
queries, not checkpoint architecture edits. Do not silently train task heads:
encoder LoRA only; explicit inventory and per-parameter hashes enforce that.

Verification:10 non-optimizing tests pass (all24 native subcases);1 training
acceptance test passes;24 optimizer steps plus four isolated task-gradient checks;
144 changed adapter tensors,0 changed frozen tensors.24 decoded outputs identical
before/after adapter reload.137 protected hashes unchanged. Code/artifact hashes
frozen before review. Training test emits failures and does not retry; current
smoke-run output cannot be overwritten. First native test failed on dict attribute
access, fixed using installed configuration shape before any optimization.

Limitations: native oracle supplies perfect scores, not model correctness. Dense
record formation is exercised/capacity checked, but oracle field equality is through
native ragged decode; actual dense losses are exercised by model training. Full
Trainer.train schedule and dev checkpoint selection not exercised. Gradients per
task observed on fixed P02 only, joint finite checks all24. No quality metrics or
fair latency claims. Guard is defense in depth. Training whole-model parameter
hashes are computed before/after in memory, counts retained; original checkpoint
files also covered by independent protected manifest. Full training not run.

Challenge points: target identity without gold rewriting; absent relation labels
really yield zero edges; scope/read isolation; no auxiliary losses silently dropped;
adapter saving contains all trained weights; parity not mistaken for usefulness;
review allowance4/4 honored. Recommend accepting measured compatibility only if
evidence supports it, not treating this author account as a readiness verdict.


Review supplement: native dense oracle now transports gold field assignments
through the packed-to-ragged decoder on all24 cases. Saved-adapter reserialization
now checks seeded training-mode losses and complete batch fingerprints as well
as parameters/outputs, without optimization. Python random sampling explained
the initial loss mismatch; torch-only seeding was insufficient. Original
pre-first-save losses were never captured; this narrower supplement cannot
retroactively establish them. See FINDINGS.md for retained failed attempts.
