"""Persistent local GLiNER worker in its existing POC Python environment."""
import json,os,selectors,subprocess,tempfile,time,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;POC=HERE.parents[1]
sys.path.insert(0,str(POC))
from agent_contract.advisory_lookup_v1.runtime import IntegrityError

class ProcessExtractor:
    def __init__(self,seed=1701,*,command=None,timeout=60):
        if seed not in (1701,1702):raise ValueError('Unsupported frozen adapter')
        self.timeout=timeout;self.sequence=0;self.buffer=b'';self.after=None;self.integrity_failure=None
        logdir=HERE/'test-output/runtime-cache';logdir.mkdir(parents=True,exist_ok=True)
        self.log=tempfile.NamedTemporaryFile(prefix='gliner-',suffix='.log',dir=logdir,delete=False)
        self.process=None
        command=command or [str(POC/'gliner_feasibility/env/.venv/bin/python'),'-B',str(HERE/'worker.py'),'--seed',str(seed)]
        try:
            self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.log,bufsize=0)
            os.set_blocking(self.process.stdout.fileno(),False)
            ready=self._read()
            if ready.get('error_type')=='IntegrityError':raise IntegrityError(str(ready.get('error')))
            if ready.get('ready') is not True or not isinstance(ready.get('parameters'),dict):raise RuntimeError('Invalid extractor startup')
            self.before=ready['parameters'];self.load_seconds=ready['load_seconds']
        except Exception:
            self.close();raise

    def _read(self):
        deadline=time.monotonic()+self.timeout
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout,selectors.EVENT_READ)
            while b'\n' not in self.buffer:
                remaining=deadline-time.monotonic()
                if remaining<=0 or not selector.select(remaining):raise TimeoutError('GLiNER worker timed out')
                chunk=os.read(self.process.stdout.fileno(),65536)
                if not chunk:raise RuntimeError('GLiNER worker exited; log: '+self.log.name)
                self.buffer+=chunk
                if len(self.buffer)>16*1024*1024:raise RuntimeError('Oversized worker response')
        line,self.buffer=self.buffer.split(b'\n',1)
        value=json.loads(line)
        if not isinstance(value,dict):raise RuntimeError('Invalid worker response')
        return value

    def _exchange(self,operation,**payload):
        try:
            if self.integrity_failure is not None:raise IntegrityError(self.integrity_failure)
            if self.process.poll() is not None:raise RuntimeError('GLiNER worker unavailable')
            self.sequence+=1
            self.process.stdin.write((json.dumps(dict(id=self.sequence,op=operation,**payload))+'\n').encode())
            result=self._read()
            if result.get('id')!=self.sequence:raise RuntimeError('Worker response identity mismatch')
            if result.get('error_type')=='IntegrityError':raise IntegrityError(str(result.get('error')))
            if 'error' in result:raise RuntimeError(str(result['error']))
            if 'result' not in result:raise RuntimeError('Missing worker result')
            return result['result']
        except IntegrityError as exc:
            self.integrity_failure=str(exc)
            self.close();raise
        except Exception:
            self.close();raise

    def __call__(self,text):return self._exchange('extract',text=text)

    def verify_unchanged(self):
        result=self._exchange('verify');self.after=result['parameters']
        if self.after!=self.before:
            self.integrity_failure='Frozen worker parameters changed'
            self.close()
            raise IntegrityError(self.integrity_failure)
        return dict(result['checks'],worker_log=self.log.name)

    def close(self):
        if self.process is not None:
            if self.process.poll() is None:
                self.process.terminate()
                try:self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:self.process.kill();self.process.wait()
            for stream in (self.process.stdin,self.process.stdout):
                if stream is not None:stream.close()
        self.log.close()
