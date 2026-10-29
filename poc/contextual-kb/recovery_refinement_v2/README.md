# Guided recovery comparison

This supplements, and does not replace, the unchanged
[retrieval refinement v1](../retrieval_refinement_v1/README.md) frozen rubric.
It compares two source trees and two caller policies on the original public G3
initialization and G4 collision plans. Facts, provenance, the database and the
original plan conditions remain unchanged.

## Frozen inputs

Revision 1 freezes the two original requests/plans, eight essential support facets
and the guided policy before tool execution. G3 reuses the four initialization
facets from v1: initial model preparation, fallback eligibility, returned
Observable lifetime and manual subscription cleanup. G4 reuses four facets:
keyed model scope, key versus DOM identity, shared-control lookup and validator
ownership. Preset/build/formState details are conditional on the broad plan's
particular configuration branch. Hiding and repeater operations are conditional
collision branches, not universally necessary recommendations. Equivalent evidence
retains v1's exact alternatives. Historical 12/9 expected-ID counts are separately
reported; they are not the essential denominator.

The guided policy makes at most four follow-up calls: two discovery/fetch rounds,
with at most sixteen candidate summaries and four requested facts per round.
Each round focuses on a frozen plain-language distinction from the supplied plan.
Both sources use that same focus text to select returned IDs. Only a source whose
tool schema exposes `focus` receives it as a discovery argument. Candidate
selection rewards focus terms not represented by already delivered evidence,
then total focus overlap, then the stable discovery order. It never receives
expected IDs, facts from the rubric or the corpus. Grading loads only after every
source/policy transcript has been written.

This is **guided fixed-intent replay**, not autonomous planning, a held-out
relevance test, or a measure of minimum recovery effort. More records per fetch
and different intent selection can improve the caller independently of a server
change. The factorial comparison keeps those effects visible:

| Source | Caller policy | What comparison establishes |
| --- | --- | --- |
| Baseline | Original frozen v1 | Previous bounded heuristic |
| Baseline | Guided | Caller-policy effect without focus API |
| Candidate | Original frozen v1 | Default behavior regression control |
| Candidate | Guided | Combined behavior; compare with baseline/guided for focus API effect |

Three deterministic repeats produce 24 actual MCP stdio case executions. The
separate v1 run exercises all fifteen cases, both sources and three repeats
(90 executions) with its original gates and exact frozen inputs.

## Run

Use an existing MCP Python environment and the unchanged pinned database:

```sh
python poc/contextual-kb/recovery_refinement_v2/run.py \
  --baseline-poc /absolute/path/to/baseline/poc/contextual-kb \
  --candidate-poc /absolute/path/to/candidate/poc/contextual-kb \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09 \
  --output test-output/recovery-round2/guided-new
```

The source-only harness tests run without installed assets:

```sh
python -B -m unittest discover -s poc/contextual-kb/recovery_refinement_v2
```

Frozen gates require all eight essential facets in candidate/guided, no facet
regression compared with either the same source's old policy or baseline/guided,
unchanged first packets, a positive aggregate historical recovery gain over
candidate/original, deterministic repeats, no tool errors or undiscovered fetch
IDs, and unchanged call/transport limits. Failed gates remain recorded failures.
Manual fresh-answer review remains necessary: evidence delivery cannot certify
that an answer preserves conditions or refuses a universal same-path winner.

## First result

All frozen gates passed in 24 factorial executions with stable results across
three repeats. The separate unchanged v1 rubric also passed all 90 executions,
retaining 23/23 first-response essential facets. Per-repeat factorial results:

| Source / policy | G3 essential facets | G3 historical IDs | G4 essential facets | G4 historical IDs |
| --- | ---: | ---: | ---: | ---: |
| Baseline / original | 2/4 | 6/12 | 2/4 | 4/9 |
| Baseline / guided | 4/4 | 10/12 | 3/4 | 5/9 |
| Candidate / original | 2/4 | 6/12 | 2/4 | 4/9 |
| Candidate / guided | 4/4 | 9/12 | 4/4 | 7/9 |

The caller-policy change recovered initial-value guidance without requiring the
new API. Focused discovery additionally recovered shared-validator ownership in
collisions. All eight essential facets were delivered by candidate/guided within
four follow-ups. Maximum SDK result was 29,775 bytes in this factorial and 29,897
bytes in the full v1 comparison.

The focus API is not a universal improvement in every returned fact set. Guided
baseline recovered the conditional preset explicit-override fact, while guided
candidate did not; its historical initialization count was therefore one lower.
The candidate still recovered all four initialization essentials. Its remaining
historical omissions were rebuild-clears-validators, preset-partial-overrides and
changed-model-input-rebuilds. Collision omissions were key-paths and repeater
remove-coordination. These conditional or deeper support gaps remain visible;
passing eight essentials does not establish exhaustive support for every broad
plan branch. The old policy's 6/12 and 4/9 results remain unchanged.

Raw reports and complete MCP transcripts are retained in ignored
`test-output/recovery-round2/guided-factorial-1/` and
`test-output/recovery-round2/original-frozen-1/`. The database and both frozen input
sets matched their original hashes after execution.

Every case/mode used one lookup plus exactly four follow-up calls. Historical
omissions by mode are below (fact IDs are abbreviated to their final segment;
full topic-qualified IDs are retained in the reports and rubric):

| Mode | G3 historical omissions | G4 historical omissions |
| --- | --- | --- |
| Baseline / original | `rebuild-clears-validators`, `preset-setup-reference`, `changed-model-input-rebuilds`, `default-value-is-fallback`, `model-preferred-for-computed-initial`, `preset-partial-overrides` | `remove-coordination`, `key-paths`, `shared-validator-ownership`, `shared-key-control`, `key-id-name-roles` |
| Baseline / guided | `rebuild-clears-validators`, `changed-model-input-rebuilds` | `remove-coordination`, `key-paths`, `shared-validator-ownership`, `shared-key-control` |
| Candidate / original | Same as baseline / original | Same as baseline / original |
| Candidate / guided | `rebuild-clears-validators`, `changed-model-input-rebuilds`, `preset-partial-overrides` | `remove-coordination`, `key-paths` |

The nonregression gate is explicitly for **essential facets**, not every
historical ID or conditional branch. No policy or rubric was tuned after seeing
these outcomes.
