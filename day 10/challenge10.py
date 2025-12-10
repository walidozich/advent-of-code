import re
from collections import deque
from pathlib import Path
from typing import List, Tuple


def parse_input(path: str) -> List[Tuple[str, List[List[int]], List[int]]]:
	"""Parse machines from the puzzle input file."""
	machines: List[Tuple[str, List[List[int]], List[int]]] = []
	text = Path(path).read_text().splitlines()
	for line in text:
		if not line.strip():
			continue
		pattern_match = re.search(r"\[([.#]+)\]", line)
		if not pattern_match:
			raise ValueError(f"Missing pattern in line: {line}")
		pattern = pattern_match.group(1)

		button_raw = re.findall(r"\(([^)]*)\)", line)
		buttons: List[List[int]] = []
		for raw in button_raw:
			if raw.strip() == "":
				buttons.append([])
				continue
			nums = [int(x) for x in raw.split(",") if x.strip() != ""]
			buttons.append(nums)

		req_match = re.search(r"\{([^}]*)\}", line)
		if not req_match:
			raise ValueError(f"Missing joltage requirements in line: {line}")
		targets = [int(x) for x in req_match.group(1).split(",") if x.strip() != ""]

		machines.append((pattern, buttons, targets))
	return machines


def bfs_solution(pattern: str, buttons: list[list[int]]):
	"""Return minimal button presses via BFS over light states."""
	n_lights = len(pattern)
	target = 0
	for idx, ch in enumerate(pattern):
		if ch == "#":
			target |= 1 << idx

	button_masks = []
	for toggles in buttons:
		mask = 0
		for t in toggles:
			mask |= 1 << t
		button_masks.append(mask)

	start = 0
	if start == target:
		return 0

	seen = {start: 0}
	queue = deque([start])
	while queue:
		state = queue.popleft()
		steps = seen[state]
		for mask in button_masks:
			next_state = state ^ mask
			if next_state == target:
				return steps + 1
			if next_state not in seen:
				seen[next_state] = steps + 1
				queue.append(next_state)

	raise ValueError("No solution found")


def min_presses_joltage(buttons: List[List[int]], targets: List[int]) -> int:
	"""Solve min button presses for joltage counters via MILP."""
	import pulp

	prob = pulp.LpProblem("machine", pulp.LpMinimize)
	x = [pulp.LpVariable(f"x{j}", lowBound=0, cat="Integer") for j in range(len(buttons))]
	prob += pulp.lpSum(x)

	for i, target in enumerate(targets):
		prob += pulp.lpSum(x[j] for j, toggles in enumerate(buttons) if i in toggles) == target

	status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
	if pulp.LpStatus[status] != "Optimal":
		raise ValueError("No optimal solution found")
	return int(pulp.value(prob.objective))


def main():
	machines = parse_input("puzzle_input.txt")
	total = 0
	for pattern, buttons, targets in machines:
		total += min_presses_joltage(buttons, targets)
	print(total)


if __name__ == "__main__":
	main()
