def solve_math_worksheet(filename):
    """
    Parse the math worksheet and solve all problems using cephalopod math.
    
    Cephalopod math is written right-to-left in columns.
    Each number is given in its own column, with the most significant digit at the top
    and the least significant digit at the bottom.
    
    Problems are separated with a column consisting only of spaces.
    The symbol at the bottom of the problem is still the operator to use.
    
    Example:
    123 328  51 64
     45 64  387 23
      6 98  215 314
    *   +   *   +
    
    Reading right-to-left, one column at a time:
    - Rightmost problem: column 14 (4,3,4) + column 13 (6,2,1) = 4 + 621 = ...
    - Problems are processed from right to left
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
    separator_cols = set()
    for col in range(max_len):
        if all(number_rows[i][col] == ' ' for i in range(len(number_rows))) and operator_row[col] == ' ':
            separator_cols.add(col)
    
    # Process columns from right to left
    problems = []
    col = max_len - 1
    
    while col >= 0:
        # Skip trailing separator columns
        while col >= 0 and col in separator_cols:
            col -= 1
        
        if col < 0:
            break
        
        # Collect columns for this problem (reading right-to-left)
        problem_cols = []
        while col >= 0 and col not in separator_cols:
            problem_cols.append(col)
            col -= 1
        
        # Reverse to get left-to-right order for easier processing
        problem_cols.reverse()
        
        # Extract numbers and operation from these columns
        numbers = []
        operation = None
        
        for col_idx in problem_cols:
            # Read this column top-to-bottom to form a number
            num_str = ""
            for row_idx in range(len(number_rows)):
                if number_rows[row_idx][col_idx].isdigit():
                    num_str += number_rows[row_idx][col_idx]
            
            if num_str:
                numbers.append(int(num_str))
            
            # Check for operation in this column
            if operator_row[col_idx] in ['+', '*']:
                if not operation:
                    operation = operator_row[col_idx]
        
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
