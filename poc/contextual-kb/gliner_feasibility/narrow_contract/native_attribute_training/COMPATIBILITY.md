# Native attribute compatibility findings

Installed package: gliner2 2.1.0; checkpoint architecture: boundary (`gliner2.5-base-v1`). Package source files and prior checkpoints are included in the immutable run manifest. No package edits or new dependency were required.

The supported `InputExample` format does not expose an attribute field. Native schema construction lowers `entity_attributes` to qualified entity queries. This experiment uses supported exact-offset entity annotations with those identical qualified names to train the same native boundary scorer. All seven attribute queries are present in every record, with explicit empty lists for absent roles. The native boundary objective supervises spans; inference normalizes the attribute logits with softmax. This is not a newly implemented classification head and not a document classifier.

## Evidence before full training

- Exact roundtrip and native target checks pass for194 original training questions and449 generated malformed span targets, on both frozen checkpoints. Ordinary six-role targets are retained for replay; malformed spans are positive only for the qualified no_entity query.
- A qualified-query-only loss test has zero ordinary extraction queries. Swapping no_entity and registration span targets changes native loss262.9623→149.1192 and changes nonzero gradient tensors. Thus total-loss backpropagation is not merely updating original entity extraction.
- Two real train-only optimizer updates change202 LoRA parameters and native attribute predictions. After saving/reloading, predictions and parameter hashes are identical. The initial unsorted-query smoke is retained as provenance; `ordered-smoke` is the final smoke matching native schema query order.
- Both frozen models agree between public native attribution and the exact supplied-span helper on57 returned mentions, covering all six source roles. Repeated identical `'badge'` occurrences in different roles receive distinct contextual scores; their exact targets survive transport separately. This establishes occurrence conditioning, not correct role selection before training.
- Six unit tests cover exact offsets, absent queries, malformed/gold separation, same-span-only resolution, partial-overlap preservation, and retaining raw output on no_entity.

## Private API limitation

The public API attributes retained detected entities. It does not expose a public supplied-span classifier. `native.supplied` calls the existing `_attach_entity_attributes` routine on exact frozen-extractor offsets, after native schema encoding. The routine itself invokes native `score_explicit_spans`. This is a small pinned private-API adapter, not a claim of stable public API support. No library implementation was copied, and no new head/loss was invented.

Unrepresentable token boundaries are reported as `unaligned`, never semantic no_entity predictions. A semantic no_entity prediction also retains the original operational raw output as unresolved. The separate gold/malformed supplied-span audit never supplies boundaries to the operational resolver.

Primary source: [GLiNER span attributes](https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/13-span_attributes.md). Local inspected paths: `gliner2/inference/schema.py`, `training/data.py`, and `models/boundary/engine.py` in the frozen POC environment. The exact attribute training lowering is source-inspected and experimentally verified; the tutorial itself primarily documents inference.
