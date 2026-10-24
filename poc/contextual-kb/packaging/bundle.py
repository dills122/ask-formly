"""Build and verify an allowlisted local recovery bundle; never include evaluation."""
import argparse,hashlib,io,json,tarfile
from pathlib import Path

META='contextual-kb/BUNDLE-MANIFEST.json'
def digest(stream):
 h=hashlib.sha256()
 for chunk in iter(lambda:stream.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def allowed(name):
 p=Path(name)
 if p.is_absolute() or '..' in p.parts or 'sealed' in p.parts or 'evaluation' in p.parts or name=='BUNDLE-MANIFEST.json':raise ValueError('Unsafe or evaluation path: '+name)
 return p

def build(root,names,output):
 root=Path(root).resolve();output=Path(output);files={}
 for name in sorted(set(names)):
  relative=allowed(name);path=(root/relative).resolve()
  if not path.is_relative_to(root):raise ValueError('Source outside POC: '+name)
  if not path.is_file():raise FileNotFoundError(path)
  with path.open('rb') as f:files[name]=digest(f)
 with output.open('xb') as dest:
  with tarfile.open(fileobj=dest,mode='w:gz',dereference=True) as archive:
   for name in files:archive.add(root/name,arcname='contextual-kb/'+name,recursive=False)
   data=json.dumps({'format':1,'files':files},indent=2).encode();info=tarfile.TarInfo(META);info.size=len(data);info.mode=0o644
   archive.addfile(info,io.BytesIO(data))
 actual=verify(output)
 if actual!=files:raise ValueError('Bundle verification mismatch')
 with output.open('rb') as f:checksum=digest(f)
 output.with_suffix(output.suffix+'.sha256').write_text(checksum+'  '+output.name+'\n')
 return files

def verify(path):
 with tarfile.open(path,'r:gz') as archive:
  members=archive.getmembers();names=[m.name for m in members]
  if len(names)!=len(set(names)) or names.count(META)!=1:raise ValueError('Duplicate or missing bundle manifest')
  manifest=json.load(archive.extractfile(META));expected=manifest['files'];actual={}
  for member in members:
   if member.name==META:continue
   if not member.name.startswith('contextual-kb/') or not member.isfile():raise ValueError('Unsafe bundle member')
   name=member.name[len('contextual-kb/'):];allowed(name)
   actual[name]=digest(archive.extractfile(member))
  if actual!=expected:raise ValueError('Bundle content hash mismatch')
  return actual

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 root=Path(__file__).resolve().parents[1];names=json.loads((Path(__file__).parent/'runtime-files.json').read_text())
 files=build(root,names,args.output);print(json.dumps({'archive':str(args.output),'verified_files':len(files)}))
if __name__=='__main__':main()
