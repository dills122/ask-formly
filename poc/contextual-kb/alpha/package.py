"""Build an allowlisted model-free alpha artifact; no models or evaluation."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
from install import MANIFEST, safe_path

HERE = Path(__file__).resolve().parent
POC = HERE.parent


def runtime_files(poc):
    poc = Path(poc).resolve()
    manifest = json.loads((poc / 'mcp_runtime/model-free.json').read_text())
    files = {}
    pins = dict(manifest['files'])
    pins['mcp_v1/versions.json'] = 'c75aa77f0c058a7c1dd0bce785fd9eaac00a5be96abc5426cfcc6bb1f342e99f'
    for name, expected in pins.items():
        relative = safe_path(name)
        path = poc / relative
        if path.is_symlink() or not path.resolve().is_relative_to(poc):
            raise ValueError('Runtime source outside POC or symlink: ' + name)
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Runtime hash mismatch: ' + name)
        files['runtime/' + name] = data
    for name in ('mcp_runtime/launcher.py', 'mcp_runtime/model-free.json'):
        files['runtime/' + name] = (poc / name).read_bytes()
    return files


def build(output, poc=POC):
    output = Path(output)
    checksum = Path(str(output) + '.sha256')
    if output.exists() or checksum.exists():
        raise FileExistsError('Archive/checksum already exists')
    files = dict(runtime_files(poc))
    for name in ('install.py', 'ask_formly.py', 'healthcheck.py', 'requirements.lock', 'README.md'):
        files[name] = (HERE / name).read_bytes()
    manifest = {'format': 1, 'release': '0.1.0-alpha.1', 'mode': 'model-free',
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    files[MANIFEST] = (json.dumps(manifest, indent=2) + '\n').encode()
    with output.open('xb') as raw:
        with gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w') as archive:
                for name, data in sorted(files.items()):
                    safe_path(name)
                    info = tarfile.TarInfo('ask-formly-alpha/' + name)
                    info.size = len(data); info.mode = 0o644
                    archive.addfile(info, io.BytesIO(data))
    with checksum.open('x') as stream:
        stream.write(hashlib.sha256(output.read_bytes()).hexdigest() + '  ' + output.name + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.output)
    print(json.dumps({'archive': str(args.output), 'files': len(manifest['files']), 'mode': 'model-free'}))


if __name__ == '__main__':
    main()
