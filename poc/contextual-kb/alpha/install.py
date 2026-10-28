"""Install a verified model-free alpha into a new directory; never overwrite."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import venv

MANIFEST = 'ALPHA-MANIFEST.json'
PRIVATE = {'evaluation', 'qualification', 'sealed', 'models', '.venv', 'test-output', 'local', '.git', '.codex', '__pycache__'}


def safe_path(name):
    path = PurePosixPath(name)
    if not name or ':' in name or '\\' in name or path.is_absolute() or '..' in path.parts or str(path) != name or PRIVATE.intersection(path.parts):
        raise ValueError('Unsafe/private package path: ' + name)
    return Path(*path.parts)


def verify(source):
    source = Path(source).resolve()
    manifest_path = source / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError('Manifest symlink is not allowed')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('format') != 1 or not isinstance(manifest.get('files'), dict):
        raise ValueError('Unsupported alpha manifest')
    for name, expected in manifest['files'].items():
        relative = safe_path(name)
        path = source / relative
        if any(p.is_symlink() for p in [path, *path.parents] if p != source and p.is_relative_to(source)):
            raise ValueError('Package symlink is not allowed: ' + name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Missing file or hash mismatch: ' + name)
    return manifest


def stage(source, target):
    source = Path(source).resolve()
    target = Path(target).absolute()
    manifest = verify(source)
    target.mkdir(parents=True, exist_ok=False)
    try:
        for name in manifest['files']:
            dest = target / safe_path(name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, dest)
        shutil.copyfile(source / MANIFEST, target / MANIFEST)
        verify(target)
    except BaseException:
        shutil.rmtree(target)
        raise
    return target


def install(source, target):
    if sys.version_info < (3, 11):
        raise ValueError('Python 3.11 or newer is required; see README for tested platforms')
    target = stage(source, target)
    try:
        venv.EnvBuilder(with_pip=True, system_site_packages=False).create(target / 'venv')
        python = target / 'venv' / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
        subprocess.run([str(python), '-I', '-m', 'pip', '--isolated', 'install', '--no-cache-dir', '--only-binary=:all:', '--no-deps', '-r', str(target / 'requirements.lock')], check=True)
        subprocess.run([str(python), '-I', '-m', 'pip', 'check'], check=True)
        subprocess.run([str(python), '-I', str(target / 'ask_formly.py'), 'doctor'], check=True)
        subprocess.run([str(python), '-I', str(target / 'ask_formly.py'), 'self-test'], check=True)
        config = {'mcpServers': {'ask-formly': {'command': str(python), 'args': ['-I', str(target / 'ask_formly.py'), 'serve']}}}
        (target / 'mcp-config.json').write_text(json.dumps(config, indent=2) + '\n')
        return config
    except BaseException:
        shutil.rmtree(target)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', type=Path, required=True, help='New absolute installation directory')
    args = parser.parse_args()
    if not args.prefix.is_absolute():
        parser.error('--prefix must be absolute')
    try:
        config = install(Path(__file__).resolve().parent, args.prefix)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Installation failed: {exc}\nUse a new destination and check network/dependency availability.\n')
    print(json.dumps(config, indent=2))


if __name__ == '__main__':
    main()
