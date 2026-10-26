# Author Explanation

## Intent And Success Criteria
Prevent malformed condition generation exposed by arraysQ20 without editing knowledge or weakening validation. Fixed gates require45real-agent answers with >=14/15each repeat, all controls and no critical/delivery errors, plus all18fresh planner probes passing independent semantic review.

## Plan-To-Implementation Traceability
PLAN.md defines the separate runtime candidate and measurements. Candidate planner changes only generation contract/schema selection. New experiment changes only selected planner and checked DB path. Candidate-only evaluator implements the declared gates.

## Technical Approach And Flow
Same one-shot hosted transport, raw audit, command builder/decoder/model settings; full old contract prefix plus completion audit and index-array minItems1. CapitalizingPlanner and strict validator remain unchanged. MCP opens the original isolated85-fact DB read-only; no build entry point exists.

## Changed-Component Walkthrough
condition_candidate_v1 owns prompt/schema/transport and tests. arrays-condition-v1 owns immutable artifact selection, experiment wrapper, copied assessment assets, fixed cases, fresh planner probes and decision evaluator. Ignored scripts orchestrate three repeat streams, preserving every attempt and denominator.

## Decisions And Rejected Alternatives
Strengthen generation prospectively. Do not infer empty index assignments, normalize arbitrary API casing, drop ledger conditions or retry until a case passes. No full replan/repair loop is introduced.

## Invariants And Boundary Conditions
229 protected pins include installed/runtime/model state and prior arrays source/build/freeze artifacts. Copied grading assets and array facts must equal originals. Original failure remains rejected. Structural validity cannot prove semantic attachment or detect undeclared omissions; fresh probes are an additional gate.

## Verification Performed And Results
Worker TDD reports12planner tests and14harness tests passing, with baseline-schema empty-index acceptance failing before change. No hosted inference yet. Independent reviewer will run proportionate checks. All229baseline pins and exact85-fact DB hash checked during preparation.

## Risks, Tradeoffs, And Maintenance Costs
Prompt/schema changes reduce a known malformed-output path but do not guarantee future generation. One-shot transport is duplicated narrowly to select explicit local paths without changing frozen globals. Unseeded hosted generation remains variable. Concurrent repeats cannot establish comparative latency.

## Deviations, Deferrals, And Known Gaps
Same15arrayscases are deliberately reused for requalification, supplemented with six new planner-only cases. No concurrent old-runtime baseline is rerun, so prior44/45cannot establish causal improvement. No promotion or publication. Semantic checks and full end-to-end delivery remain unexecuted until the run.

## Challenge Points For The Reviewer
Check exact contract prefix/schema delta, one-call/no-tool behavior, strict-validation negatives, preserved global state, copied facts/assets, output confinement, complete denominators, semantic scope/negation/literals, and absence of hidden retry or stale-assessment reuse.
