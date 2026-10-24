"""Matched sample schedules; distillation coefficient is the sole arm difference."""
import random
LAMBDA={'control':0.,'treatment':100.}
def cycle(seed,count,total):
 rng=random.Random(seed);result=[]
 while len(result)<total:
  x=list(range(count));rng.shuffle(x);result.extend(x)
 return result[:total]
def schedule(seed):
 ids=cycle(seed,242,992);return [ids[i:i+8] for i in range(0,992,8)]
def anchor_schedule(seed):
 ids=cycle(seed+50000,194,248);return [ids[i:i+2] for i in range(0,248,2)]
def anchor_weights(counts):
 available=sum(c>0 for c in counts)
 return [1./available if c>0 else 0. for c in counts]
def penalty(raw_kl,arm):return raw_kl*LAMBDA[arm]
