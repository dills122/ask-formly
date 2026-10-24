# Small-catalog question-layer bake-off

**21 October 2026. Decision: keep all three paths experimental.** This is one
frozen local comparison of the current eight-fact packet, a broad contextual
hybrid pool, and a full-catalog selector. It changes no authored fact, database
schema, seed, or serving MCP path. The read-only database SHA-256 remained
`3cdef0fc65e7afd747d3283adfdc47346ecfd64abd7d555d469fb982a2f84ea3`.

## Method and boundaries

The [13-case fixture](CATALOG-BAKEOFF-CASES.json) was written before either new
arm was run. It contains nine answerable developer questions and four negative
or out-of-scope questions. Gold IDs were not present in model prompts. All arms
used the same 46 authored Formly 6.3.12 core/Material facts in the existing
SQLite database. The broad arm used one fixed recipe: hybrid top 16, contextual
FTS probes, and explicit links, capped at 24 candidates. The full arm exposed
all 46 facts. One local Qwen3 Coder 30B call selected at most eight fact IDs and
named unresolved parts for each new arm. The current arm returned its existing
eight-fact candidates. Every packet copied original database claims, context,
conditions, limits, source path and source quote; no selector-generated Formly
advice entered a packet.

The [selection artifact](../../test-output/contextual-kb-catalog-bakeoff.json)
contains all packets, candidate counts, IDs, missing gold IDs, timings and
hashes. A separate [answer artifact](../../test-output/contextual-kb-catalog-answer-diagnostic.json)
contains one local-model answer from every packet. That answerer is a **proxy**
for a calling agent, not an MCP/agent end-to-end measurement. All reported times
are local warm times and exclude MCP transport and Codex reasoning. One run per
case/arm was made; no prompt or pool tuning followed the frozen run.

## Objective measurements

| Arm | Complete required-ID sets | Negative packets empty | Successful negative abstentions | Selector errors | Mean packet bytes | Mean local selection time | Mean local selection + answer time | Slowest local total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Current eight | 7/9 | 2/4 | 2/4 | 0 | 5,946 | 0.03 s | 4.48 s | 7.69 s |
| Broad 24 | 8/9 | 3/4 | 2/4 | 1 | 2,731 | 3.22 s | 6.39 s | 14.10 s |
| Full catalog | 8/9 | 3/4 | 3/4 | 0 | 2,809 | 5.50 s | 8.35 s | 13.84 s |

Both new arms reduced mean packet size by about half while gaining one strict
required-ID case. Neither reliably withheld unsupported evidence. On B10, the
broad arm returned two topical facts while flagging the persistence question
unresolved; the full arm returned three topical facts and **did not flag the
gap**. B11 broad had a selector-contract error and emitted no packet. That is
a safe failure, **not a successful unsupported-case decision**; the successful
abstention column excludes it.
Version and adapter conflicts were rejected in all arms.

The strict ID check is only a coverage diagnostic. B05's full-catalog packet
omitted one predeclared ID but included other facts that explain registration;
its answer was substantively complete. B06's broad packet omitted the
reverse-merging fact, although the question could be answered from the password
inheritance example and `defaultOptions` registration fact. Conversely, a
complete ID set does not mean the answer used facts correctly.

## Strict answer audit

I read all 39 answer outputs against the questions and selected source-linked
facts. The audit counts an answer as clean only if it addresses every asked
part, preserves material qualifications, contains no unsupported advice, and
does not simultaneously mark an answered part unresolved. This is an in-session
human assessment, **not an independent or blinded review**.

| Case | Current | Broad | Full | Main reason for a failed clean answer |
| --- | :---: | :---: | :---: | --- |
| B01 computed initial/default | Yes | No | Yes | Broad answers the default question, then marks it unresolved. |
| B02 hidden shared key | No | No | Yes | Current and broad answer, then mark the whole question unresolved. |
| B03 wrapper/value accessor | No | No | No | All three give both facts, then mark those same asks unresolved. |
| B04 custom props/generic | No | No | Yes | Current duplicates an unresolved ask; broad emits eight mostly extraneous claims and duplicates the unresolved ask. |
| B05 path key/type registration | Yes | Yes | Yes | All three answer the question despite different cited ID sets. |
| B06 inherited password type | No | No | No | All three supply useful facts, then mark the same question unresolved; current includes unrelated default-value material. |
| B07 modern/legacy callback | No | Yes | No | Current and full mark the signature comparison unresolved after stating both signatures. |
| B08 shared context | Yes | Yes | Yes | Both aspects are answered. |
| B09 hidden array/default | No | No | No | All turn the source's qualified “can clear” into definite child clearing. |
| B10 formState browser persistence | No | No | No | Current and full assert lack of automatic persistence without supporting evidence; broad adds unrelated claims and an unsupported causal detail. |
| B11 HTTP retry/backoff | Yes | Error | Yes | Current and full abstain; broad's selector error produces an empty packet but is not a valid answer run. |
| B12 Formly v7 | Yes | Yes | Yes | Explicit version gate abstains. |
| B13 PrimeNG adapter | Yes | Yes | Yes | Explicit adapter gate abstains. |

Strict clean local answers were **6/13 current, 5/13 broad, and 8/13 full**;
the broad arm also had one failed run.
The full catalog improved this small proxy sample, but none clears an
accuracy-first adoption gate. On B10 the full-catalog answer cites the
`formState` shared-context fact for a browser-persistence assertion that the
fact and its source quote do not make. This is the same failure class seen in
the earlier [three-question probe](../../test-output/contextual-kb-full-catalog-probe.json):
the model may cite a related fact while inventing a missing prescription.

## What this resolves

1. **The eight-fact cap does lose evidence sometimes.** B05 and B06 lack a
   predeclared fact in the current packet; both wider paths place every B05/B06
   gold fact in their candidate pool. The new selector then omitted B05 in the
   full arm and B06 in the broad arm. These are selection losses, not pool misses.
2. **A larger evidence window alone is insufficient.** The full arm improves
   the strict local answer audit, but it incorrectly treats B10 as answerable.
3. **The answer contract itself is weak.** B03 and B06 show useful cited claims
   plus contradictory `unresolved` entries. B09 loses the source's “can”
   qualification. Citation validation catches invented IDs, not entailment.
4. **Latency is not yet qualified.** All local totals were under 25 seconds,
   but the provisional 25-second gate concerns the real MCP-to-agent final
   answer. This trial cannot claim that gate passes.

An [independent fresh-task review](../../test-output/contextual-kb-bakeoff-independent-review.md)
confirmed the measured figures and identified the B11 scoring error. We
accepted the finding, added regression tests, and fixed future trial scoring
and diagnostic status. The frozen raw artifacts remain unchanged; this report
uses the corrected interpretation. The reviewer judged the experiment ready
as a diagnostic, with no serving-path adoption supported.

No arm was promoted. A further iteration should be a **different response
contract experiment**, not more question splitting or FTS/prompt microtuning:
test whether a calling agent given original facts plus explicit provenance can
produce a concise answer with no unsupported claims or contradictory gap flags.
Retain B10, B03, B06 and B09 as diagnostic failures and use new held-out cases
for any next scored comparison. The full-catalog path is a viable small-corpus
comparison arm, not a proven serving architecture.

## Reproduce

From `poc/contextual-kb` with the local model cache and Ollama daemon:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -q
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.catalog_bakeoff_trial --output ../../test-output/contextual-kb-catalog-bakeoff.json
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m kbcompiler.catalog_answer_trial --input ../../test-output/contextual-kb-catalog-bakeoff.json --output ../../test-output/contextual-kb-catalog-answer-diagnostic.json
```

The isolated suite passed **82 tests** after the review correction. The trial commands overwrite their
output paths, so choose new paths to retain this frozen run.
