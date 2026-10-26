import unittest
from delivery import verify_calls

def event(kind, request='one', server='formly', tool='lookup_formly', item_id='c1', item_type='mcp_tool_call'):
 return {'type':kind,'item':{'id':item_id,'type':item_type,'server':server,'tool':tool,'arguments':{'request':request}}}
class DeliveryTests(unittest.TestCase):
 def test_valid_sequential_calls(self):
  self.assertEqual(verify_calls([event('item.started'),event('item.completed')],['one']),1)
 def test_rejects_extra_tool(self):
  with self.assertRaises(ValueError):verify_calls([event('item.completed',item_type='command_execution')],[])
 def test_rejects_wrong_server(self):
  with self.assertRaises(ValueError):verify_calls([event('item.started',server='other')],['one'])
 def test_rejects_reordering(self):
  with self.assertRaises(ValueError):verify_calls([event('item.started',request='two'),event('item.completed',request='two')],['one','two'])
 def test_rejects_parallel_start(self):
  with self.assertRaises(ValueError):verify_calls([event('item.started'),event('item.started',request='two',item_id='c2')],['one','two'])
 def test_rejects_missing_completion(self):
  with self.assertRaises(ValueError):verify_calls([event('item.started')],['one'])
 def test_rejects_extra_request_fields(self):
  row=event('item.started');row['item']['arguments']['extra']=True
  with self.assertRaises(ValueError):verify_calls([row],['one'])
if __name__=='__main__':unittest.main()
