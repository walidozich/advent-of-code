import sys
import re


INS_RE = re.compile(r'^\s*([LR])\s*([0-9]+)\s*$', re.IGNORECASE)

def compute_final(instructions, start=50):
    pos = start % 100
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
    return pos


def compute_final_and_count_zero(instructions, start=50):
    pos = start % 100
    zero_count = 0
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
            if val > 0:
                if dir_ == 'R':
                    k0 = (100 - pos) % 100
                else:
                    k0 = pos % 100
                if k0 == 0:
                    k0 = 100
                if val >= k0:
                    zero_count += 1 + (val - k0) // 100

            if dir_ == 'L':
                pos = (pos - val) % 100
            else:
                pos = (pos + val) % 100
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
    print(zero_count)