"""Deterministic proposals must preserve source and expose unresolved blocks."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from kbcompiler.pipeline import build, import_sources
from kbcompiler.trial_audit import audit
from test_pipeline import manifest, setup_source


class FactProposalTests(unittest.TestCase):
    def _build(self, root: Path, text: str) -> tuple[Path, Path]:
        source, catalog = setup_source(root, text)
        corpus = root / "corpus"
        import_sources(manifest(source), corpus)
        database = root / "knowledge.sqlite"
        build(corpus, catalog, database)
        return source, database

    def test_table_rows_propose_exact_source_without_promoting_prose_or_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, database = self._build(root, """# Configuration

## Mechanisms

| Mechanism | Use when | Evidence |
| --- | --- | --- |
| Type | Render a control | [K05](sources.md#k05) |
| Wrapper | Decorate a field | [K04](sources.md#k04) |

This paragraph mixes two claims and a caveat [K05](sources.md#k05).

```ts
const example = true;
```
""")
            with sqlite3.connect(database) as connection:
                rows = connection.execute("""
                    SELECT p.kind, p.subject_md, p.statement_md, p.source_quote,
                           p.source_start_offset, p.source_end_offset, p.status,
                           v.formly_version, v.adapter
                    FROM fact_proposals p
                    JOIN fact_candidates f ON f.id=p.candidate_id
                    JOIN concept_variants v ON v.id=f.variant_id
                    ORDER BY p.id
                """).fetchall()
                links = connection.execute("""
                    SELECT p.subject_md, e.evidence_id
                    FROM fact_proposals p JOIN proposal_evidence e ON e.proposal_id=p.id
                    ORDER BY p.id
                """).fetchall()
            self.assertEqual(2, len(rows))
            self.assertEqual(["Type", "Wrapper"], [row[1] for row in rows])
            self.assertEqual(["Render a control", "Decorate a field"], [row[2] for row in rows])
            self.assertEqual([("Type", "K05"), ("Wrapper", "K04")], links)
            source_text = source.read_text(encoding="utf-8")
            for kind, _, _, quote, start, end, status, version, adapter in rows:
                self.assertEqual("table_row", kind)
                self.assertEqual(quote, source_text[start:end])
                self.assertEqual(("proposal", "6.3.12", "core"), (status, version, adapter))
            result = audit(database, root)
            self.assertEqual(2, result["proposals"])
            self.assertEqual(2, result["unresolved_candidates"])
            self.assertEqual(0, result["verified_atomic_facts"])
            self.assertEqual(result["candidates"], len(result["candidate_dispositions"]))
            self.assertEqual({"fence": 1, "paragraph": 1}, result["unresolved_by_kind"])
            self.assertFalse(result["promotion_gate_met"])

    def test_explicit_fact_items_keep_conditions_exceptions_and_own_citations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, database = self._build(root, """# Configuration

## Explicit facts

- Fact: A default applies to undefined values [K05](sources.md#k05).
  Condition: The field is eligible for defaulting.
  Exception: An existing null is retained.
- Fact: A type name resolves through registration [K04](sources.md#k04).
""")
            with sqlite3.connect(database) as connection:
                rows = connection.execute("""
                    SELECT statement_md, condition_md, exception_md, source_quote,
                           source_start_offset, source_end_offset
                    FROM fact_proposals ORDER BY ordinal
                """).fetchall()
                links = connection.execute("""
                    SELECT p.ordinal, e.evidence_id FROM proposal_evidence e
                    JOIN fact_proposals p ON p.id=e.proposal_id ORDER BY p.ordinal
                """).fetchall()
            self.assertEqual(2, len(rows))
            self.assertIn("undefined values", rows[0][0])
            self.assertEqual("The field is eligible for defaulting.", rows[0][1])
            self.assertEqual("An existing null is retained.", rows[0][2])
            self.assertIsNone(rows[1][1])
            self.assertIsNone(rows[1][2])
            self.assertEqual([(0, "K05"), (1, "K04")], links)
            source_text = source.read_text(encoding="utf-8")
            for _, _, _, quote, start, end in rows:
                self.assertEqual(quote, source_text[start:end])

    def test_ordinary_or_mixed_list_is_unresolved_not_misread_as_fact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, database = self._build(root, """# Configuration

## Notes

- A normal bullet [K05](sources.md#k05).
- Fact: One explicit item [K04](sources.md#k04).
""")
            result = audit(database, root)
            self.assertEqual(0, result["proposals"])
            self.assertEqual(1, result["unresolved_candidates"])

    def test_rebuild_produces_identical_proposals(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, database = self._build(root, """# Configuration

## Mechanisms

| Mechanism | Use when |
| --- | --- |
| Type | Render a control [K05](sources.md#k05) |
""")
            with sqlite3.connect(database) as connection:
                before = connection.execute("SELECT * FROM fact_proposals").fetchall()
            build(root / "corpus", root / "catalog.json", database)
            with sqlite3.connect(database) as connection:
                after = connection.execute("SELECT * FROM fact_proposals").fetchall()
            self.assertEqual(before, after)

    def test_audit_rejects_changed_proposal_statement_and_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, database = self._build(root, """# Configuration

## Mechanisms

| Mechanism | Use when |
| --- | --- |
| Type | Render a control [K05](sources.md#k05) |
""")
            with sqlite3.connect(database) as connection:
                connection.execute("UPDATE fact_proposals SET statement_md='Invented behavior'")
            with self.assertRaisesRegex(ValueError, "proposal fields differ"):
                audit(database, root)

            build(root / "corpus", root / "catalog.json", database)
            with sqlite3.connect(database) as connection:
                connection.execute("UPDATE proposal_evidence SET evidence_id='K04'")
            with self.assertRaisesRegex(ValueError, "proposal evidence differs"):
                audit(database, root)


if __name__ == "__main__":
    unittest.main()
