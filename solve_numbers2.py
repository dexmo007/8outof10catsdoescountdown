#!/usr/bin/python3
import sys
import itertools
import operator
import time

tiles = []
for ns in sys.argv[1].split(','):
    ns = ns.strip()
    tiles.append(int(ns))

target = int(sys.argv[2])

ops = {
    operator.add: '+',
    operator.mul: '*',
    operator.sub: '-',
    operator.truediv: '/'
}

def is_float(num):
    return isinstance(num, float)

def calculate(e):
    stack = []
    for i in range(len(e)):
        el = e[i]
        if callable(el):
            r, rrep = stack.pop()
            l, lrep = stack.pop()
            res = el(l, r)
            if res == l:
                raise 'Identity operations are redundant'
            if res == 0:
                raise 'Zeros are redundant'
            if res < 0:
                raise 'No negs allowed'
            if is_float(res):
                raise 'Floating points are not allowed'
            stack.append((res, f'({lrep}{ops[el]}{rrep})'))
        else:
            stack.append((el, str(el)))
    if len(stack) != 1:
        raise f'Invalid equation {stack}'
    return stack[0]

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
                for _ in range(o):
                    map_entry.append(0)
        _map.append(map_entry)
    return _map
#equation = [1,2,4,operator.add,3,3,operator.mul, operator.add, operator.mul]

def build_equation(map_entry, numbers, op_stack):
    equation = []
    for rule in map_entry:
        if rule > 0:
            for _ in range(rule):
                equation.append(numbers.pop())
        else:
            equation.append(op_stack.pop())
    return equation

start = time.time()
i = 0
solutions = []
for k in range(2, len(tiles) + 1):
    map_entries = get_map_entries(k - 1)
    for combination in itertools.combinations(tiles, k):
        for permutation in itertools.permutations(combination):
            for map_entry in map_entries:
                for op_stack in itertools.product(ops.keys(), repeat=k - 1):
                    i = i + 1
                    equation = build_equation(map_entry, list(permutation), list(op_stack))
                    try:
                        res, eqrepr = calculate(equation)
                        if res == target:
                            solutions.append(eqrepr)
                    except:
                        pass
                    
for solution in solutions:
    print(solution)
print(f'Tested {i} combinations in {time.time() - start}')
print(f'Found {len(solutions)} solutions')
