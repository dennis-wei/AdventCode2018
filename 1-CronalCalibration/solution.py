import time

start = time.time()
with open('input.txt', 'r') as f:
    nums = [int(l.strip()) for l in f]

print(f'Part 1 solution is {sum(nums)}')

curr = 0
curr_index = 0
reached = set()

while True:
    curr += nums[curr_index]
    if curr in reached:
        print(f'Part 2 solution is {curr}')
        break
    else:
        reached.add(curr)
        curr_index = (curr_index + 1) % len(nums)

print(f'Took {time.time() - start} seconds')