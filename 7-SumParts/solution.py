import re
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

def heap_node(node):
    return (ord(node.value) - 4, node)

def print_tree(root_nodes):
    eligible = []
    seen = set()
    for root_node in root_nodes:
        heappush(eligible, heap_node(root_node))
    solution = ''
    while eligible:
        curr_node = heappop(eligible)[1]
        solution += curr_node.value
        seen.add(curr_node.value)
        for child in curr_node.children:
            if set(x.value for x in child.parents) <= seen:
                heappush(eligible, heap_node(child))
    print(solution)
    return solution

def handle_tree_workers(root_nodes, num_workers):
    eligible = []
    current = []
    seen = set()
    for root_node in root_nodes:
        heappush(eligible, heap_node(root_node))
    solution = ''
    while eligible:
        while eligible and len(current) <= 5:
            new_node = heappop(eligible)[1]
            heappush(current, heap_node(new_node))

def part1(dep_list):
    root_nodes = construct_graph(dep_list)
    return print_tree(root_nodes)

def part2(dep_list, num_workers):
    root_nodes = construct_graph(dep_list)
    return handle_tree_workers(root_nodes, num_workers)

test_input = parse_input('test_input.txt')
assert(part1(test_input) == 'CABDFE')
assert(part2(test_input, 2) == 15)

real_input = parse_input('input.txt')
part1(real_input)
