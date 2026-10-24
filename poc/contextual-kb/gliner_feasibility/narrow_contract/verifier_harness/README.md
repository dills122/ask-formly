# Verifier training harness

Implements the training portion of ../verifier_training_plan/PROTOCOL.md, with frozen
input validation, native alignment preflight, two independent fresh LoRA adapters,
216-row cyclic schedules/26 coverage-only rows, question-mean BCE,124updates×8,
AdamW1e-4/wd.01,clip1 and full-state first/final save verification with RNG restoration.
No retrieval, MCP, answer assembly, or baseline changes.

Run using ../env relative to gliner_feasibility, or repository root:

```
poc/contextual-kb/gliner_feasibility/env/.venv/bin/python -B poc/contextual-kb/gliner_feasibility/narrow_contract/verifier_harness/run.py --name preflight-001
```

Default preflight has no encoder forward or optimizer. `--mode smoke` executes one
update per seed using the actual training schedule and saves disposable adapters.
`--mode full` is the later explicit124-update experiment, not executed during harness
implementation. All modes require new output names, refuse reuse, and write only here.
No resume/checkpoint selection supported. Failures retain logs and after-check evidence.

This is a training harness, not full evaluation/qualification orchestration. Threshold
calibration, operational resolution, fresh-case generation/sealing, regression replay,
and latency measurement remain governed by the frozen plan and must be implemented
and reviewed before claiming the whole experiment ready for full training. No test
here reads sealed evaluation content. No accuracy claims from smoke losses.
