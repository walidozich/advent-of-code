#!/usr/bin/env python3
from shapely.geometry import Polygon, box

def read_input(filename):
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                coordinates.append((x, y))
    return coordinates

def find_largest_rectangle(red_tiles):
    polygon = Polygon(red_tiles)
    n = len(red_tiles)
    max_area = 0
    
    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area <= max_area:
                continue
            
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            rect = box(min_x, min_y, max_x, max_y)
            
            if polygon.contains(rect) or polygon.covers(rect):
                if area > max_area:
                    max_area = area
    
    return max_area

def main():
    red_tiles = read_input('puzzle_input.txt')
    largest_area = find_largest_rectangle(red_tiles)
    print(largest_area)

if __name__ == "__main__":
    main()
