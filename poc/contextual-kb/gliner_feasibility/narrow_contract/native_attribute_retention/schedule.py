"""Fixed paired sample schedule; all indices address training-only rows."""
import random

def schedule(seed, arm):
 if arm not in ('control','treatment'):raise ValueError('unknown arm')
 rng=random.Random(seed);replay=[];contrast=[]
 while len(replay)<992:
  cycle=list(range(194));rng.shuffle(cycle);replay.extend(cycle)
 while len(contrast)<124:
  cycle=list(range(194,242));rng.shuffle(cycle);contrast.extend(cycle)
 return [[(replay[step*8+i],1.) for i in range(7)]+[(replay[step*8+7],1.) if arm=='control' else (contrast[step],.25)] for step in range(124)]

def weighted_loss(native_loss, weight, batch_size):
 return native_loss*weight/batch_size
