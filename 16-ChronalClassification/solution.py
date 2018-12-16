import re
import time

def addr(tokens, a, b, c):
    result = tokens[a] + tokens[b]
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def addi(tokens, a, b, c):
    result = tokens[a] + b
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def mulr(tokens, a, b, c):
    result = tokens[a] * tokens[b]
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def muli(tokens, a, b, c):
    result = tokens[a] * b
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def banr(tokens, a, b, c):
    result = tokens[a] & tokens[b]
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def bani(tokens, a, b, c):
    result = tokens[a] & b
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def borr(tokens, a, b, c):
    result = tokens[a] | tokens[b]
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def bori(tokens, a, b, c):
    result = tokens[a] | b
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def setr(tokens, a, b, c):
    result = tokens[a]
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def seti(tokens, a, b, c):
    result = a
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def gtir(tokens, a, b, c):
    result = int(a > tokens[b])
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def gtri(tokens, a, b, c):
    result = int(tokens[a] > b)
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens
    
def gtrr(tokens, a, b, c):
    result = int(tokens[a] > tokens[b])
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def eqir(tokens, a, b, c):
    result = int(a == tokens[b])
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

def eqri(tokens, a, b, c):
    result = int(tokens[a] == b)
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens
    
def eqrr(tokens, a, b, c):
    result = int(tokens[a] == tokens[b])
    new_tokens = tokens[:]
    new_tokens[c] = result
    return new_tokens

OP_FUNCTIONS = [
    addr,
    addi,
    mulr,
    muli,
    banr,
    bani,
    borr,
    bori,
    setr,
    seti,
    gtir,
    gtri,
    gtrr,
    eqir,
    eqri,
    eqrr
]

def get_num_viable(before, op, after):
    a, b, c = op[1:]
    num_viable = 0
    for f in OP_FUNCTIONS:
        if f(before, a, b, c) == after:
            num_viable += 1
            # print(f"{f.__name__} was viable for {before} | {op} | {after}")

    return num_viable

def get_viable_funcs(opcode_map, before, op, after):
    op_number, a, b, c = op
    viable = set()
    for f in OP_FUNCTIONS:
        if f(before, a, b, c) == after:
            viable.add(f)
    
    opcode_map[op_number] = opcode_map[op_number] & viable

def parse_set(lines):
    numbers = re.compile(r'\d+')
    parsed_lines = [numbers.findall(l) for l in lines]
    int_lines = [list(map(int, l)) for l in parsed_lines]
    return tuple(int_lines)

def part1(filename):
    with open(filename, 'r') as f:
        sample_sets = [s.split("\n") for s in f.read().split("\n\n")]
    
    parsed_sets = [parse_set(s) for s in sample_sets]

    sufficient_sets = list(filter(lambda x: get_num_viable(*x) >=3, parsed_sets))
    print(f"There are {len(sufficient_sets)} sets that have at least 3 satisfying op codes")
    return len(sufficient_sets)

def get_singleton_sets(opcode_map):
    return { k: v for k, v in opcode_map.items() if len(v) == 1}

def reduce_opcode_map(opcode_map):
    original_len = len(opcode_map)
    singleton_sets = get_singleton_sets(opcode_map)
    while len(singleton_sets) < original_len:
        for v1 in singleton_sets.values():
            fun = list(v1)[0]
            for v2 in opcode_map.values():
                if fun in v2 and len(v2) > 1:
                    v2.remove(fun)
        singleton_sets = get_singleton_sets(opcode_map)

def get_final_opcode_map(opcode_file):
    with open(opcode_file, 'r') as f:
        sample_sets = [s.split("\n") for s in f.read().split("\n\n")]

    parsed_sets = [parse_set(s) for s in sample_sets]

    opcode_map = { i: set(f for f in OP_FUNCTIONS) for i in range(len(OP_FUNCTIONS)) }

    for s in parsed_sets:
        get_viable_funcs(opcode_map, *s)
    
    reduce_opcode_map(opcode_map)
    return { k: list(v)[0] for k, v in opcode_map.items() }

def parse_program(program_file):
    with open(program_file, 'r') as f:
        str_tokens = [l.strip().split() for l in f]
        tokens = [list(map(int, l)) for l in str_tokens]
    return tokens

def part2(opcode_file, program_file):
    opcode_map = get_final_opcode_map(opcode_file)
    instruction_list = parse_program(program_file)
    curr_device = [0, 0, 0, 0]
    for ins in instruction_list:
        opcode, a, b, c = ins
        fun = opcode_map[opcode]
        curr_device = fun(curr_device, a, b, c)
    
    print(f"The final register is {curr_device}")

def test():
    assert part1('test_input.txt') == 1

part1_start = time.time()
part1('input_part1.txt')
print(f"Part 1 took {time.time() - part1_start} seconds")
part2_start = time.time()
part2('input_part1.txt', 'input_part2.txt')
print(f"Part 2 took {time.time() - part2_start} seconds")