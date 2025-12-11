def count_paths(graph, start, end, path=None, memo=None):
    """
    Count all unique paths from start to end in a directed graph using DFS.
    
    Args:
        graph: Dictionary mapping device names to lists of output devices
        start: Starting device name
        end: Target device name
        path: Current path being explored
        memo: Memoization cache to avoid recalculating
    
    Returns:
        Number of unique paths from start to end
    """
    if path is None:
        path = []
    if memo is None:
        memo = {}
    
    # Create a key for memoization (use tuple of path for cache)
    path_key = tuple(path + [start])
    if path_key in memo:
        return memo[path_key]
    
    # If we've reached the end, we found one path
    if start == end:
        memo[path_key] = 1
        return 1
    
    # Prevent infinite loops by checking if we've visited this node in current path
    if start in path:
        memo[path_key] = 0
        return 0
    
    path_count = 0
    
    # Explore all outputs of the current device
    if start in graph:
        for output in graph[start]:
            path_count += count_paths(graph, output, end, path + [start], memo)
    
    memo[path_key] = path_count
    return path_count


def solve(puzzle_input):
    """Parse input and solve the challenge."""
    graph = {}
    
    # Parse the input
    for line in puzzle_input.strip().split('\n'):
        device, outputs = line.split(': ')
        graph[device] = outputs.split()
    
    # Count paths from "you" to "out"
    result = count_paths(graph, "you", "out")
    return result


# Read puzzle input
with open('puzzle_input.txt', 'r') as f:
    puzzle_input = f.read()

# Solve and print result
answer = solve(puzzle_input)
print(f"Number of different paths from 'you' to 'out': {answer}")
