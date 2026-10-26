#!/usr/bin/env python3
"""Source checks and local qualification for the accepted Formly library MCP."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
POC = ROOT / 'poc/contextual-kb'


def verify_files(root, manifest):
    root = Path(root).resolve()
    for name, expected in manifest.items():
        path = (root / name).resolve()
        if Path(name).is_absolute() or not path.is_relative_to(root):
            raise ValueError(f'Unsafe manifest path: {name}')
        if not path.is_file():
            raise ValueError(f'Missing preserved source: {name}')
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Preserved source changed: {name}')


def validate():
    manifest = json.loads((POC / 'packaging/source-files.json').read_text())
    verify_files(ROOT, manifest)
    relocation = json.loads((ROOT / 'docs/history/relocation.json').read_text())
    verify_files(ROOT, {r['current']: r['sha256'] for r in relocation['files']})
    sys.path.insert(0, str(POC))
    from kbcompiler.current_source import lint_sources
    errors = lint_sources(POC / 'authored', ROOT, POC / 'corpus/evidence-catalog.json')
    if errors:
        raise ValueError('\n'.join(errors))
    # Historical source snapshots retain their original links; current guides do not.
    docs = [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md')),
            ROOT / 'docs/history/README.md', ROOT / 'docs/history/experiments.md']
    for path in docs:
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            target = unquote(target.strip('<>').split('#')[0])
            if not target or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            if not (path.parent / target).exists():
                raise ValueError(f'Broken link in {path.relative_to(ROOT)}: {target}')
    print(f'Source validation passed: {len(manifest)} preserved files; authored facts lint clean', flush=True)


def run_tests(python, folder, pattern='test_*.py'):
    subprocess.run([str(python), '-B', '-m', 'unittest', 'discover',
                    '-s', str(folder), '-p', pattern], cwd=POC, check=True)


def source_checks():
    validate()
    compiler = POC / '.venv/bin/python'
    python = compiler if compiler.is_file() else Path(sys.executable)
    run_tests(python, ROOT / 'tools', 'test_project.py')
    run_tests(python, POC / 'mcp_runtime', 'test_launcher.py')
    for pattern in ('test_pipeline.py', 'test_structured_source.py'):
        run_tests(python, POC / 'tests', pattern)
    run_tests(python, POC / 'packaging', 'test_bundle.py')
    # These suites use temporary fixtures only, never installed DB/model assets.
    run_tests(python, POC / 'knowledge-expansion/admission')
    run_tests(python, POC / 'knowledge-expansion/promotion-v3')
    run_tests(python, POC / 'knowledge-expansion/promotion-v4')
    run_tests(python, POC / 'knowledge-expansion/promotion-v5')
    run_tests(python, POC / 'knowledge-expansion/promotion-v6')
    run_tests(python, POC / 'knowledge-expansion/promotion-v7')
    run_tests(python, POC / 'knowledge-expansion/promotion-v8')
    run_tests(python, POC / 'knowledge-expansion/material-select-v1', 'test_candidate.py')
    run_tests(python, POC / 'knowledge-expansion/material-select-v1', 'test_evaluate.py')
    run_tests(python, POC / 'knowledge-expansion/validation-v1', 'test_candidate.py')
    run_tests(python, POC / 'knowledge-expansion/validation-v1', 'test_evaluate.py')
    run_tests(python, POC / 'knowledge-expansion/combined-v2', 'test_run.py')
    context_python = POC / 'mcp_v1/.venv/bin/python'
    run_tests(context_python if context_python.is_file() else Path(sys.executable),
              POC / 'mcp_v1', 'test_project_context.py')
    run_tests(python, POC / 'versioned_knowledge_v1', 'test_compiler.py')
    print('Source-only checks passed; models, DB and hosted service NOT qualified by this command', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('source', 'check'))
    args = parser.parse_args()
    if args.command == 'check':
        for env in (POC / '.venv/bin/python', POC / 'mcp_v1/.venv/bin/python'):
            if not env.is_file():
                raise SystemExit(f'Local qualification requires existing environment: {env}; use source for CI-only checks')
    source_checks()
    if args.command == 'check':
        python = POC / 'mcp_v1/.venv/bin/python'
        subprocess.run([str(python), '-B', str(POC / 'mcp_runtime/launcher.py'), 'doctor'], check=True)
        subprocess.run([str(python), '-B', str(POC / 'mcp_foundation/launcher.py'), 'doctor'], check=True)
        subprocess.run([str(python), '-B', str(POC / 'packaging/check.py')], check=True)
        print('Local foundation checks passed; no hosted inference or sealed evaluation used', flush=True)


if __name__ == '__main__':
    main()
