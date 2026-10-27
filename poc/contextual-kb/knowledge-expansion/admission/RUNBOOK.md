# Repeatable knowledge admission

Run from the repository root unless stated otherwise. This process is self-contained in the POC. The current foundation is192 facts/36 documents, exact Formly6.3.12 core/Material. Both runtime implementations, models and the installed DB remain locked during preparation. Evaluation stays sealed.

## 1. Inventory and source decisions

Verify sources at the pinned upstream revision, check existing facts for equivalent support, and record each target as admitted, existing support, excluded with rationale, or explicitly deferred. Retain source paths/bytes used by authored quotations. The three-guide ledger utility is useful within its original manifest scope; it does not automatically cover every later source.

```sh
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py check \
  --ledger poc/contextual-kb/knowledge-expansion/source-ledger/ledger.json \
  --authored-dir poc/contextual-kb/authored \
  --database poc/contextual-kb/build/knowledge.sqlite --require-complete
```

The DB check is read-only seeded-ID coverage, not full record equality or semantic approval. Later batch ledgers preserve their own source formats and scopes. Use the [completion backlog](../../../../docs/knowledge-completion-backlog.md) to reconcile them.

## 2. Freeze the candidate and test contract

Before building, review the draft facts, source mappings, exact version/adapter applicability, fresh development requests, grading criteria, recovery budget and preservation controls. Record immutable hashes and independent review. Do not tune on the sealed evaluation or redefine a failed gate after seeing results.

The active schema2 compiler is `kbcompiler/current_source.py` with `versioned_knowledge_v1/compiler.py`. It checks provenance, applicability and evidence links. Build to a new isolated candidate path with the documented compiler CLI; never invoke a historical schema1 batch builder against the current installed foundation. See [pipeline commands and boundaries](../../../../docs/knowledge-pipeline.md).

## 3. Compare through the MCP

Use the same frozen requests, scope and budgets for baseline/candidate. Keep the installed runtime/model/DB pins unchanged. The default model-free caller supplies plans, inspects evidence and uses bounded discovery/fetch recovery. Record full requests, plans, packets, citations and errors under ignored test-output. Run three repeats and report separately whether these were independent caller generations or deterministic fixed-plan replays.

Credit supporting evidence already present in the baseline. Distinguish missing knowledge, retrieval loss and caller omissions. Keep failed deliveries in denominators and require correct scope controls and no critical unsupported claims. Model-backed qualification is separate; never pool its score with model-free results.

The retained `assess_run.py` is a tested adapter for compatible historical batch assessors, not an automatic grader for arbitrary new experiments. New scoring/wiring requires TDD and review. Freeze assessment/call hashes before report generation; independently review actual answers and supporting evidence, not just process exit codes.

## 4. Explicit promotion and closeout

A passing candidate does not authorize installation. A separately reviewed transition must verify the installed/candidate hashes, reviewed inputs, preserved canonical rows, exact source reproduction and runtime manifests; snapshot targets before writes and verify afterward. The retained `promotion-v7/promote.py` supplies the tested guarded-replacement helper used by versioned promotion. Its old executable transition must not be reapplied. Historical multi-file rollback handles caught errors/interrupts; it is not crash-atomic.

After an authorized promotion, run `python3 tools/project.py check`, real-agent installed smoke, independent review and both restarted MCP connection checks. Keep original failed results visible. Commit/publish only when requested.

Close each batch by preserving required provenance and source dispositions, retaining a concise result/history entry, and retiring duplicate handoffs and one-off runners after dependencies are checked. Historical detailed implementations are available at [checkpoint5dc8a89](https://github.com/dills122/ask-formly/tree/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion); restore into a separate checkout if needed. Raw runs and local recovery archives stay ignored.
