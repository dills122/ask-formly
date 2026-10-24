"""Deterministic source blocks for a fact-candidate seeding trial.

Blocks are candidates, not verified atomic claims. A later trial must assess
whether prose can be split further without detaching necessary qualifications.
"""

from __future__ import annotations

from dataclasses import dataclass

from markdown_it import MarkdownIt


PARSER = MarkdownIt("commonmark")
BLOCK_TYPES = {
    "paragraph_open": "paragraph",
    "fence": "fence",
    "code_block": "code",
    "html_block": "html",
    "blockquote_open": "blockquote",
    "bullet_list_open": "list",
    "ordered_list_open": "list",
}


@dataclass(frozen=True)
class CandidateBlock:
    kind: str
    body_md: str
    context_text: str
    source_start_line: int
    source_end_line: int


def _table_rows(lines: list[str], start: int, end: int) -> list[tuple[int, str]]:
    segment = lines[start:end]
    if len(segment) < 3 or not segment[0].lstrip().startswith("|"):
        return []
    separator = segment[1].strip().strip("|").replace("|", "").replace("-", "").replace(":", "")
    if separator.strip():
        return []
    rows: list[tuple[int, str]] = []
    for index, line in enumerate(segment[2:], 2):
        if not line.lstrip().startswith("|") or not line.strip():
            break
        rows.append((start + index, line))
    return rows


def split_candidate_blocks(body_md: str, source_start_line: int,
                           document_title: str, heading_path: str) -> list[CandidateBlock]:
    """Return exact, non-overlapping source blocks under one heading unit."""
    lines = body_md.splitlines(keepends=True)
    context = f"{document_title} > {heading_path}"
    spans: list[tuple[int, int, str]] = []
    covered: set[int] = set()
    for token in PARSER.parse(body_md):
        if token.level != 0 or token.map is None:
            continue
        first, end = token.map
        if token.type == "heading_open":
            covered.update(range(first, end))
        elif token.type in BLOCK_TYPES:
            spans.append((first, end, BLOCK_TYPES[token.type]))
            covered.update(range(first, end))

    # Reference definitions and other unparsed nonblank lines still need a home.
    for index, line in enumerate(lines):
        if index not in covered and line.strip():
            spans.append((index, index + 1, "unparsed"))

    blocks: list[CandidateBlock] = []
    for first, end, kind in sorted(spans):
        rows = _table_rows(lines, first, end) if kind == "paragraph" else []
        if rows:
            header = lines[first].strip()
            for row_index, row in rows:
                blocks.append(CandidateBlock(
                    "table_row", row, f"{context}; columns: {header}",
                    source_start_line + row_index, source_start_line + row_index,
                ))
            # CommonMark may include immediately following prose in one paragraph
            # token with the table. Retain it as an exact source candidate.
            tail_start = rows[-1][0] + 1
            tail = "".join(lines[tail_start:end])
            if tail.strip():
                blocks.append(CandidateBlock(
                    "paragraph", tail, context,
                    source_start_line + tail_start, source_start_line + end - 1,
                ))
            continue
        content = "".join(lines[first:end])
        if content.strip():
            blocks.append(CandidateBlock(
                kind, content, context,
                source_start_line + first, source_start_line + end - 1,
            ))
    return blocks
