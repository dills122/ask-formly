# Assessment correction and diagnostic scope

Recorded during the frozen selector run, before scores are complete. No runtime prompt, policy, input, gold or earlier output changed.

1. Reviewer identified that comparing aggregate covered-group counts can hide a lost group offset by a new group. assessment.py now records individual group identities and makes any loss fail the authoritative retrieval gate. Two tests demonstrate the defect and correction. Frozen experiment.py remains intact, and its original summary will remain as provenance; final-gate.json is an explicitly named correction, not a silent rewrite.

2. The first unchanged-foundation output for freshF01 failed exact-copy validation before retrieval. The ledger excerpt contains "props.disabled to track model.isLocked" while question0 inserts "be configured". The three planned selector repeats stay failed/unavailable, with no replacement plan or retry. Thus the frozen overall all-slot gate cannot pass. Conditional retrieval results are reported separately on valid plans; no claim that the failed overall gate passed.

3. If all conditional retrieval/nonregression checks pass, native_check.py will still exercise the new serving path on three existing diagnostic requests with both retained adapters. This is an explicit limited diagnostic continuation under the user's integration-testing authorization, not promotion qualification or replacement ofF01. Original protocol's promotion gate remains failed; original MCP remains unchanged. The purpose is to complete useful verification of the requested retrieval fix while retaining the unrelated upstream limitation. No further tuning loop is authorized by this addendum.
