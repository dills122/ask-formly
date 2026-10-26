# Model-free parity: first diagnostic and discovery candidate

## Decision

Parity is not established. The fresh reference is stronger on initial evidence
selection. Keep the connected repair candidate and installed foundation unchanged;
the new additive discovery tool is an isolated candidate for caller qualification.

## Matched diagnostic

One pass: 10 covered requests plus exact-version and missing-knowledge controls,
same 93-fact DB. The old foundation9 ran its internal planner/GLiNER/retrieval/selector
with explicit user authorization for benchmarking only. No new-arm caller CLI was
launched: this conversation made native lookup/fetch calls. Native plans were saved
before inspecting reference output; native answer sketches were saved before reading
reference answers. Cases and expected IDs were author-visible throughout.

| Diagnostic | Old reference | Native model-free |
|---|---:|---:|
| Initial packets containing all designated IDs | 8/10 | 4/10 |
| All designated IDs after manual fetches | Not tested | 10/10 |
| Follow-up fetch calls | Not tested | 6 |
| Operational failures | 0/12 | 0/18 calls |

The six fetches used known diagnostic IDs selected by the author. Their success
establishes that the DB and scoped fetch path can supply the missing evidence;
it does not establish autonomous discovery accuracy or an unbiased 100% score.
The reference misses designated IDs in P03/P09; P03's disabled-ancestor fact tests
more detail than its request explicitly asks, so ID incompleteness alone must not
be interpreted as an incorrect final answer. Neither arm has a blind answer grade.

P11 stopped on unavailable 7.0.0 scope in both arms. P12 returned unrelated lexical
hits in both arms: the native answer correctly disclosed missing signing-service
evidence. Server success is not semantic support. Old output is an evidence packet,
not a final answering-agent response.

Median old covered-request tool time was 26.84 seconds; native lookup was 0.0335
seconds. These are not comparable end-to-end times: native agent planning, reading,
reasoning and answer synthesis are excluded. Parallel native calls also differ from
serial old calls. Payload sizes, individual timings and missing IDs are recorded in
test-output/score.json. No latency improvement claim is based on this comparison.

## Bounded change

The frozen lookup limits initial evidence to four ranked facts per question. Some
needed facts rank well below that; initial hits can match exclusions or irrelevant
API mentions. Merely growing the packet does not solve semantic selection.

discovery.py and serve_discovery.py add discover_formly_candidates alongside the
unchanged two tools. It reuses the existing plan/repair and exact-scope gates, fairly
interleaves omitted candidate IDs, and returns paginated complete fact records
without heavy source quotations. Claims, conditions, limits and applicability are
preserved. Default16/max32 records, maximum24KB candidate-array bytes per page;
envelope and MCP duplicated text/structured representations are additional bytes.
No record is clipped or silently skipped. The caller must select relevant IDs and
fetch full citations before answering. Identical request, plan and resolved scope
are required across pages. No new ranking or model was introduced.

This exposes evidence for the calling agent's selection, the responsibility formerly
handled by the old hosted selector. It does not guarantee that the caller will choose
correctly, and broad lexical pools can still require several pages. The candidate
is not installed in .codex/config.toml or promoted into the working foundation.

## Verification

- TDD: six discovery tests first failed because the module did not exist, then passed.
- Five benchmark harness tests passed before the reference run.
- Independent review1 found a scorer failure-accounting issue (current successful
  run unaffected). Fixed with five additional tests, including aggregate timeout/
  early-stop accounting and receipt inconsistencies; all16 parity tests pass.
- Independent review2 accepted the bounded scoring fix with no actionable findings;
  review1 accepted retaining the discovery candidate with that follow-up. Neither
  review qualifies promotion or answer parity.
- Real stdio transport under the existing no-model/network/subprocess Python guard:
  12 original lookup packets unchanged; all designated facts reachable for10covered
  cases; version-stop, missing-plan, malformed-condition and pagination checks pass.
  Exhaustive paging is a mechanical reachability check, not agent selection testing.
- Initial transport attempt failed on a launcher import path; retained failure logs,
  fixed the candidate's own import path, and reran successfully.
- 18 existing model-free repair regressions pass.
- python3 tools/project.py check passes. Its asset checks do not establish external
  service availability; the separate reference run supplies that evidence for this pass.
- 802 frozen files verified before/after reference and discovery replay. Installed
  DB, models, existing candidates and sealed evaluation remain unchanged/unopened.

## Next qualification

After review, expose this isolated candidate to the same-agent native connection,
then run new fixed requests without expected-ID access during selection. Record
selected IDs, rejected hits, all discovery/fetch calls, answer support and unresolved
gaps; repeat batches three times without tuning. Compare reference evidence on the
same cases. Target90% fully supported covered requests each repeat, zero critical
condition/scope errors, with controls reported separately. Do not tune to this
author-visible twelve-case diagnostic or call reachability parity.
