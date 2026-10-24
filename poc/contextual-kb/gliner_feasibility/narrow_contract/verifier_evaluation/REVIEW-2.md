# Independent review 2 of 3

Verdict: Not ready pending two bounded corrections. Reviewer read all source, verified 13 freeze hashes, and ran 28 passing tests without model execution or evaluation access.

- P2: native infinite logits became finite confidence after sigmoid. Accept: reject all nonfinite native logits before sigmoid; regression covers positive infinity, negative infinity and NaN, plus finite and unsupported control.
- P3: supported-only boundary rejection denominator/rate absent. Accept: report negative_supported and supported_rejection_fraction (null when undefined), retaining total-denominator selection and qualification.

Both reproductions failed before fixes; all 31 tests pass after fixes. Evidence: test-output/review-2-red.txt and review-2-green.txt. No architecture change. Review 3 required for material numerical correction. Full training and real evaluation remain unexecuted.
