"""Independent read-only retained-evidence check; no inference or generation."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
for name in ('harness-freeze.json','protected-before.json'):
 manifest=read(R/'test-output'/name)
 for p,h in manifest.items():
  if isinstance(h,str): assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h,p
for name in ('wording_candidate_v1','retrieval_repair_v1'):
 for p,h in read(R.parent/name/'test-output/final-freeze.json').items():assert hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==h,p
selector=[]
for p in R.glob('test-output/**/selector/*/events.jsonl'):
 events=[json.loads(s) for s in p.read_text().splitlines()]
 assert events[-1]['type']=='turn.completed',p
 msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 assert len(msgs)==1 and json.loads(msgs[0])==read(p.parent/'decision.json'),p
 assert all(e['item']['type'] in ('agent_message','reasoning') for e in events if e.get('type')=='item.completed'),p
 receipt=read(p.parent/'receipt.json'); assert receipt['exit_code']==0 and receipt['error'] is None,p
 assert events[-1]['usage']['input_tokens']>0 and events[-1]['usage']['output_tokens']>0,p
 selector.append(str(p.relative_to(R)))
assert len(selector)==10,len(selector)
for seed in (1701,1702):
 root=R/f'test-output/native/{seed}'; events=[json.loads(s) for s in (root/'events.jsonl').read_text().splitlines()]
 assert events[-1]['type']=='turn.completed'
 calls=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='mcp_tool_call']
 assert len(calls)==4
 assert all(e['item']['type'] in ('mcp_tool_call','agent_message','reasoning') for e in events if e.get('type')=='item.completed')
 assert len(list((root/'runtime/planner').glob('*/receipt.json')))==4
 for call in calls:
  packet=call['result']['structured_content']; generation=packet['generation']; job=root/'runtime/planner'/generation['attempt_id']
  es=[json.loads(s) for s in (job/'events.jsonl').read_text().splitlines()]
  raw=[e['item']['text'] for e in es if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  assert len(raw)==1 and json.loads(raw[0])==generation['wording_normalization']['original_plan']
  assert es[-1]['type']=='turn.completed' and read(job/'receipt.json')['exit_code']==0
print(json.dumps({'pass':True,'selector_events_verified':len(selector),'fresh_planner_events_verified':8,'caller_batches_verified':2,'direct_manifest_hash_checks':'passed'},indent=2))
