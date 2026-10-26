"""Read-only verification; writes a result receipt only in this run's outputs."""
import json,hashlib,sys,sqlite3
from pathlib import Path
HERE=Path(__file__).resolve().parent
POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from mcp_foundation.launcher import preflight,sha256
report=preflight();assert report['ok'],report
pins=json.loads((HERE/'test-output/freeze.json').read_text())
for name,expected in pins.items():assert sha256(POC/name)==expected,name
old=json.loads((HERE/'test-output/before/mcp_foundation/foundation.json').read_text())
for name,expected in old['files'].items():
 if name!='build/knowledge.sqlite':assert sha256(POC/name)==expected,name
before=json.loads((HERE/'test-output/before.json').read_text())
for name,expected in before.items():assert sha256(HERE/'test-output/before'/name)==expected,name
checks=0;calls=0
for f in (HERE/'test-output/stable-live').glob('r*-b*-candidate/mcp/audit/*.json'):
 d=json.loads(f.read_text())['result'];assert d['runtime']['db_unchanged'];calls+=1
 for check in d['runtime']['model_checks']:assert check['parameters_unchanged'];checks+=1
assert calls==24,calls
expected='3a2024cf5fc22c7fdd6e70020d3f7c5c82e0a56a4000bb90928043cd5b418a09'
assert sha256(POC/'build/knowledge.sqlite')==expected
result=dict(doctor=report,frozen_files=len(pins),prior_runtime_assets_unchanged=len(old['files'])-1,rollback_files_verified=len(before),live_calls=calls,model_checks=checks,installed_db_sha256=expected)
(HERE/'test-output/final-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
