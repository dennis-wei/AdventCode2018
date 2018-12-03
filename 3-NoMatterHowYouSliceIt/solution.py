from typing import List, Dict, Tuple
import numpy as np
import time

GridOffset = Tuple[int, int]
RectangleSize = Tuple[int, int]
Rectangle = Tuple[GridOffset, RectangleSize]
RectangleClaim = Tuple[Rectangle, int]

def parse_input_line(line: str) -> RectangleClaim:
    parts = line.split()
    claim = int(parts[0][1:])
    offset: GridOffset = tuple(map(int, parts[2][:-1].split(',')))
    size: RectangleSize = tuple(map(int, parts[3].split('x')))
    return ((offset, size), claim)

def add_zipped_rectangle(rectangle: Rectangle) -> Tuple[int, int]:
    zipped = zip(*rectangle)
    res = tuple(sum(x) + 1 for x in zipped) 
    return res

def construct_grid(rectangles: List[RectangleClaim]):
    added_rectangles = [add_zipped_rectangle(r[0]) for r in rectangles]
    max_length, max_width = tuple(max(x) for x in zip(*added_rectangles))
    print(f"max_length: {max_length}")
    print(f"max_width: {max_width}")
    full_grid = [[[] for i in range(max_length)] for i in range(max_width)]
    return np.zeros([max_length, max_width]), full_grid

def add_rectangle(
    number_grid: List[List[int]],
    list_grid: List[List[List[int]]],
    rectangle_claim: RectangleClaim
) -> None:
    rectangle, claim = rectangle_claim
    for i in range(rectangle[0][0], rectangle[0][0] + rectangle[1][0]):
        for j in range(rectangle[0][1], rectangle[0][1] + rectangle[1][1]):
            number_grid[i,j] += 1
            list_grid[i][j].append(claim)

start = time.time()

with open('input.txt', 'r') as f:
    input = [l.strip() for l in f]

rectangles = [parse_input_line(l) for l in input]
number_grid, list_grid = construct_grid(rectangles)

for rectangle in rectangles:
    add_rectangle(number_grid, list_grid, rectangle)

unique, counts = np.unique(number_grid, return_counts=True)
overlapped_squares = 0
for k, v in dict(zip(unique, counts)).items():
    if k >= 2:
        overlapped_squares += v

print(f"overlapped: {overlapped_squares}")

claims_set = set(r[1] for r in rectangles)
for row in list_grid:
    for entry in row:
        if len(entry) > 1:
            for c in entry:
                if c in claims_set:
                    claims_set.remove(c)

print(f"Lone non-overlapping claim is {list(claims_set)[0]}")

print(f"Took {time.time() - start} seconds")