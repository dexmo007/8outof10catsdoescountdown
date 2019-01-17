#!/usr/bin/python3
import multiprocessing
import itertools
import operator
import time

ops = {
    operator.add: '+',
    operator.mul: '*',
    operator.sub: '-',
    operator.truediv: '/'
}

def is_float(num):
    return isinstance(num, float)

def ocs(j, n, total_ops):
    if n == total_ops:
        return list(map(lambda x: x[0],filter(lambda x: x[1] == 2, j)))
    else:
        next_j = []
        for (os, ns) in j:
            for i in range(ns):
                next_j.append((os+[i],ns+1-i))
        return ocs(next_j, n + 1, total_ops)

def get_map_entries(total_ops):
    _map = []
    for oc in ocs([([], 2)], 0, total_ops):
        map_entry = []
        counter = 2
        for o in oc:
            if o == 0:
                counter += 1
            else:
                map_entry.append(counter)
                counter = 1
                map_entry.extend([0] * o)
        _map.append(map_entry)
    return _map

def calculate_direct(map_entry, numbers, op_stack):
    stack = []
    i_numbers = 0
    i_op_stack = 0
    for rule in map_entry:
        if rule > 0:
            for _ in range(rule):
                stack.append(numbers[i_numbers])
                i_numbers += 1
        else:
            op = op_stack[i_op_stack]
            i_op_stack += 1
            r = stack.pop()
            l = stack.pop()
            res = op(l, r)
            if res == l or res <= 0 or is_float(res):
                return False
            stack.append(res)
    return (True, stack[0])

def build_possibilities():
    cpu = 0
    cpu_count = multiprocessing.cpu_count()
    possibilities = [[]] * cpu_count
    for k in range(2,7):
        map_entries = get_map_entries(k - 1)
        op_stacks = list(itertools.product(ops.keys(), repeat=k - 1))
        for combination in itertools.combinations([1,2,3,4,5,6], k):
            for permutation in itertools.permutations(combination):
                for map_entry in map_entries:
                    for op_stack in op_stacks:
                        possibilities[cpu].append((map_entry, permutation, op_stack))
                        cpu += 1
                        if cpu == cpu_count:
                            cpu = 0  
    return possibilities

def solve(possibilities, output):
    solutions = 0
    tested = 0
    for (map_entry, permutation, op_stack) in possibilities:
        tested += 1
        try:
            success, res = calculate_direct(map_entry, permutation, op_stack)
            if success and res == 6:
                solutions += 1
        except:
            pass
    output.put((tested, solutions))

start = time.time()
queue = multiprocessing.Queue()
possibilities = build_possibilities()
processes = [multiprocessing.Process(target=solve, args=(possibilities[cpu], queue)) for cpu in range(multiprocessing.cpu_count())]

for p in processes:
    p.start()

for p in processes:
    p.join()

elapsed = time.time() - start
results = [queue.get() for _ in processes]

t = 0
s = 0
for (tested, solutions) in results:
    t += tested
    s += solutions
print(f'Tested {t} possibilities in {elapsed}')
print(f'Found {s} solutions')