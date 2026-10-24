"""One-shot literal-to-JSON transport. No generated code or semantic repair."""
import argparse
import ast
import json
from pathlib import Path


def deliver(source, destination):
    """Preserve the first saved literal and exclusively create its JSON encoding."""
    rows = ast.literal_eval(Path(source).read_text(encoding='utf-8'))
    if not isinstance(rows, list):
        raise ValueError('Response batch must be a list')
    encoded = json.dumps(rows, ensure_ascii=False, allow_nan=False, indent=2) + '\n'
    # Encode fully before opening: failed parsing/encoding never creates an output.
    payload = encoded.encode('utf-8')
    with Path(destination).open('xb') as stream:
        stream.write(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    deliver(args.source, args.destination)


if __name__ == '__main__':
    main()
