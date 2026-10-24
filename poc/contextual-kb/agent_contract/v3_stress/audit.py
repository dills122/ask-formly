"""Read-only byte verification of inherited manifests; never parse sealed cases."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
ROOT=POC.parents[1]
N=POC/'gliner_feasibility/narrow_contract'
def verify(manifest):
    data=json.loads(manifest.read_text())
    for name,expected in data.items():
        p=Path(name)
        if not p.is_absolute():p=ROOT/p if p.parts[0]=='poc' else manifest.parent.parent/p
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=expected:raise ValueError(f'Protected artifact changed: {p}')
    return len(data)
def audit():
    h=N/'verifier_harness/test-output'
    manifests=[ROOT/r['manifest'] for r in json.loads((h/'preflight-002/protected-after.json').read_text())]+[h/'final-freeze.json']
    manifests += [N/p for p in ['entailment_trial/test-output/final-freeze.json','verifier_shadow/test-output/final-freeze.json','verifier_evaluation/test-output/full-run-final-freeze.json','verifier_evaluation/test-output/sealed-preparation-freeze.json','verifier_diagnosis/test-output/final-freeze.json']]
    manifests += [HERE.parent/'refinement_v3/test-output/final-freeze.json']
    return {str(p):verify(p) for p in manifests}
if __name__=='__main__':print(json.dumps(audit(),indent=2))
