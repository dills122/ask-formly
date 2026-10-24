# Author explanation

## Intent and scope
User requested a new candidate addressing missing support checks and dropped conditions, fresh requests repeated three times, independent review, all existing candidates/baselines/DB unchanged and evaluation sealed. New files only in refinement_v6. No runtime deployment, retrieval, answer assembly, training or GLiNER changes.

## Approach
V6 preserves the full v5 contract and adds AUDIT.md before the output section. The added instructions distinguish requested support from conditional use, build per-aspect condition attachment, propagate ancestors of nested gates and same-scenario dependencies, reconcile exclusions and uncertain global scope, then check every requested aspect. The emitted three-field schema is unchanged. candidate.py only selects this prompt and delegates validation/advisory projection to frozen same-POC v3 code. No source code from outside this POC is imported. This is a fallible prompt refinement, not a deterministic semantic completeness algorithm.

## Verification design
TDD red occurred because the new candidate module did not exist; green6 tests verify selection, verbatim input, invalid input, strict parsing, exact declared-condition enforcement and compatibility/hint invariance on all72 old outputs. A negative-control test confirms old semantic omissions still pass structural validation. These tests cannot establish semantic fixes. Seven frozenv5 and eight aggregation tests pass. The prior five failed requests are copied unchanged as a diagnostic batch (15 responses), separate from independently authored24 fresh requests (72 responses). Author sees v2scope/v5policy, not v6 instructions or prior cases/outputs. Candidate frozen before generation; cases/rubrics frozen before their batches run. No tuning against fresh outputs, no feedback or resampling; all first submissions retained.

## Evidence flow and limits
Each native generation context receives full frozen contract and assigned requests only. Nine fresh and three diagnostic batch contexts each run once. Saved output is parsed/reconstructed into87 slots, structural assessment uses frozen v3_stress assess.summarize; independent review supplies semantics/binding/stability grades. Fresh and diagnostics never combined into a success rate. Exact canonicalJSON separate from meaning stability.

Preservation extends v5_stress's33-manifest chain with its final43-artifact freeze (34 manifests total). Only byte reads of sealed/data/weights, no semantic inspection. Graph metadata for relevant helper paths was not_tracked; complete direct-source reads support limited code conclusions. Existing dirty worktree is excluded, no staging/commits. Native model revision/temp/seed uncontrolled, repeated outputs correlated; synthetic results cannot establish production accuracy, latency or final-answer correctness. No contemporary v5 arm, so no causal claim that historical fresh percentages improved. File hashes prove contents, not unseen generation history.

## Challenge points
Do the added instructions actually improve requested support and attachment on fresh requests without over-propagation or extra unsupported asks? Inspect every response independently, including metadata, local restrictions and optional history, not merely the known failures. Rubrics are evidence and may contain mistakes; identify true ambiguities without weakening predeclared requirements. All-negative or mixed results must remain visible. Do not read author's rationale as readiness proof.

## Pre-generation rubric corrections
Parent corrected N12 uncertain-global-version expectation and N13 meta-instruction ledger requirement before any fresh generation. Original author rubric retained; data-review.md explains both. No request changes or output-dependent rule changes. Candidate freeze9 precedes diagnostic generation; input freeze18 precedes fresh generation.

## Cost
Prompt size rises from13,491 to17,485 UTF-8bytes (+3,994). No latency or token-cost measurements taken. Added instructions may increase reasoning load and overattachment risk; full output review is required.
