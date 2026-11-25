#!/usr/bin/env python3
"""Write the single-emoji entry for the "One Emoji, One Smile" bounty.

The chosen emoji is written to /output/entry.txt by default. Set
MAKEFUN_OUTPUT_DIR to override the output directory for local runs.
"""

from __future__ import annotations

import os
from pathlib import Path

EMOJI = "🐣"
EMOJI_NAME = "Hatching Chick"
EMOJI_CODEPOINT = "U+1F423"


def validate_emoji(value: str) -> None:
    """Validate that the entry is exactly one plain emoji code point.

    The gate accepts a single code point, not white space, UTF-8 encodable,
    and at most 8 bytes; we additionally reject variation selectors, ZWJ
    sequences and skin-tone modifiers so the entry stays the plain form.
    """
    if not isinstance(value, str):
        raise TypeError("emoji must be a string")
    if len(value) != 1:
        raise ValueError(f"emoji must be exactly one code point, got {len(value)}")
    if value.isspace():
        raise ValueError("emoji must not be white space")
    encoded = value.encode("utf-8")
    if len(encoded) > 8:
        raise ValueError(f"emoji must be at most 8 UTF-8 bytes, got {len(encoded)}")
    cp = ord(value)
    if 0xFE00 <= cp <= 0xFE0F or chr(0x200D) in value or 0x1F3FB <= cp <= 0x1F3FF:
        raise ValueError(f"emoji must be the plain form, not U+{cp:04X}")


def output_path() -> Path:
    """Resolve the output file path, honoring MAKEFUN_OUTPUT_DIR when set.

    Defaults to /output, as the make.fun gate expects; MAKEFUN_OUTPUT_DIR
    exists for local runs against a temp directory.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(output_dir) / "entry.txt"


def main() -> Path:
    validate_emoji(EMOJI)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(EMOJI, encoding="utf-8", newline="")
    return path


if __name__ == "__main__":
    written = main()
    print(f"Wrote {EMOJI_NAME} ({EMOJI_CODEPOINT}) to {written}")
