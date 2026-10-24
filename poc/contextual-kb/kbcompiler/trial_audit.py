"""Reproducible audit of source-anchored fact candidates in the trial database."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path

from .fact_proposals import propose_from_block
from .pipeline import _citation_ids, _citations


def audit(database: Path, source_root: Path) -> dict:
    """Fail on stale sources or broken provenance, then summarize the trial."""
    with sqlite3.connect(f"file:{database}?mode=ro", uri=True) as connection:
        if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("database integrity check failed")
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("database has broken references")
        schema_version, input_sha256 = connection.execute(
            "SELECT schema_version, input_sha256 FROM build_info"
        ).fetchone()
        if schema_version != 4:
            raise ValueError(f"unexpected schema version {schema_version}")

        sources: dict[str, list[str]] = {}
        source_texts: dict[str, str] = {}
        citation_environments: dict[str, dict] = {}
        for doc_id, path, expected_hash, stored_body in connection.execute(
            "SELECT id, source_path, source_sha256, body_md FROM documents"
        ):
            raw = (source_root / path).read_bytes()
            if hashlib.sha256(raw).hexdigest() != expected_hash:
                raise ValueError(f"{doc_id}: source hash differs from compiled input")
            source_text = raw.decode("utf-8")
            if source_text != stored_body:
                raise ValueError(f"{doc_id}: stored document differs from source")
            sources[doc_id] = source_text.splitlines(keepends=True)
            source_texts[doc_id] = source_text
            environment: dict = {}
            _citations(source_text, environment)
            citation_environments[doc_id] = environment

        candidates = connection.execute("""
            SELECT f.id, f.block_kind, f.body_md, f.source_start_line,
                   f.source_end_line, f.body_sha256, c.doc_id, c.id
            FROM fact_candidates f
            JOIN concept_variants v ON v.id=f.variant_id
            JOIN concepts c ON c.id=v.concept_id
            ORDER BY f.id
        """).fetchall()
        kinds: dict[str, int] = {}
        proposal_kinds: dict[str, int] = {}
        dispositions: list[dict] = []
        proposal_count = 0
        covered_by_unit: dict[str, set[int]] = {}
        table_context_lines: dict[str, set[int]] = {}
        for fact_id, kind, body, start, end, body_hash, doc_id, unit_id in candidates:
            if body != "".join(sources[doc_id][start - 1:end]):
                raise ValueError(f"{fact_id}: candidate span differs from source")
            if hashlib.sha256(body.encode("utf-8")).hexdigest() != body_hash:
                raise ValueError(f"{fact_id}: candidate body hash differs")
            covered = covered_by_unit.setdefault(unit_id, set())
            for line in range(start, end + 1):
                if line in covered:
                    raise ValueError(f"{fact_id}: overlapping candidate spans")
                covered.add(line)
            expected = _citation_ids(
                _citations(body, citation_environments[doc_id]), 0, len(body.splitlines())
            )
            stored = tuple(row[0] for row in connection.execute(
                "SELECT evidence_id FROM fact_evidence WHERE fact_id=? ORDER BY evidence_id", (fact_id,)
            ))
            if expected != stored:
                raise ValueError(f"{fact_id}: evidence links differ from source")

            expected_proposals = propose_from_block(kind, body)
            stored_proposals = connection.execute("""
                SELECT id, ordinal, kind, subject_md, statement_md, condition_md,
                       exception_md, source_quote, source_start_offset,
                       source_end_offset, status
                FROM fact_proposals WHERE candidate_id=? ORDER BY ordinal
            """, (fact_id,)).fetchall()
            if len(stored_proposals) != len(expected_proposals):
                raise ValueError(f"{fact_id}: proposal count differs from source structure")
            candidate_offset = sum(len(line) for line in sources[doc_id][:start - 1])
            for ordinal, (proposal, stored_proposal) in enumerate(
                zip(expected_proposals, stored_proposals)
            ):
                (proposal_id, actual_ordinal, actual_kind, subject, statement,
                 condition, exception, quote, quote_start, quote_end, status) = stored_proposal
                if proposal_id != f"{fact_id}.p{ordinal:02d}":
                    raise ValueError(f"{proposal_id}: proposal id differs from generated id")
                expected_fields = (
                    ordinal, proposal.kind, proposal.subject_md, proposal.statement_md,
                    proposal.condition_md, proposal.exception_md, proposal.source_quote,
                    candidate_offset + proposal.local_start_offset,
                    candidate_offset + proposal.local_end_offset, "proposal",
                )
                if stored_proposal[1:] != expected_fields:
                    raise ValueError(f"{proposal_id}: proposal fields differ from source")
                if source_texts[doc_id][quote_start:quote_end] != quote:
                    raise ValueError(f"{proposal_id}: proposal quote differs from source")
                expected_links = _citation_ids(
                    _citations(quote, citation_environments[doc_id]),
                    0, len(quote.splitlines()),
                )
                actual_links = tuple(row[0] for row in connection.execute(
                    "SELECT evidence_id FROM proposal_evidence WHERE proposal_id=? ORDER BY evidence_id",
                    (proposal_id,),
                ))
                if expected_links != actual_links:
                    raise ValueError(f"{proposal_id}: proposal evidence differs from source")
                proposal_kinds[actual_kind] = proposal_kinds.get(actual_kind, 0) + 1
                proposal_count += 1
            dispositions.append({
                "candidate_id": fact_id,
                "block_kind": kind,
                "status": "proposed" if stored_proposals else "unresolved",
                "proposal_count": len(stored_proposals),
            })
            if kind == "table_row" and start >= 3:
                header, separator = sources[doc_id][start - 3:start - 1]
                if (header.lstrip().startswith("|") and "-" in separator and
                        re.fullmatch(r"\s*\|[\s:|\-]+\|\s*", separator)):
                    table_context_lines.setdefault(unit_id, set()).update((start - 2, start - 1))
            kinds[kind] = kinds.get(kind, 0) + 1

        for unit_id, doc_id, start, end in connection.execute(
            "SELECT id, doc_id, source_start_line, source_end_line FROM units"
        ):
            allowed = covered_by_unit.get(unit_id, set()) | table_context_lines.get(unit_id, set())
            for line_number in range(start, end + 1):
                line = sources[doc_id][line_number - 1]
                if (line.strip() and line_number not in allowed and
                        not re.match(r"^\s*#{1,6}\s", line)):
                    raise ValueError(f"{unit_id}: uncovered source line {line_number}")

        def count(table: str) -> int:
            return connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]

        unresolved_by_kind: dict[str, int] = {}
        for item in dispositions:
            if item["status"] == "unresolved":
                kind = item["block_kind"]
                unresolved_by_kind[kind] = unresolved_by_kind.get(kind, 0) + 1

        return {
            "schema_version": schema_version,
            "input_sha256": input_sha256,
            "documents": count("documents"),
            "heading_units": count("units"),
            "concepts": count("concepts"),
            "versioned_variants": count("concept_variants"),
            "candidates": len(candidates),
            "candidate_kinds": dict(sorted(kinds.items())),
            "verified_source_spans": len(candidates),
            "evidence_links": count("fact_evidence"),
            "proposals": proposal_count,
            "proposal_kinds": dict(sorted(proposal_kinds.items())),
            "proposal_evidence_links": count("proposal_evidence"),
            "proposals_without_direct_citation": connection.execute("""
                SELECT count(*) FROM fact_proposals p
                WHERE NOT EXISTS (SELECT 1 FROM proposal_evidence e WHERE e.proposal_id=p.id)
            """).fetchone()[0],
            "unresolved_candidates": sum(unresolved_by_kind.values()),
            "unresolved_by_kind": dict(sorted(unresolved_by_kind.items())),
            "verified_atomic_facts": 0,
            "promotion_gate_met": False,
            "candidate_dispositions": dispositions,
            "candidates_without_direct_citation": connection.execute("""
                SELECT count(*) FROM fact_candidates f
                WHERE NOT EXISTS (SELECT 1 FROM fact_evidence e WHERE e.fact_id=f.id)
            """).fetchone()[0],
            "paragraphs_over_300_characters": connection.execute("""
                SELECT count(*) FROM fact_candidates
                WHERE block_kind='paragraph' AND length(body_md)>300
            """).fetchone()[0],
            "semantic_relations": count("fact_relations"),
            "longest_candidates": [
                {"id": fact_id, "kind": kind, "characters": len(body)}
                for fact_id, kind, body, *_ in sorted(
                    candidates, key=lambda row: (-len(row[2]), row[0])
                )[:5]
            ],
        }


def main() -> None:
    poc_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=poc_root / "build/knowledge.sqlite")
    parser.add_argument("--source-root", type=Path, default=poc_root.parents[1])
    options = parser.parse_args()
    print(json.dumps(audit(options.database, options.source_root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
