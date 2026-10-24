"""Predeclared batching and paired improvement gate for this trial."""
import random
def chunks(count,seed,epoch):
 if count<=0:raise ValueError('positive dataset size required')
 order=list(range(count));random.Random(seed+epoch).shuffle(order)
 return [order[i:i+8] for i in range(0,count,8)]
def gate(checks):
 return len(checks)==2 and all(c['fresh_gain']>=.02-1e-12 and c['exact_gain']>=0
  and c['api_recall_gain']>=-1e-12 and c['adapter_precision_gain']>=-1e-12
  and c['empty_fp_gain']<=0 and not c['diagnostic_regressions'] and c['target_api_gain']>=.05-1e-12 for c in checks)
def rate(value):return 0.0 if value is None else value
