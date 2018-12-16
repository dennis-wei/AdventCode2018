import time
from collections import Counter, defaultdict
from functools import reduce
import copy

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.alive = True
        self.direction = direction
        # ["left", "straight", "up"]
        self.intersection_index = 0

    def coords(self):
        return (self.x, self.y)
    
    def kill(self):
        self.alive = False
    
    def move_up(self):
        self.y -= 1
        self.direction = "up"
    
    def move_down(self):
        self.y += 1
        self.direction = "down"
    
    def move_left(self):
        self.x -= 1
        self.direction = "left"
    
    def move_right(self):
        self.x += 1
        self.direction = "right"
    
    def turn_left(self):
        if self.direction == "up":
            self.move_left()
        elif self.direction == "down":
            self.move_right()
        elif self.direction == "left":
            self.move_down()
        elif self.direction == "right":
            self.move_up()

    def turn_right(self):
        if self.direction == "up":
            self.move_right()
        elif self.direction == "down":
            self.move_left()
        elif self.direction == "left":
            self.move_up()
        elif self.direction == "right":
            self.move_down()

    def straight(self):
        if self.direction == "up":
            self.move_up()
        elif self.direction == "down":
            self.move_down()
        elif self.direction == "left":
            self.move_left()
        elif self.direction == "right":
            self.move_right()
    
    def handle_intersection(self):
        [self.turn_left, self.straight, self.turn_right][self.intersection_index]()
        self.intersection_index = (self.intersection_index + 1) % 3
    
    def move(self, track):
        if track == '+':
            self.handle_intersection()
        elif track == '/':
            if self.direction == "left":
                self.move_down()
            elif self.direction == "up":
                self.move_right()
            elif self.direction == "right":
                self.move_up()
            elif self.direction == "down":
                self.move_left()
        elif track == '\\':
            if self.direction == "left":
                self.move_up()
            elif self.direction == "up":
                self.move_left()
            elif self.direction == "right":
                self.move_down()
            elif self.direction == "down":
                self.move_right()
        elif track == '-':
            if self.direction == "left":
                self.move_left()
            elif self.direction == "right":
                self.move_right()
        elif track == '|':
            if self.direction == "up":
                self.move_up()
            elif self.direction == "down":
                self.move_down()
        

def parse_input(lines):
    grid = {}
    carts = []
    cart_chars = set('^v<>')
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c in cart_chars:
                if c == '<':
                    grid[(x, y)] = '-'
                    carts.append(Cart(x, y, "left"))
                elif c == '>':
                    grid[(x, y)] = '-'
                    carts.append(Cart(x, y, "right"))
                elif c == '^':
                    grid[(x, y)] = '|'
                    carts.append(Cart(x, y, "up"))
                elif c == 'v':
                    grid[(x, y)] = '|'
                    carts.append(Cart(x, y, "down"))
            
            else:
                grid[(x, y)] = c
    
    return grid, carts

def is_crash(cart_list):
    coord_count = Counter()
    alive_carts = filter(lambda x: x.alive, cart_list)
    for cart in alive_carts:
        coord_count[cart.coords()] += 1
    
    most_common = coord_count.most_common(1)[0]
    return most_common[1] > 1, most_common[0]

def part1(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f]
    
    grid, carts = parse_input(lines)

    num_steps = 0
    while(True):
        # print(f"Handling step {num_steps}")
        num_steps += 1
        for c in carts:
            coords = c.coords()
            track = grid[coords]
            c.move(track)
        
        crash_occurred, location = is_crash(carts)
        if crash_occurred:
            print(f"Crash occurred on {location} at time {num_steps}")
            return location

def print_carts(cart_list):
    coords = [c.coords() for c in cart_list]
    print(coords)

def part2(filename):
    with open(filename, 'r') as f:
        lines = [l[:-1] for l in f]
    
    grid, carts = parse_input(lines)

    num_steps = 0
    while(len(carts) > 1):
        num_steps += 1
        carts.sort(key=lambda x: x.y)
        for c in carts:
            coords = c.coords()
            track = grid[coords]
            c.move(track)
            crash_occurred, location = is_crash(carts)
            if crash_occurred:
                for cart in filter(lambda x: x.coords() == location, carts):
                    cart.kill()
            carts = sorted(filter(lambda x: x.alive, carts), key=lambda x: x.y)
            
    
    print(f"Last remaining cart is at {carts[0].coords()}")
    return carts[0].coords()

print("TEST CASES")
assert(part1('test_input.txt') == (7, 3))
assert(part2('test_input2.txt') == (6,4))
print("")

print("STARTING MAIN")
part1_start = time.time()
part1('input.txt')
print(f"Took {time.time() - part1_start} seconds to finish Part 1")
part2_start = time.time()
# Answer should be 145,88
part2('input.txt')
print(f"Took {time.time() - part2_start} seconds to finish Part 2")