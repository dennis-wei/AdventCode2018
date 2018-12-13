import re
import time

class MovingCoordinate:
    def __init__(self, coords, velocity):
        self.x, self.y = coords
        self.xvel, self.yvel = velocity
    
    def move(self):
        self.x += self.xvel
        self.y += self.yvel
    
    def get_coords(self):
        return (self.x, self.y)
    
    def get_neighbors(self):
        left = (self.x - 1, self.y)
        right = (self.x + 1, self.y)
        up = (self.x, self.y - 1)
        down = (self.x, self.y + 1)
        return [left, right, up, down]

def traverse_node(node, coord_dict, unseen, curr_group):
    removed_coord = node.get_coords()
    unseen.remove(node.get_coords())
    curr_group.append(removed_coord)
    for n in node.get_neighbors():
        if n in unseen:
            traverse_node(coord_dict[n], coord_dict, unseen, curr_group)

def get_num_distinct_trees(coord_dict):
    num_distinct = 0
    unseen = set(coord_dict.keys())
    while len(unseen) > 0:
        num_distinct += 1
        for random_coord in unseen:
            break
        curr_group = []
        traverse_node(coord_dict[random_coord], coord_dict, unseen, curr_group)
    
    # print(num_distinct)
    return num_distinct

def tokenize_line(line):
    p = re.compile('-?\d+')
    raw_tokens = [int(n) for n in p.findall(line)]
    return (tuple(raw_tokens[:2]), tuple(raw_tokens[2:]))

def tokenize_input(filename):
    with open(filename, 'r') as f:
        tokens = [tokenize_line(l) for l in f]
    return tokens

def normalize(coord, min_x, min_y):
    return (coord[0] - min_x, coord[1] - min_y)

def print_image(coord_list):
    min_x = min(p[0] for p in coord_list)
    min_y = min(p[1] for p in coord_list)
    max_x = max(p[0] for p in coord_list)
    max_y = max(p[1] for p in coord_list)
    
    coord_set = set(normalize(c, min_x, min_y) for c in coord_list)

    for j in range(max_y - min_y + 1):
        for i in range(max_x - min_x + 1):
            if (i, j) in coord_set:
                print('#', end='')
            else:
                print('.', end='')
        print()

def solution(filename, limit):
    tokens = tokenize_input(filename)
    coord_list = [MovingCoordinate(*t) for t in tokens]
    coord_dict = { c.get_coords(): c for c in coord_list }
    num_seconds = 0
    while get_num_distinct_trees(coord_dict) > limit:
        for c in coord_list:
            c.move()
        coord_dict = { c.get_coords(): c for c in coord_list }
        num_seconds += 1
    
    final_coord_list = [c.get_coords() for c in coord_list]
    print_image(final_coord_list)
    return num_seconds

assert(solution('../data/test_input.txt', 5) == 3)
print()
start = time.time()
print(solution('../data/input.txt', 50))
print(f"Took {time.time() - start} seconds to complete")