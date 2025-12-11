def topological_sort(graph):
    """
    Perform topological sort on the graph.
    Returns a list of nodes in topological order.
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            if neighbor not in in_degree:
                in_degree[neighbor] = 0
            in_degree[neighbor] += 1
    
    queue = [node for node in in_degree if in_degree[node] == 0]
    topo_order = []
    
    while queue:
        node = queue.pop(0)
        topo_order.append(node)
        if node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    return topo_order


def count_paths_to_node_dp(graph, start, target):
    """
    Count all paths from start to target using dynamic programming on DAG.
    Much more efficient than DFS for dense graphs.
    
    Returns:
        Number of unique paths from start to target
    """
    # Get topological order
    topo_order = topological_sort(graph)
    
    # DP table: dp[node] = number of paths from start to node
    dp = {node: 0 for node in graph}
    if start in dp:
        dp[start] = 1
    
    # Also include target if it's not in graph (it's a sink node)
    if target not in dp:
        dp[target] = 0
    
    # Process nodes in topological order
    for node in topo_order:
        if node == start:
            dp[node] = 1
        
        if node in graph and dp[node] > 0:
            for neighbor in graph[node]:
                if neighbor not in dp:
                    dp[neighbor] = 0
                dp[neighbor] += dp[node]
    
    return dp.get(target, 0)


def count_paths_through_both(graph, start, end, node1, node2):
    """
    Count paths from start to end that go through both node1 and node2.
    This uses the formula: paths through both = paths(start->node1->node2->end) + paths(start->node2->node1->end)
    """
    # Paths that visit node1 then node2
    path1_to_n1 = count_paths_to_node_dp(graph, start, node1)
    path_n1_to_n2 = count_paths_to_node_dp(graph, node1, node2)
    path_n2_to_end = count_paths_to_node_dp(graph, node2, end)
    count1 = path1_to_n1 * path_n1_to_n2 * path_n2_to_end
    
    # Paths that visit node2 then node1
    path1_to_n2 = count_paths_to_node_dp(graph, start, node2)
    path_n2_to_n1 = count_paths_to_node_dp(graph, node2, node1)
    path_n1_to_end = count_paths_to_node_dp(graph, node1, end)
    count2 = path1_to_n2 * path_n2_to_n1 * path_n1_to_end
    
    return count1 + count2


def find_all_paths(graph, start, end, path=None):
    """
    Find all unique paths from start to end in a directed graph using DFS.
    Prevents infinite loops by checking if we've visited this node in current path.
    
    Args:
        graph: Dictionary mapping device names to lists of output devices
        start: Starting device name
        end: Target device name
        path: Current path being explored
    
    Returns:
        List of all paths (each path is a list of device names)
    """
    if path is None:
        path = []
    
    # If we've reached the end, we found one complete path
    if start == end:
        return [path + [start]]
    
    # Prevent infinite loops by checking if we've visited this node in current path
    if start in path:
        return []
    
    all_paths = []
    
    # Explore all outputs of the current device
    if start in graph:
        for output in graph[start]:
            paths = find_all_paths(graph, output, end, path + [start])
            all_paths.extend(paths)
    
    return all_paths


def count_paths_visiting_both_optimized(graph, start, end, required1, required2):
    """
    Count paths from start to end that visit both required1 and required2.
    """
    return count_paths_through_both(graph, start, end, required1, required2)


# Read puzzle input
with open('puzzle_input.txt', 'r') as f:
    puzzle_input = f.read()

# Solve and print results
graph = {}

# Parse the input
for line in puzzle_input.strip().split('\n'):
    device, outputs = line.split(': ')
    graph[device] = outputs.split()

# Part 1: Count paths from "you" to "out"
print("Calculating Part 1...")
answer1 = count_paths_to_node_dp(graph, "you", "out")
print(f"Part 1 - Paths from 'you' to 'out': {answer1}")

# Part 2: Count paths from "svr" to "out" that visit both "dac" and "fft"
print("Calculating Part 2...")
answer2 = count_paths_visiting_both_optimized(graph, "svr", "out", "dac", "fft")
print(f"Part 2 - Paths from 'svr' to 'out' visiting both 'dac' and 'fft': {answer2}")
