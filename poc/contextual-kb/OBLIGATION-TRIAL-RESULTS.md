# Obligation-level question trial

**21 October 2026. Decision: do not promote either new arm.** This bounded
experiment tests the proposed per-ask question layer beside the existing
question layer. It does not change authored facts, the seeded database, or MCP
serving. The database was opened read-only and retained SHA-256
`3cdef0fc65e7afd747d3283adfdc47346ecfd64abd7d555d469fb982a2f84ea3`.

## Method

The fixed [case set](OBLIGATION-TRIAL-CASES.json) has nine answerable questions
and two with no answer in this corpus. Seven cases were previously exposed;
N1-N4 were added and frozen before the new arms were implemented. Gold IDs
come from the authored, seeded fact claims and are a retrieval-coverage check,
not an independent audit of every source passage or a measure of answer
accuracy. The same database, contextual FTS5, dense vectors, local
cross-encoder, explicit links, version/adapter filters, and eight-ID packet
budget were used by both new arms.

- **Existing layer:** one broad hybrid query plus focused lexical probes.
- **Deterministic arm:** split punctuation and coordinated words into literal
  question spans; retrieve and rerank up to two facts per span before merging.
- **Local-model arm:** Qwen3 Coder 30B produces only literal question spans.
  Validation rejects invented spans and dropped exact API identifiers;
  malformed output falls back to the deterministic arm. It never sees source
  facts during planning.
- **Evidence-check diagnostic:** a separate local Qwen3 Coder 30B call judges
  whether each selected fact directly answers its span in the full question.
  It may cite only selected IDs. This is a model assessment, not proof of
  factual entailment.

Microsoft's [agentic retrieval overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)
describes decomposing complex questions into focused subqueries, reranking
each, and returning grounding references. This trial tests that pattern with
our facts; it does not inherit Microsoft's performance results. The separate
coverage and support measures follow [Microsoft's RAG evaluation
distinction](https://learn.microsoft.com/en-au/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators?view=foundry)
between completeness and groundedness.

## Results

| Arm | Complete required-ID sets | Negative questions withheld | Warm query time for 11 cases | Slowest local case |
| --- | ---: | ---: | ---: | ---: |
| Existing layer | 5/9 | 0/2 | 0.548 s | 0.100 s |
| Deterministic obligations | 6/9 | 1/2 | 2.404 s | 0.468 s |
| Local-model obligations | 5/9 | 2/2 | 11.814 s (9.038 planning + 2.776 retrieval) | 1.493 s |

The evidence checker rejected both negatives in both arms, but only **3/9**
answerable cases passed both gold-ID coverage and its all-asks assessment for
the deterministic arm, and **2/9** for the model arm. Checking added 28.583 s
and 29.580 s respectively across the 11 cases. The slowest measured case with
checking was 3.879 s deterministic and 6.204 s model-backed. These are local
warm timings. They exclude MCP transport, fact-packet rendering, and final
agent answer time; they do not establish the 25-second whole-answer gate. The
first model-planning run took 21.056 s for 11 calls before the later warm run
took 9.038 s.

The run artifacts are saved under `test-output/` as
`contextual-kb-obligation-old-layer-baseline.json`,
`contextual-kb-obligation-deterministic-final.json`,
`contextual-kb-obligation-model-final.json`, and the corresponding
`*-check-final.json` files. Each new-arm artifact records hashes of the case
fixture, question-layer code, index code, and database.

## Failure ledger

| Case | Observation |
| --- | --- |
| Q2c, hide/disable/value/control | The deterministic splitter makes four asks and retrieves hide, value, and control, but misses the conditional-disabled fact. The local model makes only two broad asks and misses three of four required facts. Its evidence checker nevertheless marks both asks supported: a **false support decision**. |
| F1, default and reset | The deterministic arm retrieves all three facts that the existing layer lost under its global cap. The model splits incidental phrases such as `amount: 0` and `after an edit` into separate asks; those have no evidence, so its packet is withheld. |
| F2, hidden value and control | Both planners split `keep its answer` into an independent fragment with no lexical anchor. The packet is withheld despite useful candidates for other fragments. |
| F5, key and type | Both planners isolate user-supplied literals (`key: 'secret'`, `type: 'passwordBox'`) instead of keeping the key/type relationship. Neither returns the two required facts. |
| F6, HTTP/RxJS | Both arms expose an unresolved ask and withhold the merged packet. Other fragments still retrieve topical initial-value candidates, which are retained only in the diagnostic per-ask trace. |
| N4, PostgreSQL | The deterministic arm leaves the question broad and returns topical candidates; the evidence checker rejects them. The model isolates `PostgreSQL`, finds no lexical anchor, and withholds its packet. |

The layer now returns **no merged fact IDs** whenever any ask has no candidate
or the merged set exceeds eight IDs. Per-ask candidates remain in the trace
for diagnosis. This avoids silently delivering partial evidence, but it
cannot by itself decide semantic support. The model checker failed that test
on Q2c, so it must not be used as an authoritative gate.

## Decision and next test

The per-ask structure addresses the observed global-budget problem in one
case, but literal-span extraction is not a reliable representation of a
developer question. Deterministic splitting over-fragments context; the local
model both merges independent outcomes and splits incidental literals. A
larger model or another prompt is not justified by this fixed set.

The next structural candidate should represent each ask as a **target plus
shared question context**, preserving exact APIs and the relationship between
them. It must be scored against explicit gold aspects, not only a global ID
set. An answerability gate needs independent tests for topical false support
and missing qualifications before it can suppress or approve evidence. Use a
new unseen set for that experiment; these eleven questions are exposed.

## Reproduce

From `poc/contextual-kb` with the seeded database and local model caches:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.question_layer_trial --cases OBLIGATION-TRIAL-CASES.json --output ../../test-output/contextual-kb-obligation-old-layer-baseline.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.obligation_trial --arm deterministic --output ../../test-output/contextual-kb-obligation-deterministic-final.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.obligation_trial --arm model --output ../../test-output/contextual-kb-obligation-model-final.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.obligation_trial --arm deterministic --check-evidence --output ../../test-output/contextual-kb-obligation-deterministic-check-final.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.obligation_trial --arm model --check-evidence --output ../../test-output/contextual-kb-obligation-model-check-final.json
```

The model arm and evidence check contact only the local Ollama daemon at
`127.0.0.1`. The isolated suite passed **70 tests**. The new logic was added
beside the existing question layer, and none of the new arms was promoted to
MCP use.
