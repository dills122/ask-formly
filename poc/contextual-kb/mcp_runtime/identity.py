"""Content-derived runtime identity, independent of SDK and release numbering."""
import hashlib
import json


def build_identity(manifest):
    fingerprint = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    runtime_id = manifest['id']
    return dict(runtime_id=runtime_id, runtime_sha256=fingerprint,
                build_id=runtime_id + '+' + fingerprint[:12],
                distribution='development-candidate', release=None)
