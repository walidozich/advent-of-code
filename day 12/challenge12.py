from itertools import permutations

def parse_input(filename):
    """Parse the puzzle input file."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    shapes = {}
    i = 0
    
    # Parse shapes until we hit a line with 'x' (dimension line)
    while i < len(lines):
        line = lines[i]
        if 'x' in line and ':' in line:
            # This is the start of regions section
            break
        
        if line and ':' in line:
            # Shape header
            shape_id = int(line.rstrip(':'))
            i += 1
            grid = []
            while i < len(lines) and lines[i] and 'x' not in lines[i]:
                if ':' in lines[i] and any(c.isdigit() for c in lines[i].split(':')[0]):
                    # Next shape header
                    break
                grid.append(list(lines[i]))
                i += 1
            shapes[shape_id] = grid
        else:
            i += 1
    
    # Parse regions
    regions = []
    while i < len(lines):
        line = lines[i].strip()
        if line and 'x' in line:
            parts = line.split(': ')
            dims = parts[0].split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].split()))
            regions.append((width, height, counts))
        i += 1
    
    return shapes, regions

def get_shape_coords(grid):
    """Get coordinates of # cells in a shape (relative to bounding box)."""
    coords = set()
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == '#':
                coords.add((r, c))
    return coords

def normalize_shape(coords):
    """Normalize shape coordinates to start from (0, 0)."""
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    normalized = frozenset((r - min_r, c - min_c) for r, c in coords)
    return normalized

def get_all_rotations_and_flips(coords):
    """Get all unique orientations of a shape (rotations and flips)."""
    orientations = set()
    
    current = coords
    for _ in range(4):  # 4 rotations
        orientations.add(normalize_shape(current))
        # Rotate 90 degrees clockwise: (r, c) -> (c, -r)
        current = frozenset((c, -r) for r, c in current)
    
    # Flip horizontally and repeat rotations
    current = frozenset((r, -c) for r, c in coords)
    for _ in range(4):
        orientations.add(normalize_shape(current))
        current = frozenset((c, -r) for r, c in current)
    
    return list(orientations)

def can_place_shape(grid, shape_coords, row, col):
    """Check if a shape can be placed at (row, col) in the grid."""
    for dr, dc in shape_coords:
        r, c = row + dr, col + dc
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return False
        if grid[r][c] != 0:  # 0 means empty
            return False
    return True

def place_shape(grid, shape_coords, row, col, shape_id):
    """Place a shape on the grid (in-place)."""
    placed_cells = []
    for dr, dc in shape_coords:
        r, c = row + dr, col + dc
        grid[r][c] = shape_id
        placed_cells.append((r, c))
    return placed_cells

def grid_to_tuple(grid):
    """Convert grid to tuple for hashing."""
    return tuple(tuple(row) for row in grid)

def can_fit_presents(width, height, present_counts, all_shapes):
    """Check if all presents can fit in the region using backtracking."""
    grid = [[0] * width for _ in range(height)]
    available_area = width * height
    
    # Quick check: if total area needed is bigger than available, it can't fit
    total_needed = 0
    for shape_id, count in enumerate(present_counts):
        if count > 0 and shape_id in all_shapes:
            # Get size of first orientation
            shape_size = len(all_shapes[shape_id][0])
            total_needed += shape_size * count
    
    if total_needed > available_area:
        return False
    
    # Create list of presents to place (sorted by shape_id for consistency)
    presents = []
    for shape_id, count in enumerate(present_counts):
        for _ in range(count):
            presents.append(shape_id)
    
    if not presents:
        return True
    
    def find_first_empty():
        """Find the first empty cell."""
        for r in range(height):
            for c in range(width):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    
    def backtrack(present_idx):
        """Try to place all remaining presents."""
        if present_idx == len(presents):
            return True
        
        empty_cell = find_first_empty()
        if empty_cell is None:
            return False
        
        start_row, start_col = empty_cell
        shape_id = presents[present_idx]
        
        # Try all orientations
        for orientation in all_shapes[shape_id]:
            # Start search from the first empty cell
            for row in range(start_row, height):
                col_start = start_col if row == start_row else 0
                for col in range(col_start, width):
                    if can_place_shape(grid, orientation, row, col):
                        # Place the shape
                        placed_cells = []
                        for dr, dc in orientation:
                            r, c = row + dr, col + dc
                            grid[r][c] = present_idx + 1
                            placed_cells.append((r, c))
                        
                        # Recursively try to place remaining presents
                        if backtrack(present_idx + 1):
                            return True
                        
                        # Backtrack
                        for r, c in placed_cells:
                            grid[r][c] = 0
        
        return False
    
    return backtrack(0)

def solve(input_file):
    """Solve the puzzle."""
    shapes, regions = parse_input(input_file)
    
    # Pre-compute all rotations and flips for each shape
    all_shapes = {}
    for shape_id, grid in shapes.items():
        coords = get_shape_coords(grid)
        all_shapes[shape_id] = get_all_rotations_and_flips(coords)
    
    # Check each region
    count = 0
    total = len(regions)
    for idx, (width, height, present_counts) in enumerate(regions):
        if idx % 10 == 0:
            print(f"Progress: {idx}/{total}", flush=True)
        if can_fit_presents(width, height, present_counts, all_shapes):
            count += 1
    
    return count

if __name__ == "__main__":
    result = solve("puzzle_input.txt")
    print(f"Number of regions that can fit all presents: {result}")
