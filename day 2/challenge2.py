import sys


def sum_repeated_double_in_range(a: int, b: int) -> int:
	
	total = 0
	s_b = len(str(b))
	for k in range(1, (s_b // 2) + 1):
		mult = 10**k + 1
		t_min = 10 ** (k - 1)
		t_max = 10**k - 1

		lo = (a + mult - 1) // mult
		hi = b // mult

		lo = max(lo, t_min)
		hi = min(hi, t_max)
		if lo <= hi:
			count = hi - lo + 1
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
	if len(sys.argv) > 1 and sys.argv[1] in ('part2', '--part2'):
		# build list of ranges
		fname = 'sample.txt'
		data = open(fname, 'r', encoding='utf-8').read().strip()
		ranges = list(parse_ranges(data))

		max_b = max(b for _, b in ranges)

		nums = set()
		max_len = len(str(max_b))
		for k in range(1, max_len + 1):
			# r must be at least 2 and k*r <= max_len
			rmax = max_len // k
			if rmax < 2:
				continue
			t_min = 10 ** (k - 1)
			t_max = 10**k - 1
			for r in range(2, rmax + 1):
				mult = (10 ** (k * r) - 1) // (10 ** k - 1)
				high_t = min(t_max, max_b // mult)
				if high_t < t_min:
					continue
				for t in range(t_min, high_t + 1):
					n = t * mult
					if n <= max_b:
						nums.add(n)

		nums_list = sorted(nums)
		from bisect import bisect_left, bisect_right

		pref = [0]
		for v in nums_list:
			pref.append(pref[-1] + v)

		total2 = 0
		for a, b in ranges:
			i = bisect_left(nums_list, a)
			j = bisect_right(nums_list, b)
			total2 += pref[j] - pref[i]

		print(total2)
	else:
		main(sys.argv)

