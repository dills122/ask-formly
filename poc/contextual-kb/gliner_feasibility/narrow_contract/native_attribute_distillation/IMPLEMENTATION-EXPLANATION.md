# Author explanation — after preliminary review

This checks one prerequisite for a later experiment: can the existing native role distribution supply a differentiable preservation term without modifying GLiNER or training a new head? It does not test whether distillation improves extraction.

The adapter lowers the same schema as earlier native attributes, calls public boundary encode and score_explicit_spans, selects seven qualified queries by exact role names, and applies the checkpoint's pair temperature. Test-only interception captures the existing private native attribute scorer's actual logits independently for parity. It is not a replacement runtime head. Native inference token mappings can be lists or dictionaries; an initial dict-only assumption failed before any update, was preserved in attempt-1-mapping-error.log and fixed with a RED→GREEN regression test.

Panel selection uses only authorized training gold features before teacher predictions: all roles, malformed families, repeated raw strings, padded to eight rows. Masking protects only correct teacher decisions above0.5. Wrong teachers remain represented in ordinary gold supervision, but contribute no preservation gradient. Missing correct coverage is reported; no model-dependent search is used to fill it.

The cache is detached JSON with exact occurrence/query identity and source, schema, tokenizer, installed implementation and teacher state hashes. Teacher is separately loaded, wholly frozen and eval; all teacher calls are no_grad. The optimizer references only student LoRA tensors. Full state hashes and repeated teacher outputs check more than trainable parameters alone.

The gradient check uses the same native supervised batch and perturbed student state for λ0 and λ1. It separately computes the KL gradient, then checks the combined gradient equals their sum. The subsequent three SGD steps minimize only the preservation term in dropout-free eval mode to test local descent. They do not simulate joint full training, and their cached-anchor improvement is not a generalization score. No learning-rate search or extra steps are allowed if this fixed check fails.

Only the disposable compatibility copies are saved at steps1/3. Teacher and all prior candidates stay frozen. A passed result would justify designing a separately reviewed full experiment; it would not authorize running one or imply adoption.
