"""Experimental local assessment of whether selected facts answer each ask.

This is a diagnostic judge, not proof of source entailment. Invalid or failed
model output is treated as unsupported rather than being sent as an answer.
"""

from __future__ import annotations

import json
import urllib.request

from .obligation_layer import LOCAL_MODEL, ObligationEvidence


def validate_assessments(payload: object, obligations: tuple[ObligationEvidence, ...]
                         ) -> tuple[tuple[bool, tuple[str, ...]], ...]:
    if not isinstance(payload, dict) or not isinstance(payload.get("assessments"), list):
        raise ValueError("checker must return assessments array")
    rows = payload["assessments"]
    if len(rows) != len(obligations):
        raise ValueError("checker omitted an obligation")
    result: list[tuple[bool, tuple[str, ...]]] = []
    for position, (row, obligation) in enumerate(zip(rows, obligations)):
        if not isinstance(row, dict) or row.get("index") != position:
            raise ValueError("checker obligation indexes differ")
        supported = row.get("supported")
        ids = row.get("fact_ids")
        if not isinstance(supported, bool) or not isinstance(ids, list) or any(
            not isinstance(item, str) for item in ids
        ):
            raise ValueError("checker returned malformed support")
        if any(item not in obligation.candidate_ids for item in ids):
            raise ValueError("checker cited a fact not in the obligation packet")
        if supported != bool(ids):
            raise ValueError("support must have citations and abstention must not")
        result.append((supported, tuple(dict.fromkeys(ids))))
    return tuple(result)


def ollama_assess(question: str, obligations: tuple[ObligationEvidence, ...],
                  facts: dict[str, dict]) -> tuple[tuple[bool, tuple[str, ...]], ...]:
    packet = [{
        "index": index, "ask": obligation.span,
        "candidates": [{
            "id": fact_id, "claim": facts[fact_id]["claim"],
            "context": facts[fact_id]["context"],
            "conditions": facts[fact_id].get("conditions", []),
            "limits": facts[fact_id].get("limits", []),
        } for fact_id in obligation.candidate_ids],
    } for index, obligation in enumerate(obligations)]
    prompt = (
        "Assess whether the listed facts directly answer EACH ask in the "
        "context of the original question. Similar topic words alone are not "
        "enough. Use only the listed claims, context, conditions and limits. "
        "For every ask return index, supported (true/false), and fact_ids "
        "that directly support it. If no listed fact directly answers it, "
        "set supported=false and fact_ids=[]. Do not answer the question. "
        "Return JSON only: {\"assessments\":[{\"index\":0,"
        "\"supported\":false,\"fact_ids\":[]}]}. "
        "Original question: " + json.dumps(question) + "\nAsks and facts: "
        + json.dumps(packet)
    )
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({
            "model": LOCAL_MODEL, "prompt": prompt, "format": "json",
            "stream": False, "keep_alive": "10m",
            "options": {"temperature": 0, "num_predict": 500},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.load(response)
    return validate_assessments(json.loads(body["response"]), obligations)
