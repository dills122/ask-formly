"""Trained occurrence typing using spaCy's public span categorizer API.
Sources: https://spacy.io/api/spancategorizer and https://spacy.io/api/doc#char_span
"""
import json,random,sys,time
from pathlib import Path
import spacy
from spacy import registry
from spacy.tokens import Doc
from spacy.training import Example
from spacy.util import fix_random_seed,minibatch
from thinc.api import Ragged
from policy import ROLES,select
HERE=Path(__file__).resolve().parent;OUT=HERE/'test-output'
if not Doc.has_extension('role_candidates'):Doc.set_extension('role_candidates',default=None)
@registry.misc('formly_occurrences.v1')
def make_suggester():
 def suggest(docs,ops=None):
  spans=[];lengths=[]
  for doc in docs:
   pairs=doc._.role_candidates or [];spans.extend(pairs);lengths.append(len(pairs))
  return Ragged(ops.asarray2i(spans).reshape((-1,2)),ops.asarray1i(lengths))
 return suggest

def candidates(doc,offsets):
 good=[];failed=[]
 for a,b in offsets:
  span=doc.char_span(a,b,alignment_mode='strict')
  if span is None:failed.append((a,b))
  else:good.append((span.start,span.end))
 return good,failed

def decision(labels,vector):
 if len(vector)!=len(labels)+1:return None
 return select(dict(zip([*labels,'no_entity'],map(float,vector))))

def predict(nlp,question,offsets):
 doc=nlp.make_doc(question);pairs,failed=candidates(doc,offsets);doc._.role_candidates=pairs
 indices,scores=nlp.get_pipe('spancat_singlelabel').predict([doc]);rows=[]
 for pair,vector in zip(indices.data,scores):
  span=doc[int(pair[0]):int(pair[1])]
  rows.append(dict(start=span.start_char,end=span.end_char,text=span.text,scores=dict(zip([*nlp.get_pipe('spancat_singlelabel').labels,'no_entity'],map(float,vector))),selected=decision(nlp.get_pipe('spancat_singlelabel').labels,vector)))
 return dict(rows=rows,alignment_failures=failed)

def train():
 fix_random_seed(1701);nlp=spacy.blank('en');pipe=nlp.add_pipe('spancat_singlelabel',config={'suggester':{'@misc':'formly_occurrences.v1'},'spans_key':'roles'})
 for role in ROLES[:-1]:pipe.add_label(role)
 rows=json.loads((HERE.parent/'role_boundary_adaptation/test-output/train.json').read_text());examples=[];alignment=[];counts={'positive':0,'negative':0};corpus=[]
 for row in rows:
  doc=nlp.make_doc(row['question']);ref=nlp.make_doc(row['question']);spans=[];pairs=[]
  for m in row['mentions']:
   s=ref.char_span(m['start'],m['end'],label=m['kind'],alignment_mode='strict')
   if s is None:alignment.append(dict(id=row['question_id'],mention=m));continue
   spans.append(s);pairs.append((s.start,s.end));counts['positive']+=1
  # All one-token spans wholly outside every annotated mention are negatives.
  negative=[(t.i,t.i+1) for t in doc if not t.is_space and not any(t.idx<m['end'] and m['start']<t.idx+len(t) for m in row['mentions'])]
  counts['negative']+=len(negative);pairs=sorted(set(pairs+negative));doc._.role_candidates=pairs;ref.spans['roles']=spans
  examples.append(Example(doc,ref));corpus.append(dict(id=row['question_id'],candidates=pairs,positive=[(s.start,s.end,s.label_) for s in spans]))
 write('training-candidates.json',corpus);write('training-alignment.json',alignment);write('spacy-config.json',dict(nlp.config))
 optimizer=nlp.initialize(lambda:examples);losses=[]
 for epoch in range(30):
  order=list(range(len(examples)));random.Random(1701+epoch).shuffle(order);loss={}
  for batch in minibatch(order,size=8):nlp.update([examples[i] for i in batch],sgd=optimizer,drop=.1,losses=loss)
  losses.append(dict(epoch=epoch+1,**loss));print('spacy',epoch+1,loss,flush=True)
 nlp.to_disk(OUT/'spacy-model');fresh=spacy.load(OUT/'spacy-model');panel=rows[-8:];before=[predict(nlp,r['question'],[(m['start'],m['end']) for m in r['mentions']]) for r in panel];after=[predict(fresh,r['question'],[(m['start'],m['end']) for m in r['mentions']]) for r in panel]
 write('spacy-losses.json',losses);write('spacy-save-before.json',before);write('spacy-save-after.json',after)
 if before!=after:raise ValueError('save parity')
 fit=[]
 for r in rows:fit.append(dict(id=r['question_id'],prediction=predict(fresh,r['question'],[(m['start'],m['end']) for m in r['mentions']])))
 write('spacy-training-fit.json',fit);write('spacy-receipt.json',dict(version=spacy.__version__,questions=len(rows),counts=counts,unaligned_positive=len(alignment),save_parity=True,seed=1701,epochs=30,optimizer_steps=30*25))

def write(name,obj):
 with (OUT/name).open('x') as f:json.dump(obj,f,indent=2,allow_nan=False)

def compare():
 nlp=spacy.load(OUT/'spacy-model')
 for seed in (1701,1702):
  folder=OUT/str(seed)
  for file in sorted(folder.glob('*-inputs.json')):
   rows=json.loads(file.read_text());outputs=[]
   for row in rows:
    start=time.perf_counter();result=predict(nlp,row['question'],row['offsets']);outputs.append(dict(id=row['id'],**result,seconds=time.perf_counter()-start))
   with file.with_name(file.name.replace('-inputs','-spacy')).open('x') as f:json.dump(outputs,f,indent=2,allow_nan=False)
if __name__=='__main__':train() if sys.argv[1]=='train' else compare()
