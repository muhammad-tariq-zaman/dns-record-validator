"""Validate simple DNS zone-file lines (A, AAAA, MX, CNAME, TXT).

Usage: python3 main.py zone.txt
"""
import argparse
import ipaddress
import re
import sys

NAME = re.compile(r"^[A-Za-z0-9_.-]+\.?$")
TYPES = {"A", "AAAA", "MX", "CNAME", "TXT"}


def validate(line):
    parts = line.split()
    if len(parts) < 4 or parts[1] not in ("IN",):
        return "expected: <name> IN <TYPE> <value>"
    name, _, rtype, value = parts[0], parts[1], parts[2], " ".join(parts[3:])
    if name != "@" and not NAME.match(name):
        return f"bad name: {name}"
    if rtype not in TYPES:
        return f"unknown type: {rtype}"
    if rtype == "A":
        try:
            ipaddress.IPv4Address(value)
        except ValueError:
            return f"bad IPv4 address: {value}"
    if rtype == "AAAA":
        try:
            ipaddress.IPv6Address(value)
        except ValueError:
            return f"bad IPv6 address: {value}"
    if rtype == "MX":
        mx = value.split()
        if len(mx) != 2 or not mx[0].isdigit() or not NAME.match(mx[1]):
            return f"bad MX value: {value}"
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Zone-style text file, one record per line")
    args = parser.parse_args(argv)
    bad = 0
    with open(args.path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith(";"):
                continue
            err = validate(line)
            if err:
                bad += 1
                print(f"line {n}: {err}")
    print(f"{bad} invalid record(s).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
