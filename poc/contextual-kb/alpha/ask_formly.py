"""Model-free-only installed entry point; caller harness owns all inference."""
import argparse
import importlib.util
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('doctor', 'serve', 'self-test'))
    parser.add_argument('--runtime-dir', type=Path, help='Mutable settings directory; defaults to this installation/state')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    from install import verify
    verify(root)
    if args.command == 'self-test':
        from healthcheck import main as healthcheck
        healthcheck()
        return 0
    spec = importlib.util.spec_from_file_location('alpha_runtime_launcher', root / 'runtime/mcp_runtime/launcher.py')
    launcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launcher)
    return launcher.main([args.command, '--mode', 'model-free', '--runtime-dir', str(args.runtime_dir or root / 'state')])


if __name__ == '__main__':
    sys.exit(main())
