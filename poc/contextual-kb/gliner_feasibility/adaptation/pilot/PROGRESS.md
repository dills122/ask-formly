# Pilot progress

Scope: 24 training questions and compatibility checks only. No full training,
development/evaluation dataset creation, held-out access, A execution or DB work.
Using TDD and independent annotation; one remaining engineering review instance
(3 of 3) will review the pilot findings before any full-training recommendation.

- Created questions and guide v1 before predictions.
- Verified prior protected hashes and captured current base-model hashes.
- Completed two independent annotation rounds: initial exact feature F1 .801603;
  after guide clarification .981053; counts/status agree24/24 throughout.
- Completed TDD unit work (13 pass), native semantic round trips (24 pass), and
  real training preprocessing (24 corrected records pass). Original failed logs
  and separately corrected gold retained.
- Native same-target record identity fails even with oracle candidate scores.
  Stopped before optimization under the design's representation gate; backward,
  gradient and adapter save/reload checks remain unexecuted.
- Final combined acceptance:16/17 tests pass, one deliberate unmet requirement.
- Verified90 protected hashes unchanged. Independent findings review3/3 completed:
  accepts pilot findings, full training not ready; reproduced16/17 and105 hashes.
  Accept structural blocker. No implementation fix or new review instance started.
  No full-training or evaluation access follows automatically from this review.
