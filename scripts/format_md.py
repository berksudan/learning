#!/usr/bin/env python3
"""Minimal formatter for the learning notes, rewriting files in place.

Rules (fenced code blocks are left untouched):
- No end-of-line whitespace; blank lines are empty.
- Indent with tabs; each run of up to 4 leading spaces becomes one tab.
- Top-level bullets use `+`, nested bullets use `-`.
- A `+` label that opens a block of sub-items has no trailing colon.
- One blank line before every `+` item and `#` heading, no blank lines inside a `+` block, never two blank lines in a row.
- Exactly one newline at the end of the file.

Usage: scripts/format_md.py [FILE ...]   (defaults to every *.md in the repo root)
"""

import math
import sys
from collections.abc import Collection
from pathlib import Path

_BULLET_MARKERS = ("- ", "+ ", "* ")
_FENCE = "```"
_REPO_ROOT = Path(__file__).parent.parent


def _normalize_line(raw_line: str) -> str:
    trimmed = raw_line.rstrip()
    content = trimmed.lstrip(" \t")
    leading = trimmed[: len(trimmed) - len(content)]
    depth = leading.count("\t") + math.ceil(leading.count(" ") / 4)
    if content.startswith(_BULLET_MARKERS):
        return "\t" * depth + ("- " if depth else "+ ") + content[2:]
    return "\t" * depth + content


def _format_text(text: str) -> str:
    # Blank lines are held back as a pending gap and only written once the next line shows whether they belong.
    formatted_lines: list[str] = []
    is_in_code_block = has_pending_gap = False
    for raw_line in text.split("\n"):
        is_fence = raw_line.lstrip().startswith(_FENCE)
        is_code = is_in_code_block or is_fence
        is_in_code_block ^= is_fence
        line = raw_line.rstrip() if is_code else _normalize_line(raw_line)
        if not is_code and not line:
            has_pending_gap = True
            continue
        is_indented = not is_code and line.startswith("\t")
        if formatted_lines:
            if (has_pending_gap and not is_indented) or (not is_code and line.startswith(("+ ", "#"))):
                formatted_lines.append("")
            elif is_indented and formatted_lines[-1].startswith("+ "):
                formatted_lines[-1] = formatted_lines[-1].removesuffix(":")
        formatted_lines.append(line)
        has_pending_gap = False
    return "\n".join(formatted_lines) + "\n"


def _format_files(*, paths: Collection[Path]) -> None:
    for path in paths:
        original = path.read_text()
        formatted = _format_text(original)
        if formatted != original:
            path.write_text(formatted)
            print(f"formatted {path}")


def main() -> None:
    _format_files(paths=[Path(arg) for arg in sys.argv[1:]] or sorted(_REPO_ROOT.glob("*.md")))


if __name__ == "__main__":
    main()
