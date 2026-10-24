"""Read-only byte checks of inherited protected paths; no data inspection."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
prior=HERE.parent/'vocabulary_adaptation'
records=json.loads((prior/'test-output/protected-after.json').read_text())
paths=[Path(r['manifest']) for r in records]+[prior/'test-output/final-freeze.json']
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
results=[]
for manifest in paths:
 hashes=json.loads(manifest.read_text());changed=[]
 for name,expected in hashes.items():
  path=Path(name)
  if not path.is_absolute():path=manifest.parent.parent/path
  if digest(path)!=expected:changed.append(str(path))
 results.append(dict(manifest=str(manifest),checked=len(hashes),changed=changed))
with (HERE/'test-output/protected-after.json').open('x') as f:json.dump(results,f,indent=2)
print('checked',sum(r['checked'] for r in results),'changed',sum(len(r['changed']) for r in results))
if any(r['changed'] for r in results):raise ValueError('protected files changed')
