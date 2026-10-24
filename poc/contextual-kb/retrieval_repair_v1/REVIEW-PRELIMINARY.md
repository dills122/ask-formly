# Preliminary independent review
Review instance: 1 of 3. Tests and all eight new Python files inspected before author explanation; author rationale not yet read. Review boundary is only retrieval_repair_v1 on dirty main; unrelated changes excluded. Graph coverage reports all eight files not_tracked, so conclusions use complete direct source reads.

The policy preserves baseline slot order, permits at most two distinct outside additions, validates verbatim evidence and question indices, and retains baseline on ordinary selection failures. IntegrityError remains fatal. No source-level issue yet establishes an unsafe runtime promotion. Semantic irrelevance of a removal remains model judgment, requiring strict frozen-label regression evidence.

Concerns to resolve before verdict:
- experiment.score compares required-group counts instead of identities. A previously covered group can be lost while another becomes covered. Independently recompute group identity losses on all records.
- New subprocess adapter lacks direct failure/cleanup tests in the new suite; inspect inherited transport tests and exercise mocked failure paths without provider calls.
- Fresh foundation F01 has a disclosed exact-copy failure. Its three repetitions must remain failures; an all-pass qualification cannot be claimed.
- Final panel, native launcher qualification (only if gates pass), protected hashes and initial/output packet correspondence remain pending.

No author explanation has been used to resolve these concerns. Final verdict intentionally deferred until complete evidence is available.
