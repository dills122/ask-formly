"""Copy candidate examples to a NEW output directory and execute pinned browser checks."""
import argparse
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(HERE.parent):
        parser.error('Use an output directory outside the candidate source tree')
    output.mkdir(parents=True, exist_ok=False)
    shutil.copytree(HERE.parent / 'examples', output / 'examples')
    (output / 'fixtures').mkdir()
    for name in ('browser.ts', 'run.mjs', 'package.json', 'package-lock.json'):
        shutil.copyfile(HERE / name, output / 'fixtures' / name)
    for name in ('package.json', 'package-lock.json'):
        shutil.copyfile(HERE / name, output / name)
    subprocess.run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=output, check=True)
    tsc = output / 'node_modules' / 'typescript' / 'bin' / 'tsc'
    sources = sorted((output / 'examples').glob('*/example.ts')) + [output / 'fixtures/browser.ts']
    subprocess.run(['node', str(tsc), '--noEmit', '--skipLibCheck', '--target', 'ES2022',
                    '--moduleResolution', 'node', '--module', 'es2022', *map(str, sources)], cwd=output, check=True)
    subprocess.run(['node', str(output / 'fixtures/run.mjs')], cwd=output, check=True)


if __name__ == '__main__':
    main()
