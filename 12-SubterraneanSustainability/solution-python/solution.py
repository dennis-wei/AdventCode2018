from collections import deque
import copy
import time

def parse_file(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f]
    
    initial_input = deque([i, e] for i, e in enumerate(list(lines[0])))
    split_patterns = [l.split(" => ") for l in lines[2:]]
    pattern_dict = { s[0]: s[1] for s in split_patterns }
    return initial_input, pattern_dict

def pad_state(state):
    if state[0][1] == "#":
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
    elif state[1][1] == '#':
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
    elif state[2][1] == '#':
        state.appendleft([state[0][0] - 1, '.'])
        state.appendleft([state[0][0] - 1, '.'])
    elif state[3][1] == '#':
        state.appendleft([state[0][0] - 1, '.'])

    if state[-1][1] == "#":
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
    elif state[-2][1] == '#':
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
    elif state[-3][1] == '#':
        state.append([state[-1][0] + 1, '.'])
        state.append([state[-1][0] + 1, '.'])
    elif state[-4][1] == '#':
        state.append([state[-1][0] + 1, '.'])

def print_state(state):
    print(' ', end='')
    print(' '.join(c[1] for c in state))
    print(' ', end='')
    print("")

def print_state_history(all_states):
    print("STATE HISTORY")
    min_i = all_states[-1][0][0]
    max_i = all_states[-1][-1][0]
    print((' ' * (abs(min_i) + 4)) + ('0         ' * (max_i // 10 + 1)))
    for i, state in enumerate(all_states):
        print(f"{i:2d}: {get_state_string(state, min_i, max_i)}")
    print("") 

def get_state_string(state, min_i, max_i):
    ret = ''
    start = state[0][0]
    for _i in range(min_i, start):
        ret += '.'
    ret += ''.join(c[1] for c in state)
    end = state[-1][0]
    for _i in range(end, max_i):
        ret += '.'
    return ret

def print_state_brackets(state, center):
    for i in range(len(state)):
        if i == center - 2:
            print('[' + state[i][1], end='')
        elif i == center + 3:
            print(']' + state[i][1], end='')
        else:
            print(' ' + state[i][1], end='')
    print("")

def print_with_arrow(state, center):
    for i in range(len(state)):
        if i == center - 2:
            print('[ ', end='')
        elif i == center + 3:
            print('] ', end='')
        elif i == center:
            print(' v', end='')
        else:
            print('  ', end='')
    print("")

def part1(filename, num_gens):
    curr_state, patterns = parse_file(filename)
    sum_lambda = lambda s: sum(x[0] for x in filter(lambda x: x[1] == '#', s))
    all_sums = [sum_lambda(curr_state)]
    for g in range(num_gens):
        pad_state(curr_state)
        new_state = copy.deepcopy(curr_state)
        for i in range(2, len(new_state) - 2):
            pattern = ''.join(curr_state[i][1] for i in range(i - 2, i + 3))
            new_state[i][1] = patterns.get(pattern, '.')
        
        curr_state = new_state
        all_sums.append(sum_lambda(curr_state))

    return all_sums

def part2(filename, num_gens):
    all_sums = part1(filename, 200)
    diffs = [all_sums[i + 1] - all_sums[i] for i in range(len(all_sums) - 1)]
    repeating_diff = diffs[-1]
    starting_index = diffs.index(repeating_diff)
    return all_sums[starting_index] + (num_gens - starting_index) * repeating_diff

assert part1('../data/test_input.txt', 20)[-1] == 325
part1_start = time.time()
print(part1('../data/input.txt', 20)[-1])
print(f"Took {time.time() - part1_start} seconds to complete Part 1")
part2_start = time.time()
print(part2('../data/input.txt', 50000000000))
print(f"Took {time.time() - part2_start} seconds to complete Part 2")