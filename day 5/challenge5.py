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


def merge_ranges(ranges):
    """Merge overlapping ranges to get non-overlapping ranges."""
    if not ranges:
        return []
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps or is adjacent to the last merged range
        if start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))
    
    return merged


def count_all_fresh_ids(filename):
    """Count total unique ingredient IDs considered fresh by the ranges."""
    ranges, _ = parse_input(filename)
    
    # Merge overlapping ranges to avoid counting IDs multiple times
    merged = merge_ranges(ranges)
    
    # Count all IDs in the merged ranges
    total_count = 0
    for start, end in merged:
        total_count += (end - start + 1)
    
    return total_count


if __name__ == "__main__":
    # Part 1
    result1 = count_fresh_ingredients("puzzle_input.txt")
    print(f"Part 1 - Number of fresh ingredient IDs: {result1}")
    
    # Part 2
    result2 = count_all_fresh_ids("puzzle_input.txt")
    print(f"Part 2 - Total ingredient IDs considered fresh: {result2}")
