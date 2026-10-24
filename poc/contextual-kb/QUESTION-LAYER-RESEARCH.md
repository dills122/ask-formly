# Question layer research for the contextual knowledge POC

**Status: design investigation, 21 October 2026.** This document records the
pre-pilot design and research. An isolated diagnostic harness has since tested
three arms; see the [one-pass pilot results](QUESTION-PILOT-RESULTS.md). No
serving MCP answer path was implemented. The
[data and DB foundation](DATA-FOUNDATION-STATUS.md) stays workable while we
decide how a free-form question should reach its answer-bearing facts.

## The problem in this POC

The database has 46 source-linked Formly facts and a contextual FTS5 row for
each. The [direct-query trial](DB-QUERY-TRIAL.md) supplied two search expressions
*by hand* for each of ten developer questions. It reached all required fact IDs
for 6/10 questions directly and 7/10 after one outgoing link hop. The misses
were Q2 (broad `hide` crowded out conditional hide), Q4 (`Material prop`
excluded the Material bridge fact), and Q9 (the terms missed type-registration
options). Targeted probes found each missing fact. This is evidence about the
supplied queries and candidate limits, not an automatic question layer.

An FTS term inventory can show which words exist and how broad they are. It
cannot reliably recognize every separate ask, map arbitrary prose to Formly
concepts, or decide whether a retrieved fact answers the question. The layer
needs to preserve exact API identifiers while handling paraphrases and
multi-part questions without an ever-growing hardcoded synonym list.

The current 46 facts occupy **14,506 UTF-8 bytes** as ID, claim, conditions,
limits, and context; including source quotes gives **34,789 bytes**. These are
local serialized byte counts, not token or latency measurements. They make an
internal whole-fact selector a credible **comparison arm**. Anthropic advises
considering full context for small knowledge bases, but that advice does not
establish our selector's accuracy or speed.
[Anthropic contextual retrieval](https://www.anthropic.com/research/contextual-retrieval).

## Research findings

| Source-backed mechanism | Consequence for this POC |
| --- | --- |
| Contextual Retrieval adds chunk-specific context before **both** lexical indexing and embedding, with optional reranking. Anthropic reports lower top-20 retrieval failure on its own datasets. | Our authored `context` is indexed in FTS5. We have **not** built contextual embeddings, an Anthropic-style generated preface, or a reranker. Its percentages are not our result. [Anthropic](https://www.anthropic.com/research/contextual-retrieval). |
| Hybrid search uses lexical matching for exact identifiers and vectors for conceptual paraphrases; reciprocal-rank fusion merges different ranking scales. | Formly questions mix `props.disabled`, `defaultValue`, and ordinary descriptions. Compare lexical and semantic candidates over the **same facts**, with exact version/adapter filtering. Fusion cannot recover a fact absent from both candidate lists. [Microsoft hybrid search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview). |
| An LLM can split a complex question into focused subqueries that run in parallel. Microsoft also notes added latency and labels its Azure query-planning capability preview. | Borrow the bounded multi-query pattern, not the Azure service or its performance claims. Measure whether one planner call earns its cost under our 25-second whole-answer gate. [Microsoft agentic retrieval](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview). |
| Vector search returns nearest neighbors even for off-topic input; exact similarity is suitable for a small collection. | A vector hit cannot mean “supported.” Test negative and unsupported-version questions. At 46 facts, an ANN service is unnecessary for this experiment. [Microsoft vector-query behavior](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-query) · [Sentence Transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html). |
| Retrieval coverage and final-answer correctness require separate measures. Recall@K, precision, negative cases, groundedness, and completeness expose different failures. | Grade selected facts and eventual agent answers separately. Citation presence alone proves neither relevance nor correctness. [Microsoft retrieval evaluation](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval) · [Microsoft RAG evaluators](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/rag-evaluators). |

The [older contextual-hybrid plan](../../docs/knowledge-poc-contextual-hybrid-plan.md)
targeted a different 148-section POC. It remains research provenance; its index
and benchmark do not exist in this 46-fact POC. Whether our authored fact
context is enough for paraphrase retrieval requires a fresh test.

## Three architecture candidates

All arms must read the **same frozen facts**, enforce the same version/adapter
scope, and return the same bounded evidence-packet size. The existing
designer-supplied FTS fixture remains a diagnostic, not an automatic baseline.

| Arm | Question processing | Retrieval or selection | What it isolates |
| --- | --- | --- | --- |
| A: direct hybrid | Original question plus exact API tokens; no planner call | Current FTS5 plus one new dense similarity path, fused by rank, then explicit links | Whether semantic retrieval alone handles the wording changes and observed misses. |
| B: planned hybrid | One bounded model call returns distinct answer obligations and focused searches | Per-obligation lexical and dense candidates, rank fusion, explicit links, and fact selection | Whether decomposition materially improves complete fact-set delivery. |
| C: whole-fact selector | One model call sees the compact, version-filtered fact catalog and returns IDs per obligation | Exact DB reads by selected ID; no search-index candidate step | Whether this small corpus can avoid query-planning/search complexity and still return a compact packet. |

C is a small-corpus control, not an agreed replacement for contextual hybrid
retrieval. A must be measured before crediting B's planner; otherwise a vector
gain could be misattributed to decomposition. We should select one serving path
from evidence instead of permanently stacking all three.

## Proposed B path if planning earns its place

```text
question + explicit version/adapter context
  → obligations and preserved API identifiers
  → focused lexical and semantic searches per obligation
  → version-filtered candidate union and rank fusion
  → bounded explicit see_also expansion
  → fact selection and per-obligation evidence check
  → one compact cited fact packet for the calling agent
```

The planner would return a small validated structure, **not** an answer. Each
obligation retains the user's ask, focused natural-language search wording,
verbatim API identifiers, and explicit scope clues. Q2, for example, has
separate obligations for conditional hiding, conditional disabling, and the
effects of hiding on the model and control. Unknown version or adapter stays
unknown until an explicit baseline is applied visibly. A request for another
Formly version cannot silently receive 6.3.12 claims.

The FTS vocabulary can help validate query syntax and expose rare or broad
terms. It should not be injected wholesale into the planner prompt or treated
as a closed list of meanings. The current `unicode61` tokenizer may split
dotted API paths, so retain the exact original identifier even if the FTS
query uses component tokens. [SQLite FTS5 documentation](https://www.sqlite.org/fts5.html).

Give each obligation its own candidate allowance before merging. This directly
tests Q2's failure, where broad `hide` results filled the five-row limit. Apply
version and adapter filters before ranking. A dense arm can embed deterministic
text from fact title, claim, context, conditions, and limits; the vector is a
locator, while the original claim and source remain evidence. Exact similarity
over 46 vectors suffices to test the method. If promoted, vectors should stay
rebuildable derivatives keyed by fact ID, input hash, and pinned model version,
without a second canonical knowledge store.

The packet should group selected facts by obligation, retain their conditions,
limits, version/adapter and citations, and identify gaps. The layer may report
that it found **candidate evidence**; a matching fact ID alone does not certify
semantic sufficiency. Any automatic “supported” judgment needs negative-case
tests and independent grading of false support. The calling agent forms the
final answer from the packet.

Do not add a cross-encoder reranker by default. Test one only if required facts
enter candidate lists but repeatedly fall below the packet cutoff. Reranking
adds a query-time step and cost. [Anthropic](https://www.anthropic.com/research/contextual-retrieval) ·
[Microsoft information retrieval](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval).

## Decisive experiment and decision rule

1. **Freeze questions and source-backed grading first.** Keep Q1–Q10 as exposed
   diagnostics. Add held-out paraphrases, exact API identifiers, multi-part
   questions, misleading near-matches, spelling variants, version/adapter
   conflicts, and truly unanswered questions. Predeclare essential fact IDs
   and qualifications. Do not give those IDs to the planner or selector.
2. **Build A, B, and C as separate arms.** Use the same seed and packet budget.
   Freeze one embedding model and one planner/selector model for the trial.
   Record cold and warm startup. Avoid synonym-list, BM25-weight, and prompt
   micro-tuning on held-out questions.
3. **Score each failure stage.** Record whether the source fact existed, the
   obligation was recognized, the fact entered candidates, survived ranking
   and packet limits, retained its qualifications, and was used in the final
   answer. This distinguishes retrieval failures from answer-use failures.
4. **Measure the whole request.** Report complete fact-set recall at the packet
   budget, irrelevant fact rate, wrong-version/adapter delivery, false support
   on unanswered cases, packet bytes, component times, and prompt-to-final
   answer time. The provisional 25-second gate concerns the whole answer, not
   SQLite search alone. Run a fresh-agent answer trial after packet reachability
   is credible.
5. **Keep one path.** Promote a planner only if it rescues several material
   held-out misses without critical scope errors or a failed latency gate. If
   A performs comparably, skip planning. If C wins at this corpus size, record
   its scale limit and decide explicitly whether to use it until the corpus
   grows. Independently review the results and failure ledger first.

The first build slice should cover Q2, Q4, Q9, and a negative/version case with
failing-before-fix tests, then run the frozen comparison. Authored facts and the
validated seed stay unchanged unless testing reveals a real source error. This
research does not claim that any arm has improved accuracy or latency yet.
