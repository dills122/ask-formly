# Question plan design review

Date: 21 October 2026. Scope: [contract](QUESTION-PLAN-CONTRACT.md) and
[evaluation protocol](QUESTION-PLAN-EVALUATION.md) only. No implementation,
dependencies, executable schema, fixtures, or tests were created in this stage.

Repository baseline: branch `main`, HEAD
`c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. The repository already had extensive
working-tree changes and the POC was untracked. Review targets are explicitly
bounded documents, not the entire working-tree diff. No staging or commits.

## Review instance 1 of 3

A fresh-context, read-only reviewer used the independent-review skill, read
canonical guidance and the design before receiving author rationale, checked
the working-tree scope and inspected LlamaIndex's native output type. Verdict:
**Not ready** until three bounded corrections. No heavy pivot requested.

Reviewed SHA-256 values before revision:

- Contract: `6b6c6dddad6764d5032ad0eb07a3f15e38fa8158cbe95906653f1bfd1a736d45`
- Evaluation: `2bb8d29ffca4e32245de98357749eda7355c1bfc123f0e1327d1f2eeced7ec92`

| Finding | Author disposition | Correction |
| --- | --- | --- |
| P1: Native SubQuestion has no route to required ambiguity metadata. | Accept. | Specify SEARCH/AMBIGUITY prefix transport in native sub_question text, deterministic decoding, one tool name, rejection cases, and a real-library development feasibility gate. No second semantic pass. |
| P1: One whole-question echo could pass multi-ask completeness. | Accept. | Gold rubric marks independently searchable outcomes and permissible combinations; distinct focused requests required for separable asks. Explicitly reject whole-question echo on those cases. |
| P2: Changed repeats graded only for critical errors cannot establish completeness stability. | Accept. | Grade every distinct normalized output using the full rubric. Define stability as cases whose five outputs all pass completeness. |

The author explained the intent to preserve optional attribution spans, keep
the shared adapter nonsemantic, and separate quality from unapproved latency
targets. The reviewer confirmed those intentions matched the design but did
not waive the findings. No tests or DB operations were run by the reviewer.

## Review instance 2 of 3

A second fresh-context, read-only reviewer verified all three corrections and
returned **Ready** for the next implementation stage as a reviewed design,
with no actionable findings. This is not runtime qualification. Preliminary
assessment preceded author disposition; no additional rationale was needed.

Reviewed corrected SHA-256 values:

- Contract: `82a613b9bb537bafa7a8180ff49c7c652d50a928662873952dc2e19da9edda42`
- Evaluation: `3a85bb5d02ac1d91e2ea40e3010a3b1e539361e110203c6ff71c4db7cc9b4188`

The reviewer confirmed the locked boundary, separation of structural and
semantic grading, held-out isolation, failure retention, and repeat scoring.
Author disposition: accept the verdict and retain the development compatibility
gate and implementation review checkpoint before held-out execution.

Implementation remains unstarted. Runtime compatibility, semantic quality,
and product latency suitability remain unmeasured. Two of the maximum three
fresh review instances have been used in this review flow; one remains for
the implementation checkpoint. Further independent grading/results review
needs an explicitly agreed review budget if it would exceed that bound.

## Verification of this stage

Local Markdown link targets in both design documents were checked and existed.
No automated behavioral checks are claimed for a documentation-only stage.
No data/DB, retrieval, or existing implementation files were edited.

## Implementation review instance 3 of 3

The independent report is retained at repository
`test-output/question-ab-20261021/implementation-review.md`. Verdict: **Not ready**.
All 20 original freeze entries matched and 31 new-suite tests passed. No held-out
cases were opened by the reviewer or implementer.

| Finding | Author disposition | Implemented correction, pending independent revalidation |
| --- | --- | --- |
| P1: Supervisor timeout aborted remaining samples. | Accept. | Retain the failed sample; replace the stopped worker before its next scheduled sample, with development-only warmup and explicit recovery overhead. No retry of failed case/pass. Synthetic test reproduces old abort and passes after correction. |
| P2: Hardware/server provenance incomplete. | Accept. | Capture and freeze CPU/model/memory/core information, explicitly unavailable server settings, and record runtime Ollama device/model state. Verify hardware before reading sealed cases. |

The corrected suite passes 33 tests. These are author checks, not a new review
verdict. Current implementation freeze has been refreshed; the reviewed freeze
is retained separately. The review count is exhausted. No fourth independent
review, Ready receipt, held-out opening, or comparison has occurred.
