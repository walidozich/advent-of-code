def solve_math_worksheet(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    lines = [line.rstrip('\n') for line in lines]
    
    if len(lines) < 4:
        raise ValueError("Expected at least 4 lines in the input")
    
    number_rows = [lines[i] for i in range(len(lines) - 1)]
    operator_row = lines[-1]
    
    max_len = max(len(row) for row in lines)
    
    number_rows = [row.ljust(max_len) for row in number_rows]
    operator_row = operator_row.ljust(max_len)
    
    separator_cols = set()
    for col in range(max_len):
        if all(number_rows[i][col] == ' ' for i in range(len(number_rows))) and operator_row[col] == ' ':
            separator_cols.add(col)
    
    problems = []
    col = max_len - 1
    
    while col >= 0:
        while col >= 0 and col in separator_cols:
            col -= 1
        
        if col < 0:
            break
        
        problem_cols = []
        while col >= 0 and col not in separator_cols:
            problem_cols.append(col)
            col -= 1
        
        problem_cols.reverse()
        
        numbers = []
        operation = None
        
        for col_idx in problem_cols:
            num_str = ""
            for row_idx in range(len(number_rows)):
                if number_rows[row_idx][col_idx].isdigit():
                    num_str += number_rows[row_idx][col_idx]
            
            if num_str:
                numbers.append(int(num_str))
            
            if operator_row[col_idx] in ['+', '*']:
                if not operation:
                    operation = operator_row[col_idx]
        
        if numbers and operation:
            problems.append({'numbers': numbers, 'operation': operation})
    
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
