"""Fail-closed stage boundary before any evaluation loader runs."""
from decisions import GRID


def evaluation_ready(decision,bindings,loader):
    if decision.get('mode')!='calibration' or decision.get('selected') is None or tuple(decision['selected']) not in GRID:
        raise ValueError('no frozen full-run calibration decision')
    if decision.get('bindings')!=bindings:raise ValueError('calibration binding mismatch')
    return loader()


def review_receipt(receipt,fresh_sha256):
    if receipt.get('verdict')!='ready' or receipt.get('fresh_sha256')!=fresh_sha256 or receipt.get('independent') is not True or not isinstance(receipt.get('reviewer'),str) or not receipt['reviewer'].strip():
        raise ValueError('independent review receipt bound to fresh bytes required')
    return True
