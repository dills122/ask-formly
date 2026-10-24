# Author explanation — focused attribute contrasts

## Purpose and scope

The previous native attribute run established trainability but failed operational reliability: one candidate selected value for a registration name and for an invalid combined API/value fragment. Rejection was weakest on merged assignments and clipped API paths. This round tests a bounded data intervention, not a new architecture or decoder. Both previous candidates and the original extractors remain unchanged.

## Data choices

The194 original questions and449 negatives are preserved exactly. The48 new questions explicitly contrast complete versus incomplete occurrences, whole opaque values versus interior fragments, and the same lexical spelling in different roles. The85 new negative spans are manually specified by text and occurrence index and reviewed as incomplete occurrences in their context. They do not form an inference allow-list or string classifier. For example a complete API `props` is positive while another occurrence inside `props.label` is negative. A complete opaque object is a positive value even when its interior property/value fragment is negative. Native transport checks all242 examples/534 negatives on both starting checkpoints.

## Candidate and runtime path

Candidates start from the corresponding previous native attribute epoch6 adapters, using fixed4epoch continuation and no fresh-guided selection. This retains the prior native qualified-query training and private native supplied-span force scorer unchanged. Existing source-pinned POC helpers are reused; no external project implementation or new library component is imported. Flat original extractor outputs remain the sole source of operational spans. Candidate inference can only resolve an identical-span conflict among its existing labels; it cannot change boundaries or nonconflicting mentions.

## Preservation and evaluation

The baseline phase reproduces both the original raw extractions and prior candidate scores/resolutions on all296 earlier questions; it also reproduces the old156 probe predictions. New fresh gold supplies no training input and no operational boundaries. After training, the336-question operational comparison is separate from supplied-span role/rejection audits.

The strict gate is intentionally asymmetric between original and prior candidate: original accepted metrics may not decline, while prior candidate correctness must be preserved but a previously unsafe structurally valid wrong record may revert to the original unresolved invalid record. That is reported as safe abstention, not a repair. Every such metric change is recorded. Both seeds still need at least one real correct operational repair, zero wrong resolutions, and preservation of every previously correct diagnostic probe. Full qualification remains separate and stricter.

## Checks and limits

Nine unit tests were written failing first and then passed; they cover occurrence identity, complete-value protection, missing/duplicate/ambiguous negative anchors, restoring unsafe prior outputs, losing correct mentions, invalid-to-valid wrong outcomes, and the both-model repair requirement. Both native compatibility checks pass. First/final saves reload exact parameter hashes and native outputs on training-only panels. Actual outcomes and all remaining failures will be recorded without tuning. The source-pinned private GLiNER API remains a feasibility limitation; this is not a public API stability or final-answer accuracy claim.
