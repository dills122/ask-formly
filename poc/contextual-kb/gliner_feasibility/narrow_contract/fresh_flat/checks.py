"""Identity, grounding and coverage checks for fresh evaluation only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'pilot'))
from contract import validate

def validate_inputs(rows,families,previous):
 ids=[r['question_id'] for r in rows];questions=[r['question'] for r in rows]
 if len(set(ids))!=len(ids) or len(set(questions))!=len(questions):raise ValueError('duplicate identity/question')
 if set(ids)!=set(families):raise ValueError('family coverage')
 if set(questions)&{r['question'] for r in previous}:raise ValueError('reused question')
 for row in rows:
  validate(row,row['question_id'],row['question'])
  if row['status']!='ok':raise ValueError('clear cases only')

def validate_predictions(gold,predictions):
 ids=[r['id'] for r in predictions]
 if len(ids)!=len(gold) or len(set(ids))!=len(ids) or set(ids)!={r['question_id'] for r in gold}:raise ValueError('prediction coverage')
