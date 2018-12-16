import time
import sys

def get_neighboring(grid, x, y):
    max_y = len(grid)
    max_x = len(grid[0])
    up_value = grid[y-1][x] if y - 1 >= 0 else None
    left_value = grid[y][x-1] if x - 1 >= 0 else None
    right_value = grid[y][x+1] if x + 1 < max_x else None
    down_value = grid[y+1][x] if y + 1 < max_y else None
    up_dir = (x, y - 1)
    left_dir = (x - 1, y)
    right_dir = (x + 1, y)
    down_dir = (x, y + 1)
    up = (up_dir, up_value)
    left = (left_dir, left_value)
    right = (right_dir, right_value)
    down = (down_dir, down_value)
    return [up, left, right, down]

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemy = 'N'
        self.ally = 'N'
        self.alive = True
        self.health = 200
        self.damage_given = 3
        self.moved = False
    
    def coords(self):
        return (self.x, self.y)
    
    def take_damage(self, damage_taken):
        self.health -= damage_taken
        if self.health <= 0:
            self.alive = False
            return True, 'EG'.find(self.ally)
        return False, -1
    
    def attack(self, grid, bad_neighbors, entity_dict, team_counts):
        bad_entities = [entity_dict[n[0]] for n in bad_neighbors]
        min_health = min(bad_entities, key = lambda x: x.health).health
        min_health_enemies = [e for e in bad_entities if e.health == min_health]
        min_health_enemies.sort(key=lambda e: (e.y, e.x))
        enemy = min_health_enemies[0]

        killed, idx = enemy.take_damage(self.damage_given)
        if killed:
            team_counts[idx] -= 1
            kill_x, kill_y = enemy.coords()
            grid[kill_y][kill_x] = '.'
            entity_dict.pop(enemy.coords())
    
    def move(self, grid, entity_dict, team_counts):
        if not self.alive:
            return
        self.moved = True
        bfs_queue = [(self.coords(), [self.coords()])]
        queued = set([self.coords()])
        enemy_found = False

        while len(bfs_queue) > 0 and not enemy_found:
            curr_coords, path_to_curr = bfs_queue.pop(0)
            neighbors = get_neighboring(grid, *curr_coords)
            for n in neighbors:
                if self.enemy == n[1]:
                    if len(path_to_curr) > 1:
                        old_x, old_y = path_to_curr[0]
                        new_x, new_y = path_to_curr[1]
                        self.x, self.y = new_x, new_y
                        grid[new_y][new_x] = self.ally
                        grid[old_y][old_x] = '.'

                        entity_dict[(new_x, new_y)] = entity_dict.pop((old_x, old_y))

                
                    enemy_found = True
                    if len(path_to_curr) <= 2:
                        bad_neighbors = [n for n in neighbors if n[1] == self.enemy]
                        self.attack(grid, bad_neighbors, entity_dict, team_counts)

                    break
                
                if n[0] not in queued and n[1] == '.':
                    bfs_queue.append((n[0], path_to_curr + [n[0]]))
                    queued.add(n[0])

class Elf(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemy = 'G'
        self.ally = 'E'

    def get_health_string(self):
        return f"E: {self.health}"
    

class Goblin(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.enemy = 'E'
        self.ally = 'G'

    def get_health_string(self):
        return f"G: {self.health}"

def parse_lines(lines):
    num_rows = len(lines)
    num_columns = len(lines[0])
    grid = [[' ' for i in range(num_columns)] for i in range(num_rows)]
    elves = []
    goblins = []
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == 'E':
                elves.append(Elf(x, y))
            elif c == 'G':
                goblins.append(Goblin(x, y))
            grid[y][x] = c
    
    return grid, elves, goblins

def print_grid(grid, entity_dict):
    elves = filter(lambda x: x.ally == 'E', entity_dict.values())
    goblins = filter(lambda x: x.ally == 'G', entity_dict.values())
    elf_tiles = { e.coords(): e for e in elves }
    goblin_tiles = { g.coords(): g for g in goblins }

    for j in range(len(grid[0])):
        if j % 10 == 6:
            print("5", end = '')
        elif j % 10 == 1:
            print("0", end = '')
        else:
            print(' ', end = '')
    print("")
    for y, l in enumerate(grid):
        row_entities = []
        if y % 10 == 5:
            print("5", end='')
        elif y % 10 == 0:
            print("0", end = '')
        else:
            print(' ', end='')
        for x, c in enumerate(l):
            if (x, y) in elf_tiles:
                row_entities.append(elf_tiles[(x, y)])
            elif (x, y) in goblin_tiles:
                row_entities.append(goblin_tiles[(x, y)])
            print(c, end='')

        print(f"\t{', '.join(e.get_health_string() for e in row_entities)}", end='')
        print("")
    print("")

def not_all_dead(entity_dict):
    return len(set(e.ally for e in entity_dict.values())) > 1

def part1(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f]
    
    grid, elves, goblins = parse_lines(lines)
    elves_goblins = sorted(elves + goblins, key=lambda e: (e.y, e.x))
    entity_dict = { e.coords(): e for e in elves_goblins }
    team_counts = [len(elves), len(goblins)]

    # print(f"INITIAL")
    # print_grid(grid, entity_dict)

    round_count = 0
    # while not_all_dead(entity_dict) > 0:
    while not_all_dead(entity_dict) > 0 and round_count < 79:
        # print(f"ROUND {round_count + 1}")
        for e in entity_dict.values():
            e.moved = False
        elves = list(filter(lambda x: x.ally == 'E', entity_dict.values()))
        goblins = list(filter(lambda x: x.ally == 'G', entity_dict.values()))
        elves_goblins = sorted(elves + goblins, key=lambda e: (e.y, e.x))
        for e in elves_goblins:
            if e.coords() not in entity_dict:
                continue
            e.move(grid, entity_dict, team_counts)
            if team_counts[0] == 0 or team_counts[1] == 0:
                break
        
        if team_counts[0] == 0 or team_counts[1] == 0:
            break
        
        # print_grid(grid, entity_dict)
        round_count += 1
    
    num_moved = sum([1 if e.moved else 0 for e in entity_dict.values()])
    if num_moved == len(entity_dict):
        round_count += 1
    # print(f"FINAL GRID: {round_count} rounds")
    # print_grid(grid, entity_dict)
    return round_count * sum(e.health for e in entity_dict.values())

def part2(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f]
    
    curr_power = 4

    while True:
        grid, elves, goblins = parse_lines(lines)
        orig_num_elves = len(elves)
        for e in elves:
            e.damage_given = curr_power
        elves_goblins = sorted(elves + goblins, key=lambda e: (e.y, e.x))
        entity_dict = { e.coords(): e for e in elves_goblins }
        team_counts = [len(elves), len(goblins)]

        # print(f"INITIAL")
        # print_grid(grid, entity_dict)

        elf_killed = False
        round_count = 0
        while not_all_dead(entity_dict) > 0 and elf_killed == False:
            # print(f"ROUND {round_count + 1}")
            for e in entity_dict.values():
                e.moved = False
            elves = list(filter(lambda x: x.ally == 'E', entity_dict.values()))
            goblins = list(filter(lambda x: x.ally == 'G', entity_dict.values()))
            elves_goblins = sorted(elves + goblins, key=lambda e: (e.y, e.x))
            for e in elves_goblins:
                if e.coords() not in entity_dict:
                    continue
                e.move(grid, entity_dict, team_counts)
                if team_counts[0] < orig_num_elves:
                    elf_killed = True
                    break
                if team_counts[0] == 0 or team_counts[1] == 0:
                    break
            
            if team_counts[0] == 0 or team_counts[1] == 0 or elf_killed:
                break
            
            # print_grid(grid, entity_dict)
            round_count += 1
        
        if not elf_killed:
            num_moved = sum([1 if e.moved else 0 for e in entity_dict.values()])
            if num_moved == len(entity_dict):
                round_count += 1
            # print(f"FINAL GRID: {round_count} rounds")
            # print_grid(grid, entity_dict)
            return curr_power, round_count * sum(e.health for e in entity_dict.values())
        else:
            curr_power += 1

def do_assert(actual, expected):
    try:
        assert actual == expected
    except:
        print(f"Expected {expected} but received {actual}")

def test_part1():
    do_assert(part1('data/part1/test_input1.txt'), 27730)
    do_assert(part1('data/part1/test_input2.txt'), 36334)
    do_assert(part1('data/part1/test_input3.txt'), 39514)
    do_assert(part1('data/part1/test_input4.txt'), 27755)
    do_assert(part1('data/part1/test_input5.txt'), 28944)
    do_assert(part1('data/part1/test_input6.txt'), 18740)

# test_part1()

def test_part2():
    do_assert(part2('data/part2/test_input1.txt'), 4988)
    do_assert(part2('data/part2/test_input2.txt'), 31284)
    do_assert(part2('data/part2/test_input3.txt'), 3478)
    do_assert(part2('data/part2/test_input4.txt'), 6474)
    do_assert(part2('data/part2/test_input5.txt'), 1140)

# test_part2()

part1_start = time.time()
part1('data/input.txt')
print(f"Answer to part 1 is: {part1('data/input.txt')}")
print(f"Took {time.time() - part1_start} seconds to complete Part 1")

part2_start = time.time()
part2_result = part2('data/input.txt')
print(f"Answer to part 2 is: {part2_result[1]}")
print(f"Elf power was {part2_result[0]}")
print(f"Took {time.time() - part2_start} seconds to complete Part 2")