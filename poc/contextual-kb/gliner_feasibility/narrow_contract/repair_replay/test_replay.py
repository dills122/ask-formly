import unittest
from replay import stats
class MetricTests(unittest.TestCase):
 def test_review_mentions_not_accepted(self):
  r={'envelope':{'mentions':[dict(kind='value',start=0,end=1,raw='0')],'status':'needs_review','issues':[]}}
  g={'mentions':[dict(kind='value',start=0,end=1,raw='0')],'status':'ok','issues':[]}
  out=stats([(r,g)])
  self.assertEqual(out['diagnostic']['all']['tp'],1)
  self.assertEqual(out['accepted']['all']['fn'],1)
  self.assertEqual(out['exact'],0)
 def test_failed_empty_is_not_exact(self):
  r={'envelope':{'mentions':[],'status':'extraction_error','issues':[]}}
  g={'mentions':[],'status':'ok','issues':[]}
  self.assertEqual(stats([(r,g)])['exact'],0)
if __name__=='__main__':unittest.main()
