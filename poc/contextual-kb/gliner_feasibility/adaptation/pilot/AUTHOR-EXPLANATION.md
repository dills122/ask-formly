# Author explanation

Intent: determine annotation reliability and whether the proposed native
question-frame representation is trainable in principle before full adaptation.

Implemented: 24 new training-only questions; independent raw annotations by author
and fresh-context annotator; v1/v2 guide calibration and raw agreement; adjudication
and explicit correction history; pure validator/exporter and access guard with
TDD; installed InputExample round trip; real local-model training preprocessing;
native instance-formation/oracle decoding acceptance test; integrity manifests.

The flow is annotations -> strict source validation -> native JSON structures,
entities/classification/relations -> library preprocessing. No retrieval plan or
queries, no database access, no optimizer and no prediction pass. Existing model,
prior evidence and A remain frozen. New files only in pilot/.

Key implementation choices: preserve exact Unicode occurrence offsets and two
gold aspects even when they share an anchor. Native decoder test invokes real
RecordHead.forward_group with supplied candidates, then supplies perfect assignment
scores; it isolates record capacity from prediction quality. Empty fields remain
empty. Pure helper tests do not pretend to establish semantic annotation quality.

Verification: 13 unit tests pass; 24 native round trips pass after a test-only
default-normalization correction; all24 corrected record fields survive real
training preprocessing; distinct-anchor control passes; same-anchor acceptance
fails. Final suite16/17 pass, one unmet native requirement. Initial red logs,
overstrict test failure and P20 annotation failure retained. Raw v2 agreement
.981053; count/status agreement1.0. The P20 shared error was discovered after
adjudication and separately frozen, not retroactively removed from agreement.

Plan deviations/deferrals: stop at representation gate, so backward, optimizer,
save/reload parity and bulk/full training are unexecuted. Model loads locally and
PEFT exists; that is not training success. Initial guideline failure was resolved
through the planned independent re-annotation. After the representation failure,
only non-optimization transport diagnosis/verification proceeded. No material
architecture pivot implemented. Review3/3 is spent on this user-requested findings
review rather than the later full-training implementation gate; future review
budget requires explicit revision, not an automatic reset.

Costs/limits: agent annotations, no human gold; agreement helper assumes source
order (valid here, not a general semantic matcher); no entity/relation graph-loss
verification; empty relation labels currently omit those tasks. Guard is an audit
hook, not OS isolation. Existing model-loader warnings retained. Native synthetic
oracle is a capacity check, not an accuracy measurement.

Challenge points: exact anchor collision, real rather than assumed instance
formation, annotation correction history, shell vs test status, protected hashes,
and unsupported claims about full learning/save-reload. Do not accept a misleading
all-green/full-training conclusion. Author recommends revisiting aspect identity
but has not selected or implemented alternate modes.
