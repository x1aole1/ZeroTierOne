#!/usr/bin/env python3
"""Patch ZeroTier Linux TAP setup for old embedded kernels.

ZeroTierOne issue #1524/#1314 documents old Linux 2.6.x devices where setting
TAP MAC after bringing the device UP can produce:

    WARNING: ioctl() failed setting up Linux tap device (set MAC)

This script is intentionally source-layout based rather than version based:
- if the bring-up ioctl appears before the first set-MAC ioctl, move bring-up
  after the first set-MTU ioctl;
- make sure IFF_NOARP/IFF_NOTRAILERS are set before the bring-up ioctl.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def find_stmt_block(text: str, start: int) -> tuple[int, int]:
    """Return [start, end) for an if/statement block starting at start."""
    brace = text.find("{", start)
    if brace == -1:
        raise SystemExit("could not find opening brace for ioctl block")
    depth = 0
    i = brace
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                # Include following semicolon/newlines/usleep line if present.
                semi = re.match(r"[ \t]*(?:\r?\n[ \t]*)?(?:usleep\(100000\);[ \t]*(?:\r?\n)?)?", text[end:])
                if semi:
                    end += semi.end()
                return start, end
        i += 1
    raise SystemExit("could not find end of ioctl block")


def patch_tap(path: Path) -> bool:
    text = path.read_text()
    original = text

    mac_pos = text.find("SIOCSIFHWADDR")
    mtu_pos = text.find("SIOCSIFMTU")
    up_flag = text.find("ifr.ifr_flags |= IFF_UP;")
    up_ioctl = text.find("SIOCSIFFLAGS", up_flag if up_flag != -1 else 0)

    if mac_pos == -1 or up_flag == -1 or up_ioctl == -1:
        raise SystemExit(f"{path}: could not locate TAP MAC/up ioctl code")

    # Ensure the flags are applied immediately before the interface is raised.
    flag_block = (
        "ifr.ifr_flags |= IFF_UP;\n"
        "\t\t\t\tifr.ifr_flags &= ~IFF_NOARP;\n"
        "\t\t\t\tifr.ifr_flags &= ~IFF_NOTRAILERS;"
    )
    if "IFF_NOARP" not in text:
        text = text.replace("ifr.ifr_flags |= IFF_UP;", flag_block, 1)
    elif text.find("IFF_NOARP") > text.find("SIOCSIFFLAGS", text.find("ifr.ifr_flags |= IFF_UP;")):
        raise SystemExit(f"{path}: IFF_NOARP appears after bring-up ioctl")

    # Recompute positions after optional flag insertion.
    mac_pos = text.find("SIOCSIFHWADDR")
    mtu_pos = text.find("SIOCSIFMTU")
    up_flag = text.find("ifr.ifr_flags |= IFF_UP;")
    up_ioctl = text.find("SIOCSIFFLAGS", up_flag)

    # Older ZeroTier releases brought the interface UP before setting MAC/MTU.
    # Move that whole block after the first MTU ioctl block.
    if up_flag < mac_pos:
        if mtu_pos == -1:
            raise SystemExit(f"{path}: bring-up is before MAC but no MTU block found")
        up_start, up_end = find_stmt_block(text, up_flag)
        up_block = text[up_start:up_end]
        text_without_up = text[:up_start] + text[up_end:]
        mtu_pos2 = text_without_up.find("SIOCSIFMTU")
        _, mtu_end = find_stmt_block(text_without_up, text_without_up.rfind("if", 0, mtu_pos2))
        text = text_without_up[:mtu_end] + "\n\t\t\t\t" + up_block.strip() + "\n" + text_without_up[mtu_end:]

    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: patch-zerotier-linux-tap.py /path/to/LinuxEthernetTap.cpp", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    changed = patch_tap(path)
    print(f"{'patched' if changed else 'already patched'}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
