"""Lint and seed controlled Formly knowledge sources."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

from .structured_source import build_sources, lint_sources


POC_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = POC_ROOT.parents[1]
AUTHORED = POC_ROOT / "authored"
CATALOG = POC_ROOT / "corpus" / "evidence-catalog.json"
DATABASE = POC_ROOT / "build" / "knowledge.sqlite"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("lint", "build", "all", "inspect"))
    arguments = parser.parse_args()

    if arguments.command in {"lint", "all"}:
        errors = lint_sources(AUTHORED, REPO_ROOT, CATALOG)
        if errors:
            raise SystemExit("\n".join(errors))
        print(f"Validated {len(list(AUTHORED.glob('*.json')))} authored source files")

    if arguments.command in {"build", "all"}:
        build_sources(AUTHORED, REPO_ROOT, CATALOG, DATABASE)
        print(f"Seeded {DATABASE}")

    if arguments.command == "inspect":
        with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute("""
                SELECT f.id, f.claim, f.conditions_json, f.limits_json, f.context,
                       d.formly_version, d.adapter, d.source_path,
                       f.source_start_offset, f.source_end_offset,
                       (SELECT group_concat(evidence_id, ',') FROM fact_evidence
                        WHERE fact_id=f.id) AS evidence_ids
                FROM facts f JOIN documents d ON d.id=f.doc_id ORDER BY f.id
            """).fetchall()
            print(json.dumps([dict(row) for row in rows], indent=2))


if __name__ == "__main__":
    main()
