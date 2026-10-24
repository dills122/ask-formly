"""First-save receipts and whole-packet accounting, after response submission."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

RUNNER = Path(__file__).with_name('runner.py').resolve()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_new(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def execute(packet, source, attempt):
    """Reserve an attempt before execution; never overwrite or rerun it."""
    packet, source, attempt = (Path(p).resolve() for p in (packet, source, attempt))
    attempt.mkdir(exist_ok=False)
    receipt = dict(packet=str(packet), source=str(source), runner=str(RUNNER),
                   packet_sha256=digest(packet), source_sha256=digest(source),
                   runner_sha256=digest(RUNNER))
    save_new(attempt / 'first-save.json', receipt)
    command = [sys.executable, '-B', str(RUNNER), str(source), str(attempt / 'output.json')]
    try:
        process = subprocess.run(command, cwd=attempt, capture_output=True, text=True)
        code, stdout, stderr = process.returncode, process.stdout, process.stderr
    except OSError as error:
        code, stdout, stderr = -1, '', repr(error)
    with (attempt / 'stdout.txt').open('x', encoding='utf-8') as stream:
        stream.write(stdout)
    with (attempt / 'stderr.txt').open('x', encoding='utf-8') as stream:
        stream.write(stderr)
    result = dict(command=command, returncode=code, source_before=receipt['source_sha256'],
                  source_after=digest(source),
                  output_sha256=digest(attempt / 'output.json') if (attempt / 'output.json').exists() else None)
    save_new(attempt / 'completion.json', result)
    return result


def load_attempt(packet_path, source, attempt):
    """Integrity or execution failure invalidates the whole scheduled packet."""
    packet_path, source, attempt = (Path(p).resolve() for p in (packet_path, source, attempt))
    packet = json.loads(packet_path.read_text(encoding='utf-8'))
    try:
        receipt = json.loads((attempt / 'first-save.json').read_text())
        result = json.loads((attempt / 'completion.json').read_text())
        expected = dict(packet=str(packet_path), source=str(source), runner=str(RUNNER),
                        packet_sha256=digest(packet_path), source_sha256=digest(source),
                        runner_sha256=digest(RUNNER))
        if receipt != expected:
            raise ValueError('First-save receipt mismatch')
        if result['returncode'] != 0 or result['source_before'] != expected['source_sha256'] or result['source_after'] != expected['source_sha256']:
            raise ValueError('Execution failed or first source changed')
        if result['output_sha256'] != digest(attempt / 'output.json'):
            raise ValueError('Saved output hash mismatch')
        return account(packet, (attempt / 'output.json').read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError, KeyError) as error:
        return [{'id': request['id'], 'output': None} for request in packet['requests']], str(error)


def account(packet, raw_text):
    """Invalid delivery envelopes fail every slot; never repair or salvage rows."""
    ids = [request['id'] for request in packet['requests']]

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError('Invalid JSON constant: ' + value)

    try:
        rows = json.loads(raw_text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
        if not isinstance(rows, list) or any(not isinstance(row, dict) or set(row) != {'id', 'output'} for row in rows):
            raise ValueError('Invalid batch envelope')
        if [row['id'] for row in rows] != ids:
            raise ValueError('Batch IDs/count/order mismatch')
        return rows, None
    except (ValueError, TypeError) as error:
        return [{'id': identity, 'output': None} for identity in ids], str(error)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('source', type=Path)
    parser.add_argument('attempt', type=Path)
    args = parser.parse_args()
    result = execute(args.packet, args.source, args.attempt)
    print(json.dumps(result))
    raise SystemExit(0 if result['returncode'] == 0 else 1)
