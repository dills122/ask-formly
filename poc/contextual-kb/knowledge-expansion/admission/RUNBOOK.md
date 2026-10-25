# Repeatable knowledge admission and qualification

Run from the repository root. Commands operate inside the POC. Preserve existing run directories: outputs are exclusive or are explicitly validated before reuse. Source interpretation is reviewed curation; the scripts make the decisions and execution reproducible rather than automatically deciding what is true.

## 1. Inventory and disposition

Generate a fresh skeleton with `ledger.py inventory`. Reconcile each section and claim into the reviewed ledger; never replace reviewed decisions with the skeleton. For the current candidate:

```sh
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py check \
  --ledger poc/contextual-kb/knowledge-expansion/source-ledger/ledger.json \
  --authored-dir poc/contextual-kb/authored \
  --database poc/contextual-kb/build/knowledge.sqlite
```

The three-guide installed ledger was completed at 70 facts and retains that source scope. The separate validation-v1 ledger covers the validation additions installed at 79 facts. Other future ledgers may remain incomplete. `--require-complete` is a separate closure gate. Seeded-ID coverage is not full record equality. Review exclusions and omitted assertions semantically, not merely by matching IDs.

## 2. Build from authored inputs

After source, cases and criteria review, freeze hashes and run the batch builder in a fresh batch directory:

```sh
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/extensions-v2/candidate.py
```

The command intentionally refuses an existing candidate-build or candidate-inputs directory. In this checkout it has already run; inspect the manifest or reproduce into a separate disposable directory instead of overwriting it. The builder copies canonical plus draft authored JSON, lints exact source/evidence relationships, compiles with the preserved compiler, compares accepted rows across all five knowledge tables, checks actual runtime version/adapter eligibility, and writes a pinned manifest. Do not update hashes to hide unexpected drift.

## 3. Execute fixed real-agent tests

Only after frozen inputs and independent prebuild review:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/extensions-v2/experiment.py agents \
  --cases poc/contextual-kb/knowledge-expansion/extensions-v2/qualification-cases.json \
  --name qualification-1 --repeats 3 --batch-size 5

poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/combined-v2/run.py \
  --name combined-qualification-1
```

These invoke authenticated hosted planning/selection/calling agents and require access to Codex state. They are not source-only CI commands. Existing runs cannot be overwritten. Both use separate runtime directories. This session's repaired runs reuse visible cases from an aborted metadata-defective candidate; they are not fresh unseen evaluation. Keep the old failed runs and fixed missing-result denominators.

## 4. Grade and summarize without changing the cases

After each run, use the versioned one-pass orchestrator. Completed grades are reused only if saved prompts and full case fields match. Any prior incomplete attempt or case drift fails closed; investigate instead of silently regrading.

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py \
  --implementation extensions-v2 \
  --root poc/contextual-kb/knowledge-expansion/extensions-v2/test-output/qualification-1 \
  --cases poc/contextual-kb/knowledge-expansion/extensions-v2/qualification-cases.json \
  --repeats 3 --arms baseline,candidate

poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/admission/assess_run.py \
  --implementation extensions-v2 \
  --root poc/contextual-kb/knowledge-expansion/extensions-v2/test-output/combined-qualification-1 \
  --cases poc/contextual-kb/knowledge-expansion/combined-v2/cases.json \
  --repeats 3 --arms candidate
```

Grading reuses the established assessor and fixed-denominator summarizer. Semantic source equivalence counts; exact fact IDs are only diagnostics. A separate reviewer audits real answers, delivery, citations and preservation. Process exit zero is not sufficient.

## 5. Matched-plan diagnostics and outcome review

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/extensions-v2/replay.py \
  --root poc/contextual-kb/knowledge-expansion/extensions-v2/test-output/qualification-1 \
  --cases poc/contextual-kb/knowledge-expansion/extensions-v2/qualification-cases.json --repeats 3
```

Forty-five requests reuse saved normalized plans against the other DB. This tests retrieval packets, not another45final answers. Verify input/candidate/model hashes, full row preservation and per-call DB/model checks. Retain failures and report all three repeats separately. Do not tune on fixed qualification outputs. Concurrency makes latency descriptive only.

## 6. Explicit promotion

A qualified candidate is not automatically installed. The reviewed `promotion-v3/promote.py` shows the scripted64-fact promotion: exact old/new hashes and review pins, full-source reproduction, recovery snapshots, four authorized file writes, postchecks and caught-error rollback. It is intentionally specific to that reviewed transition and refuses a second apply. A later transition needs its own reviewed spec/command; never repin that historical one.

Install only at an authorized promotion stage. Canonical authored facts and installed DB must reproduce all five tables. Run local maintenance and real-agent smoke tests, then independently review. Preserve models and sealed evaluation. Generated databases, copied inputs and raw run artifacts stay ignored; concise source/decision/test summaries remain reviewable.

The authorized70-fact transition uses [promotion-v4](../promotion-v4/PLAN.md), with its own immutable preconditions. It is now applied; historical promotion commands intentionally refuse a second apply.

The authorized 79-fact transition uses [promotion-v5](../promotion-v5/PLAN.md). Its exact candidate is installed as foundation6; see [results](../promotion-v5/RESULTS.md) for the current installation smoke and review status.
