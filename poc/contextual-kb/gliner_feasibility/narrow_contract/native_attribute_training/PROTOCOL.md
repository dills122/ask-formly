# Native span-attribute training experiment

Scope: isolated new adapters only. Existing role_boundary_adaptation after-1701/1702 epoch-6 extractors, A, agent v2 and all knowledge/DB/retrieval code remain frozen. No spaCy component.

## Verified native mechanism

Installed GLiNER `InputExample` has no attribute-training field. `Schema.entity_attributes` lowers qualified attributes into entity query labels, such as `target_role: registration_name`. We supervise those exact native span queries through supported InputExample offset dictionaries, including all seven labels in every example (absent labels have empty targets). This uses native boundary entity losses, not document classification or a new attribute cross-entropy head. Inference applies a native softmax over attribute span logits; the training loss itself is not that softmax.

The 194 existing training questions remain the only training questions. Valid gold occurrences train their six-role extraction query and qualified role query. Deterministic malformed training candidates train `target_role: no_entity`: broken quotes, dotted-path fragments, nested opaque fragments and adjacent merged different-role spans, at most four per question. They do not become positive content entities. A negative is an invalid complete occurrence under this contract, not a forbidden string. Gold exact offsets are never negative. Every input query, including absent labels, and every target offset is checked after native collation without containment deduplication. No old evaluation text influences negatives.

Official source references: https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/13-span_attributes.md ; installed gliner2/inference/schema.py, training/data.py, models/boundary/engine.py. The source tutorial documents retained-span attribution; the training transport above is an inspected and tested lowering, not a documented first-class attribute-training API.

## Candidate occurrence scoring

The frozen extractor remains the sole source of operational spans. A thin POC adapter calls GLiNER's native `_attach_entity_attributes` force-scoring routine on those exact occurrences, using the same schema and encoder as public `entity_attributes`. No third-party code is copied or edited. Smoke comparison must demonstrate equivalent labels/confidence at spans retained by public inference. This private API dependency is explicitly version/source-pinned and is a feasibility limitation.

Operational resolution only removes losing roles for an identical-span cross-role conflict when one candidate role wins at confidence >0.5. Partial overlaps, unaligned boundaries, low-confidence predictions, an unsupported role, and predicted no_entity retain the entire original raw output as unresolved. No_entity is recorded separately from abstention; deletion is never used to manufacture validity. Nonconflicting spans cannot change. Supplied gold and malformed probe offsets are a separate role/rejection audit, never operational resolver input.

## Fixed training

Two candidates start from the corresponding frozen extractor adapters (1701 and 1702). Six fixed epochs over all194 training questions, shuffled with seed+epoch; AdamW learning rate0.0001, weight decay0.01, gradient clipping1, serial accumulation8 (last chunk2),25updates/epoch,150total. Existing LoRA configuration only, CPU float32,4threads, deterministic. All base parameters frozen. No model selection, schema tuning or thresholds changed after fresh data exposure. First-save at epoch1 and final epoch6 verify exact parameter and native role-prediction equality after reload on training-only examples. Preserve all raw outputs before scoring.

## Testing and decision

Before training, capture both frozen extractors on40 independently authored fresh questions plus all256 prior diagnostics; confirm prior raw outputs match. Both candidate role scorers are assessed before/after, plus independently authored supplied valid/malformed probes. No old sealed evaluation is read.

Improvement requires BOTH seeds: at least one correctly resolved previously conflicting occurrence; zero correct occurrences lost; zero nonconflicting modifications; zero accepted precision/recall/F1 decrease on any split; no increase in invalid outputs; zero invalid-to-valid-but-wrong outputs. Report unresolved counts, learned no_entity, low-confidence abstentions and unaligned cases separately. Malformed probe rejection precision/recall and valid-span role accuracy/acceptance recall are separate; absence or low confidence is not learned rejection. Undefined precision is reported as undefined and treated as zero for the no-decrease gate when previously defined. Full qualification additionally retains at least90% precision/recall for every nonempty role, zero invalid/runtime outputs and zero critical quoted/compound boundary misses, and requires zero wrong resolutions and at least90% malformed rejection recall with zero valid spans rejected, across both models. Improving diagnostics is not general qualification or final-answer accuracy.

Fresh40 and probe gold are authored independently before model output and remain excluded from training. Previous exposed cases remain diagnostics. One independent review of compatibility/protocol precedes full training; same reviewer audits final receipts, all changed outcomes and verdict.
