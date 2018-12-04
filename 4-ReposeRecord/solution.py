import re
from collections import defaultdict
import time

start = time.time()

with open('test_input_scrambled.txt', 'r') as f:
    test_lines = [l.strip() for l in f]

with open('test_input.txt', 'r') as f:
    test_sorted_lines = [l.strip() for l in f]

test_lines.sort(key = lambda x: x[:18])

assert(test_lines == test_sorted_lines)

with open('input.txt', 'r') as f:
    real_lines = [l.strip() for l in f]

real_lines.sort(key = lambda x: x[:18])

def is_begins_shift(line):
    if 'begins' in line:
        return int(re.findall('\d+', line[18:])[0])
    else:
        return None

def construct_guard_shifts(lines):
    guard_shift = {}
    curr_guard = None
    fall_asleep = None
    for line in lines:
        guard_id = is_begins_shift(line)
        if guard_id:
            curr_guard = guard_id
            continue
        
        if 'falls' in line:
            fall_asleep = int(re.findall(':\d+', line)[0][1:])
            continue
        
        if 'wakes' in line:
            wake_up = int(re.findall(':\d+', line)[0][1:])
        
        for i in range(fall_asleep, wake_up):
            if not curr_guard in guard_shift:
                guard_shift[curr_guard] = defaultdict(int)
            guard_shift[curr_guard][i] += 1
    
    return guard_shift

def part1(guard_shifts, lines_name):
    print(f"PART 1 - {lines_name.upper()}")

    times_asleep = []
    for k, v in guard_shifts.items():
        times_asleep.append((k, sum(v.values())))

    most_sleepy_guard = max(times_asleep, key = lambda x: x[1])[0]

    most_sleepy_guard_times = guard_shifts[most_sleepy_guard]
    most_slept_minute = max(most_sleepy_guard_times.items(), key = lambda x: x[1])[0]
    print(f"Sleepiest Guard: {most_sleepy_guard}")
    print(f"Most Slept Minute: {most_slept_minute}")
    res = most_sleepy_guard * most_slept_minute
    print(f"Result: {res}\n")
    return res

def get_most_slept_time(x):
    return max(x.items(), key = lambda y: y[1])

def part2(guard_shifts, lines_name):
    print(f"PART 2 - {lines_name.upper()}")

    guard_most_slept_time = [(k, get_most_slept_time(v)) for k, v in guard_shifts.items()]
    guard, slept_time_amount = max(guard_most_slept_time, key = lambda x: x[1][1])
    slept_time, slept_amount = slept_time_amount

    print(f"Guard ID: {guard}")
    print(f"Time: {slept_time}")
    print(f"Time Sleep Frequency: {slept_amount}")
    res = guard * slept_time
    print(f"Result: {res}\n")
    return res


test_guard_shifts = construct_guard_shifts(test_lines)
assert(part1(test_guard_shifts, "test_input") == 240)
assert(part2(test_guard_shifts, "test_input") == 4455)

real_guard_shifts = construct_guard_shifts(real_lines)
part1(real_guard_shifts, "real_input")
part2(real_guard_shifts, "real_input")

print(f"Took {time.time() - start} seconds")