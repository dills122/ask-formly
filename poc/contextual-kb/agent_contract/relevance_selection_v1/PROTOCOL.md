# Candidate depth and semantic selection — fixed development experiment

Authorization: the user explicitly requested testing candidate retrieval and relevance-based selection together. This isolated harness is an authorized extension of the older question-only steering scope; no serving code, existing candidate, model, knowledge data, DB, or index is modified. Only this new directory is writable. All imports are within this POC or installed standard/third-party libraries. Evaluation remains sealed; byte hashes only.

## Design, frozen before generation/retrieval

36 fresh realistic Formly requests, three batches of twelve, generated once through the frozen qualification_v3 foundation contract in separate native contexts. Retain every failed delivery/plan; no repairs or retries. These are fresh wordings over the existing bounded catalog, not unseen topics or a sealed evaluation. The author does not generate expected IDs. A fresh-context preflight reviewer labels source requests against the unchanged 46-fact catalog and reviews plan semantics BEFORE retrieval or selection.

Four arms separate acquisition from selection:
- foundation: exact existing hybrid(query,8), then merge_obligations(...,8).
- wide_rank: existing hybrid(query,20) for every identical foundation query. Append any original top8 IDs missing from each depth20 list, then existing merge into eight. No extra generated search terms or links.
- narrow_select: relevance selection from the union of original per-question top8 lists.
- wide_select: identical relevance selection from union of depth20 and original lists.

Depth20 is fixed now, no sweep. The engine fuses lexical/dense lists at the supplied depth, so depth20 is NOT assumed to have depth8 as a prefix. Explicitly retaining the original candidates isolates selection losses and prevents accidental candidate removal. Actual narrow and wide calls are separately acquired once; all arms share their saved lists. No pool exceeds the existing catalog and no absent fact is injected.

Selection uses a fresh native agent context per batch AND arm, supplied only the frozen selector contract, foundation questions/conditions and retrieved fact claims/conditions/limits/version/adapter. Candidate IDs are opaque handles sorted by a stable hash, with no retrieval rank or gold. It outputs up to eight ordered handles with short relevance rationales. Zero IDs is valid when nothing materially helps; partial support may be selected without claiming full answerability. No external knowledge, search, library instruction or invented fact is permitted. All first submissions are retained. Native inference is a feasibility test, not a pinned deployed model or latency benchmark. No GLiNER inference/training occurs.

## Accounting and gates

Gold: relevant_fact_ids and required_groups (alternatives allowed) for each original request. Unsupported cases have neither. Prospective semantic review separately checks foundation coverage/conditions; structural passes alone do not prove meaning.

Report all arms at4 and8: macro relevant-fact recall, precision@k (fixed k denominator even if fewer selected), nDCG, MRR, complete required groups, required-group recall, unsupported candidate exposures, packet size and selected-fact precision. Include per-batch results, paired relevant facts lost/gained against foundation, group losses, and candidate-pool available recall. Report literal failures and selection validation failures; invalid selection produces an empty packet, never repairs/fallback that hides it.

The joint wide_select arm qualifies only if: no structural/runtime/delivery/semantic failures; no relevant foundation fact lost at8 on any supported request; no complete-group loss; unsupported exposures do not increase; pooled recall improves by >=0.5 percentage points; precision@8 does not decrease; no batch recall regression; every batch and pooled recall >=89.25% (90% target separately). Thresholds are prospective, not a claim that these small batches estimate population performance to ±0.75pp. Ablations are diagnostic, not independently promoted. Report all failures, including a plausible benefit that fails the strict preservation gate.

Index setup and actual query acquisition wall time are measured separately. Selector input/output bytes and batch wall time are recorded, including tool and scheduling overhead; do not report that as model inference latency. No final-answer accuracy or abstention correctness claim from packet metrics.

## Execution and review

TDD for acquisition, opaque candidate presentation, selection validation and comparison/gates. Freeze protocol, requests and selector contract before generation; freeze code, gold, semantic review and transitive inputs before retrieval. Freeze acquisition before selection; freeze first selections before scoring. Preserve first-source hashes. Up to3 independent reviews total: prospective implementation/labels, completed evidence, material-fix review only if required. Independent review must reconstruct raw results and verify preservation. Do not tune based on qualification results.
