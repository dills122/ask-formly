"""Prompt packaging and structural validation only; no semantic inference or I/O to KB."""
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def exact_keys(value, keys, location):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(f'{location}: expected exactly {sorted(keys)}')


def validate(value):
    """Return the unchanged object or reject. Does not judge library relevance."""
    exact_keys(value, ('formly_questions', 'library_constraints'), 'output')
    questions = value['formly_questions']
    if not isinstance(questions, list):
        raise ValueError('formly_questions: expected array')
    for index, question in enumerate(questions):
        exact_keys(question, ('question', 'reason'), f'question[{index}]')
        if not all(nonempty(question[key]) for key in ('question', 'reason')):
            raise ValueError(f'question[{index}]: question and reason must be nonempty strings')
    constraints = value['library_constraints']
    exact_keys(constraints, ('formly_version', 'ui_adapter'), 'library_constraints')
    for key, constraint in constraints.items():
        if constraint is not None and not nonempty(constraint):
            raise ValueError(f'{key}: expected nonempty string or null')
    return value


def parse_json(text):
    """Strict JSON parsing shared by standalone and trial validation."""
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate key: {key}')
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError(f'Invalid JSON constant: {value}')
    return json.loads(text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def parse_output(text):
    return validate(parse_json(text))


def build_messages(request):
    if not nonempty(request):
        raise ValueError('Request must be a nonempty string')
    return [
        {'role': 'system', 'content': (HERE/'CONTRACT.md').read_text(encoding='utf-8')},
        {'role': 'user', 'content': request},
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    prompt = commands.add_parser('prompt')
    prompt.add_argument('--request', required=True)
    check = commands.add_parser('validate')
    check.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'prompt':
            print(json.dumps(build_messages(args.request), ensure_ascii=False, indent=2))
        else:
            parse_output(args.output.read_text(encoding='utf-8'))
            print('Valid structure; semantic quality not assessed.')
    except (ValueError, OSError) as exc:
        print(f'Invalid: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
