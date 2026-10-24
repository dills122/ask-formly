import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from kbcompiler.pipeline import build, import_catalog, import_sources, lint_corpus


SOURCE = """# Configuration and model

Scope: source-checked at 6.3.12.

## Defaults and resets

A default applies when a keyed value is undefined [K05](sources.md#k05).

```ts
// ## This is not a heading.
{ key: 'city', defaultValue: 'Toronto' }
```

## Props and registrations

| Setting | Purpose |
| --- | --- |
| `type` | Selects a registered type [K04](sources.md#k04) |
"""


def setup_source(root: Path, text: str = SOURCE) -> tuple[Path, Path]:
    source = root / "source.md"
    source.write_text(text, encoding="utf-8")
    upstream = root / "evidence.json"
    upstream.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "baseline": "6.3.12",
                "records": [
                    {"id": "K04", "url": "https://example.test/k04"},
                    {"id": "K05", "url": "https://example.test/k05"},
                ],
            }
        ),
        encoding="utf-8",
    )
    examples = root / "examples.md"
    examples.write_text("# Examples\n", encoding="utf-8")
    catalog = root / "catalog.json"
    import_catalog(upstream, examples, catalog, base_dir=root)
    return source, catalog


def manifest(source: Path) -> dict:
    return {
        "schema_version": 1,
        "documents": [
            {
                "id": "formly.configuration",
                "source": str(source),
                "kind": "guide",
                "formly_version": "6.3.12",
                "adapter": "core",
            }
        ],
    }


class PipelineTests(unittest.TestCase):
    def test_code_fence_citation_does_not_count_as_support(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, "# X\n\n## Y\n\n```md\n[K05](sources.md#k05)\n```\n")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                self.assertEqual("unresolved", connection.execute("SELECT support_status FROM units").fetchone()[0])

    def test_reference_style_citation_target_is_validated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, "# X\n\n## Y\n\nClaim [K05][support].\n\n[support]: examples.md#wrong\n")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            self.assertTrue(any("invalid citation" in e for e in lint_corpus(corpus, catalog)))

    def test_reimport_removes_documents_no_longer_in_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            alpha, _ = setup_source(root)
            beta = root / "beta.md"
            beta.write_text("# Beta\n\n## Topic\n\nText.\n", encoding="utf-8")
            corpus = root / "corpus"
            first = manifest(alpha)
            first["documents"].append({
                "id": "formly.beta", "source": str(beta), "kind": "guide",
                "formly_version": "6.3.12", "adapter": "core",
            })
            import_sources(first, corpus)
            import_sources(manifest(alpha), corpus)
            self.assertEqual(["formly.configuration.md"], sorted(path.name for path in corpus.glob("*.md")))

    def test_lint_rejects_citation_with_wrong_target_or_anchor(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, "# X\n\n## Y\n\nClaim [K05](examples.md#wrong).\n")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            self.assertTrue(any("invalid citation" in error for error in lint_corpus(corpus, catalog)))

    def test_example_catalog_uses_relative_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            setup_source(root)
            upstream = root / "evidence.json"
            examples = root / "examples.md"
            examples.write_text("# Examples\n\n## E08\n\nVisibility.\n", encoding="utf-8")
            catalog = root / "catalog.json"
            import_catalog(upstream, examples, catalog, base_dir=root)
            item = next(x for x in json.loads(catalog.read_text(encoding="utf-8"))["records"] if x["id"] == "E08")
            self.assertEqual("examples.md", item["source_path"])

    def test_example_catalog_and_nested_headings_are_compiled_without_empty_parent_unit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, _ = setup_source(root, """# Visibility

## Expressions

### Hide a field

Use a visibility expression [K05](sources.md#k05) and inspect the
official example [E08](examples.md#e08).
""")
            examples = root / "examples.md"
            examples.write_text("# Examples\n\n## E08\n\nVisibility example.\n", encoding="utf-8")
            catalog = root / "catalog.json"
            import_catalog(root / "evidence.json", examples, catalog, base_dir=root)
            example_record = next(
                item for item in json.loads(catalog.read_text(encoding="utf-8"))["records"]
                if item["id"] == "E08"
            )
            self.assertIn("Visibility example.", example_record["body_md"])
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            self.assertEqual([], lint_corpus(corpus, catalog))
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                units = connection.execute("SELECT id FROM units ORDER BY ordinal").fetchall()
                citations = connection.execute(
                    "SELECT evidence_id FROM unit_evidence ORDER BY evidence_id"
                ).fetchall()
                support = connection.execute("SELECT support_status FROM units").fetchone()[0]
            self.assertEqual([("formly.configuration.expressions.hide-a-field",)], units)
            self.assertEqual([("E08",), ("K05",)], citations)
            self.assertEqual("direct", support)

    def test_table_led_section_gets_extractively_generated_headmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Expressions

## Callback contracts

| API | Contract |
| --- | --- |
| `expressions` | Receives a field [K05](sources.md#k05) |
| Legacy `hideExpression` | Receives model state [K04](sources.md#k04) |

Evidence: declarations [K05](sources.md#k05).
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                about = connection.execute("SELECT about FROM units").fetchone()[0]
            self.assertIn("expressions", about)
            self.assertIn("hideExpression", about)
            self.assertNotIn("Evidence: declarations", about)

    def test_lint_rejects_unclosed_fence_in_imported_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, """# Defaults

## Static values

```ts
{ defaultValue: 1 }
""")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            self.assertTrue(any("unclosed code fence" in error for error in lint_corpus(corpus, catalog)))

    def test_uncited_unit_is_explicitly_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root, "# Topic\n\n## A note\n\nA useful note.\n")
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                status = connection.execute("SELECT support_status FROM units").fetchone()[0]
            self.assertEqual("unresolved", status)

    def test_import_preserves_source_body_and_generates_routing_headmatter(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"

            import_sources(manifest(source), corpus)
            generated = (corpus / "formly.configuration.md").read_text(encoding="utf-8")

            self.assertTrue(generated.startswith("---\n"))
            self.assertIn("id: formly.configuration", generated)
            self.assertIn("about:", generated)
            self.assertIn("Defaults and resets", generated.split("---\n", 2)[1])
            self.assertTrue(generated.endswith(SOURCE))
            self.assertEqual([], lint_corpus(corpus, catalog))

    def test_compiler_splits_on_real_headings_and_preserves_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)

            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            with sqlite3.connect(database) as connection:
                rows = connection.execute(
                    "SELECT heading, body_md, about, source_start_line, source_end_line "
                    "FROM units ORDER BY ordinal"
                ).fetchall()
                links = connection.execute(
                    "SELECT unit_id, evidence_id FROM unit_evidence ORDER BY unit_id, evidence_id"
                ).fetchall()

            self.assertEqual(2, len(rows))
            self.assertEqual("Defaults and resets", rows[0][0])
            self.assertIn("// ## This is not a heading.", rows[0][1])
            self.assertIn("Props and registrations", rows[1][0])
            self.assertIn("| `type` |", rows[1][1])
            self.assertIn("Defaults and resets", rows[0][2])
            self.assertEqual((5, 13), rows[0][3:5])
            self.assertEqual(
                [("formly.configuration.defaults-and-resets", "K05"),
                 ("formly.configuration.props-and-registrations", "K04")],
                links,
            )

    def test_invalid_evidence_fails_without_replacing_previous_database(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, catalog = setup_source(root)
            corpus = root / "corpus"
            import_sources(manifest(source), corpus)
            database = root / "knowledge.sqlite"
            build(corpus, catalog, database)
            original = database.read_bytes()

            doc = corpus / "formly.configuration.md"
            doc.write_text(doc.read_text(encoding="utf-8").replace("[K05]", "[K99]"), encoding="utf-8")
            errors = lint_corpus(corpus, catalog)
            self.assertTrue(any("K99" in error for error in errors))
            with self.assertRaises(ValueError):
                build(corpus, catalog, database)
            self.assertEqual(original, database.read_bytes())


if __name__ == "__main__":
    unittest.main()
