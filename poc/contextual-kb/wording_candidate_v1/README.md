# Bounded wording candidate

Accepts one meaning-preserving configuration-question grammar before the unchanged strict condition validator. It converts:

`In Formly, how can props.disabled be configured to track model.isLocked?`

into:

`In Formly, how can I configure props.disabled to track model.isLocked?`

Both ask how to configure the same ordered dependency. The ledger remains the exact source excerpt `props.disabled to track model.isLocked`. The original raw plan and before/after rewrite are retained in `generation.wording_normalization`; the underlying planner also retains its raw event artifacts. The complete canonical plan must pass the original validator.

This is deliberately narrow. It recognizes a complete question with two dotted identifiers and the exact dependency verb `track`, with an existing matching source-grounded condition binding. It does not infer or verify APIs, use approximate token similarity, drop words to force a match, rewrite the ledger, or accept arbitrary paraphrases. Different identifiers, operators, negation, extra clauses and unsupported grammar do not match. Other bound restrictions must still pass their original exact checks. Already-valid plans remain byte-for-byte equivalent as JSON values. The adapter adds no hosted call and no training.

The original validator does not detect all semantic failures (for example a source condition never declared in the ledger); this candidate does not claim otherwise. Its purpose is to support a bounded grammatical equivalent without relaxing those existing checks. It is not a new question decomposition design.

## Opt-in use

From repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/wording_candidate_v1/serve.py
```

The launcher composes the adapter with the unchanged foundation planner, original service, frozen GLiNER advisory extractor and retrieval_repair_v1 backend. Same `--seed 1701` or `--seed 1702`, `--runtime-dir`, `--audit-dir` flags as the prior candidate. Existing default and candidates are untouched. The hosted planner and optional hosted selection still have their prior latency, authentication, logging and timeout characteristics; no global client registration is changed here. See retrieval_repair_v1/README.md for those operational requirements.

## Evidence and limits

Nine new test methods (with multiple negative subcases) and 57 prior tests pass. The prior MCP suite emits an unclosed SQLite ResourceWarning while passing; that existing warning is retained in its log. Development replay accepts all 84 slots: 81 previously valid plans are identical; three repetitions of one saved F01 output are repaired. This is one recovered distinct output, not three independent planner successes. Prior failed qualification scores remain unchanged. This replay measures structural acceptance, not new retrieval relevance or final-answer accuracy.

The local integration replay uses the saved raw F01 response, real frozen GLiNER models and actual retrieval, with a no-op selector test double. It does not regenerate the planner, invoke the hosted selector, or represent a new real calling-agent qualification. A hosted test was rejected by automatic approval review because of external payload transfer; no transfer was retried. See test-output/native for the local result, and REVIEW.md for independent review.

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/wording_candidate_v1 -p 'test_*.py'
```

All implementation and evidence are inside this POC. Existing candidates, models, data/DB remain unchanged; sealed evaluation is hash-checked only. No dependency installation, training, commits or publication.
