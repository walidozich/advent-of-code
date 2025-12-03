
#!/usr/bin/env python3
"""Advent of Code - Day 3 (custom puzzle):

Each input line is a bank of battery digits. You must turn on exactly two
batteries (keeping their original order) to form a two-digit joltage value.
This script finds the maximum two-digit value for each bank and prints the
sum of those maxima for all banks in `puzzleinput.txt`.
"""

from pathlib import Path
import sys


def max_two_digit_from_line(s: str) -> int:
	s = s.strip()
	n = len(s)
	if n < 2:
		return 0

	# Convert characters to integer digits (fast)
	digits = [ord(c) - 48 for c in s]

	# Build suffix maximum digit to the right of each position
	# suffix_max[i] = maximum digit in s[i+1:]
	suffix_max = [-1] * n
	# last position has no digit to its right
	suffix_max[-1] = -1
	for i in range(n - 2, -1, -1):
		right_digit = digits[i + 1]
		next_suffix = suffix_max[i + 1]
		suffix_max[i] = right_digit if right_digit > next_suffix else next_suffix

	best = 0
	for i in range(n - 1):
		ones = suffix_max[i]
		if ones < 0:
			continue
		val = digits[i] * 10 + ones
		if val > best:
			best = val
			# early exit if maximum possible reached
			if best == 99:
				break

	return best


def main(input_path: Path) -> int:
	total = 0
	with open(input_path, "r") as fh:
		for line in fh:
			s = line.strip()
			if not s:
				continue
			total += max_two_digit_from_line(s)

	print(total)
	return total


if __name__ == "__main__":
	input_path = Path(__file__).parent / "puzzleinput.txt"
	if len(sys.argv) > 1:
		input_path = Path(sys.argv[1])
	if not input_path.exists():
		print(f"Input file not found: {input_path}")
		sys.exit(1)
	main(input_path)

