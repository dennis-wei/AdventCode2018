import numpy as np
from collections import defaultdict

def part1(filename):
    with open(filename, 'r') as f:
        coords = [tuple(int(x) for x in l.strip().split(', ')) for l in f]
    expanded_coords = [(x[0] + 1, x[1] + 1) for x in coords]

    max_x = max(c[0] for c in coords) + 2
    max_y = max(c[1] for c in coords) + 2

    reg_grid = np.zeros((max_x, max_y))
    expanded_grid = np.zeros((max_x + 2, max_y + 2))

    reg_counts = get_counts(coords, reg_grid, max_x, max_y)
    expanded_counts = get_counts(expanded_coords, expanded_grid, max_x, max_y)

    same_counts = set(reg_counts.items()) & set(expanded_counts.items())
    print(same_counts)
    result = max(same_counts, key=lambda x: x[1])
    print(result)
    return result[1]

def part2(filename, max_dist):
    with open(filename, 'r') as f:
        coords = [tuple(int(x) for x in l.strip().split(', ')) for l in f]
    expanded_coords = [(x[0] + 500, x[1] + 500) for x in coords]

    max_x = max(c[0] for c in coords) + 2
    max_y = max(c[1] for c in coords) + 2

    grid = np.zeros((max_x + 500, max_y + 500))

    for idx, _ in np.ndenumerate(grid):
        total_dist = sum(get_dist(idx, c) for c in expanded_coords)
        if total_dist < max_dist:
            grid[idx] = 1

    return np.sum(grid)

def get_dist(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def get_counts(main_coords, grid, max_x, max_y):
    for idx, _ in np.ndenumerate(grid):
        min_dist = max_x + max_y
        best_coord = -1
        for i, c in enumerate(main_coords):
            dist = get_dist(c, idx)
            if dist < min_dist:
                min_dist = dist
                best_coord = i
        grid[idx] = best_coord

    #  print(grid)
    counts = defaultdict(int)
    for cell in np.nditer(grid):
        counts[int(cell)] += 1

    return counts

assert(part1('test_input1.txt') == 17)
print(part2('test_input1.txt', 32))
assert(part2('test_input1.txt', 32) == 16)

part1('input.txt')
print(part2('input.txt', 10000))
