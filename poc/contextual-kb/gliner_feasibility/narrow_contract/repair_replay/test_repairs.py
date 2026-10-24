import unittest
from repairs import repair
def row(text, specs):
 entities={}
 for kind,raw,n in specs:
  starts=[];start=0
  while True:
   at=text.find(raw,start)
   if at<0:break
   starts.append(at);start=at+1
  at=starts[n]
  entities.setdefault(kind,[]).append(dict(text=raw,start=at,end=at+len(raw)))
 return {'output':{'entities':entities}}
def run(text,specs,stage=3):return repair('q',text,row(text,specs),stage)['envelope']
class RepairsTests(unittest.TestCase):
 def test_quotes_exact_not_substring(self):
  text="key 'birch'"
  e=run(text,[('model_key','birch',0)],1)
  self.assertEqual(e['mentions'][0]['raw'],"'birch'")
  self.assertEqual(run(text,[('model_key','bir',0)],1)['mentions'][0]['raw'],'bir')
 def test_escape_parity(self):
  for text,raw in [(r"defaultValue 'Lee\'s'",r"Lee\'s"),(r"defaultValue 'x\\'",r"x\\")]:
   self.assertEqual(run(text,[('value',raw,0)],1)['mentions'][0]['raw'],text[13:])
 def test_apostrophe_unicode_backtick(self):
  text="🙂 user's key `'elm'`"
  e=run(text,[('model_key','elm',0)],1)
  self.assertEqual(e['status'],'ok');self.assertEqual(e['mentions'][0]['raw'],"'elm'")
 def test_api_path(self):
  text="rules['props.hidden']"
  e=run(text,[('api_reference','rules',0),('value','props.hidden',0)],2)
  self.assertEqual([(m['kind'],m['raw']) for m in e['mentions']],[('api_reference',text)])
 def test_no_cross_prose(self):
  text="rules and ['hidden']"
  self.assertEqual(run(text,[('api_reference','rules',0)],2)['mentions'][0]['raw'],'rules')
 def test_unsupported_path_review(self):
  for text in ('rules[getKey()]','rules[','rules()'):
   self.assertEqual(run(text,[('api_reference','rules',0)],2)['status'],'needs_review')
 def test_roles_by_occurrence(self):
  text="type 'oak' key 'oak' defaultValue false"
  e=run(text,[('value','oak',0),('api_reference','oak',1),('model_key','false',0),('value','false',0)])
  self.assertEqual([(m['kind'],m['raw']) for m in e['mentions']],
   [('registration_name',"'oak'"),('model_key',"'oak'"),('value','false')])
 def test_prose_and_path_not_assignment(self):
  for text in ("custom type 'oak'","other.key 'oak'","keyName 'oak'"):
   e=run(text,[('value','oak',0)])
   self.assertEqual(e['mentions'][0]['kind'],'value')
 def test_unresolved_conflict(self):
  e=run("Choose 'oak'",[('model_key','oak',0),('registration_name','oak',0)])
  self.assertEqual(e['status'],'needs_review');self.assertEqual(e['mentions'],[])
 def test_owned_payload(self):
  text="defaultValue 'key birch' key 'birch'"
  e=run(text,[('value','key birch',0),('model_key','birch',0),('model_key','birch',1)])
  self.assertEqual([(m['kind'],m['raw']) for m in e['mentions']],
   [('value',"'key birch'"),('model_key',"'birch'")])
 def test_unclosed(self):
  text="label string 'unfinished"
  e=run(text,[('value','unfinished',0)])
  self.assertEqual(e['status'],'needs_review');self.assertEqual(e['issues'][0]['start'],13)
 def test_empty_literal(self):
  self.assertEqual(run("defaultValue ''",[('value',"''",0)])['mentions'][0]['raw'],"''")
 def test_no_partial_unquoted_role_repair(self):
  e=run('defaultValue false',[('model_key','als',0)])
  self.assertEqual(e['mentions'][0]['raw'],'als')
  self.assertEqual(e['mentions'][0]['kind'],'model_key')
 def test_malformed(self):
  for r in (42,None,{'output':None}):
   self.assertEqual(repair('q','text',r,3)['envelope']['status'],'extraction_error')
 def test_order_confidence_idempotence(self):
  text="key 'cedar'"
  r=row(text,[('model_key','cedar',0),('value','cedar',0)])
  a=repair('q',text,r,3)['envelope']
  r['output']['entities']=dict(reversed(list(r['output']['entities'].items())))
  for v in r['output']['entities'].values():
   for m in v:m['confidence']=.001
  self.assertEqual(repair('q',text,r,3)['envelope'],a)
  specs=[(m['kind'],m['raw'],0) for m in a['mentions']]
  self.assertEqual(run(text,specs),a)
if __name__=='__main__':unittest.main()
