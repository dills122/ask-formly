# Bounded verifier compatibility check

Scope: exact-span, independent binary boundary/role verification only. No full training,
no operational resolver integration, and no efficacy or latency qualification.
Both baseline extractors, A, v2, all previous artifacts and data/DB remain frozen.
All new files live in this directory. No evaluation content is read.

Use the eight previously selected training-only compatibility questions, verifying
membership against the original 194 training rows and their negatives. Add one
explicitly synthetic repeated-occurrence transport probe; never count it as evaluation.
Targets: complete=1 and exactly the gold role=1 for gold mentions; all seven targets=0
for malformed negatives. Boundary and role logits share parameters; independent
sigmoid decisions do not mean independent representations or calibrated probabilities.

Check both frozen baseline adapters read-only using the new schema, not a claim that
those adapters were trained for this schema. Compare explicit-span scores to native
multi-label attribute attachment, including each probability and exact character identity.
Unsupported offsets must be reported without snapping or claiming learned rejection.
Synthetic logits must show native zero, one, and multiple role outputs and boundary veto.

Create a separate fresh LoRA verifier from the pinned local pretrained checkpoint for
each seed (1701,1702). Do one disposable SGD update at 1e-4 on the eight training rows,
using BCE on the seven supplied-span logits. Check finite nonzero gradients, only LoRA
parameters updated, frozen state preserved, and first-save state/output parity. This
is gradient compatibility, not full training or a requirement that accuracy improves.

Freeze source/panel before model execution. Retain raw results. Check all inherited
protected manifests before and after. Independent fresh-context review precedes any
full training decision. Full training would still need a reviewed dataset, fixed
threshold selection protocol, and operational nonregression/repair/latency gates.
