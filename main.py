#!/usr/bin/env python3
"""Copy the committed front-page image to /output/entry.png.

Stdlib-only, copy-only entry for news-image-20261126. The grader is a
bare Python 3.13 runtime with no third-party packages, so this program
only reads the entry.png shipped in this repository, verifies its PNG
signature and IHDR width/height (1024x1024) with struct, and writes
the exact same bytes to /output/entry.png. Deterministic: every run
produces byte-identical output.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUTPUT = OUTPUT_DIR / "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def check_png(data):
    """Verify PNG signature and IHDR dimensions; return (width, height)."""
    if len(data) < 33:
        raise ValueError("file too short to be a PNG")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        raise ValueError("missing or malformed IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if data[-12:] != struct.pack(">I", 0) + b"IEND" + b"\xaeB`\x82":
        raise ValueError("PNG is truncated: missing IEND chunk")
    return width, height


def main():
    data = SOURCE.read_bytes()
    width, height = check_png(data)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            "unexpected PNG size %dx%d, expected %dx%d"
            % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, OUTPUT)
    # Confirm the copy is byte-identical to the source.
    if OUTPUT.read_bytes() != data:
        raise ValueError("output does not match source bytes")
    print("wrote %s (%d bytes, %dx%d)" % (OUTPUT, len(data), width, height))
    return 0


if __name__ == "__main__":
    sys.exit(main())
