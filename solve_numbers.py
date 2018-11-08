#!/usr/bin/python3
import sys
import itertools
import operator

numbers = []
for ns in sys.argv[1].split(','):
    ns = ns.strip()
    numbers.append(int(ns))

target = int(sys.argv[2])

solutions = []

OPS = [
    (operator.add, '+'),
    (operator.sub, '-'),
    (operator.mul, '*'),
    (operator.truediv, '/'),
]

def is_float(num):
    return isinstance(num, float)

def test_order(inter, ops, p):
    if is_float(inter):
        return
    if inter == target:
        solutions.append(ops)
        return
    if not p:
        return

    for i in range(len(p)):
        #todo optimization: if next inter value was previously reached we don't to test this path
        chosen=p[i]
        if chosen in p[:i]:
            # skip testing duplicate values again
            continue
        for op, op_prefix in OPS:
            res = op(inter, chosen)
            if inter == res:
                continue
            test_order(res, ops+[f'{op_prefix}{chosen}'], p[:i]+p[(i+1):])
    if len(p) >= 2:
        for l,r in itertools.combinations(p, 2):
            for lrop, lrs in OPS:
                new_p = p[:]
                new_p.remove(l)
                new_p.remove(r)
                lrres = lrop(l,r)
                if lrres != 0 and not is_float(lrres):
                    test_order(inter, ops, new_p + [lrres])
                    


for j in range(len(numbers)):
    test_order(numbers[j], [str(numbers[j])],numbers[:j]+numbers[(j+1):])

if not solutions:
    print('No solution found')
    exit()
solutions.sort(key=len)
terms=[]
for solution in solutions:
    first,*rest=solution
    term=first
    for r in rest:
        if len(term) > 1 and (r.startswith('*') or r.startswith('/')):
            term=f'({term}){r}'
        else:
            term=f'{term}{r}'
    terms.append(term)

terms=list(set(terms))
terms.sort(key=len)
if len(sys.argv) > 3 and 'v' in sys.argv[3]:
    for term in terms:
        print(term)
    print(f'found {len(terms)} solutions')
else:
    print(f'the shorted solution {terms[0]}')
    print(f'{len(solutions) - 1} more solutions found')