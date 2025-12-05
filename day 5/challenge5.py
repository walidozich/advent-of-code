def parse_input(filename):
    """Parse the puzzle input to extract ranges and ingredient IDs."""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    
    # Find the blank line that separates ranges from ingredient IDs
    blank_line_idx = lines.index('')
    
    # Parse fresh ingredient ranges
    ranges = []
    for line in lines[:blank_line_idx]:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Parse available ingredient IDs
    ingredient_ids = [int(line) for line in lines[blank_line_idx + 1:]]
    
    return ranges, ingredient_ids


def is_fresh(ingredient_id, ranges):
    """Check if an ingredient ID falls within any of the fresh ranges."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(filename):
    """Count how many available ingredient IDs are fresh."""
    ranges, ingredient_ids = parse_input(filename)
    
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
    
    return fresh_count


if __name__ == "__main__":
    result = count_fresh_ingredients("puzzle_input.txt")
    print(f"Number of fresh ingredient IDs: {result}")
