# Independent compatibility review

Review instance: 1 of 3

## Preliminary ledger (before author explanation)

Scope: only `native_attribute_distillation/`, with read-only surrounding dependencies. Main HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`; this directory is new inside an otherwise broadly dirty working tree. No implementation history was inherited. Root instructions and POC STEERING read.

Inspected tests before implementation: loss identity/zero gradients, wrong and low-confidence teacher masks, masked gradients, empty mask rejection; later offset occurrence identity, duplicate rejection, invalid coordinate rejection. Inspected protocol, loss, panel selection and public scoring transport, plus existing native transport dependency.

Preliminary concerns requiring executed evidence (not yet findings):
- Exact supplied-span/query mapping and temperature scaling must agree with independent native attribute output, including unsupported token coordinates.
- Teacher immutability must cover every parameter, eval/no-grad state, native predictions, optimizer exclusion and detached cache identity.
- Selected eight source rows must remain training-only, with explicit category coverage and teacher-correct role counts rather than favorable-anchor searches.
- KL must reach actual existing student LoRA tensors and alter supervised gradients; zero KL on identical models alone cannot prove that route.
- Fixed bounded perturbation/descent, two seeds and save/reload must be recorded without promoting compatibility to learning efficacy.
- Unit tests alone cannot establish these native runtime invariants. Runtime runner, neutral bootstrap and evidence are still pending.

The protocol freezes three SGD updates per seed, lr 1e-4, no schedule search, save/reload after steps 1 and 3, and limits conclusions to future controlled-training readiness.

## Findings

No actionable findings remain for the bounded compatibility gate. The preliminary source-identity gap was corrected before execution by binding original training files, selector, panel, schema, tokenizer, native implementation and teacher state. An initial dict-only mapping assumption failed before any updates; the author preserved the failure and added list/dict mapping coverage. This report completes the same review instance; no further review instance was started.

## Plan Review

The protocol and implementation agree: existing epoch-6 adapters for seeds 1701/1702, original 194-question/449-negative training prefix, deterministic eight-row panel, no model-dependent anchor search, teacher-correct confidence >0.5 mask, temperature 1, gradient comparison on identical student state, and exactly three preservation-only SGD steps at lr 1e-4. Steps 1 and 3 are saved/reloaded in disposable scope. No full training or evaluation-data accuracy experiment is implemented. Imports remain within this POC or installed third-party packages. The temporary test-only method interception observes native scores and calls the original method unchanged; no library files are modified.

## Author-Claim Reconciliation

| Claim | Evidence | Status / consequence |
| --- | --- | --- |
| Public native scoring remains differentiable | `native_logits.logits`, `check.kl_value`, per-seed gradient receipts | Confirmed: nonzero finite LoRA KL gradients; no detached student path. |
| Exact occurrence/query identity and native parity | `cache_teacher`, cache targets/query IDs, offset tests | Confirmed: public scores compared to captured native attribute scores; role order checked against native schema; unsupported mid-token probes excluded. |
| Training-only source and cache binding | `prepare_panel.py`, `check.main`, `check.identity`, current cache source hash revalidation | Confirmed: source prefix/index identity verified; teacher outputs do not select rows. |
| Teacher wholly frozen and unchanged | `check.main`, full state hashes, repeated cache outputs and optimizer identity exclusion | Confirmed by code and both completed runtime receipts. |
| Wrong teachers cannot teach preservation | `correct_mask`, unit tests, independently recalculated cache masks | Confirmed algorithmically; native panel has zero wrong/low-confidence teacher anchors, so real-error coverage is not demonstrated. |
| λ1 adds KL to λ0 gradients | supervised/combined/KL gradient code and receipts | Confirmed within tolerances on same batch and state. |
| Bounded step and reload compatibility | traces and four reload receipts | Confirmed. Descent is small; seed 1701 is not monotonic at every step. |
| Protected prior artifacts remain unchanged | `protected-after.json`, retention freeze rehash | Author records 37,548 checks unchanged; reviewer independently rehashed all 211 retention files unchanged. |

## Verification Performed

Reviewer executed from this directory:

`PYTHONDONTWRITEBYTECODE=1 ../../env/.venv/bin/python -m unittest -v test_loss test_offsets`

Seven tests passed before the mapping correction; eight passed after it. An initial reviewer command using `../../env/bin/python` failed because that executable does not exist; the corrected `.venv` command is the passing command. Inspected author RED logs for missing loss module, missing offset validator, and subsequent mapping regression, plus the preserved initial native mapping failure. No claim is made that these synthetic tests alone establish native compatibility.

Reviewer ran read-only Python checks which loaded both per-seed receipts/caches, recomputed SHA256 of cache bytes and every `identity.sources` file, recalculated every mask from cached probabilities and gold role identity, and asserted all four step-1/step-3 reload receipts. All passed. Separately SHA256-rehashed every path in `native_attribute_retention/test-output/final-freeze.json`: 211 unchanged.

Author executed the bounded native `check.py` run; reviewer inspected its complete code and retained output/receipts rather than performing additional optimizer updates. Results:

| Seed | Initial KL | Perturbed KL → after 3 steps | KL gradient norm | Max gradient-additivity error | Max native-logit difference |
| --- | --- | --- | --- | --- | --- |
| 1701 | -1.72e-9 | 1.26560e-5 → 1.26325e-5 | 0.00894413 | 6.84e-7 | 5.72e-6 |
| 1702 | -4.32e-9 | 2.37196e-5 → 2.36620e-5 | 0.01401369 | 3.25e-7 | 4.77e-6 |

Small negative initial KL values are floating-point roundoff within the frozen 1e-6 identity tolerance. Each seed retains 60/60 anchors (37 valid-role, 23 no_entity), excludes eight unsupported-coordinate probes, passes teacher immutability, leaves non-LoRA student state unchanged, and passes exact parameter/prediction save/reload identity twice.

## Open Questions And Residual Risks

This is a CPU, eval/dropout-disabled, training-anchor compatibility experiment. It does not establish joint-training stability, useful retention, extraction accuracy, generalization, an appropriate full-training λ or schedule, or model adoption. Only one supervised batch is used for gradient isolation. All selected native teachers happened to be correct, so exclusion behavior is tested with synthetic wrong teachers. The tiny bounded descent is local evidence of gradient flow; the first seed has a small middle-step increase. Existing private schema transport and test-only private native comparison remain pinned implementation dependencies. Protected audit totals count checks and may overlap manifests; they are not unique-file counts.

## Verdict

**Ready** for designing a separately authorized, reviewed controlled-training experiment. The frozen-teacher native compatibility gate passes for both seeds. This verdict does not authorize full training and makes no learning-efficacy or adoption claim.

## Recommended Next Actions

Preserve these receipts and failure logs. If future controlled training is authorized, define its data boundaries, repair-versus-retention objectives, λ/schedule, stopping rules, evaluation gate and review target before running it. Carry forward the native-panel masking limitation and the distinction between local KL descent and improved extraction.

Final documentation audit: read `RESULTS.md` after the runtime receipts completed. Its quantitative claims and limits match the inspected evidence. The author acknowledged no actionable findings and will replace the in-progress review sentence with the final verdict before freezing.
