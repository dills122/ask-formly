"""Reviewed adapter entry point; frozen experiment implementation remains intact."""
from contract import adapt as frozen_adapt, envelope, tokens, counts

def adapt(id, text, row):
    if row is not None and not isinstance(row, dict):
        return (
            envelope(id, text, [], status='extraction_error', reason='invalid_output'),
            [],
            'prediction must be an object',
        )
    return frozen_adapt(id, text, row)

def score_case(gold, row):
    result, raw, error = adapt(gold['question_id'], gold['question'], row)
    expected = tokens(gold['mentions'])
    predicted = tokens(raw)
    accepted = tokens(result['mentions']) if result['status'] == 'ok' else set()
    return dict(
        envelope=result, raw_mentions=raw, error=error,
        raw=counts(predicted, expected), accepted=counts(accepted, expected),
        exact=error is None and result['status'] == gold['status']
              and accepted == expected and result['issues'] == gold['issues'],
        status_match=result['status'] == gold['status'],
    )
