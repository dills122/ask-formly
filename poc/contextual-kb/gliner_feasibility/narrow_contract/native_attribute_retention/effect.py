"""Paired correctness contrast; abstention never equals learned no_entity."""
def selected(prediction):
 return prediction['label'] if prediction['status']=='scored' and prediction['confidence']>.5 else None

def superiority(rows):
 return all(any(r['seed']==seed and r['fresh'] and not r['before_correct'] and r['after_correct'] for r in rows) and not any(r['seed']==seed and r['before_correct'] and not r['after_correct'] for r in rows) for seed in (1701,1702))
