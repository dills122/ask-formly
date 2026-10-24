"""One fixed development extraction run, three passes; no A execution or plan adapter."""
import hashlib
import importlib.metadata
import json
import os
import platform
import signal
import sys
from pathlib import Path
from time import perf_counter

from probe import HERE, POC, build_schema, check_access, load_development, observe


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_protected():
    entries = json.loads((HERE / 'evidence/protected-before.json').read_text())
    changed = [name for name, sha in entries.items() if digest(POC / name) != sha]
    if changed:
        raise ValueError(f'Protected files changed: {changed}')
    return len(entries)


def run():
    verify_protected()
    cases = load_development()
    # Reserve exclusive output before any model work; never overwrite a prior run.
    with (HERE / 'evidence/raw.jsonl').open('x') as output:
        metadata = {'status': 'starting', 'python': sys.version, 'platform': platform.platform(),
                    'model_revision': '54785d51df8d86a0d8f2eb212fec15871aad2c4d',
                    'device': 'cpu', 'torch_threads': 4, 'threshold': 0.5, 'repeats': 3,
                    'timing_scope': 'development extraction + span validation; not qualified planner timing',
                    'packages': {n: importlib.metadata.version(n) for n in
                                 ['gliner2','torch','transformers','huggingface-hub']}}
        try:
            os.environ.update({'HF_HOME': str(HERE / '.cache/hf'), 'HF_HUB_OFFLINE': '1',
                               'TRANSFORMERS_OFFLINE': '1', 'TOKENIZERS_PARALLELISM': 'false'})
            start = perf_counter()
            import torch
            from gliner2 import AutoExtractor
            torch.set_num_threads(4)
            torch.manual_seed(1701)
            model = AutoExtractor.from_pretrained(str(HERE / 'models/gliner2.5-base-v1'),
                                                  local_files_only=True, map_location='cpu')
            model.eval()
            metadata['load_seconds'] = perf_counter() - start
            metadata['parameter_count'] = sum(p.numel() for p in model.parameters())
            schema = build_schema(model)
            # Offline inference has no authority to read knowledge/held-out inputs.
            sys.addaudithook(check_access)
            def expired(signum, frame):
                raise TimeoutError('60-second diagnostic alarm (not a hard native-code deadline)')
            signal.signal(signal.SIGALRM, expired)
            for repeat in range(3):
                for case in cases:
                    signal.alarm(60)
                    try:
                        with torch.inference_mode():
                            row = observe(case['question'], lambda: model.extract(
                                case['question'], schema, threshold=0.5,
                                include_confidence=True, include_spans=True))
                    finally:
                        signal.alarm(0)
                    row.update({'case_id': case['id'], 'repeat': repeat, 'question': case['question']})
                    output.write(json.dumps(row, ensure_ascii=False)+'\n')
                    output.flush()
                    print(case['id'], repeat, round(row['seconds'], 3), row.get('error', 'ok'), flush=True)
                    if row.get('error', {}).get('type') == 'TimeoutError':
                        raise TimeoutError('Stopping bounded probe after diagnostic alarm')
            metadata['status'] = 'completed'
        except BaseException as exc:
            metadata['error'] = {'type': type(exc).__name__, 'message': str(exc)}
            metadata['status'] = 'incomplete'
            raise
        finally:
            (HERE / 'evidence/runtime.json').write_text(json.dumps(metadata, indent=2)+'\n')


if __name__ == '__main__':
    run()
