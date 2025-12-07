from pathlib import Path


def parse_grid(path: Path) -> list[str]:
	text = path.read_text().splitlines()
	if not text:
		raise ValueError("Input grid is empty")
	width = len(text[0])
	for line in text:
		if len(line) != width:
			raise ValueError("All rows must have equal width")
	return text


def find_start(grid: list[str]) -> tuple[int, int]:
	for r, line in enumerate(grid):
		c = line.find("S")
		if c != -1:
			return r, c
	raise ValueError("No start position 'S' found")


def count_splits(grid: list[str]) -> int:
	height = len(grid)
	width = len(grid[0])
	start_row, start_col = find_start(grid)

	# Beams always move downward; represent active beams by their column in the current row.
	beams = {start_col}
	splits = 0

	for row in range(start_row, height):
		queue = list(beams)
		processed_row = set()
		next_row_beams = set()

		while queue:
			col = queue.pop()
			if col < 0 or col >= width or col in processed_row:
				continue
			processed_row.add(col)

			cell = grid[row][col]
			if cell == "^":
				splits += 1
				for ncol in (col - 1, col + 1):
					if 0 <= ncol < width:
						queue.append(ncol)
			else:  # '.' or 'S'
				next_row_beams.add(col)

		beams = next_row_beams
		if not beams:
			break  # All beams have exited the manifold

	return splits


def main() -> None:
	grid = parse_grid(Path(__file__).with_name("puzzle_input.txt"))
	result = count_splits(grid)
	print(result)


if __name__ == "__main__":
	main()
