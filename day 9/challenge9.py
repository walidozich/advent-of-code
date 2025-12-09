#!/usr/bin/env python3

def read_input(filename):
    """Read the puzzle input and return a list of (x, y) coordinates."""
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                coordinates.append((x, y))
    return coordinates

def find_largest_rectangle(coordinates):
    """
    Find the largest rectangle that can be formed using any two red tiles
    as opposite corners.
    
    For two points to form opposite corners of a rectangle, they must have
    different x and different y coordinates. The area includes the boundary:
    (|x2 - x1| + 1) * (|y2 - y1| + 1)
    """
    max_area = 0
    n = len(coordinates)
    
    # Check all pairs of coordinates
    for i in range(n):
        x1, y1 = coordinates[i]
        for j in range(i + 1, n):
            x2, y2 = coordinates[j]
            
            # Calculate the area of the rectangle formed by these two corners
            # Include the boundary tiles in the count
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
    
    return max_area

def main():
    # Read the input
    coordinates = read_input('puzzle_input.txt')
    
    print(f"Number of red tiles: {len(coordinates)}")
    
    # Find the largest rectangle
    largest_area = find_largest_rectangle(coordinates)
    
    print(f"Largest rectangle area: {largest_area}")

if __name__ == "__main__":
    main()
