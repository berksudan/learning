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
import re
import sys
from dataclasses import dataclass
from pathlib import Path

FENCE = re.compile(r"^\s*```")
BULLET = re.compile(r"^(\t*)[-+*] ")


@dataclass
class Line:
    text: str
    in_code: bool

    @property
    def blank(self) -> bool:
        return not self.in_code and self.text == ""

    @property
    def indented(self) -> bool:
        return not self.in_code and self.text.startswith("\t")

    @property
    def opens_block(self) -> bool:
        return not self.in_code and (self.text.startswith("+ ") or self.text.startswith("#"))


def normalize_line(text: str) -> str:
    text = text.rstrip()
    stripped = text.lstrip(" \t")
    leading = text[: len(text) - len(stripped)]
    depth = leading.count("\t") + math.ceil(leading.count(" ") / 4)
    text = "\t" * depth + stripped
    return BULLET.sub(lambda m: m.group(1) + ("- " if m.group(1) else "+ "), text)


def classify(raw_lines: list[str]) -> list[Line]:
    lines = []
    in_code = False
    for raw in raw_lines:
        is_fence = bool(FENCE.match(raw))
        if is_fence:
            in_code = not in_code
        lines.append(Line(raw.rstrip() if in_code or is_fence else normalize_line(raw), in_code or is_fence))
    return lines


def next_content(lines: list[Line], index: int) -> Line | None:
    return next((line for line in lines[index + 1 :] if not line.blank), None)


def format_text(text: str) -> str:
    lines = classify(text.split("\n"))
    out: list[Line] = []
    for index, line in enumerate(lines):
        following = next_content(lines, index)
        if line.blank:
            if not out or out[-1].blank or following is None or following.indented:
                continue
        elif line.opens_block and out and not out[-1].blank:
            out.append(Line("", False))
        if line.text.startswith("+ ") and not line.in_code and following and following.indented:
            line = Line(line.text.removesuffix(":"), False)
        out.append(line)
    return "\n".join(line.text for line in out) + "\n"


def main() -> None:
    paths = [Path(arg) for arg in sys.argv[1:]] or sorted(Path(__file__).parent.parent.glob("*.md"))
    for path in paths:
        original = path.read_text()
        formatted = format_text(original)
        if formatted != original:
            path.write_text(formatted)
            print(f"formatted {path}")


if __name__ == "__main__":
    main()
