#!/usr/bin/env python3

import argparse
import functools
import sys

from pathlib import Path

integer = functools.wraps(int)(functools.partial(int, base=0))

def find_free_space(*, rom, needed_bytes, start_at=0):
    start_at &= 0x1FFFFFF

    # round needed_bytes up to next multiple of 4
    # if it is already a multiple of 4, it is left as-is
    rounded = (needed_bytes + 3) & ~3

    needle = b"\xff" * rounded
    pos = rom.find(needle, start_at)

    while pos & 0b11 != 0 and pos != -1:
        pos = rom.find(needle, pos + 1)

    return pos | 0x08000000

def main():
    argparser = argparse.ArgumentParser(description="Locates free space inside a GBA ROM.")
    argparser.add_argument("--rom", "-r", required=True, type=Path)
    argparser.add_argument("--needed-bytes", "-n", required=True, type=integer)
    argparser.add_argument("--start-at", "-s", default="0", type=integer)

    args = argparser.parse_args()

    try:
        rom = args.rom.read_bytes()
    except OSError:
        print(f"{argparser.prog}: error: unable to open '{args.rom}' for reading", file=sys.stderr)
        return 1

    addr = find_free_space(rom=rom, needed_bytes=args.needed_bytes, start_at=args.start_at)

    if addr == -1:
        print(f"{argparser.prog}: error: end of file reached before a suitable location was found", file=sys.stderr)
        return 1

    print(f"0x{addr :08X}")

if __name__ == "__main__":
    sys.exit(main())
