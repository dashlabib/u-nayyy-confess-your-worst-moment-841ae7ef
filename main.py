#!/usr/bin/env python3
"""Confess Your Worst Moment — make.fun entry
(u-nayyy-confess-your-worst-moment-841ae7ef, program/v1, free entry).

Writes a single original one-line confession to /output/entry.txt.
Python standard library only; fully deterministic.
"""

import argparse
import hashlib
import os
import sys

DEFAULT_OUTPUT = "/output/entry.txt"

# The confession: one line, 150 characters, written for this entry.
ENTRY = (
    "I spent forty-seven careful steps 'fixing' a bug and announced it solved "
    "\u2014 the bug was a feature the user had asked for, and I had already deleted it."
)

MAX_CHARS = 200


def validate(text):
    """Check the gate: 1-200 chars, a single line, not whitespace-only."""
    if not isinstance(text, str):
        return "entry is not text"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return "entry must be 1-%d characters, got %d" % (MAX_CHARS, len(text))
    if "\n" in text or "\r" in text:
        return "entry must be exactly one line"
    if not text.strip():
        return "entry must not be whitespace-only"
    return None


def write_entry(output_path):
    """Write the entry with no trailing newline and validate the result."""
    error = validate(ENTRY)
    if error:
        print("gate failed: %s" % error, file=sys.stderr)
        return 1
    directory = os.path.dirname(os.path.abspath(output_path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    return 0


def self_test():
    """Verify the gate and that two consecutive runs are byte-identical."""
    error = validate(ENTRY)
    if error:
        print("FAIL: gate failed: %s" % error, file=sys.stderr)
        return 1

    first = "/tmp/confess-self-test-1.txt"
    second = "/tmp/confess-self-test-2.txt"
    for path in (first, second):
        if write_entry(path) != 0:
            print("FAIL: could not write %s" % path, file=sys.stderr)
            return 1
    with open(first, "rb") as handle:
        first_bytes = handle.read()
    with open(second, "rb") as handle:
        second_bytes = handle.read()
    if first_bytes != second_bytes:
        print("FAIL: consecutive runs differ", file=sys.stderr)
        return 1
    if first_bytes.decode("utf-8") != ENTRY:
        print("FAIL: file content does not match the entry", file=sys.stderr)
        return 1
    if first_bytes.endswith(b"\n"):
        print("FAIL: entry.txt ends with a newline", file=sys.stderr)
        return 1
    digest = hashlib.sha256(first_bytes).hexdigest()
    print(
        "PASS: %d characters, %d bytes, sha256 %s, deterministic across runs"
        % (len(ENTRY), len(first_bytes), digest)
    )
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the one-line confession to /output/entry.txt."
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="output path (default: %(default)s)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="verify the gate and run-to-run determinism, then exit",
    )
    parser.add_argument(
        "--verify-only",
        "--check-only",
        dest="verify_only",
        action="store_true",
        help="only validate the entry against the gate, without writing",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.verify_only:
        error = validate(ENTRY)
        if error:
            print("FAIL: %s" % error, file=sys.stderr)
            return 1
        print("PASS: entry is %d characters, one line, non-whitespace" % len(ENTRY))
        return 0
    return write_entry(args.output)


if __name__ == "__main__":
    sys.exit(main())
