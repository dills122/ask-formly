"""Import Formly knowledge as uniform documents and compile extractive units."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

from .fact_trial import split_candidate_blocks
from .fact_proposals import propose_from_block


PARSER = MarkdownIt("commonmark")
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$")
EVIDENCE_ID_PATTERN = re.compile(r"[KE]\d+")
REQUIRED = ("id", "title", "kind", "formly_version", "adapter", "about", "source_path", "source_sha256")
KINDS = {"guide", "reference", "troubleshooting"}


@dataclass(frozen=True)
class Section:
    level: int
    title: str
    start: int  # zero-based source line


@dataclass(frozen=True)
class Unit:
    id: str
    doc_id: str
    ordinal: int
    heading: str
    heading_path: str
    about: str
    body_md: str
    source_start_line: int
    source_end_line: int
    evidence_ids: tuple[str, ...]


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _valid_citation(evidence_id: str, target: str) -> bool:
    expected_file = "sources.md" if evidence_id.startswith("K") else "examples.md"
    return target == f"{expected_file}#{evidence_id.lower()}"


def _citations(body: str, environment: dict | None = None) -> list[tuple[int, str, str]]:
    """Find rendered evidence links, including reference links, outside code tokens."""
    citations: list[tuple[int, str, str]] = []
    for token in PARSER.parse(body, environment if environment is not None else {}):
        if token.type != "inline" or token.map is None or not token.children:
            continue
        children = token.children
        for index, child in enumerate(children):
            if child.type != "link_open":
                continue
            closing = next((end for end in range(index + 1, len(children))
                            if children[end].type == "link_close"), len(children))
            label = "".join(part.content for part in children[index + 1:closing]
                            if part.type in {"text", "code_inline"})
            if EVIDENCE_ID_PATTERN.fullmatch(label):
                citations.append((token.map[0], label, child.attrGet("href") or ""))
    return citations


def _citation_ids(citations: list[tuple[int, str, str]], start: int, end: int) -> tuple[str, ...]:
    return tuple(sorted({evidence_id for line, evidence_id, target in citations
                         if start <= line < end and _valid_citation(evidence_id, target)}))


def _headings(body: str) -> list[Section]:
    tokens = PARSER.parse(body)
    sections: list[Section] = []
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or token.map is None:
            continue
        level = int(token.tag[1:])
        title = tokens[index + 1].content.strip()
        sections.append(Section(level, title, token.map[0]))
    return sections


def _unclosed_fences(body: str) -> list[int]:
    lines = body.splitlines()
    unclosed: list[int] = []
    for token in PARSER.parse(body):
        if token.type != "fence" or token.map is None:
            continue
        opening = token.markup
        last = lines[token.map[1] - 1].strip() if token.map[1] else ""
        if not re.fullmatch(re.escape(opening[0]) + "{" + str(len(opening)) + r",}\s*", last):
            unclosed.append(token.map[0] + 1)
    return unclosed


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def _document_about(title: str, headings: list[Section]) -> str:
    topics = [heading.title for heading in headings if heading.level == 2]
    if not topics:
        return f"Use for questions about {title}."
    return f"Use for questions about {title}: {', '.join(topics)}."


def _table_topics(body: str) -> list[str]:
    rows = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    if len(rows) < 3:
        return []
    topics: list[str] = []
    for row in rows[2:8]:
        first = row.strip("|").split("|", 1)[0].strip()
        if first and not re.fullmatch(r"[-: ]+", first):
            topics.append(first)
    return topics


def _unit_about(title: str, heading_path: str, body: str) -> str:
    # Routing description is extractive: title/path plus the first prose sentence.
    table_topics = _table_topics(body)
    if table_topics:
        return f"Use for questions about {title} > {heading_path}; covers {', '.join(table_topics)}."
    lead = ""
    for line in body.splitlines()[1:]:
        candidate = line.strip()
        if not candidate or candidate.startswith(("|", "```", "~~~", "#", "<!--")):
            continue
        if candidate.startswith(("Scope:", "Baseline:", "Evidence:", "[", "- ", "* ")):
            continue
        lead = re.sub(r"\[((?:K|E)\d+)\]\([^)]+\)", "", candidate).strip()
        break
    if lead:
        lead = lead.split(". ", 1)[0].rstrip(".") + "."
        if len(lead) > 240:
            lead = ""
    return f"Use for questions about {title} > {heading_path}." + (f" {lead}" if lead else "")


def _read_document(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    try:
        _, raw_metadata, body = text.split("---\n", 2)
    except ValueError as error:
        raise ValueError("unterminated YAML frontmatter") from error
    metadata = yaml.safe_load(raw_metadata)
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    return metadata, body


def _catalog_payload(upstream: Path, examples: Path, base_dir: Path | None) -> dict:
    upstream_bytes = upstream.read_bytes()
    examples_bytes = examples.read_bytes()
    source = json.loads(upstream_bytes.decode("utf-8"))
    if source.get("schema_version") != 1 or not isinstance(source.get("records"), list):
        raise ValueError("unsupported upstream evidence catalog")
    records = list(source["records"])
    examples_text = examples_bytes.decode("utf-8")
    example_lines = examples_text.splitlines(keepends=True)
    example_headings = _headings(examples_text)
    for index, heading in enumerate(example_headings):
        if heading.level == 2 and re.fullmatch(r"E\d+", heading.title):
            following = (
                candidate.start for candidate in example_headings[index + 1:]
                if candidate.level <= 2
            )
            end = next(following, len(example_lines))
            records.append({
                "id": heading.title,
                "kind": "example",
                "source_path": str(examples.relative_to(base_dir)) if base_dir else str(examples),
                "source_sha256": _digest(examples_bytes),
                "source_start_line": heading.start + 1,
                "source_end_line": end,
                "body_md": "".join(example_lines[heading.start:end]),
            })
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate evidence id")
    return {
        "schema_version": 1,
        "baseline": source["baseline"],
        "records": sorted(records, key=lambda item: item["id"]),
        "source_inputs": {
            "upstream_path": str(upstream.relative_to(base_dir)) if base_dir else str(upstream),
            "upstream_sha256": _digest(upstream_bytes),
            "examples_path": str(examples.relative_to(base_dir)) if base_dir else str(examples),
            "examples_sha256": _digest(examples_bytes),
        },
    }


def import_catalog(upstream: Path, examples: Path, output: Path,
                   base_dir: Path | None = None) -> None:
    """Copy pinned K records and catalog example IDs from authored Formly data."""
    payload = _catalog_payload(upstream, examples, base_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def import_sources(manifest: dict, corpus: Path, base_dir: Path | None = None) -> None:
    """Copy only manifest-selected knowledge text; generate uniform metadata."""
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("documents"), list):
        raise ValueError("unsupported import manifest")
    seen: set[str] = set()
    generated: dict[str, str] = {}
    for item in manifest["documents"]:
        doc_id = item.get("id")
        if not isinstance(doc_id, str) or not ID_PATTERN.fullmatch(doc_id) or doc_id in seen:
            raise ValueError(f"invalid or duplicate document id: {doc_id}")
        seen.add(doc_id)
        if item.get("kind") not in KINDS:
            raise ValueError(f"invalid kind for {doc_id}")
        source = Path(item["source"])
        if base_dir is not None and not source.is_absolute():
            source = base_dir / source
        source = source.resolve()
        raw = source.read_bytes()
        body = raw.decode("utf-8")
        headings = _headings(body)
        if not headings or headings[0].level != 1:
            raise ValueError(f"{source}: expected H1 title")
        title = headings[0].title
        metadata = {
            "id": doc_id,
            "title": title,
            "kind": item["kind"],
            "formly_version": str(item["formly_version"]),
            "adapter": item["adapter"],
            "about": _document_about(title, headings),
            "source_path": item["source"],
            "source_sha256": _digest(raw),
        }
        prefix = "---\n" + yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True) + "---\n"
        generated[f"{doc_id}.md"] = prefix + body
    corpus.mkdir(parents=True, exist_ok=True)
    for name, content in generated.items():
        (corpus / name).write_text(content, encoding="utf-8")
    for path in corpus.glob("*.md"):
        if path.name not in generated:
            path.unlink()


def _units(metadata: dict, body: str) -> list[Unit]:
    headings = _headings(body)
    citations = _citations(body)
    lines = body.splitlines(keepends=True)
    doc_id = metadata["id"]
    title = metadata["title"]
    section_headings = [h for h in headings if h.level >= 2]
    if not section_headings:
        return []

    units: list[Unit] = []
    first = section_headings[0].start
    h1_end = headings[0].start + 1
    introduction = "".join(lines[h1_end:first])
    substantive_intro = [
        line.strip() for line in introduction.splitlines()
        if line.strip() and not line.startswith(("Scope:", "Baseline:"))
    ]
    if substantive_intro:
        intro_body = "".join(lines[h1_end:first])
        intro_topics = _table_topics(intro_body)
        intro_about = f"Use for an overview of {title}"
        if intro_topics:
            intro_about += f"; covers {', '.join(intro_topics)}"
        units.append(Unit(
            f"{doc_id}.overview", doc_id, 0, "Overview", title,
            intro_about + ".", intro_body, h1_end + 1, first,
            _citation_ids(citations, h1_end, first),
        ))

    ancestors: dict[int, str] = {}
    for index, section in enumerate(section_headings):
        for level in tuple(ancestors):
            if level >= section.level:
                del ancestors[level]
        ancestors[section.level] = section.title
        heading_path = " > ".join(ancestors[level] for level in sorted(ancestors))
        end = section_headings[index + 1].start if index + 1 < len(section_headings) else len(lines)
        part = "".join(lines[section.start:end])
        if not "".join(lines[section.start + 1:end]).strip():
            continue
        slug = ".".join(_slug(ancestors[level]) for level in sorted(ancestors))
        units.append(Unit(
            f"{doc_id}.{slug}", doc_id, len(units), section.title, heading_path,
            _unit_about(title, heading_path, part), part, section.start + 1, end,
            _citation_ids(citations, section.start, end),
        ))
    return units


def lint_corpus(corpus: Path, catalog: Path) -> list[str]:
    errors: list[str] = []
    try:
        evidence = json.loads(catalog.read_text(encoding="utf-8"))
        if evidence.get("schema_version") != 1 or not isinstance(evidence.get("records"), list):
            raise ValueError("unsupported evidence catalog")
        known_ids = {record["id"] for record in evidence["records"]}
        baseline = str(evidence["baseline"])
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [f"invalid evidence catalog: {error}"]
    seen_docs: set[str] = set()
    seen_units: set[str] = set()
    paths = sorted(corpus.glob("*.md"))
    if not paths:
        return ["corpus has no documents"]
    for path in paths:
        try:
            metadata, body = _read_document(path)
            for key in REQUIRED:
                if not isinstance(metadata.get(key), str) or not metadata[key].strip():
                    errors.append(f"{path.name}: missing or invalid {key}")
            if any(key not in metadata for key in REQUIRED):
                continue
            doc_id = metadata["id"]
            if not ID_PATTERN.fullmatch(doc_id) or doc_id != path.stem or doc_id in seen_docs:
                errors.append(f"{path.name}: invalid or duplicate document id {doc_id}")
            seen_docs.add(doc_id)
            if metadata["kind"] not in KINDS:
                errors.append(f"{path.name}: unsupported kind")
            if metadata["formly_version"] != baseline:
                errors.append(f"{path.name}: version differs from evidence baseline {baseline}")
            if metadata["adapter"] not in {"core", "material", "mixed"}:
                errors.append(f"{path.name}: unsupported adapter")
            headings = _headings(body)
            if not headings or headings[0].level != 1 or sum(h.level == 1 for h in headings) != 1:
                errors.append(f"{path.name}: expected exactly one H1")
                continue
            if headings[0].title != metadata["title"]:
                errors.append(f"{path.name}: title does not match H1")
            if metadata["about"] != _document_about(metadata["title"], headings):
                errors.append(f"{path.name}: generated about is stale")
            if _digest(body.encode("utf-8")) != metadata["source_sha256"]:
                errors.append(f"{path.name}: source body differs from imported hash")
            for line, evidence_id, target in _citations(body):
                if not _valid_citation(evidence_id, target):
                    errors.append(f"{path.name}: invalid citation [{evidence_id}]({target}) at source line {line + 1}")
            for line in _unclosed_fences(body):
                errors.append(f"{path.name}: unclosed code fence at source line {line}")
            if not any(h.level >= 2 for h in headings):
                errors.append(f"{path.name}: no section headings")
            for unit in _units(metadata, body):
                if not ID_PATTERN.fullmatch(unit.id) or unit.id in seen_units:
                    errors.append(f"{path.name}: duplicate or invalid unit id {unit.id}")
                seen_units.add(unit.id)
                for evidence_id in unit.evidence_ids:
                    if evidence_id not in known_ids:
                        errors.append(f"{path.name}: unknown evidence {evidence_id} in {unit.id}")
        except (OSError, ValueError, TypeError, KeyError, IndexError) as error:
            errors.append(f"{path.name}: {error}")
    return errors


def build(corpus: Path, catalog: Path, database: Path) -> None:
    """Validate and atomically replace a compiled SQLite knowledge database."""
    errors = lint_corpus(corpus, catalog)
    if errors:
        raise ValueError("\n".join(errors))
    evidence = json.loads(catalog.read_text(encoding="utf-8"))
    database.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".knowledge-", suffix=".sqlite", dir=database.parent)
    os.close(descriptor)
    try:
        with closing(sqlite3.connect(temporary)) as connection:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.executescript("""
                CREATE TABLE build_info (schema_version INTEGER NOT NULL, input_sha256 TEXT NOT NULL);
                CREATE TABLE documents (
                  id TEXT PRIMARY KEY, title TEXT NOT NULL, kind TEXT NOT NULL,
                  formly_version TEXT NOT NULL, adapter TEXT NOT NULL,
                  about TEXT NOT NULL, source_path TEXT NOT NULL,
                  source_sha256 TEXT NOT NULL, body_md TEXT NOT NULL
                );
                CREATE TABLE units (
                  id TEXT PRIMARY KEY, doc_id TEXT NOT NULL REFERENCES documents(id),
                  ordinal INTEGER NOT NULL, heading TEXT NOT NULL,
                  heading_path TEXT NOT NULL, about TEXT NOT NULL,
                  body_md TEXT NOT NULL, source_start_line INTEGER NOT NULL,
                  source_end_line INTEGER NOT NULL, body_sha256 TEXT NOT NULL,
                  support_status TEXT NOT NULL CHECK(support_status IN ('direct', 'unresolved')),
                  UNIQUE(doc_id, ordinal)
                );
                CREATE TABLE evidence (id TEXT PRIMARY KEY, record_json TEXT NOT NULL);
                CREATE TABLE unit_evidence (
                  unit_id TEXT NOT NULL REFERENCES units(id),
                  evidence_id TEXT NOT NULL REFERENCES evidence(id),
                  PRIMARY KEY(unit_id, evidence_id)
                );
                CREATE TABLE concepts (
                  id TEXT PRIMARY KEY,
                  doc_id TEXT NOT NULL REFERENCES documents(id),
                  title TEXT NOT NULL,
                  heading_path TEXT NOT NULL
                );
                CREATE TABLE concept_variants (
                  id TEXT PRIMARY KEY,
                  concept_id TEXT NOT NULL REFERENCES concepts(id),
                  formly_version TEXT NOT NULL,
                  adapter TEXT NOT NULL,
                  UNIQUE(concept_id, formly_version, adapter)
                );
                CREATE TABLE fact_candidates (
                  id TEXT PRIMARY KEY,
                  variant_id TEXT NOT NULL REFERENCES concept_variants(id),
                  ordinal INTEGER NOT NULL,
                  block_kind TEXT NOT NULL,
                  body_md TEXT NOT NULL,
                  context_text TEXT NOT NULL,
                  source_start_line INTEGER NOT NULL,
                  source_end_line INTEGER NOT NULL,
                  body_sha256 TEXT NOT NULL,
                  status TEXT NOT NULL CHECK(status = 'candidate'),
                  UNIQUE(variant_id, ordinal)
                );
                CREATE TABLE fact_evidence (
                  fact_id TEXT NOT NULL REFERENCES fact_candidates(id),
                  evidence_id TEXT NOT NULL REFERENCES evidence(id),
                  PRIMARY KEY(fact_id, evidence_id)
                );
                CREATE TABLE fact_relations (
                  source_fact_id TEXT NOT NULL REFERENCES fact_candidates(id),
                  target_fact_id TEXT NOT NULL REFERENCES fact_candidates(id),
                  kind TEXT NOT NULL CHECK(kind IN ('requires_context', 'example_of')),
                  PRIMARY KEY(source_fact_id, target_fact_id, kind)
                );
                CREATE TABLE fact_proposals (
                  id TEXT PRIMARY KEY,
                  candidate_id TEXT NOT NULL REFERENCES fact_candidates(id),
                  ordinal INTEGER NOT NULL,
                  kind TEXT NOT NULL CHECK(kind IN ('table_row', 'explicit_fact')),
                  subject_md TEXT,
                  statement_md TEXT NOT NULL,
                  condition_md TEXT,
                  exception_md TEXT,
                  source_quote TEXT NOT NULL,
                  source_start_offset INTEGER NOT NULL,
                  source_end_offset INTEGER NOT NULL,
                  status TEXT NOT NULL CHECK(status='proposal'),
                  UNIQUE(candidate_id, ordinal)
                );
                CREATE TABLE proposal_evidence (
                  proposal_id TEXT NOT NULL REFERENCES fact_proposals(id),
                  evidence_id TEXT NOT NULL REFERENCES evidence(id),
                  PRIMARY KEY(proposal_id, evidence_id)
                );
                CREATE INDEX units_by_doc ON units(doc_id, ordinal);
                CREATE INDEX facts_by_variant ON fact_candidates(variant_id, ordinal);
                CREATE INDEX fact_evidence_by_evidence ON fact_evidence(evidence_id);
                CREATE INDEX proposals_by_candidate ON fact_proposals(candidate_id, ordinal);
            """)
            inputs = [catalog.read_bytes()]
            for record in sorted(evidence["records"], key=lambda item: item["id"]):
                connection.execute("INSERT INTO evidence VALUES (?, ?)",
                                   (record["id"], json.dumps(record, sort_keys=True)))
            for path in sorted(corpus.glob("*.md")):
                inputs.append(path.read_bytes())
                metadata, body = _read_document(path)
                connection.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    metadata["id"], metadata["title"], metadata["kind"], metadata["formly_version"],
                    metadata["adapter"], metadata["about"], metadata["source_path"],
                    metadata["source_sha256"], body,
                ))
                citation_environment: dict = {}
                _citations(body, citation_environment)
                line_offsets = [0]
                for line in body.splitlines(keepends=True):
                    line_offsets.append(line_offsets[-1] + len(line))
                for unit in _units(metadata, body):
                    connection.execute("INSERT INTO units VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        unit.id, unit.doc_id, unit.ordinal, unit.heading, unit.heading_path,
                        unit.about, unit.body_md, unit.source_start_line, unit.source_end_line,
                        _digest(unit.body_md.encode("utf-8")),
                        "direct" if unit.evidence_ids else "unresolved",
                    ))
                    for evidence_id in unit.evidence_ids:
                        connection.execute("INSERT INTO unit_evidence VALUES (?, ?)", (unit.id, evidence_id))
                    connection.execute("INSERT INTO concepts VALUES (?, ?, ?, ?)", (
                        unit.id, unit.doc_id, unit.heading, unit.heading_path,
                    ))
                    variant_id = f"{unit.id}@{metadata['formly_version']}/{metadata['adapter']}"
                    connection.execute("INSERT INTO concept_variants VALUES (?, ?, ?, ?)", (
                        variant_id, unit.id, metadata["formly_version"], metadata["adapter"],
                    ))
                    blocks = split_candidate_blocks(
                        unit.body_md, unit.source_start_line, metadata["title"], unit.heading_path,
                    )
                    for ordinal, block in enumerate(blocks):
                        fact_id = f"{variant_id}.b{ordinal:03d}"
                        connection.execute("INSERT INTO fact_candidates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                            fact_id, variant_id, ordinal, block.kind, block.body_md,
                            block.context_text, block.source_start_line, block.source_end_line,
                            _digest(block.body_md.encode("utf-8")), "candidate",
                        ))
                        cited = _citation_ids(
                            _citations(block.body_md, citation_environment),
                            0, len(block.body_md.splitlines()),
                        )
                        for evidence_id in cited:
                            connection.execute("INSERT INTO fact_evidence VALUES (?, ?)", (fact_id, evidence_id))
                        candidate_offset = line_offsets[block.source_start_line - 1]
                        for proposal_ordinal, proposal in enumerate(
                            propose_from_block(block.kind, block.body_md)
                        ):
                            proposal_id = f"{fact_id}.p{proposal_ordinal:02d}"
                            start = candidate_offset + proposal.local_start_offset
                            end = candidate_offset + proposal.local_end_offset
                            if body[start:end] != proposal.source_quote:
                                raise ValueError(f"{proposal_id}: proposal quote differs from source")
                            connection.execute(
                                "INSERT INTO fact_proposals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (proposal_id, fact_id, proposal_ordinal, proposal.kind,
                                 proposal.subject_md, proposal.statement_md,
                                 proposal.condition_md, proposal.exception_md,
                                 proposal.source_quote, start, end, "proposal"),
                            )
                            proposal_citations = _citation_ids(
                                _citations(proposal.source_quote, citation_environment),
                                0, len(proposal.source_quote.splitlines()),
                            )
                            for evidence_id in proposal_citations:
                                connection.execute(
                                    "INSERT INTO proposal_evidence VALUES (?, ?)",
                                    (proposal_id, evidence_id),
                                )
            if connection.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("compiled knowledge contains broken references")
            connection.execute("INSERT INTO build_info VALUES (?, ?)", (4, _digest(b"".join(inputs))))
            connection.commit()
        os.replace(temporary, database)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
