"""Exact occurrence comparisons: gains cannot hide suppressed correct mentions."""
def tokens(mentions):return {(m['kind'],m['start'],m['end'],m['raw']) for m in mentions}
def deltas(before,after,gold):
 b,a,g=map(tokens,(before,after,gold))
 return {k:[list(v) for v in sorted(values)] for k,values in dict(
  lost_correct=(b&g)-a,new_correct=(a&g)-b,removed_false=(b-g)-a,new_false=(a-g)-b).items()}
def overlaps(mentions):
 counts=dict(within_role=0,cross_role=0)
 for i,a in enumerate(mentions):
  for b in mentions[i+1:]:
   if a['start']<b['end'] and b['start']<a['end']:
    counts['within_role' if a['kind']==b['kind'] else 'cross_role']+=1
 return counts
def decision(byseed):
 if set(byseed)!={1701,1702}:return False
 for rows in byseed.values():
  if len(rows)!=2:return False
  if sum(r['invalid_after'] for r in rows)>=sum(r['invalid_before'] for r in rows):return False
  if any(r['lost_correct'] or r['new_invalid'] or r['accepted_after']<r['accepted_before']-1e-12 for r in rows):return False
 return True
