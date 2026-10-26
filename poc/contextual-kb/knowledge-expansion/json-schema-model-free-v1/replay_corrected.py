"""New complete run after a reviewed caller-scope fix; never overwrite old runs."""
import json
from pathlib import Path
import subprocess
import sys
from harness import HERE,POC
from scope import fetch_arguments


def main():
    out=HERE/'test-output/corrected'
    out.mkdir(exist_ok=False)
    for repeat in (1,2,3):
        for arm in ('baseline','candidate'):
            root=out/f'r{repeat}/{arm}';root.mkdir(parents=True)
            observed={};packets={};delivered={}
            for stage in ('batch-1-lookup','batch-2-lookup','batch-3-lookup','discovery','discovery2','fetch'):
                if stage.startswith('batch-'):
                    calls=json.loads((HERE/(stage.replace('-lookup','')+'.json')).read_text())
                else:
                    calls=json.loads((HERE/f'test-output/r1/{arm}/{stage}-input.json').read_text())
                if stage=='fetch':
                    for call in calls:
                        i=call['id'];ids=call['arguments']['fact_ids']
                        if not set(ids)<=observed[i]:raise ValueError('Unobserved fetch ID')
                        call['arguments']=fetch_arguments(ids,packets[i])
                input_path=root/(stage+'-input.json');input_path.write_text(json.dumps(calls,indent=2))
                output_path=root/(stage+'.json')
                subprocess.run([sys.executable,'-B',str(HERE/'harness.py'),arm,str(input_path),str(output_path)],check=True)
                for row in json.loads(output_path.read_text()):
                    if row.get('operational_or_tool_error'):continue
                    i=row['id'];packet=row['result']['structuredContent']
                    if row['tool']=='lookup_formly':packets[i]=packet
                    observed.setdefault(i,set()).update(f['id'] for f in packet.get('facts',[])+packet.get('candidates',[]))
                    delivered.setdefault(i,{}).update({f['id']:(f,packet['citations'][f['id']]) for f in packet.get('facts',[])})
            original={}
            for stage in ('batch-1-lookup','batch-2-lookup','batch-3-lookup','fetch'):
                for row in json.loads((HERE/f'test-output/r1/{arm}/{stage}.json').read_text()):
                    packet=row['result']['structuredContent'];original.setdefault(row['id'],{}).update({f['id']:(f,packet['citations'][f['id']]) for f in packet.get('facts',[])})
            # Do not reuse an answer if the fresh evidence differs.
            if original!=delivered:raise ValueError('Fresh evidence changed; independently reassess before answering')
            answers=json.loads((HERE/f'test-output/r1/{arm}/answers.json').read_text())
            for a in answers:a['author']='Root caller answer retained only after exact fresh full-fact/citation equality; not independent generation'
            (root/'answers.json').write_text(json.dumps(answers,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
