import sys
import re

#!/usr/bin/env python3
"""
challenge.py

Simulate a dial 0-99 starting at 50. Each instruction is "L<n>" (subtract n) or "R<n>" (add n).
Reads instructions from stdin or from a file passed as first argument. Prints final dial value (0-99).
"""


INS_RE = re.compile(r'^\s*([LR])\s*([0-9]+)\s*$', re.IGNORECASE)

def compute_final(instructions, start=50):
    pos = start % 100
    for line in instructions:
        line = line.strip()
        if not line:
            continue
        # Allow multiple instructions on the same line separated by commas or whitespace,
        # e.g. "L10 R20" or "L10,R20" or single-instruction lines.
        tokens = re.split(r'[,\s]+', line)
        for token in tokens:
            if not token:
                continue
            m = INS_RE.match(token)
            if not m:
                raise ValueError(f"Invalid instruction: {token!r} (from line: {line!r})")
            dir_, val = m.group(1).upper(), int(m.group(2))
            if dir_ == 'L':
                pos = (pos - val) % 100
            else:
                pos = (pos + val) % 100
    return pos


def compute_final_and_count_zero(instructions, start=50):
    """Return (final_pos, zero_count): number of times dial pointed to 0 during moves.

    A zero is counted each time the dial equals 0 after applying a move.
    Multiple instructions per input line are supported (commas/whitespace separated).
    """
    pos = start % 100
    zero_count = 1 if pos == 0 else 0
    for line in instructions:
        line = line.strip()
        if not line:
            continue
        tokens = re.split(r'[,\s]+', line)
        for token in tokens:
            if not token:
                continue
            m = INS_RE.match(token)
            if not m:
                raise ValueError(f"Invalid instruction: {token!r} (from line: {line!r})")
            dir_, val = m.group(1).upper(), int(m.group(2))
            if dir_ == 'L':
                pos = (pos - val) % 100
            else:
                pos = (pos + val) % 100
            if pos == 0:
                zero_count += 1
    return pos, zero_count

def read_lines_from_stdin():
    return sys.stdin.read().splitlines()

def read_lines_from_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        lines = read_lines_from_file(sys.argv[1])
    else:
        lines = read_lines_from_stdin()
    final_pos, zero_count = compute_final_and_count_zero(lines, start=50)
    # Print the password (how many times the dial pointed to 0)
    print(zero_count)