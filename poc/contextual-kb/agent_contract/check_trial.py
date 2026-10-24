"""Check saved trial coverage/structure; never infer semantic pass from valid JSON."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from contract import validate, parse_json


def check_trial(cases, rows):
    if not isinstance(rows, list):
        raise ValueError('Trial must be an array')
    if any(not isinstance(row, dict) or set(row) != {'id', 'output'} or
           not isinstance(row['id'], str) for row in rows):
        raise ValueError('Expected trial rows with id and output')
    expected = [case['id'] for case in cases]
    actual = [row['id'] for row in rows]
    if len(set(expected)) != len(expected) or len(set(actual)) != len(actual) or set(actual) != set(expected):
        raise ValueError('Trial must contain every case exactly once, with no extras')
    checked = []
    for row in rows:
        try:
            validate(row['output'])
            checked.append({'id': row['id'], 'valid_structure': True,
                            'question_count': len(row['output']['formly_questions'])})
        except ValueError as exc:
            checked.append({'id': row['id'], 'valid_structure': False, 'error': str(exc)})
    valid = sum(row['valid_structure'] for row in checked)
    return {'total_cases': len(rows), 'valid_structures': valid,
            'invalid_structures': len(rows) - valid, 'per_case': checked,
            'semantic_assessment': 'not performed by this checker'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--trial', type=Path, required=True)
    args = parser.parse_args()
    try:
        case_bytes, trial_bytes = args.cases.read_bytes(), args.trial.read_bytes()
        result = check_trial(parse_json(case_bytes), parse_json(trial_bytes))
        result['sha256'] = {'cases': hashlib.sha256(case_bytes).hexdigest(),
                            'trial': hashlib.sha256(trial_bytes).hexdigest()}
        print(json.dumps(result, indent=2))
        return int(result['invalid_structures'] > 0)
    except (ValueError, OSError) as exc:
        print(f'Invalid trial: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
