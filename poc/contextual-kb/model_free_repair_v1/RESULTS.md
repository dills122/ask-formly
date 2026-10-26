# Structured caller repair: feasibility results

The round trip worked in the controlled external-Codex test. The MCP returned
specific feedback and finished each call; the caller repaired inputs and called
again. No inference occurred inside the MCP. Installed foundation and model_free_v1
remain unchanged; this separate candidate is not promoted.

| Scenario | Observed tool statuses | Lookup calls |
| --- | --- | --- |
| Declared condition missing from second question | needs_refinement → ok | 2 |
| Plan missing | needs_refinement → ok | 2 |
| Plan version conflicts with explicit6.3.12request | needs_refinement → ok | 2 |
| UnsupportedFormly7 | unsupported_scope, stopped | 1 |
| Valid comparison question | ok | 1 |

Each of3repair cases needed1correction, below caller policy's maximum2. All original
request strings were retained. The missing resetOnHide:false condition was restored
to both question roles with its binding preserved. UnsupportedFormly7was not changed
to6.3.12to force a hit. The caller also made1get_formly_facts follow-up for control
behavior and cited the returned control/shared-key qualifications.

caller-2:5scenarios,8lookups+1follow-up,38.85seconds external caller elapsed. Text and
structured feedback match, including isError=true on invalid submitted plans.
Missingplan is a normal result with PLAN_REQUIRED. The server never waits for a
callback. The2repair limit is caller policy, not statelessserver enforcement; observed
compliance does not prove compliance by every harness or under arbitrary errors.

The initialcaller-1pre-corrected injected inputs before sending them. It did not
exercise recovery and is retained as RECOVERY-NOT-EXERCISED, not counted as a pass.
The second run used explicit test-only firstcallinstructions and only public
scenarioinputs, not expectedstatuses, answerchecks or supportIDs. These are controlled
fault-injection tests, not natural error-rate or general answer-quality measurements.

18tests pass, including realstdio under denied network/subprocess/model-import
attempts and empty caches/PATH. Local project maintenance passed. All769baselinepins
and previousmodel-freefiles remain unchanged. Sealed evaluation was not accessed.

A postlive diagnosticpath fix is separately recorded: malformed explicitversion now
points to /formly_version rather than the planfield. RED/GREEN test covers this branch;
currentcode locally reproduces all9savedtoolpackets exactly. Originalfreeze and
live-revision-1 snapshot preserve the live-tested revision; freeze-current pins final
code. No hosted rerun is claimed for the new branch.

Limitations: SDK schema failures use ordinary validation errors; semantic omissions
can still evade checks; Kiro/Claude untested; no autonomous retry enforcement or new
context classifier. Broader fresh/repeated caller qualification remains futurework.
See REVIEW.md for independent verdict and README.md for use of this isolated path.
