#!/usr/bin/env python3
"""Sum all IDs that are a repeated digit-sequence twice within given ranges.

Reads ranges from `sample.txt` in the same directory (comma-separated
`start-end` pairs) and prints the sum of all numbers whose decimal
representation is some digits `t` repeated twice (i.e. `tt`).
"""
import sys


def sum_repeated_double_in_range(a: int, b: int) -> int:
	"""Return sum of numbers n in [a,b] where n = t repeated twice (no leading zeros).

	For a given split length k (t has k digits), numbers are n = t * (10^k + 1).
	We compute bounds on t and use arithmetic series sum.
	"""
	total = 0
	s_b = len(str(b))
	# k is the length of the half (t). n has length 2*k, so k up to s_b//2
	for k in range(1, (s_b // 2) + 1):
		mult = 10**k + 1
		t_min = 10 ** (k - 1)
		t_max = 10**k - 1

		# t must satisfy: a <= t*mult <= b
		lo = (a + mult - 1) // mult
		hi = b // mult

		lo = max(lo, t_min)
		hi = min(hi, t_max)
		if lo <= hi:
			count = hi - lo + 1
			# sum of t from lo..hi = (lo+hi)*count//2
			tsum = (lo + hi) * count // 2
			total += mult * tsum
	return total


def parse_ranges(s: str):
	parts = [p.strip() for p in s.strip().split(',') if p.strip()]
	for p in parts:
		if '-' not in p:
			continue
		a_str, b_str = p.split('-', 1)
		yield int(a_str), int(b_str)


def main(argv):
	fname = 'sample.txt' if len(argv) <= 1 else argv[1]
	data = open(fname, 'r', encoding='utf-8').read().strip()
	total = 0
	for a, b in parse_ranges(data):
		total += sum_repeated_double_in_range(a, b)
	print(total)


if __name__ == '__main__':
	main(sys.argv)

