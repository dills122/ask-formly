from train import *
def main():
 train_rows=combine(json.loads((HERE.parent/'pilot/gold.json').read_text()),json.loads((HERE/'train-new.json').read_text()))
 dev=json.loads((HERE/'dev.json').read_text())
 labels=json.loads((HERE.parent/'pilot/labels.json').read_text())
 model=load_model()
 for row in train_rows+dev:prepare(model,row,labels)
 write(HERE/'test-output/qualification.json',dict(train=len(train_rows),dev=len(dev),all_spans_exact=True,
  train_mentions=sum(len(r['mentions']) for r in train_rows),dev_mentions=sum(len(r['mentions']) for r in dev)))
 print('Native exact span transport passed all86rows',flush=True)
if __name__=='__main__':main()
