# v6 results: targeted fixes pass, fresh completeness remains short

V6 adds an internal requested-aspect and condition-attachment audit to the frozen v5 prompt. It distinguishes requested support checks from conditional usage, carries nested gates and shared dependencies, reconciles exclusions and preserves uncertain scope metadata. The same three-field JSON and frozen v3 validation/advisory transport remain in place. No existing candidate, baseline, extractor, data/DB, retrieval or answer component changed.

## Executed test

24 independently authored fresh requests in3 batches of8, each repeated3times:72 fresh responses. Separate five previously failed v5 requests repeated3times:15 diagnostic responses. All87 first submissions retained, no repairs or retries. Candidate/input/raw hashes frozen at their respective pre-generation/pre-review checkpoints. No tuning after generation.

| Measure | Fresh requests | Known diagnostics |
| --- | ---: | ---: |
| Structural validity | 72/72 | 15/15 |
| Useful question text | 70/72 | 15/15 |
| Meaning plus global scope | 70/72 | 15/15 |
| Complete, correctly attached bindings | 60/72 | 15/15 |
| Full contract pass | 60/72 | 15/15 |
| Full pass by repeat | 19/24,21/24,20/24 | 5/5,5/5,5/5 |
| Requests passing all3 repeats | 18/24 | 5/5 |
| Question-meaning stability | 23/24 | 5/5 |
| Ledger-meaning stability | 20/24 | 5/5 |
| Exact canonical JSON equality | 3/24 | 0/5 |

The targeted diagnostic gate passes. The full fresh gate fails: required24/24 requests across all3 repeats, observed18/24. This is progress on exposed failure cases, not proof of a general improvement over v5: fresh panels differ and no contemporary comparator was run.

## Remaining failures

- N01 run1: true-setting meaning appears in the configuration question, but its binding omits that question.
- N02 all3: later-change observation survives in text but its scenario is missing from the ledger.
- N11 runs2–3: invalid-state transition survives in text but lacks a binding.
- N18 runs1/3: usage-only `without polling` restriction leaks onto the support check, narrowing its meaning.
- N09 all3 and N14 run1: fail frozen ledger criteria at genuine interpretation boundaries. Current-model-from-callback may be a requested target rather than a separate condition; prospective use after registration may suffice without repeating the prior unregistered state. Text remains useful. These4 failures are retained, not silently waived.

Even accepting those4 ambiguous slots would yield64/72 full responses and20/24 requests passing all repeats. The fresh gate would still fail. Official score remains60/72. Detailed per-response notes and stability decisions are retained in test-output/semantic-review.json and stability-review.json.

## Independent review and decision

[Independent review1](REVIEW-1.md): evidence ready; candidate Not ready for acceptance. No actionable selector/transport defect. Six v6 tests, seven frozen v5 tests and eight aggregation tests pass. The initial TDD failure was the absent candidate module; passing unit tests prove selection and transport compatibility, not semantic fixes. Actual native generation/review provides semantic evidence. All87 output projections remain unchanged under optional missing, malformed, valid and conflicting role hints.

Keep v6 as an experimental candidate with a passing diagnostic replay, not a replacement promoted as fully reliable. Further work should first clarify which requested events and prerequisites must also appear in the ledger. Clear missing bindings and local-condition leakage remain real defects even after that clarification. Another prompt expansion alone should not be assumed sufficient. No further candidate or experiment was started here.

## Preservation and limits

All34 inherited preservation manifests (38,385 hash entries, including overlaps) verified before/after. Evaluation remains sealed: protected payloads were byte-hashed only. All code and evidence writes stay inside refinement_v6 in the POC. No staging, commits or publication.

The full prompt grows from13,491 to17,485 UTF-8 bytes (+3,994). No latency or cost measurement. Native model revision/temperature/seed uncontrolled, contexts isolated but repeats correlated. Synthetic development evidence does not establish production accuracy, retrieval utility or final-answer accuracy. Separate-context review is not vendor independence; file hashes cannot prove unseen generation history.

## Evidence map

- Candidate: CONTRACT.md, AUDIT.md, candidate.py, test_candidate.py.
- Design: PROTOCOL.md, data-review.md, AUTHOR.md; original author rubric retained before two documented pre-generation corrections.
- Inputs: data/fresh-cases.json and fresh-rubric.json; diagnostic-cases.json and diagnostic-rubric.json; four full prompt/request packets.
- Outputs: test-output/b1-r1-raw.json through b4-r3-raw.json (12files), records.json and aggregate.json; full denominators retained.
- Reviews: REVIEW-1-preliminary.md, REVIEW-1.md, REVIEW-RESPONSE.md.
- Integrity: candidate-freeze.json, input-freeze.json, raw-freeze.json, protected-before.json, protected-after.json and final-freeze.json in test-output.
