import re
import time
from heapq import heappush, heappop

def get_dep_pair(input_line):
    p = re.compile("[A-Z]");
    return p.findall(input_line)[1:]

def parse_input(filename):
    with open(filename, 'r') as f:
        dep_pairs = [get_dep_pair(l.strip()) for l in f]
    return dep_pairs

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parents = []

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parents.append(parent)

def construct_graph(dep_list):
    node_dict = {}
    for dep in dep_list:
        if not dep[0] in node_dict:
            node_dict[dep[0]] = Node(dep[0])
        if not dep[1] in node_dict:
            node_dict[dep[1]] = Node(dep[1])
        node_dict[dep[0]].add_child(node_dict[dep[1]])
        node_dict[dep[1]].add_parent(node_dict[dep[0]])
    top_nodes = [n for n in node_dict.values() if n.parents == []]
    return top_nodes

def heap_node(node, offset):
    return [ord(node.value) - 64 + offset, node]

def print_tree(root_nodes):
    eligible = []
    seen = set()
    for root_node in root_nodes:
        heappush(eligible, heap_node(root_node, 60))
    solution = ''
    while eligible:
        curr_node = heappop(eligible)[1]
        solution += curr_node.value
        seen.add(curr_node.value)
        for child in curr_node.children:
            if set(x.value for x in child.parents) <= seen:
                heappush(eligible, heap_node(child, 60))
    print(solution)
    return solution

def handle_tree_workers(root_nodes, num_workers, offset):
    eligible = []
    current = []
    seen = set()
    time_taken = 0
    for root_node in root_nodes:
        heappush(eligible, heap_node(root_node, offset))
    solution = ''
    while eligible or current:
        while eligible and len(current) < num_workers:
            new_node = heappop(eligible)[1]
            heappush(current, heap_node(new_node, offset))

        lowest_val = current[0][0]
        time_taken += lowest_val
        for c in current:
            c[0] -= lowest_val

        for c in current:
            if c[0] == 0:
                rem = heappop(current)
                solution += rem[1].value
                seen.add(rem[1].value)
                for child in rem[1].children:
                    if set(x.value for x in child.parents) <= seen:
                        heappush(eligible, heap_node(child, offset))

    print(solution, time_taken)
    return (solution, time_taken)

def part1(dep_list):
    root_nodes = construct_graph(dep_list)
    return print_tree(root_nodes)

def part2(dep_list, num_workers, offset):
    root_nodes = construct_graph(dep_list)
    return handle_tree_workers(root_nodes, num_workers, offset)

test_input = parse_input('test_input.txt')
assert(part1(test_input) == 'CABDFE')
assert(part2(test_input, 2, 0) == ('CABFDE', 15))

start = time.time()
real_input = parse_input('input.txt')
part1(real_input)
print(f"Took {time.time() - start} seconds to complete Part 1")
start = time.time()
part2(real_input, 5, 60)
print(f"Took {time.time() - start} seconds to complete Part 2")
