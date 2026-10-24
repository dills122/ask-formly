# Independent preflight review

Review instance: 1 of 3.

## Findings

**P1 — Fix whole-packet accounting and first-save guarding before generation.** PROTOCOL.md:7 requires missing, malformed or identity-mismatched packets to fail every scheduled slot without salvage, and lines 7/15 require first literal retention and frozen hashes. runner.py:8-17 intentionally only parses and serializes a list; an empty/short list or duplicate/wrong IDs succeeds. The available v3_stress/assess.py:summarize scores individual records and therefore retains valid siblings of missing slots; its test_missing_counts_as_failure explicitly confirms that behavior. No qualification_v2 post-save accounting guard or tested first-save receipt procedure exists in this reviewed scope. As a result, applying the available scorer directly could credit part of a failed packet, contrary to the fixed protocol, and the runner alone cannot establish that input bytes equal the first saved bytes.

Smallest correction: freeze a separate parent-side post-save accounting guard before generation, with tests for missing/empty/malformed/short/duplicate/wrong-identity packets and changed saved inputs. It must preserve literal/raw/failure evidence, mark all scheduled packet slots failed when appropriate, and capture/check first-save receipts without repairing output. Keep semantic checks out of transport. Parent confirmed this gap and will address it before freeze; no fix was made in this pass.

## Plan Review

The overall plan is bounded and appropriate: fresh source/rubric review, implementation preflight, immutable input freeze, 21 isolated first generations, complete independent semantic/stability review, then fixed gate. The protocol separates semantic, binding, structural and material-intent outcomes, includes denominators for missing slots, distinguishes stable wrongness, and prevents tuning after a failed gate. The missing operational guard is a localized implementation prerequisite, not a heavy architectural pivot.

Fresh source/rubric correctness is expressly outside this verdict and remains the parent's separate prerequisite. No generated output or qualification result exists in this pass. The 48 fresh cases and five diagnostics cannot establish held-out or production behavior.

## Author-Claim Reconciliation

| Author claim | Evidence | Status and consequence |
| --- | --- | --- |
| Standalone literal-to-JSON CLI works from unrelated CWD | runner.py and actual subprocess tests | Confirmed; no POC imports, generated execution or semantic repair in runner |
| Exclusive output and failed parse/encode leave original intact | runner tests, encode-before-open source | Confirmed for tested boundaries; interrupted/failed writes can leave partial destination as acknowledged |
| Contract is previous contract plus missing ledger audit | Exact byte concatenation check | Confirmed; initial probe incorrectly assumed an extra newline, corrected by exact comparison in preflight-scope.json |
| Frozen same-POC validator/projection reused | candidate.py and refinement_v3/candidate.py | Confirmed; unchanged validator does not detect undeclared omissions |
| Tests show semantic improvement | Author explicitly disclaims this | No such claim accepted; generation and independent review remain necessary |
| All malformed packets fail all slots and first saves stay frozen | Protocol and available scorer | Not yet implemented as a reviewed tested guard; finding above |
| Prior protected state preserved | preserve.snapshot equals protected-before | Confirmed for all 41 manifest entries at review time |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v2 -p 'test_*.py' -v`: 14 pass.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/qualification_v1 -p 'test_*.py' -v`: 8 pass.
- `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/v3_stress -p 'test_assess.py' -v`: 8 pass.
- Byte-only protected snapshot: equality across 41 entries. Sealed semantic contents were not inspected.
- Exact contract concatenation: qualification_v1/CONTRACT.md + LEDGER-ADDITION.md equals qualification_v2/CONTRACT.md.
- Prior TDD logs inspected: happy paths genuinely failed without runner; negative tests passing without runner were not mistaken for meaningful red-phase verification.

Logs and reviewed hashes are under test-output/preflight-*. Review base is dirty `main`, HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; qualification_v2 is untracked within the wider untracked poc tree. Unrelated dirty repository changes were excluded. The preliminary ledger was saved before AUTHOR-EXPLANATION.md was read. Applicable code graph coverage is not_tracked; direct source was used for reviewed Python files.

## Open Questions And Residual Risks

The ledger addition is clear about timing, supplied method/channel and explicit no-substitution restrictions, retains local/shared scope and source grounding, and does not require invented conditions for mere targets. Whether models follow those instructions is unverified. Tests prove transport and existing structural behavior only.

The runner is intentionally small, standard-library-only and suitable for bounded local batches. It does not enforce native-agent behavior before the first recorded save or provide a hostile-input resource sandbox. Hashes establish recorded bytes, not unseen generation chronology. No generation, sealed evaluation, application behavior, final-answer quality or production claim was reviewed.

## Verdict

**Not ready** for generation: the whole-packet and first-save guard must be fixed and reviewed before freeze. No other material defect found in the runner, contract addition or scoped plan. This verdict does not judge fresh question semantics.

## Recommended Next Actions

Parent adds the bounded guard and regression tests without modifying existing candidates or saved evidence. Review instance 2 should assess that material fix before generation; reserve instance 3 for full results. Complete the separate source/rubric review and input freeze. Do not generate or use a later review to replace unfavorable qualification results.
