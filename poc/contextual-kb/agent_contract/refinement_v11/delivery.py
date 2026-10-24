"""Encode structured first-response batches; never repair model text or semantics."""
import json


def serialize_batch(rows):
    """Serialize JSON-shaped records without semantic validation or filtering."""
    if not isinstance(rows, list):
        raise ValueError('Response batch must be a list')
    return json.dumps(rows, ensure_ascii=False, allow_nan=False, indent=2) + '\n'
