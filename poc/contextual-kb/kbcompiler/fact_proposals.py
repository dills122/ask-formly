"""Extract only explicitly structured fact proposals from exact source blocks.

The output is a proposal for evaluation, never an approved semantic fact.
Mixed prose, examples, and ambiguous lists return no proposals.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


FACT_LINE = re.compile(r"^- Fact: (\S.*)\s*$")
CONDITION_LINE = re.compile(r"^  Condition: (\S.*)\s*$")
EXCEPTION_LINE = re.compile(r"^  Exception: (\S.*)\s*$")


@dataclass(frozen=True)
class FactProposal:
    kind: str
    subject_md: str | None
    statement_md: str
    condition_md: str | None
    exception_md: str | None
    source_quote: str
    local_start_offset: int
    local_end_offset: int


def _cells(row: str) -> list[str]:
    """Read simple Markdown table cells; return nothing on ambiguous structure."""
    line = row.strip()
    if not line.startswith("|"):
        return []
    line = line[1:-1] if line.endswith("|") else line[1:]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for character in line:
        if escaped:
            current.append(character)
            escaped = False
        elif character == "\\":
            current.append(character)
            escaped = True
        elif character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
    cells.append("".join(current).strip())
    return cells if 2 <= len(cells) <= 3 and cells[0] and cells[1] else []


def _explicit_list(body: str) -> list[FactProposal]:
    lines = body.splitlines(keepends=True)
    if not lines:
        return []
    starts: list[int] = []
    offsets: list[int] = []
    offset = 0
    for index, line in enumerate(lines):
        offsets.append(offset)
        offset += len(line)
        if FACT_LINE.fullmatch(line.rstrip("\r\n")):
            starts.append(index)
    if not starts or starts[0] != 0:
        return []

    proposals: list[FactProposal] = []
    for position, first in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        statement = FACT_LINE.fullmatch(lines[first].rstrip("\r\n"))
        if statement is None:
            return []
        condition = None
        exception = None
        for line in lines[first + 1:end]:
            content = line.rstrip("\r\n")
            if not content.strip():
                continue
            condition_match = CONDITION_LINE.fullmatch(content)
            exception_match = EXCEPTION_LINE.fullmatch(content)
            if condition_match and condition is None:
                condition = condition_match.group(1)
            elif exception_match and exception is None:
                exception = exception_match.group(1)
            else:
                return []
        quote = "".join(lines[first:end])
        proposals.append(FactProposal(
            "explicit_fact", None, statement.group(1), condition, exception,
            quote, offsets[first], offsets[end] if end < len(offsets) else len(body),
        ))
    return proposals


def propose_from_block(kind: str, body_md: str) -> list[FactProposal]:
    """Produce extractive proposals only when a block declares its structure."""
    if kind == "table_row":
        cells = _cells(body_md)
        if not cells:
            return []
        return [FactProposal(
            "table_row", cells[0], cells[1], None, None,
            body_md, 0, len(body_md),
        )]
    if kind == "list":
        return _explicit_list(body_md)
    return []
