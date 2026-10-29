# Answer response and separate provenance experiment

This isolated experiment follows the [large JSON audit](large-json-response-audit.md). It tests response delivery using unchanged 192-fact knowledge, without promoting a new default, installing a package or changing recipe storage.

The results below retain the original candidate and its limitations. The
[excerpt and identity follow-up](excerpt-identity-followup.md) records subsequent
candidate fixes and a separate fresh-caller comparison.

## Candidate contract

The new `poc/contextual-kb/answer_response_v1/` server wraps the source16 model-free service. Lookup retains the baseline selection/ranking and complete selected fact objects. Initial responses retain claims, context, conditions, limits, applicability, related targets and short evidence citations with stable source URLs/paths/lines. They explicitly mark detailed provenance as deferred.

`get_formly_provenance` accepts fact IDs and explicit resolved version/adapter and returns exact original citation records. Source quotations, excerpts, hashes and authored offsets remain available there. An authored summary is not an implementation quotation; missing source excerpts stay missing. Ordinary answers may cite initial references without claiming to have inspected detailed source evidence.

Both fetch paths validate all IDs and scope before delivery, preserve 28 KB packet/30 KB MCP bounds, and return measured retry batches when necessary. Explicit compact/full fact fetch remains available. Lookup still uses the baseline byte-based selection before projection, so this prototype does not establish greater retrieval capacity.

The candidate is separate from the installed launcher and manifest. Its identity hashes selected candidate/baseline files, not every actual transitive dependency. Complete staged-file hashes and baseline pin verification, rather than that identity alone, bind the caller experiment. Full dependency identity hardening is required before promotion.

## Fixed-packet comparison

All selected fact objects and original provenance records rejoined exactly. These are deterministic packet comparisons, separate from caller quality or call-count results. UTF-8 JSON bytes:

| Facts | Baseline response | Answer response | Answer plus all provenance |
| ---: | ---: | ---: | ---: |
|1|2,946 compact|2,488|4,486|
|10|26,442 compact|16,656|34,753|
|16|38,724 full|23,478|49,595|

The initial larger responses shrink roughly 37–39%, but fetching all provenance costs more total bytes than the original response. Selectivity is essential; a smaller initial response alone does not establish lower journey cost. MCP envelopes were measured separately in the retained probe receipts.

## Fresh caller protocol

Six questions were generated without reading facts, runtime code or previous answers: four ordinary development questions and two explicit source audits. Each runs once against baseline and candidate in a fresh Codex CLI session, with the same prompt per pair. Callers may use local parsing on returned evidence but receive no parser recommendation. The budget is eight non-help calls, two help calls and six local commands. No quality reruns.

Questions, essential/optional rubric, prompts and runtime hashes are frozen before calls. Grading accepts explicit evidence gaps and does not treat authored prose as an implementation excerpt. Ordinary source links do not automatically require a detailed provenance call. The comparison tracks all response bytes, total calls, provenance requests, repeated retrieval, observed parsing and answer quality. This is bounded Codex evidence, not Kiro IDE qualification.

## Caller cost results

All twelve sessions completed without tool errors, budget excesses, local parser
commands or quality retries. Totals include help and separate provenance calls.
Bytes are measured response text and serialized MCP result envelopes, not model
tokens or observed model-visible context.

| Metric | Baseline | Candidate |
| --- | ---: | ---: |
| All calls | 26 | 26 |
| Non-help calls | 20 | 22 |
| Help calls | 6 | 4 |
| `get_formly_provenance` calls | 0 | 3 |
| Response text bytes | 350,943 | 279,191 |
| Response-envelope bytes | 374,258 | 299,985 |
| Largest response text | 27,972 | 21,624 |

The candidate used 19.8% fewer envelope bytes overall. Ordinary questions used
253,358 versus 197,402 bytes (22.1% lower), with seventeen calls in each arm and
no candidate provenance calls. The two source-audit questions used 120,900 versus
102,583 bytes (15.2% lower), with nine calls in each arm. The latter includes all
three candidate provenance calls and their 22,854 envelope bytes.

The savings are not uniform. N01 needed an additional call for only a small byte
reduction; N06 needed one additional call and saved less than 1% of envelope
bytes. Candidate non-help calls rose by two while help calls fell by two. These
single paired runs show smaller responses without a total-call improvement;
they do not prove a general causal reduction in recovery or discovery work.

## Answer quality and remaining work

The independent grader froze judgments before unmasking X as candidate and Y as
baseline. Both arms supported 20 of 22 required decisions. The remaining two
were explicitly bounded source gaps in N06: literal implementation quotations
and the complete Material rendering connection. All ordinary required decisions
were satisfied. Neither arm invented missing source passages. All final source
URLs matched delivered pinned records. Baseline N02 dropped a truthy condition
in optional precedence advice; this was recorded separately from required
decision coverage. Distinguishable response schemas limit the masking.

The smaller response did not create an observed answer-quality regression in
these six pairs. It also did not fill the existing source-evidence gaps. Callers
correctly distinguished authored notes from implementation quotations.

N06 still exposes unnecessary recovery: both callers eventually retried already
delivered facts in full format without obtaining the missing excerpts. The
candidate repeated four facts and baseline three. These were reasonable attempts
under incomplete guidance, but redundant in outcome. The next response-contract
improvement should explicitly identify whether an implementation excerpt exists
and explain that changing representation cannot retrieve absent source text.
This is metadata/guidance work, not permission to add or alter facts.

The metrics' three provenance calls count the new named tool. The grader also
classifies candidate N06's full fact retry as provenance-seeking work (four such
calls total); baseline N06's full retry serves the same purpose. All those calls
and bytes are already included in journey totals.

Keep the candidate isolated pending that stopping-guidance improvement, complete
dependency identity hardening and a further fresh comparison. The results support
the direction, but do not establish an optimal response format, universal size
threshold, Kiro IDE compatibility or reduced total call count. Existing full
evidence delivery remains the default.

## Preservation and evidence

Code lives in the isolated candidate directory. Raw inputs, packets, frozen sessions and review evidence live in ignored `test-output/answer-response-v1/`. Current facts, installed DB, existing runtime and source16 manifest stay unchanged. Recipe storage remains deferred.

All 144 protected paths, complete stage pins, frozen question/runtime inputs,
84 raw result files and twelve masked session sets verified unchanged. Ten
candidate fixture tests and native stdio answer/provenance checks pass. Review
instance 1 found the dependency identity limitation described above and judged
the hash-bound experiment ready with that non-blocking follow-up. Two SDK
preflight harness failures from passing uppercase `Material` instead of returned
resolved `material` are retained; no caller was rerun because of answer quality.

The existing 348 source checks pass. Full `python3 tools/project.py check` remains blocked by the missing worktree compiler environment, so source checks do not establish full runtime qualification.
