def count_adjacent_rolls(grid, row, col):
    """Count how many rolls (@) are adjacent to position (row, col)"""
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    
    # Check all 8 adjacent positions
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),    # left, right
        (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
    ]
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Check if the position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1
    
    return count


def solve(filename):
    # Read the grid from the file
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # If this position has a roll
            if grid[row][col] == '@':
                # Count adjacent rolls
                adjacent = count_adjacent_rolls(grid, row, col)
                
                # If fewer than 4 adjacent rolls, it's accessible
                if adjacent < 4:
                    accessible_count += 1
    
    return accessible_count


if __name__ == "__main__":
    result = solve("puzzle_input.txt")
    print(f"Number of accessible rolls: {result}")
