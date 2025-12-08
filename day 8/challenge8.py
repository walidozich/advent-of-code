import heapq
from collections import defaultdict

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True
    
    def get_component_sizes(self):
        component_sizes = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in component_sizes:
                component_sizes[root] = self.size[root]
        return list(component_sizes.values())

def distance(p1, p2):
    """Calculate Euclidean distance between two 3D points"""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5

def solve():
    # Read input
    with open('puzzle_input.txt', 'r') as f:
        lines = f.read().strip().split('\n')
    
    # Parse junction boxes
    boxes = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        boxes.append((x, y, z))
    
    n = len(boxes)
    print(f"Number of junction boxes: {n}")
    
    # Calculate all pairwise distances and store in a min heap
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            heapq.heappush(distances, (dist, i, j))
    
    print(f"Total pairs: {len(distances)}")
    
    # Initialize Union-Find
    uf = UnionFind(n)
    
    # Connect the 1000 shortest pairs
    pairs_processed = 0
    pairs_needed = 1000
    actual_connections = 0
    
    while pairs_processed < pairs_needed and distances:
        dist, i, j = heapq.heappop(distances)
        pairs_processed += 1
        if uf.union(i, j):
            actual_connections += 1
            if pairs_processed <= 10 or pairs_processed % 100 == 0:
                print(f"Pair {pairs_processed}: boxes {i} and {j}, distance: {dist:.2f}, connected (total connections: {actual_connections})")
        else:
            if pairs_processed <= 10:
                print(f"Pair {pairs_processed}: boxes {i} and {j}, distance: {dist:.2f}, already in same circuit")
    
    print(f"\nPairs processed: {pairs_processed}")
    print(f"Actual connections made: {actual_connections}")
    
    # Get component sizes
    component_sizes = uf.get_component_sizes()
    component_sizes.sort(reverse=True)
    
    print(f"\nNumber of circuits: {len(component_sizes)}")
    print(f"Top 10 circuit sizes: {component_sizes[:10]}")
    
    # Multiply the three largest circuit sizes
    if len(component_sizes) >= 3:
        result = component_sizes[0] * component_sizes[1] * component_sizes[2]
        print(f"\nAnswer: {component_sizes[0]} × {component_sizes[1]} × {component_sizes[2]} = {result}")
    else:
        print(f"\nNot enough circuits! Only {len(component_sizes)} circuits found.")
        result = None
    
    return result

if __name__ == "__main__":
    answer = solve()
