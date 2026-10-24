# Question-layer pilot: one fixed pass

**21 October 2026.** This is a small, exposed diagnostic over the current
46-fact Formly 6.3.12 database. It compares three ways to select fact IDs for
a question. It does not generate an answer or exercise an MCP request. The
[case fixture](QUESTION-PILOT-CASES.json) was fixed before the measured run;
there was one prompt-format smoke correction before that run and no tuning
against its results. The detailed local run is
`test-output/contextual-kb-question-pilot.json` (ignored by Git).

## Method

- **A, direct hybrid:** run the original question against contextual FTS5 and
  exact cosine similarity over local BGE embeddings, fuse their ranks, then
  follow explicit `see_also` links.
- **B, planned hybrid:** ask a local Qwen 2.5 Coder 3B model for one to four
  subqueries, run each through the same hybrid lookup, interleave candidates,
  then follow links.
- **C, whole-fact selector:** give the same local model the compact catalog of
  46 facts and ask it to return relevant IDs; read those facts directly.

All arms use the same read-only database and return at most eight fact IDs.
The embedding model is `BAAI/bge-small-en-v1.5`; the model call uses
`qwen2.5-coder:3b-instruct` at temperature zero through local Ollama. The
database source-input SHA-256 was
`88dfedb45ddedf11fcf793790de5b2c43f297f45466eb6a4f19ea61cbf2605ad`;
the case-fixture SHA-256 was
`f066b478f461fb13a9982833aa7b228cb9469e1b5dfc07b97dd5ccc7c07109f7`.
The BGE local cache revision was
`52398278842ec682c6f32300af41344b1c0b0bb2`.

The score asks whether the selected packet contains **every predeclared
required fact ID**. It is not an answer-accuracy, factual-entailment, or
semantic-precision score. Q1–Q10 reuse earlier exposed gold IDs; P11–P13 are
additional paraphrases; P14 is unrelated; P15 asks about an unsupported
Formly version. The suite is too small and exposed to estimate production
accuracy.

| Arm | Answerable cases with all required IDs | Unrelated P14 abstention | Measured query time, 15 cases | Median case time |
| --- | ---: | ---: | ---: | ---: |
| A: direct hybrid | 10/13 | Failed: 7 facts | 0.133 s | 0.007 s |
| B: planned hybrid | 7/13 | Failed: 3 facts | 13.980 s | 0.940 s |
| C: whole-fact selector | 3/13 | Failed: 3 facts | 59.509 s | 4.457 s |

Startup, including local embedding load and indexing, was 0.766 s for this
run. The explicit Formly v7 case P15 returned no facts in every arm because a
shared deterministic major-version gate stopped it before search or model
selection. Including that shared gate yields 11/15, 8/15, and 4/15 respectively,
but it is clearer to report the 13 answerable cases separately. These times
exclude MCP transport, agent reasoning, and final answer generation; the
25-second whole-answer gate remains untested.

## Failure ledger

| Case | A | B | C | Observation |
| --- | --- | --- | --- | --- |
| Q2, hide/disable/model/control | Miss | Miss | Miss | A and B retrieved several hide effects but missed both conditional expression facts. The gold itself omits the control-unregistration fact asked for in the question. |
| Q10, wrapper vs type | Miss | Miss | Miss | A missed the wrapper insertion point; B and C also missed the Material owner fact. |
| P12, hidden value and control | Miss | Miss | Miss | All missed control unregistration. |
| P13, registered component and key | Pass | Miss | Pass | B's planner replaced `key` with invented `fieldKey` and lost the type-selection distinction. |
| P14, unrelated Stripe question | False support | False support | False support | None has a reliable evidence-sufficiency or abstention decision. |

Other B misses were Q9 and P11. C missed Q1, Q4, Q5, Q7, Q8, Q9, and P11
in addition to the shared misses. A read-only lexical-only/dense-only check
at the same packet size reached 10/15 and 11/15 exact-ID cases respectively;
this pilot shows **no aggregate complete-case gain from fusing them** over
dense alone, although their per-case results differ.

## Independent review and limits

A separate reviewer examined the fixture, code, and run output without
changing files or rerunning models. The reviewer found three interpretation
limits:

1. Q2's required IDs omit the fact that a hidden control unregisters, despite
   the wording asking about the control. Exact-ID completion therefore does
   not establish answer completeness. The runner's raw field named
   `irrelevant_count` counts all **non-required** IDs; some are useful facts.
   It must not be treated as measured irrelevance or precision.
2. Candidate budgets differ before the final eight-ID packet: A takes six
   direct hybrid candidates; B takes three per planned query before merging,
   so a single-query B has only three; C can choose eight. The comparison
   does not prove planning itself caused any specific miss.
3. P13 shows a concrete planner fidelity failure. The current validation
   checks the output shape, not whether planned queries preserve exact API
   terms and every part of the question.

## Decision from this bounded pilot

A has the strongest observed required-ID reach and lowest query time in this
specific configuration. **No arm is ready to serve as the knowledge MCP's
evidence packet:** all returned Formly facts for an unrelated question, and
all missed at least one multi-part or control-lifecycle case. The weak C result
is evidence about this 3B model and prompt on this corpus, not a rejection of
whole-catalog selection generally. The B result does not justify adding a
planner now, especially given the unequal candidate budgets.

The next meaningful test is a bounded relevance and sufficiency check on
packets: can the system preserve all question obligations, distinguish
answering evidence from topical neighbors, and abstain when the corpus cannot
answer? That should use repaired, source-reviewed gold obligations and
negative cases before any ranking or prompt tuning. This pilot deliberately
stops before that next build.

## Reproduce the local harness

From `poc/contextual-kb` with the seeded database and the two local models
available:

```sh
uv sync --frozen
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m kbcompiler.question_pilot --output ../../test-output/contextual-kb-question-pilot.json
```

The isolated suite passed 43 tests. The model run is optional and can differ
across model revisions or hardware. It was not rerun after inspecting misses.
