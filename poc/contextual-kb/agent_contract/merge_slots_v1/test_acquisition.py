import unittest
from acquisition import acquire
class Index:
 def __init__(self):self.calls=[]
 def hybrid(self,q,k):self.calls.append(q);return list('abcdefgh') if q=='original' else list('zabcdefg')
CORE=dict(formly_questions=[dict(question='original',reason='request')],condition_bindings=[])
class TestAcquisition(unittest.TestCase):
 def test_shared_query_lists_only_acquired_once(self):
  idx=Index();r=acquire(idx,CORE,[dict(question_index=0,query='rewrite')])
  self.assertEqual(idx.calls,['original','rewrite']);self.assertEqual(set(r['packets']),{'foundation','current','protected'});self.assertEqual(r['packets']['foundation'],list('abcdefgh'))
 def test_identical_and_invalid_supplement_do_not_requery(self):
  for supp in ([dict(question_index=0,query='original')],[]):
   idx=Index();r=acquire(idx,CORE,supp);self.assertEqual(idx.calls,['original']);self.assertEqual(r['packets']['protected'],r['packets']['foundation'])
if __name__=='__main__':unittest.main()
