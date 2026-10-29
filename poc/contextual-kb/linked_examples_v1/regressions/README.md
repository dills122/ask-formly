# Linked-example retrieval checks

These are public development cases, separate from sealed evaluation. G1–G4
retain the issue-21 fixed plans; E1–E3 exercise the three initial examples. A
Formly 7 request checks unsupported-scope stopping. Expected fact IDs are a
selected-evidence rubric, not an exhaustive definition of a correct answer.

Run with the MCP dependencies installed, a read-only baseline DB and its pinned
hash, and a new ignored output directory:

```sh
python poc/contextual-kb/linked_examples_v1/regressions/run.py \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09 \
  --output test-output/linked-examples-v1/replay-new
```

The harness runs each case three times against the baseline and isolated candidate
through real stdio. It records complete transcripts, stderr and a report with
DB/case/rubric hashes. The DB hash is checked before and after. New settings files
live in the output directory. No installed service or launcher is changed.

The fixed caller policy reads two pages of eight omitted candidates, ranks those
returned records by request-word overlap, and fetches at most four facts in pairs.
It lists examples linked to delivered facts and fetches up to three distinct
examples. Only after all caller decisions are recorded does the grader load the
expected IDs. The grader checks that recovery IDs were actually discovered.

Report first-pass coverage, post-recovery coverage, missing rubric IDs, calls,
example fetches, errors and actual serialized SDK bytes separately. An
outside-rubric fact is not automatically irrelevant; this harness does not claim
precision or answer accuracy. Baseline/candidate first-pass and recovered fact IDs
must match, so optional example metadata cannot displace facts. Three deterministic
repeats check stability; they do not establish autonomous caller reliability.

## Fresh callers

Give a fresh caller only a user question and this command, with an independent
transcript path. Do not supply the fixed plans, rubric, expected IDs or replay
results. `list_tools` returns server instructions and tool schemas:

```sh
python poc/contextual-kb/linked_examples_v1/regressions/call.py \
  --database /absolute/path/to/knowledge.sqlite --sha256 PINNED_HASH \
  --transcript test-output/linked-examples-v1/caller-a.jsonl \
  --tool list_tools
```

For subsequent calls, use `--tool lookup_formly` (or another exposed tool) and
`--arguments /absolute/path/to/arguments.json`. `--mode baseline` selects the
unchanged baseline adapter. Every call starts a new stateless MCP process and
appends complete inputs/outputs to the JSONL transcript. The caller owns relevance
assessment and stopping. Grade its final answer independently for evidence use,
conditions/limits, illustration versus verification, and unsupported claims.
