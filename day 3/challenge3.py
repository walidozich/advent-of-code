


from pathlib import Path
import sys


def max_k_subsequence_value(s: str, k: int) -> int:
	s = s.strip()
	n = len(s)
	if k <= 0 or n < k:
		return 0

	digits = [ord(c) - 48 for c in s]

	picked = []
	pos = 0
	for remaining in range(k, 0, -1):
		end = n - remaining
		max_d = -1
		max_idx = pos
		for i in range(pos, end + 1):
			d = digits[i]
			if d > max_d:
				max_d = d
				max_idx = i
				if max_d == 9:
					break

		picked.append(max_d)
		pos = max_idx + 1

	val = 0
	for d in picked:
		val = val * 10 + d
	return val


def main(input_path: Path) -> int:
	total = 0
	k = getattr(main, "k_override", 2)
	with open(input_path, "r") as fh:
		for line in fh:
			s = line.strip()
			if not s:
				continue
			total += max_k_subsequence_value(s, k)

	print(total)
	return total


if __name__ == "__main__":
	input_path = Path(__file__).parent / "puzzleinput.txt"
	k = 2
	if len(sys.argv) > 1:
		first = sys.argv[1]
		if first.isdigit():
			k = int(first)
		else:
			input_path = Path(first)
	if len(sys.argv) > 2:
		try:
			k = int(sys.argv[2])
		except ValueError:
			pass

	if not input_path.exists():
		print(f"Input file not found: {input_path}")
		sys.exit(1)

	setattr(main, "k_override", k)
	main(input_path)

