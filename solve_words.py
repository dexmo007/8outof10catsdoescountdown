#!/usr/bin/python3
import sys
import itertools

letters = list(map(lambda l: l.strip().lower(), sys.argv[1].split(',')))
for l in letters:
    if len(l) != 1:
        raise "Must be letters"
    
n_letters = len(letters)
print(f'Working with {n_letters} letters: {letters}')

def can_be_build(word):
    if len(word) > n_letters:
        return False
    al = set(letters)
    for l in word:
        if l in al:
            al.remove(l)
        else:
            return False
    return True

possible_words = []
with open('words_alpha.txt') as f:
    for line in f:
        line = line.strip()
        if len(line) < 2:
            continue
        if can_be_build(line):
            possible_words.append(line)

if not possible_words:
    print('There is no solution!')
    exit
possible_words.sort(key=len,reverse=True)
solutions = itertools.groupby(possible_words, key=len)
best_count, best_words = next(solutions)
print(f'The best solution(s) is/are ({best_count} letters): {", ".join(list(best_words))}')
print('The remaining possibilties are:')
for k,g in solutions:
    print(f'\tWith {k} letters: {", ".join(list(g))}')
