# Recovery efficiency follow-up

This follows the [excerpt/identity trial](excerpt-identity-followup.md). Changes stay in the isolated answer candidate. Facts, installed DB, default runtime and recipe storage are unchanged.

## Why the previous totals rose

The raw-call audit reconciles all 74 calls across the previous paired trial: 35→39 calls, 293,639→308,408 response-text bytes (+14,769), and 317,102→333,057 serialized result bytes (+15,955). All help, errors, discovery, facts and provenance are included. These bytes are not model tokens or JSON-RPC wire size.

| Case | Call delta | Text-byte delta | Interpretation |
| --- | ---: | ---: | --- |
| E01 hide/reset | +1 | +4,721 | Split fact fetch and different selected facts; not established waste |
| E02 inheritance/key | +2 | +8,134 | Useful recovery explained nested addressing missing from baseline |
| E03 hide audit | 0 | −8,868 | Smaller discovery page and narrower selected evidence |
| E04 inheritance audit | 0 | −11,431 | Different call mix and narrower help; one omitted-plan failure still occurred |
| E05 validation/Material | +3 | +20,830 | One omitted-plan failure plus additional retrieval, including useful K74 evidence |
| E06 key/defaults audit | −2 | +1,383 | Provenance batching saved calls; other response differences outweighed byte savings |

The two omitted-plan discovery calls are clearly avoidable recovery: 726 text bytes each, returning PLAN_REQUIRED. Their schema advertised plan as optional even though runtime validation required it. Their structured feedback incorrectly named lookup_formly as the next tool. The successful repairs supplied the original lookup plan. Those two calls explain only part of the total increase; treating all extra retrieval as waste would erase useful coverage.

E04 also re-requested a defaults record after acknowledging missing source text. Its batch included a repeated K71 excerpt (531 content bytes), but also new K70 guide text and distinct authored material. Removing the whole call would lose evidence. Shared evidence IDs do not erase per-fact provenance obligations.

Deterministic same-input probes separate some metadata overhead from changes in caller selection: the excerpt/identity change added 525 bytes to one unchanged-fact lookup and 900 bytes to one unchanged-citation provenance response. Full-format packets stayed byte-identical. A large provenance response crossed the batching threshold; its instruction-only initial response cannot be counted as a saving without retries. Fresh-session differences do not permit attributing the entire byte increase to metadata.

## Isolated fixes

Candidate `answer-response-v1+8eda6620a38c` makes discovery's plan required and non-null in the tool schema. Its description states that the complete original plan is required on every call; no conversation plan is saved. The server does not synthesize or weaken a plan.

For legacy direct calls or structurally valid plans needing refinement, feedback now points to discover_formly_candidates, retaining the original request, scope, question selector, focus and paging arguments while correcting the reported plan issue. Valid discovery responses remain unchanged.

Caller guidance now tracks source evidence alongside fact IDs. Reuse requires matching evidence ID, release and source location, and matching hash when supplied. Distinct authored quotations, offsets, applicability and other evidence may still require per-fact provenance. There is no server-wide seen-record cache, automatic suppression, ranking change or packet-layout rewrite.

## Deterministic validation

Twenty-four focused tests pass; the existing 348 source checks pass. Native SDK replay confirms that both historically repaired discovery requests return byte-identical results. Historical missing-plan requests still fail: now SDK schema validation returns isError=true with a 304-byte text error, rather than the older 726-byte needs_refinement packet. This is correct schema enforcement, not proof that a caller saves a call. The replay collector initially assumed every result was JSON; its failed attempt was retained, then its derived parser was corrected for expected plain SDK errors. No fresh caller was rerun.

The added help guidance increases the fixed help response from 8,220 to 8,739
text bytes. Successful lookup and provenance packets in the matched replay are
unchanged. The fix trades a small amount of guidance for a clearer contract;
it does not shrink evidence payloads or claim that all conversation tokens fall.

In-session diff inspection covered the schema, repair routing, selector preservation including question_index zero, unchanged valid discovery and continued delivery of distinct per-fact provenance. The previous independent engineering-review flow ended at 3/3; this work does not claim or restart another independent review instance.

## Fresh comparison

Four new questions, authored without reading runtime evidence or earlier answers, cover two ordinary requests and two source audits. Each runs once against frozen ff1f4cdf1a26 and updated 8eda6620a38c in a fresh Codex session. Prompts, requirements/rubric and stages are frozen; budgets remain eight non-help calls, two help calls and six local commands. Separate masked grading checks completeness, quotations, source gaps and legitimate recovery. Schemas can reveal the arm. Historical replay and fresh caller evidence are distinct. No Kiro IDE qualification or general efficiency rate is implied.

## Fresh results and remaining limits

All eight sessions completed. The updated arm had no missing-plan refinement
or SDK errors; baseline F02 had one in-band PLAN_REQUIRED response, then repaired
discovery directly without restarting lookup. Neither arm used a local parser
or exceeded the call budgets. The required schema fix eliminated the observed
omission in this small comparison, not a demonstrated universal error rate.

| Metric | Frozen ff1f baseline | Updated 8eda candidate |
| --- | ---: | ---: |
| Total calls | 33 | 30 |
| `needs_refinement` responses | 1 | 0 |
| SDK errors | 0 | 0 |
| Provenance tool calls | 4 | 2 |
| Explicit full-format fetches | 0 | 1 |
| Response text bytes | 335,568 | 372,953 |
| Serialized CLI result bytes | 361,919 | 402,121 |

Ordinary questions used 13→12 calls and 108,927→99,097 result bytes. Source audits
used 20→18 calls but 252,992→303,024 bytes. Overall bytes increased about 11%,
so fewer calls are not an overall payload-efficiency win.

The second cost audit traces the source-audit increase to discovery breadth.
F03 made three discovery calls in each arm, but candidate entries rose 40→66
(25→50 distinct) and discovery text grew by 20,794 bytes. F04 made three versus
four discovery calls, with 57→86 entries (34→70 distinct), adding 29,300 discovery
bytes. Continuation arguments differed only by the correct next offset. A later
refocus overlapped eight entries but added eighteen new IDs. These are valid
searches, not malformed requests or proof that all extra candidates were needed.
F04's full-format fetch retrieved four new fact IDs; it was not a repeated
complete-fact fetch. Plans and selections vary, so these numbers do not establish
that the contract change caused broader searches.

Masked grades were frozen before unmasking X as updated and Y as baseline.
Both arms pass F01, pass F02 and F04 with explicitly permitted source/state gaps,
and partially satisfy F03's callback-input requirement. Both discovered
`affirmative-consent-boundary`, whose control/value example supports a limited
callback-input statement, but did not fetch or use it. Complete callback
signatures and automatic sibling revalidation remain legitimate gaps; the
example does not establish a universal signature. No answer-quality regression
or unnecessary repeated full/provenance call was established. A bounded pass
does not mean every requested implementation excerpt was available.

One derived-measurement bug was also corrected: help's topic inventory was
mistakenly counted as complete delivered facts. Separate v2 collectors now
exclude it; F02's apparent three refetches become zero in both arms. All call
and byte totals are unchanged. Original frozen collectors and derived outputs
are retained, and raw sessions were not altered.

## Decision

Subsequent work: the [selection-first trial](selection-first-followup.md) tests
this priority with four new questions and a separate historical regression.
The measurements below remain the original recovery-contract trial's results.

The identified discovery-contract defect and misdirected repair action are
fixed in the isolated candidate. The audit does not justify dropping mixed
provenance calls, suppressing shared records globally, or forcing smaller pages
without checking required evidence. The next priority is selecting relevant
already-discovered evidence before expanding searches further, scored against
answer completeness and all returned bytes. Keep the candidate isolated: this
trial reduced calls and observed malformed recovery, but did not reduce overall
bytes or resolve the shared selection miss. Facts and DB remain unchanged, and
recipe storage stays deferred.

## Preservation

Raw audit ledgers, deterministic replays, stage manifests and caller evidence remain under ignored test-output/recovery-efficiency-v1/. Previous experiments and failures remain intact. Full maintenance is still blocked by the missing worktree compiler environment; source checks do not establish full installed-runtime qualification. Candidate remains isolated; facts and installed DB unchanged; recipes deferred.

All 144 protected paths, seven candidate source files, both 31-file staged
runtimes, fourteen frozen inputs, 56 raw files and eight masked sessions verified
unchanged after execution. The installed DB hash remains unchanged.
