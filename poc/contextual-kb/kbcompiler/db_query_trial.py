"""Run explicit, designer-supplied DB queries; this is not question parsing."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path


def _candidates(db: sqlite3.Connection, match: str, version: str,
                adapters: list[str], limit: int) -> list[str]:
    adapter_slots = ", ".join("?" for _ in adapters)
    rows = db.execute(f"""
        SELECT f.id FROM facts_fts
        JOIN facts f ON f.id = facts_fts.fact_id
        JOIN documents d ON d.id = f.doc_id
        WHERE facts_fts MATCH ? AND d.formly_version = ?
          AND d.adapter IN ({adapter_slots})
        ORDER BY bm25(facts_fts), f.id LIMIT ?
    """, (match, version, *adapters, limit)).fetchall()
    return [row[0] for row in rows]


def _packet(db: sqlite3.Connection, fact_id: str) -> dict:
    row = db.execute("""
        SELECT f.id, f.claim, f.context, f.conditions_json, f.limits_json,
               f.source_quote, f.source_start_offset, f.source_end_offset,
               d.formly_version, d.adapter, d.source_path, d.source_sha256
        FROM facts f JOIN documents d ON d.id = f.doc_id WHERE f.id = ?
    """, (fact_id,)).fetchone()
    if row is None:
        raise ValueError(f"missing fact {fact_id}")
    evidence = db.execute("""
        SELECT e.id, e.record_json FROM fact_evidence fe
        JOIN evidence e ON e.id = fe.evidence_id
        WHERE fe.fact_id = ? ORDER BY e.id
    """, (fact_id,)).fetchall()
    links = db.execute("""
        SELECT target_fact_id FROM fact_links
        WHERE source_fact_id = ? AND kind = 'see_also'
        ORDER BY target_fact_id
    """, (fact_id,)).fetchall()
    return {
        "id": row[0], "claim": row[1], "context": row[2],
        "conditions": json.loads(row[3]), "limits": json.loads(row[4]),
        "source_quote": row[5], "source_start_offset": row[6],
        "source_end_offset": row[7], "formly_version": row[8],
        "adapter": row[9], "source_path": row[10], "source_sha256": row[11],
        "evidence": [{"id": item[0], "record": json.loads(item[1])} for item in evidence],
        "see_also": [item[0] for item in links],
    }


def run_trial(database: Path, fixture: dict) -> dict:
    """Issue frozen FTS MATCH queries, then read candidate and one-hop packets."""
    cases = []
    with closing(sqlite3.connect(f"file:{database}?mode=ro", uri=True)) as db:
        for case in fixture["cases"]:
            candidates = list(dict.fromkeys(
                fact_id
                for match in case["matches"]
                for fact_id in _candidates(
                    db, match, fixture["baseline"], fixture["adapters"],
                    fixture["limit_per_query"],
                )
            ))
            linked = list(dict.fromkeys(
                target
                for fact_id in candidates
                for (target,) in db.execute("""
                    SELECT target_fact_id FROM fact_links
                    WHERE source_fact_id = ? AND kind = 'see_also'
                    ORDER BY target_fact_id
                """, (fact_id,))
            ))
            expanded = candidates + [fact_id for fact_id in linked if fact_id not in candidates]
            packets = [_packet(db, fact_id) for fact_id in expanded]
            required = set(case["required_fact_ids"])
            cases.append({
                "id": case["id"], "matches": case["matches"],
                "required_fact_ids": case["required_fact_ids"],
                "candidate_ids": candidates, "expanded_ids": expanded,
                "missing_from_candidates": sorted(required - set(candidates)),
                "missing_after_expansion": sorted(required - set(expanded)),
                "candidate_complete": required <= set(candidates),
                "expanded_complete": required <= set(expanded),
                "packets_have_evidence": all(packet["evidence"] for packet in packets),
                "packets": packets,
            })
    return {
        "scope": "explicit FTS queries supplied by trial designer; no question dissection or MCP",
        "baseline": fixture["baseline"], "adapters": fixture["adapters"],
        "limit_per_query": fixture["limit_per_query"],
        "cases": cases,
    }


def main() -> None:
    poc = Path(__file__).resolve().parents[1]
    fixture = json.loads((poc / "DB-QUERY-TRIAL-CASES.json").read_text(encoding="utf-8"))
    print(json.dumps(run_trial(poc / "build/knowledge.sqlite", fixture), indent=2))


if __name__ == "__main__":
    main()
