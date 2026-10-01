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
from pathlib import Path

FENCE = re.compile(r"^\s*```")
BULLET = re.compile(r"^(\t*)[-+*] ")


def normalize_line(text: str) -> str:
    text = text.rstrip()
    stripped = text.lstrip(" \t")
    leading = text[: len(text) - len(stripped)]
    depth = leading.count("\t") + math.ceil(leading.count(" ") / 4)
    text = "\t" * depth + stripped
    return BULLET.sub(lambda m: m.group(1) + ("- " if m.group(1) else "+ "), text)


def format_text(text: str) -> str:
    # Blank lines are held back as a pending gap and only written once the next line shows whether they belong.
    out: list[str] = []
    in_code = gap = False
    for raw in text.split("\n"):
        is_fence = bool(FENCE.match(raw))
        code = in_code or is_fence
        in_code ^= is_fence
        line = raw.rstrip() if code else normalize_line(raw)
        if not code and not line:
            gap = True
            continue
        indented = not code and line.startswith("\t")
        if out:
            if (gap and not indented) or (not code and line.startswith(("+ ", "#"))):
                out.append("")
            elif indented and out[-1].startswith("+ "):
                out[-1] = out[-1].removesuffix(":")
        out.append(line)
        gap = False
    return "\n".join(out) + "\n"


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
