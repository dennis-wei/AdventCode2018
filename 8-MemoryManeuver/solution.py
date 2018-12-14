import time

class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def add_child(self, child):
        self.children.append(child)

    def add_metadata(self, new_meta):
        self.metadata.append(new_meta)

def get_tokens(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
    return map(int, line.split())

def construct_node(t_iter):
    num_children = next(t_iter)
    num_metadata = next(t_iter)
    children = []
    metadata = []
    for i in range(num_children):
        child = construct_node(t_iter)
        children.append(child)

    for i in range(num_metadata):
        metadata.append(next(t_iter))

    return Node(children, metadata)

def sum_metadata(node):
    return sum(node.metadata) + sum(sum_metadata(c) for c in node.children)

def construct_tree(tokens):
    return construct_node(iter(tokens))

def part1(root):
    res = sum_metadata(root)
    print(f"Part 1 result is {res}")
    return res

def sum_meta_idx(node):
    if len(node.children) == 0:
        return sum(node.metadata)

    agg = 0
    for m in node.metadata:
        idx = m - 1
        if idx >= len(node.children):
            continue

        agg += sum_meta_idx(node.children[idx])
    return agg

def part2(root):
    res = sum_meta_idx(root)
    print(f"Part 2 result is {res}")
    return res

test_tokens = get_tokens('test_input.txt')
test_root = construct_tree(test_tokens)
assert(part1(test_root) == 138)
assert(part2(test_root) == 66)
print()

start = time.time()
real_tokens = get_tokens('input.txt')
real_tree = construct_tree(real_tokens)
part1(real_tree)
print(f"Took {time.time() - start} seconds to complete Part 1")
start = time.time()
part2(real_tree)
print(f"Took {time.time() - start} seconds to complete Part 2")
