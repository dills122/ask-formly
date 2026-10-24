# Independent review

Review instance: 1 of 3.

## Scope and independence

Reviewer initialized without the implementation conversation. Scope is the new
`native_attribute_retention/` experiment and its separately retained raw evidence.
Repository is `/Users/dsteele/repos/ask-formly`, branch `main`, HEAD
`c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. The repository has substantial pre-existing
tracked changes and untracked content; this is an explicit working-tree review,
not a claim that the entire dirty tree belongs to this experiment.

Read root guidance, README, development guidance, POC AGENTS and STEERING. Locked
data/DB, original extractors, prior evidence, and non-question layers remain
outside edit scope. Reviewer owns only this report and does not implement fixes.

## Blind semantic ledger

Completed before inspecting protocol, implementation, earlier model results, or
author explanation. Read all 40 questions and 112 gold occurrences, all 48
semantic negatives, and four transport probes against CONTRACT.md. No semantic
annotation defect found: full code paths remain maximal; opaque expressions
remain single values; quote delimiters and repeated occurrences are preserved;
hypothetical API names count as mentions without claims of existence. The four
empty questions contain generic nouns rather than explicit identifiers.

All 164 probe slices and 112 mention slices equal the exact supplied question
substring. The semantic negative families each contain 12 cases: clipped paths,
merged API/value spans, quote-or-nested fragments, and prose. The four
mid-identifier probes are correctly separate transport cases and must not improve
the semantic denominator. There are standalone valid controls for lexical strings
that are invalid as nested path fragments elsewhere.

Residual limitation: the first 12 questions use a repeated interaction template,
so these are controlled boundary diagnostics, not 12 independent natural language
styles. Fresh scores support this bounded distribution only. Native candidate
representability remains pending tokenizer checks; semantic validity alone does
not establish that a model could emit a candidate.

Blind ledger file hashes (SHA-256):
- `fresh.json`: `78e87e296a3b40e88df8eb6e499313b7a5efd2ad47976070b49e6c797efb4b7c`
- `families.json`: `eb3d402906b22bfb6af9df06d3ee001e00ae552d4a8165686bb5e16c8938275f`
- `probe_candidates.json`: `e221569e978093caa7db42580c310d5373a080947cc43490e07aa78ff2114ff4`

## Readiness checkpoint

Pending blind semantic review, neutral bootstrap, tests, and implementation.
Actual training is not yet reviewed as ready.

## Final evidence audit

Pending four-arm execution and retained raw evidence. No readiness or adoption
claim is made by this initial ledger.

## Preliminary implementation ledger (before author explanation)

Inspected PROTOCOL.md, all 12 tests and the new schedule, runner, scoring,
comparison and compatibility modules; followed direct imports into the existing
native transport, training loader and identical-span resolver. No earlier model
results were read for this pass. Executed the 12-test suite with the existing POC
Python environment: PASS.

The proposed contrast matches starting parameters, optimizer initialization,
124 updates, 992 example forwards/backwards and seven shared replay slots. The
replacement eighth slot is explicitly weighted 0.25 rather than renormalized.
It is therefore a bundled substitution/weight/total-loss intervention, not an
isolated proof that weighting alone is beneficial. Code and protocol say this.
Parameter changes are restricted to existing LoRA tensors; fixed save/reload
panels contain original training rows only and RNG state is restored.

Operational resolution consumes only original extractor coordinates. Supplied
span probes remain separate. Preservation gates inspect correct original and
starting-candidate mentions, starting exact cases, original per-role metrics,
nonconflicting mentions, and both historical probe sets. Low confidence does
not count as learned rejection; restoring unresolved invalid output does not
count as a repair. Superiority requires fresh gain in both seeds and no old or
fresh correct-outcome loss.

Pretraining items to close: training-freeze.json was not yet present when
inspected; freeze reviewed implementation, schedules and inputs before exposure.
The metric function currently stores per-family counts and aggregate totals,
but the final report must explicitly calculate representable-semantic metrics
rather than silently treating unsupported transport probes as semantic negatives.
This is a reporting requirement, not a reason to alter the frozen total gate.
The family counts contain enough information to calculate it without rerunning
models. Native tokenizer alignment confirmation from the fresh author reports
all 112 gold and 48 semantic negatives supported, four transport probes unsupported.

Final readiness awaits author reconciliation and the pre-exposure freeze.

## Author-claim reconciliation and pretraining verdict

Read IMPLEMENTATION-EXPLANATION.md only after the preceding preliminary ledger.
Claims of matched initialization and schedule budgets, tested gradient scaling,
existing native transport and conservative resolver reuse are confirmed in code.
Claims of eventual save parity, frozen parameters, no drift and protected hashes
remain prospective and require execution receipts; they are not treated as passes.
The author explicitly limits the contrast to the bundled intervention and notes
that differing sequences can consume different dropout randomness. This matches
the experiment and avoids claiming identical token-level noise.

The reporting follow-up is resolved before freeze: probe_metrics now separately
counts representable semantic negatives and their rejection recall, retaining the
unchanged total rejection gate. Inspected protect.py: it reads prior protected
manifests plus the 138-file contrast freeze, hashes bytes, and writes only a new
receipt. No heavy pivot or new review instance is needed for these reporting changes.

**Readiness checkpoint: Ready for the fixed experiment**, conditional on writing
and successfully verifying training-freeze.json before fresh exposure, and passing
the existing fail-closed baseline/start drift checks before optimization. This is
not a readiness or adoption verdict for any trained model. Preserve all four arms
and return to this same reviewer for the final evidence audit. No unresolved
pretraining blocker was found.

## Interim execution audit

Resumed the same review instance after execution began. Independently hashed all
19 training-freeze entries and all 810 run-freeze entries: zero mismatches.
For each seed independently compared retained prior artifacts against this run:
336 original outputs, 336 starting-candidate outputs (including supplied scores),
and 306 prior probe records match exactly. This establishes the requested replay
before interpreting continuation outcomes.

Seed 1701 control completed 124 updates / 992 logged examples, all weight 1.0.
Both update-31 and update-124 parity receipts pass. Independently compared its
parameter-before hashes with receipt final hashes: exactly 202 LoRA tensors
changed, zero base tensors changed. Recorded training time is 484.746 seconds;
this is not an end-to-end latency result. Remaining arms and final comparisons
are pending; this interim audit makes no model adoption claim.

### Seed 1701 paired audit

Independently matched every logged example ID, step and coefficient against each
frozen schedule: 992 per arm, 124 steps; summed loss coefficients 124 control and
112.375 treatment. Starting parameter hashes are identical. Both arms changed
202 LoRA tensors and no base tensors. Compared actual before/after saved probe
arrays at both checkpoints: exact equality, independently of parity booleans.

Fresh supplied-span correctness: both retain 112/112 valid roles. Control rejects
34 malformed probes; treatment rejects 35. Paired inspection finds two gains and
one loss, rather than a monotonic gain: the nested `options.formState.seed`
fragment changes from correct no_entity to incorrect value. Against starting
candidate, fresh treatment has four gains and two losses.

On the first historical probe set, treatment versus control has three gains and
four losses; on the contrast historical set, five gains and one loss. Treatment
loses four starting-candidate correct outcomes on each historical set. Thus the
predeclared preservation and superiority conditions already fail for treatment
on seed 1701; later seed gains cannot offset these losses.

Independently reconstructed operational mention sets from raw artifacts. Both
arms preserve every original/starting correct mention and make the same two
correct original-extractor resolutions (`va-f03-q04`, `roles-04`), zero wrong
resolutions, and zero output changes relative to the starting candidate. These
are retained repairs, not new operational benefit from continuation. This remains
an interim result; no final four-arm verdict is issued here.

## Final evidence audit

All four runs completed 124 updates and 992 examples. Independently checked all
logged IDs/steps/weights against frozen schedules; coefficients total 124 control
and 112.375 treatment for each seed. Same-seed starts match. Each run changes
exactly 202 LoRA tensors and no base tensors. All eight actual saved before/after
prediction arrays match, as do parity receipt parameter checks. No additional
candidate, epoch selection or fresh-dependent change was observed.

Recomputed all four arms' operational score objects from their raw outputs using
the unchanged scorer and obtained exact equality with scores.json. Separately
recounted correct supplied-span roles/rejections directly from raw predictions
(confidence strictly above 0.5), and reproduced all paired probe gain/loss counts.

| Seed | Fresh treatment vs control gain/loss | Native old gain/loss | Contrast old gain/loss |
| --- | --- | --- | --- |
| 1701 | 2 / 1 | 3 / 4 | 5 / 1 |
| 1702 | 0 / 0 | 0 / 3 | 2 / 3 |

Fresh valid roles are 112/112 in every arm. Fresh malformed rejection is control
34/52 and treatment 35/52 for seed 1701, and 38/52 in both arms for seed 1702.
Representable semantic denominators are 48, giving 34/48, 35/48, 38/48, 38/48.
Unsupported transport probes are kept separate, not counted as learned rejection.
These fresh improvements cannot offset old correct-outcome losses. All four arms
lose previously correct old probes. Both arms therefore fail improvement gates;
both fail full qualification, and treatment superiority is false.

Seed 1702 has zero correct operational repairs and two wrong resolutions in each
arm. Direct inspection confirms `srf-026` resolves merged API/value boundaries to
an incorrect single role, while `va-f03-q04` selects value for a registration name
and loses an original correct mention. These are structurally valid wrong outputs,
not safe abstentions. Seed 1701's two correct repairs are unchanged from its
starting candidate. The experiment demonstrates no new operational improvement.

Independently rehashed every entry named by the protected receipt: 37,337 checks,
zero mismatches. This includes prior contrast evidence and inherited protected
artifacts; the number is manifest-entry checks and may include repeated files.

## Findings

No actionable implementation or reporting defect remains within this experiment.
The measured preservation, rejection and operational failures are explicit negative
experimental results and block model adoption; they are not hidden by the report.

## Plan Review

The fixed four-arm plan was followed, with matched example/update budgets and
same-seed starts, a separately defined bundled treatment, no evaluation-based
selection, old-data retention audits and fresh evaluation only after freeze. No
architecture replacement, scope expansion or heavy pivot occurred in this review.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| Same starts and fixed budgets | Schedules, all 3,968 logged examples, before hashes | Confirmed | Contrast is interpretable within stated bundled intervention |
| Frozen base, LoRA updates only | Four before/final parameter maps | Confirmed | No new head or base-weight update |
| Eight save/reload checks pass | Actual prediction arrays and receipts | Confirmed | Saved candidates preserve checked outputs |
| Old replay unchanged before training | Both seeds' 336 original + 336 starting outputs and 306 probes | Confirmed | Starting comparison is reproducible |
| Fresh supplied accuracy differs from operational exactness | Raw probes and recomputed scores | Confirmed | 112/112 is not extraction success; exactness remains 34/40 and 35/40 |
| All improvement/qualification/superiority decisions fail | Raw outcomes, paired changes, decision.json | Confirmed | No candidate qualifies for adoption |
| Historical valid misses are rejections in these endpoints | All eight historical valid-span subsets | Confirmed | Zero accepted wrong roles and zero abstentions among current final valid subsets; rejected = 106 minus correct |
| Wrong resolutions and confidences reported accurately | Seed 1702 srf-026 and va-f03-q04 raw logs | Confirmed | Unsafe valid envelopes remain visible |
| Protected evidence unchanged | Independent 37,337 manifest-entry hashes and final 810 run-freeze checks | Confirmed | No protected mutation found |

Read final RESULTS.md and reconciled its tables, exactness, confidence examples,
historical low-confidence Material abstention, and decision claims against raw
artifacts. The report correctly treats the old contrast run as diagnostic and
refrains from claiming that weighting alone caused the observed changes.

## Verification Performed

Executed the 12-test unittest discovery command with the existing POC Python;
all passed. Independent read-only Python audits checked exact slices, schedules,
loss coefficients, starts/parameter changes, raw parity arrays, historical output
and probe equality, raw scoring reproduction, correctness gain/loss counts, and
protected/frozen byte hashes. No model rerun, training, annotation edit, fix,
staging, commit or publication was performed by this reviewer. Actual commands
and outputs are retained in the review conversation; checked artifact paths are
listed in the preceding ledger and claim table.

## Open Questions And Residual Risks

Two seeds, a synthetic 40-question packet and repeated boundary templates do not
establish generalization. Supplied offsets are an audit interface rather than
end-to-end extraction. The fixed intervention combines substitution, weighting
and total-loss changes, so causal attribution to any single ingredient remains
unresolved. Native private scoring is version-pinned. Final-answer accuracy and
production integration were not evaluated. No additional training is authorized
by this review.

## Verdict

**Ready** as a completed, credible negative experiment and evidence report.
**Not ready for model adoption:** both arms fail preservation/improvement and
full qualification; treatment does not beat continued replay under its frozen
superiority rule. Review instance 1 of 3 is complete. No new reviewer instance
or implementation loop was started.

## Recommended Next Actions

Retain all four candidates and raw evidence, keep original extractors and agent
layers unchanged, and communicate the negative decision. Any further experiment
needs a new explicit hypothesis and fresh held-out evidence; do not tune this
now-exposed packet. No outstanding corrective action blocks closing this run.
