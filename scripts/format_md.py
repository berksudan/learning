#!/usr/bin/env python3
"""Minimal formatter for the learning notes, rewriting files in place.

Rules (fenced code blocks are left untouched):
- No end-of-line whitespace; blank lines are empty.
- Indent with tabs; each run of up to 4 leading spaces becomes one tab.
- Top-level bullets use `+`, nested bullets use `-`.
- A sub-item is an indented `-` bullet or numbered item; other indented lines continue the line above.
- A `+` label directly followed by sub-items has no trailing colon.
- One blank line before every `#` heading and around every `+` item that has sub-items.
- Consecutive `+` items without sub-items stay tight, with no blank lines between them.
- No blank lines inside a `+` item, never two blank lines in a row.
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


def _is_sub_item(line: str) -> bool:
    content = line.lstrip("\t")
    marker = content.split(" ", 1)[0]
    return content.startswith("- ") or (marker.endswith(".") and marker[:-1].isdigit())


def _format_text(text: str) -> str:
    # Blank lines are held back as a pending gap and only written once the next line shows whether they belong.
    formatted_lines: list[str] = []
    is_in_code_block = has_pending_gap = False
    tight_item_index: int | None = None
    for raw_line in text.split("\n"):
        is_fence = raw_line.lstrip().startswith(_FENCE)
        is_code = is_in_code_block or is_fence
        is_in_code_block ^= is_fence
        line = raw_line.rstrip() if is_code else _normalize_line(raw_line)
        if not is_code and not line:
            has_pending_gap = True
            continue
        if is_code or not line.startswith("\t"):
            is_item = not is_code and line.startswith("+ ")
            needs_blank = tight_item_index is None if is_item else has_pending_gap or (not is_code and line.startswith("#"))
            if formatted_lines and needs_blank:
                formatted_lines.append("")
            tight_item_index = len(formatted_lines) if is_item else None
        elif _is_sub_item(line) and tight_item_index is not None:
            if tight_item_index == len(formatted_lines) - 1:
                formatted_lines[-1] = formatted_lines[-1].removesuffix(":")
            if tight_item_index > 0 and formatted_lines[tight_item_index - 1]:
                formatted_lines.insert(tight_item_index, "")
            tight_item_index = None
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
