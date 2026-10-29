# Frozen retrieval refinement rubric

Public development comparison for identifier matching, packet selection and
question-specific recovery. This does not change facts, compile knowledge, open
sealed evaluation or promote a runtime.

`freeze.json` pins the exact bytes of `cases.json`, `rubric.json` and `policy.json`
before runtime edits and before evaluation. Revision 1 was a pre-implementation
draft: review found that the key-versus-renderer fact did not establish the DOM
key/id/name distinction. Revision 2 removes that invalid alternative. The earlier
draft is retained in ignored development evidence. No observed outcome motivated
the correction.

## What the rubric measures

Thirteen gated cases cover initial values, initialization versus hooks, default
ordering, qualified/bare formState, natural collision wording, keyed scope,
shared validators, same-path uncertainty, and hide/JSON Schema/Material/version
controls. Two original G3/G4 plans remain historical diagnostics.

Each essential facet defines acceptable supporting facts. Equivalent fallback
facts can satisfy the same facet, but neighboring facts do not automatically count
as equivalents. Conditional evidence (such as repeaters) does not inflate the
essential denominator. Unsupported conclusions are recorded for separate manual
answer review. A matching fact ID proves evidence delivery, not that the caller
understood the claim or respected its limits.

Frozen automated gates require all essential facets after at most four follow-up
calls, no per-case first-response facet-count regression, all essential hide,
uniqueItems and compareWith control facets initially, and the observation fact
initially for both formState spellings. All calls must meet scope, transport,
provenance-discovery and repeat-stability checks. Failures remain failures; this
rubric must not be edited to rescue an implementation result.

## Rubric-blind recovery

The executor receives only requests/plans and policy. It selects the original
plan question with the least delivered primary-text token coverage, breaking ties
by original order. In a multi-question plan it visits different questions before
reusing one. Each of two rounds performs one discovery call of eight records and
fetches at most two returned IDs selected by that question's lexical overlap.
Already delivered IDs are excluded. One-question cases page forward.

When the server advertises `question_index`, discovery is restricted to that
original question. The older baseline falls back to global pagination. This
intentional API difference is the recovery feature under comparison; both modes
retain the same four-call maximum and selection policy. The expected-fact rubric
is loaded only after both modes' caller decisions have been saved.

## Run

Use the MCP Python environment and a new output directory. Baseline and candidate
are explicit source trees, independent of installed launchers or their manifests.
The test adapter opens the supplied database read-only using its pinned digest.

```sh
python poc/contextual-kb/retrieval_refinement_v1/run.py \
  --baseline-poc /absolute/path/to/baseline/poc/contextual-kb \
  --candidate-poc /absolute/path/to/candidate/poc/contextual-kb \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09 \
  --output test-output/retrieval-refinement-v1/replay-new
```

Fifteen cases run three times against both modes: 90 real stdio case executions.
Reports include first-pass and recovered facets, raw IDs, conditional evidence,
historical counts, errors, bytes and gate failures. Logs and full transcripts
remain under ignored `test-output/`. The database and frozen inputs are checked
again after the run. Generated evidence is not public release content.

Run the asset-free harness tests with:

```sh
python -B -m unittest discover -s poc/contextual-kb/retrieval_refinement_v1
```

Three deterministic repeats do not establish autonomous answer quality. Fresh
callers must receive only user questions and live tool instructions, and their
actual answers must be reviewed for preserved conditions, accurate citations and
unsupported claims. In particular the same-path case must disclose the missing
complete configuration-outcome matrix. Automated evidence coverage cannot pass
that manual requirement on its own.

## First comparison result

The first paired run passed the frozen gates across all 90 case executions with
stable metrics in three repeats. Per repeat, the baseline delivered 21/23
essential facets initially and 22/23 after recovery; the candidate delivered
23/23 initially and after recovery. The two newly delivered initial facets were
qualified formState observation and natural-language collision namespacing.
Maximum serialized SDK result was 29,897 bytes for the candidate and 29,742 for
the baseline. No tool errors, unsupported-scope evidence, or undiscovered-ID
fetches were observed.

Historical G3/G4 recovery remained 6/12 and 4/9 under this bounded heuristic; the
new focused rubric does not erase those broader misses. The deterministic policy
always attempts its bounded recovery rounds even when essentials happen to be
delivered, since it cannot inspect the grader. Its call counts therefore do not
measure an autonomous caller's minimum effort. Separate fresh-caller/manual
assessment remains necessary for unsupported claims and answer quality.

Raw run: ignored `test-output/retrieval-refinement-v1/replay-1/report.json`, with
complete baseline/candidate transcripts and harness input hashes alongside it.

For a fresh caller, provide only its user request and `call.py --poc SOURCE_POC
--database DB --sha256 PIN --transcript OUTPUT.jsonl --tool list_tools`. Subsequent
calls use `--tool NAME --arguments INPUT.json`. This helper reads no cases or
rubric and appends complete tool inputs/results. Every call starts a fresh stateless
MCP process; the caller retains its request and plan between calls.
