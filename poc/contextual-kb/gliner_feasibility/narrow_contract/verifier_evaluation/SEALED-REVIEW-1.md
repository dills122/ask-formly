# Sealed fresh review 1

Review instance: 1 of 3. Verdict: **Not ready**.

Dataset SHA256: `496bf6eb2f4a940ceded8429b61fb64e6450ce93ba70a003cfc05445cf2d2287`.

## Findings

- P2: incomplete explicit-property inventories in `sealed-boundary-02`, `sealed-boundary-05`, `sealed-unfamiliar-03`.
- P2: negative-family coverage mismatch in `sealed-unfamiliar-01`.

Detailed evidence remains in `sealed/review-1-details.md`; preliminary concerns were recorded before reading author rationale in `sealed/review-1-preliminary.json`.

## Plan review

40 questions; four groups of 10; 151 gold occurrences; 203 probes; 52 negatives; four no-mention questions. Six role counts: 12, 13, 20, 58, 17, 31. Mechanical counts pass, subject to the semantic findings. All questions/gold/probes were independently read.

## Author-claim reconciliation

Mechanical counts and transport reproduced. Exhaustive inventory and one family classification are disputed. No normalized duplicates against 242 training and 30 calibration rows. The disclosed near-template flag was inspected and accepted as thematic overlap; this does not prove generalization.

## Verification performed

Existing POC Python -B: validate_fresh passed; qualify_sealed passed with exactly four deliberate unsupported probes and no encoder forward. Gold intervals are nonoverlapping. No predictions, optimization, training or old held-out access. Native checks emitted existing library compatibility/deprecation warnings and completed successfully.

Frozen evaluation implementation manifest SHA256 unchanged: `e295b98fd2f0fb759085aa7336fa12327efcf877491b0228fcae6282af85f332`.

## Open questions and residual risks

Adversarial construction limits ordinary-traffic representativeness. Model performance and actual operational conflict coverage remain unmeasured. No heavy pivot is needed.

## Verdict

Not ready. No ready receipt created; dataset and implementation left unchanged.

## Recommended next actions

Send ID-based findings to the sealed author, resolve annotations, and use the next independent review instance after correction. Keep detailed evidence inaccessible to training and threshold tuning.
