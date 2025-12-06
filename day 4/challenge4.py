def count_adjacent_rolls(grid, row, col):
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1
    
    return count


def solve_part1(filename):
    with open(filename, 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    accessible_count = 0
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                
                if adjacent < 4:
                    accessible_count += 1
    
    return accessible_count


def solve_part2(filename):
    with open(filename, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]
    
    total_removed = 0
    
    while True:
        accessible_rolls = []
        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '@':
                    adjacent = count_adjacent_rolls(grid, row, col)
                    
                    if adjacent < 4:
                        accessible_rolls.append((row, col))
        
        if not accessible_rolls:
            break
        
        for row, col in accessible_rolls:
            grid[row][col] = '.'
        
        total_removed += len(accessible_rolls)
    
    return total_removed


if __name__ == "__main__":
    result_part1 = solve_part1("puzzle_input.txt")
    print(f"Part 1 - Number of accessible rolls: {result_part1}")
    
    result_part2 = solve_part2("puzzle_input.txt")
    print(f"Part 2 - Total rolls removed: {result_part2}")
