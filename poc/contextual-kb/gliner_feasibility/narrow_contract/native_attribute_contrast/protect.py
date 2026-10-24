"""Byte-hash protected artifacts; never rebuild or inspect knowledge contents."""
import json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def main():
 prior=HERE.parent/'native_attribute_training/test-output'
 manifests=[ROOT/r['manifest'] for r in json.loads((prior/'protected-after.json').read_text())]
 manifests.append(prior/'final-freeze.json');report=[]
 for manifest in manifests:
  data=json.loads(manifest.read_text());changed=[]
  for name,expected in data.items():
   p=Path(name)
   if not p.is_absolute():p=ROOT/p if p.parts[0]=='poc' else manifest.parent.parent/p
   if not p.exists() or digest(p)!=expected:changed.append(str(p))
  report.append(dict(manifest=str(manifest.relative_to(ROOT)),checked=len(data),changed=changed))
 with (HERE/'test-output/protected-after.json').open('x') as f:json.dump(report,f,indent=2)
 print('protected',sum(r['checked'] for r in report),'changed',sum(len(r['changed']) for r in report))
 if any(r['changed'] for r in report):raise ValueError('protected mutation')
if __name__=='__main__':main()
