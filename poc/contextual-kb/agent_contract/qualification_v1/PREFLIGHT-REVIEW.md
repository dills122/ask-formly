# Qualification policy and plan preflight

Review instance: 1 of 3.

Scope: policy/plan preflight before generation, not completed implementation review or output grading. Reviewed working-tree POLICY.md, PROTOCOL.md and task_plan.md against refinement_v11/CONTRACT.md and applicable AGENTS.md/STEERING.md. The task summary was already present, so a fully blind first pass was not possible. No author explanation packet, generated responses, old results, sealed evaluation semantics or data/DB contents were read. Only this report was written.

## Findings

### Resolved P2 — Question-meaning stability initially lacked an operational definition

Original evidence: PROTOCOL.md:11 required at least 44/48 stable cases without defining the per-case metric. Equivalent decomposition and optional context are allowed, so exact JSON equality cannot substitute. Three equivalent questions with different ledger completeness might otherwise be marked stable by one reviewer and unstable by another. Three consistently wrong outputs and malformed/missing slots also lacked declared treatment. This could change a gate through post-output interpretation.

The parent accepted this finding and added “Operational definitions fixed before generation” during this same preflight, before any generation. I read the revision. It defines the three-output unit, fixed denominators, required semantic equivalence, allowed variations, malformed/missing treatment, ledger stability separately, and consistency versus correctness. Consistently wrong meaning may be stable but cannot pass intent/joint gates. This resolves the finding without tuning the candidate or scoring outputs. Original concern and disposition are retained here. No outstanding material policy/plan findings remain.

## Plan Review

The interpretation rules are coherent and preserve intent. Shared subject identity is distinct from conditional ancestry. Requested setup can be optional identifying context in either mention order, but must remain prospective and cannot narrow the outcome, erase contrasts or acquire causal force. Explicit independence, different subjects and operation-local exclusions override sharing. Required source circumstances remain mandatory; optional context does not make mandatory attachment optional.

The same-capability allowance is bounded: the how-to remains a real lookup; requested support, behavior and comparison questions survive; unsupported explanations stay in scope; and consumers cannot be told to wait or skip. Genuine source gates and ancestors still bind. Inferred caveats cannot manufacture source ledger entries. POLICY precedence over inherited wording is now explicit and limited to these two issues.

The gate is fair for a prospectively chosen experimental foundation criterion: zero material intent failures, all 144 fresh responses structurally valid, at least 137/144 joint, 44/48 all-three-joint, 22/24 per group, 44/48 meaning stability, and all six diagnostic responses joint. Percentage rounding is correct. Group and repeat thresholds limit concentrated ledger-only defects. The zero-intent gate intentionally makes the aggregate tolerance relevant principally to binding defects; that is coherent. Stable wrongness is explicitly unable to qualify.

Preflight, source/rubric review, freeze, generation and independent full-results review are sensibly ordered. Two independent authors and varied groups improve breadth without establishing statistical independence or a blind held-out evaluation; the protocol acknowledges synthetic policy-informed data and correlated repeats. Diagnostic reinterpretation stays separate and cannot establish pure behavioral improvement. Failure ends this qualification without tuning; passing permits integration consideration only.

The revised protocol specifies seven packet boundaries, three isolated generation contexts per packet, full contract but no rubric in generator input, and whole-packet failure handling with fixed denominators. The planned freeze should identify exact candidate, validator, serializer, reviewed cases/rubric, delivery instructions and scheduled slot bytes/identities. These are execution evidence requirements, not assertions that an unbuilt harness is defective.

## Author-Claim Reconciliation

| Claim | Evidence | Status | Consequence |
| --- | --- | --- | --- |
| Prospective rules resolve ambiguities without permitting intent loss | POLICY.md:3–9; v11 shared-context/support/scope rules | Confirmed as policy | Apply allowances consistently in case rubrics. |
| Gate is explicit and measurable | PROTOCOL.md:9–11 and new operational definitions | Confirmed after clarification | Freeze before generation. |
| Existing candidates/baselines remain unchanged and evaluation sealed | PROTOCOL.md:3; task_plan.md:2 | Planned invariant; execution unverified | Require preservation evidence in final review. |
| No tuning, repair or resampling | PROTOCOL.md:5,13 and operational definitions | Confirmed as protocol | Full-results review must verify execution evidence. |
| Experimental eligibility only | PROTOCOL.md:11–13 | Confirmed | No production, retrieval, answer accuracy or deployed API reliability claims. |

## Verification Performed

Read the named policy, protocol, plan, baseline contract and applicable instructions; re-read the amended operational definitions. Used git status --short, git branch --show-current and git rev-parse HEAD: main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516, extensive pre-existing modified/deleted/untracked files, and POC untracked at repository level. Scope is the named working-tree documents, not the broad repository diff. Inspected directory filenames for the report destination. No tests, generation or semantic evaluation were run. A report-write attempt using unavailable python failed before writing; python3 wrote this report. No implementation correctness or byte preservation verification is claimed.

## Open Questions And Residual Risks

The 48 source/rubric pairs and execution artifacts were not yet available for this review. Their fairness and completeness remain subject to the planned pre-generation review and freeze. Semantic grading remains judgment even with fixed criteria. The later review must distinguish requested meaning, normalized globals, binding completeness, structure and material intent failures. Byte hashes cannot prove unseen execution history. This report does not qualify the candidate based on results.

## Verdict

Ready for the planned source/rubric review, freeze and generation, with the stability clarification incorporated. No outstanding material policy/plan findings. This readiness is limited to the preflight scope; it is not a completed implementation or results verdict.

## Recommended Next Actions

Review all source/rubric pairs for hidden assumptions, freeze complete experimental inputs, generate once per scheduled slot without tuning, and conduct the planned independent full-results review within the total three-instance budget. Preserve this report and historical candidates/results. Do not treat this preflight as approval of completed work.
