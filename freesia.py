#!/usr/bin/env python

from __future__ import print_function

import argparse, sys, io

def round_up_to_4(x):
    if x & 0x3 == 0:
        return x
    else:
        return round_up_to_4(x + 1)

def find_needed_bytes(rom, needed_bytes, start_at):
    needle = b"\xff" * round_up_to_4(needed_bytes)
    pos = rom.find(needle, start_at)

    while pos & 0b11 != 0 and pos != -1:
        pos = rom.find(needle, pos + 1)

    return pos

def main():
    argparser = argparse.ArgumentParser(description="Locates free space inside a GBA ROM.")
    argparser.add_argument("--rom", dest="ROM", required=True)
    argparser.add_argument("--needed-bytes", dest="NEEDED_BYTES", required=True)
    argparser.add_argument("--start-at", dest="START_AT", required=True)

    args = argparser.parse_args()
    args.NEEDED_BYTES = int(args.NEEDED_BYTES, 0)
    args.START_AT = int(args.START_AT, 0) & 0x1FFFFFF

    with open(args.ROM, "rb") as f:
        rom = f.read()
        addr = find_needed_bytes(rom=rom, needed_bytes=args.NEEDED_BYTES, start_at=args.START_AT)

        if addr == -1:
            print("{}: error: end of file reached before a suitable location was found".format(argparser.prog), file=sys.stderr)
            return 1

        print("0x{0:08X}".format(addr | 0x08000000))

if __name__ == "__main__":
    sys.exit(main())
