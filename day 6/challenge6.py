def solve_math_worksheet(filename):
    """
    Parse the math worksheet and solve all problems.
    
    The worksheet has problems arranged horizontally with separators.
    Each problem consists of:
    - A block of columns containing numbers
    - Each row has numbers written horizontally (e.g., "123")
    - Different rows may have different length numbers
    - The operation for the entire problem is at the bottom
    - Problems are separated by columns that are all spaces
    
    Example:
    123 328  51 64
     45 64  387 23
      6 98  215 314
    *   +   *   +
    
    This has 4 problems:
    - Problem 1 (cols 0-2): numbers 123, 45, 6 with operation *
    - Problem 2 (cols 4-6): numbers 328, 64, 98 with operation +
    - Problem 3 (cols 9-10): numbers 51, 387, 215 with operation *
    - Problem 4 (cols 12-14): numbers 64, 23, 314 with operation +
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Remove trailing newlines
    lines = [line.rstrip('\n') for line in lines]
    
    # We expect at least 4 lines: N number rows + 1 operator row
    if len(lines) < 4:
        raise ValueError("Expected at least 4 lines in the input")
    
    number_rows = [lines[i] for i in range(len(lines) - 1)]
    operator_row = lines[-1]
    
    # Find the maximum line length
    max_len = max(len(row) for row in lines)
    
    # Pad all rows to the same length
    number_rows = [row.ljust(max_len) for row in number_rows]
    operator_row = operator_row.ljust(max_len)
    
    # Find column boundaries (separator columns are all spaces)
    separator_cols = []
    for col in range(max_len):
        if all(number_rows[i][col] == ' ' for i in range(len(number_rows))) and operator_row[col] == ' ':
            separator_cols.append(col)
    
    # Group consecutive separator columns
    separator_ranges = []
    if separator_cols:
        start = separator_cols[0]
        for i in range(1, len(separator_cols)):
            if separator_cols[i] != separator_cols[i-1] + 1:
                # End of this separator group
                separator_ranges.append((start, separator_cols[i-1]))
                start = separator_cols[i]
        separator_ranges.append((start, separator_cols[-1]))
    
    # Now extract problem blocks (between separator ranges)
    problems = []
    problem_start = 0
    
    for sep_start, sep_end in separator_ranges:
        if problem_start < sep_start:
            # Extract problem from problem_start to sep_start-1
            problem_end = sep_start - 1
            
            numbers = []
            operation = None
            
            # Parse each row within this problem block
            for row_idx in range(len(number_rows)):
                row_text = number_rows[row_idx][problem_start:problem_end+1].strip()
                if row_text:
                    # Split by spaces to get individual numbers in this row
                    row_numbers = row_text.split()
                    numbers.extend([int(n) for n in row_numbers if n.isdigit()])
            
            # Get operation from operator row (any non-space character)
            op_text = operator_row[problem_start:problem_end+1].strip()
            for char in op_text:
                if char in ['+', '*']:
                    operation = char
                    break
            
            if numbers and operation:
                problems.append({'numbers': numbers, 'operation': operation})
        
        problem_start = sep_end + 1
    
    # Handle last problem if it exists
    if problem_start < max_len:
        numbers = []
        operation = None
        
        for row_idx in range(len(number_rows)):
            row_text = number_rows[row_idx][problem_start:].strip()
            if row_text:
                row_numbers = row_text.split()
                numbers.extend([int(n) for n in row_numbers if n.isdigit()])
        
        op_text = operator_row[problem_start:].strip()
        for char in op_text:
            if char in ['+', '*']:
                operation = char
                break
        
        if numbers and operation:
            problems.append({'numbers': numbers, 'operation': operation})
    
    # Calculate results for each problem
    grand_total = 0
    
    for problem in problems:
        numbers = problem['numbers']
        operation = problem['operation']
        
        result = numbers[0]
        for num in numbers[1:]:
            if operation == '+':
                result += num
            elif operation == '*':
                result *= num
        
        grand_total += result
    
    return grand_total


if __name__ == "__main__":
    result = solve_math_worksheet("puzzle_input.txt")
    print(f"Grand total: {result}")
