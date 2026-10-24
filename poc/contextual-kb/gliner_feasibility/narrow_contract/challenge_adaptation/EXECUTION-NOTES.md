# Execution notes

The first baseline command failed before any model loading/inference because the
runner treated challenge-freeze.json as a flat path/hash map. The reviewer used
an explicit versioned metadata envelope with files[path].sha256. The original
manifest and failed baseline.log remain preserved. An additional unit test first
failed on missing challenge_hashes, then passed after adding the explicit format
reader and wiring it into baseline(). Seven tests pass. No question, annotation,
model, or experiment setting changed in this repair. Successful replay is in
baseline-retry.log. The run freeze was first created by the repaired runner.

Baseline on fresh challenge24: seed1701 raw F1 .8863, accepted .7463, exact9,
invalid6; seed1702 raw .8682, accepted .5380, exact5, invalid11. Prior dev24 replay
matches original results exactly at the scored-span level. Challenge failures
justify the predeclared adaptation step. The separate 36 authored additions and
protocol were frozen before any successful baseline inference. No additions
were selected from challenge-specific outputs or copied from challenge questions.

Independent pretraining review found no remaining blocker. Continuation started
only after that review. Both corresponding epoch16 checkpoints are continued;
no checkpoint is selected from the pair. Model settings, code and datasets remain
frozen through both runs. The eight-epoch final checkpoint is scored regardless
of whether improvement is sufficient. Baseline challenge is now exposed; after
adaptation it is a paired diagnostic test, not a new untouched holdout.
