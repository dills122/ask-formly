"""Source-anchored fact-candidate trial; candidates are not approved claims."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from kbcompiler.pipeline import build, import_sources
from kbcompiler.trial_audit import audit
from test_pipeline import manifest, setup_source


class FactTrialTests(unittest.TestCase):
    def test_two_prose_blocks_get_distinct_candidates_under_one_versioned_concept(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Configuration

## Defaults and resets

A default applies to undefined values [K05](sources.md#k05).

Resetting restores the baseline [K04](sources.md#k04).
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)

            with sqlite3.connect(database) as connection:
                concept = connection.execute("SELECT id, title FROM concepts").fetchone()
                variant = connection.execute(
                    "SELECT concept_id, formly_version, adapter FROM concept_variants"
                ).fetchone()
                facts = connection.execute(
                    "SELECT block_kind, body_md, source_start_line, source_end_line, status "
                    "FROM fact_candidates ORDER BY ordinal"
                ).fetchall()
                links = connection.execute(
                    "SELECT e.evidence_id FROM fact_evidence e JOIN fact_candidates f ON f.id=e.fact_id "
                    "ORDER BY f.ordinal"
                ).fetchall()

            self.assertEqual(("formly.configuration.defaults-and-resets", "Defaults and resets"), concept)
            self.assertEqual((concept[0], "6.3.12", "core"), variant)
            self.assertEqual(2, len(facts))
            self.assertEqual(["paragraph", "paragraph"], [row[0] for row in facts])
            self.assertTrue(facts[0][1].startswith("A default applies"))
            self.assertTrue(facts[1][1].startswith("Resetting restores"))
            self.assertEqual(["candidate", "candidate"], [row[4] for row in facts])
            self.assertEqual([("K05",), ("K04",)], links)
            lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
            for _, body, first, last, _ in facts:
                self.assertEqual(body, "".join(lines[first - 1:last]))

    def test_table_rows_and_fenced_example_remain_exact_source_spans(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Expressions

## Contracts

| Form | Meaning |
| --- | --- |
| `props.disabled` | Current field [K05](sources.md#k05) |
| `hide` | Visibility [K04](sources.md#k04) |

```ts
const value = {

  hide: true,
};
```
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                facts = connection.execute(
                    "SELECT block_kind, body_md, context_text, source_start_line, source_end_line "
                    "FROM fact_candidates ORDER BY ordinal"
                ).fetchall()
            self.assertEqual(["table_row", "table_row", "fence"], [row[0] for row in facts])
            self.assertTrue(all("Form | Meaning" in row[2] for row in facts[:2]))
            self.assertIn("\n\n  hide: true", facts[2][1])
            lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
            for _, body, _, first, last in facts:
                self.assertEqual(body, "".join(lines[first - 1:last]))

    def test_table_like_paragraph_keeps_following_prose(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Configuration

## A table

| API | Meaning |
| --- | --- |
| props | Values [K05](sources.md#k05) |
This qualification must remain in a candidate [K04](sources.md#k04).
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                rows = connection.execute(
                    "SELECT block_kind, body_md FROM fact_candidates ORDER BY ordinal"
                ).fetchall()
                links = connection.execute(
                    "SELECT f.block_kind, e.evidence_id FROM fact_evidence e "
                    "JOIN fact_candidates f ON f.id=e.fact_id ORDER BY f.ordinal"
                ).fetchall()
            self.assertEqual(["table_row", "paragraph"], [row[0] for row in rows])
            self.assertIn("qualification", rows[1][1])
            self.assertEqual([("table_row", "K05"), ("paragraph", "K04")], links)
            self.assertEqual(2, audit(database, root)["candidates"])

    def test_table_row_reference_style_citation_uses_document_definition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Configuration

## A table

| API | Meaning |
| --- | --- |
| props | Values [K05][support] |

[support]: sources.md#k05
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                links = connection.execute(
                    "SELECT e.evidence_id FROM fact_evidence e JOIN fact_candidates f ON f.id=e.fact_id "
                    "WHERE f.block_kind='table_row'"
                ).fetchall()
            self.assertEqual([("K05",)], links)
            self.assertEqual(1, audit(database, root)["evidence_links"])

    def test_fact_relation_schema_rejects_missing_targets_and_unknown_kinds(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                connection.execute("PRAGMA foreign_keys=ON")
                fact_id = connection.execute("SELECT id FROM fact_candidates LIMIT 1").fetchone()[0]
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("INSERT INTO fact_relations VALUES (?, ?, ?)",
                                       (fact_id, "does-not-exist", "requires_context"))
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("INSERT INTO fact_relations VALUES (?, ?, ?)",
                                       (fact_id, fact_id, "loosely_related"))

    def test_audit_checks_all_candidate_spans_and_detects_source_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)

            result = audit(database, root)
            self.assertEqual(1, result["documents"])
            self.assertEqual(result["candidates"], result["verified_source_spans"])
            self.assertEqual(0, result["semantic_relations"])
            source.write_text(source.read_text(encoding="utf-8") + "Changed.\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source hash differs"):
                audit(database, root)

    def test_audit_rejects_stored_citation_that_differs_from_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                connection.execute("UPDATE fact_evidence SET evidence_id='K04' WHERE evidence_id='K05'")
            with self.assertRaisesRegex(ValueError, "evidence links differ"):
                audit(database, root)

    def test_audit_rejects_uncovered_substantive_source_line(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                fact_id = connection.execute(
                    "SELECT id FROM fact_candidates WHERE block_kind='paragraph' LIMIT 1"
                ).fetchone()[0]
                connection.execute("DELETE FROM fact_evidence WHERE fact_id=?", (fact_id,))
                connection.execute("DELETE FROM fact_candidates WHERE id=?", (fact_id,))
            with self.assertRaisesRegex(ValueError, "uncovered source line"):
                audit(database, root)


if __name__ == "__main__":
    unittest.main()
