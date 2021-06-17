# AoC 2019. Day 14. Space Stoichiometry
import util
from collections import namedtuple

Substance = namedtuple('Substance', 'name', 'amount')
Formula = namedtuple('Formula', 'source', 'result_name', 'result_amount')


def decompose(reactions, sub: Substance):
    formula = reactions[sub.name]
    required = formula.source
    if required[0].name == 'ORE':
        return sub
    # учесть sub.amount и formula.result_amount
    for s in required:

    return required

# data = dict['result_substance': [('result_substance_name',amount),('substance', amount), ...]]


def calc_ore(reactions) -> int:
    required = reactions['FUEL'].source
    while True:
        required_old = required
        required = []
        for sub in required_old:
            subs = decompose(reactions, sub)
            required.extend(subs)
        if required == required_old:
            break

    final = dict()
    for sub in required:
        if sub.name in final:
            final[sub.name] += sub.amount
        else:
            final[sub.name] = sub.amount

    ore = 0
    for k, v in final.items():
        reactions[k]


def test1(filename: str, expected: int):
    reactions = load_reactions(filename)  # reactions = dict(str,Formula)
    result = calc_ore(reactions)
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


test1('input1.txt', 31)

#print("Part 1.")
#data = util.load_int_list('input.txt')
#test1(data, 179)

#print("Part 2.")
