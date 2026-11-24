#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The only output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png; nothing is
ever written next to this file (the grader runs it from a read-only copy).
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    src_hash = sha256(SRC)
    dst_hash = sha256(dst)
    if src_hash != dst_hash:
        print(f"FAIL: sha256 mismatch src={src_hash} dst={dst_hash}", file=sys.stderr)
        return 1
    from PIL import Image

    with Image.open(dst) as im:
        if im.size != (1024, 1024):
            print(f"FAIL: unexpected size {im.size}", file=sys.stderr)
            return 1
    size = os.path.getsize(dst)
    if size > 1048576:
        print(f"FAIL: entry.png is {size} bytes (> 1 MiB)", file=sys.stderr)
        return 1
    print(f"OK: {dst} {size} bytes sha256={dst_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
