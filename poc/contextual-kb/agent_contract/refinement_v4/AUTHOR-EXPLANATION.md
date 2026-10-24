# Author explanation

## Intent and plan
The previous candidate produced useful questions but missed ledger entries. The unambiguous case omitted an active no-substitution exclusion; six other graded omissions exposed an undefined boundary between requested operations and conditions. This candidate explicitly requires scenario transitions and controlling dependencies to be audited even when inside an operation. Bare operations/targets are not separate conditions. The purpose is auditable context, not an entity inventory.

## Approach
CONTRACT.md preserves v3 derivation/output sections, replaces only its shared-condition audit with LEDGER-RULES.md, and changes version heading. The source-first inventory and final exclusion check instruct the model to restore meaningful source excerpts into both ledger and applicable questions rather than rely on paraphrases. Same three-field schema; optional hints remain advisory. candidate.py selects this new prompt and reuses same-POC v3 structural parsing, validation and envelope functions unchanged. No detector, postprocessor, automatic retry, trained model, retrieval or DB wiring was added.

## Plan trace and files
PROTOCOL.md defined policy and gate before outputs. Tests were written first; red.txt retains missing-module failure, green.txt seven passes. These validate entry-point selection, verbatim user input, rejection cases, unchanged72 saved structures/hint projection, and explicitly show the old omission remains structurally valid. v3's original13 tests also passed unchanged. These tests do not prove the prompt fixed semantic omission.

An independent author saw v2 scope and ledger policy, not v4 prompt/old cases/outputs, and authored12 fresh requests/rubrics. Parent inspected them before generation and explicitly added the F01 conditional-existence ledger expectation, already part of its requested aspect. data-review.md records that pre-generation adjustment. Four old diagnostics have new explicit v4 rubrics; no old evidence was edited. Input freeze covers15 artifacts. Six fresh-context native agents receive only their packet (full contract/eight requests), three repeats per batch,48 outputs. No response feedback or output repair is allowed. Output freezing/structural scoring precede independent semantic review.

preserve.py reuses the prior byte-only audit and includes v3_stress final-freeze46. All writes are in this new directory, no staging/commits. Main has unrelated dirty work. Existing baselines,A,v2,v3,DB and evaluation are protected; sealed evaluation bytes may be hashed but cases are not inspected.

## Tradeoffs and limits
This is a prompt-level fix, not mechanically guaranteed completeness. The ledger still depends on model interpretation and semantic review. More explicit instructions increase prompt size and may cause copying verbosity or overbinding; fresh cases test those risks. No empirical accuracy gain over a contemporaneous v3 arm is claimed: old v3 outputs serve diagnostics only.16 requests, including12 fresh, are a bounded synthetic development panel; repeats are correlated, and each batch shares context. Native inherited model configuration lacks pinned provider revision,temperature,seed and production API latency measurement. Fresh-context roles are not independent vendors. No final-answer or retrieval qualification follows from planning scores.

## Review challenge points
Check every active exclusion and its attachment, including quoted/retracted restrictions and empty plans. Audit scenario transitions and dependency relationships under the predeclared policy, not the old ambiguous one. Check requested aspects and search meaning did not regress. Mandatory rubric examples are examples, not unique spans; equivalent meaningful source excerpts/combined bindings allowed. Do not turn a passing structural check into a semantic claim. Retain failed outputs even if they prevent candidate gate success. Verify protected/inputs/raw hashes and all output denominators.
