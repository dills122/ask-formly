"""Experimental exact-span verifier. No extraction, repair, or serving integration."""
import torch
from gliner2 import AttributeGroup

ROLES = ('api_reference', 'registration_name', 'model_key', 'value', 'version', 'ui_adapter')
QUERIES = ('boundary: complete',) + tuple('supported_role: ' + r for r in ROLES)


def align(text, offsets, start_mapping, end_mapping):
    """Keep caller order and identity; never snap unsupported character offsets."""
    if len(offsets) != len(set(offsets)) or any(
        type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text)
        for a, b in offsets
    ):
        raise ValueError('duplicate or invalid offset')
    def invert(mapping, shift):
        pairs = mapping.items() if isinstance(mapping, dict) else enumerate(mapping)
        return {v: k + shift for k, v in pairs}
    starts, ends = invert(start_mapping, 0), invert(end_mapping, 1)
    supported, unsupported, tokens = [], [], []
    for a, b in offsets:
        if a in starts and b in ends:
            supported.append((a, b)); tokens.append((starts[a], ends[b]))
        else:
            unsupported.append((a, b))
    return supported, unsupported, tokens


def schema(model):
    return model.create_schema().entities(['candidate']).entity_attributes({
        'boundary': AttributeGroup(['complete'], multi_label=True, threshold=.5, qualify_labels=True),
        'supported_role': AttributeGroup(list(ROLES), multi_label=True, threshold=.5, qualify_labels=True),
    })


def score(model, text, offsets):
    base = model.get_base_model() if hasattr(model, 'get_base_model') else model
    schemas, metadata = base._build_schema_dicts_and_metadata([schema(model)])
    batch = model.processor.collate_fn_inference([(text, schemas[0])], architecture='boundary', error_policy='raise')
    supported, unsupported, tokens = align(text, offsets, batch.start_mappings[0], batch.end_mappings[0])
    if not supported:
        return torch.empty((0, len(QUERIES))), supported, unsupported, (batch, metadata)
    encoded = base.encode(batch)
    ids = {q.role_name: q.query_id for q in encoded.query_layouts[0].queries if q.task_type == 'entities'}
    indices = torch.tensor(tokens, device=encoded.text_states.device).reshape(1, 1, -1, 2).expand(1, encoded.query_states.shape[1], -1, 2)
    z = base.score_explicit_spans(encoded, indices)[0, [ids[q] for q in QUERIES]].T
    return z / base.boundary_settings.pair_temperature, supported, unsupported, (batch, metadata)


def decide(logits):
    if logits.shape != (7,) or not torch.isfinite(logits).all():
        raise ValueError('seven finite logits required')
    p = logits.detach().sigmoid().tolist()
    roles = [r for r, v in zip(ROLES, p[1:]) if v >= .5]
    accepted = p[0] >= .5 and len(roles) == 1
    return dict(status='accepted' if accepted else 'unresolved', role=roles[0] if accepted else None,
                boundary_pass=p[0] >= .5, supported_roles=roles, probabilities=p)


def objective(logits, targets):
    if logits.ndim != 2 or logits.shape[-1] != 7 or logits.shape != targets.shape or logits.numel() == 0:
        raise ValueError('nonempty matching Nx7 tensors required')
    if not torch.isfinite(logits).all() or not torch.isfinite(targets).all() or not ((targets == 0) | (targets == 1)).all():
        raise ValueError('finite logits and binary targets required')
    return torch.nn.functional.binary_cross_entropy_with_logits(logits, targets)
