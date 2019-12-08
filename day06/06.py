import sys
import os

def load_data():
    f = open("06_input.txt", "rt")
    data = [line.rstrip().split(")") for line in f.readlines()]

    sample = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L"]
    sample.extend(["K)YOU", "I)SAN"]) # for part 2
    #data = [line.rstrip().split(")") for line in sample]
    return data

def build_tree(data):
    tree = dict()

    for record in data:
        parent_name = record[0]
        child_name = record[1]
        tree[child_name] = parent_name

    return tree

def calc_ancestors(node_name, tree):
    ancestors = 0

    while node_name != "COM":
        ancestors += 1
        node_name = tree[node_name]

    return ancestors

def get_ancestors(node_name, tree):
    ancestors = []

    while node_name != "COM":
        node_name = tree[node_name]
        ancestors.append(node_name)

    return ancestors

########################################################
data = load_data()
tree = build_tree(data)
#print(tree)

orbits = 0
for node in tree.items():
    node_name = node[0]
    orbits += calc_ancestors(node_name, tree)

print("Part 1. Orbits = ", orbits)  # 142497

########################################################

a1 = get_ancestors("YOU", tree)
a2 = get_ancestors("SAN", tree)
s1 = set(a1)
s2 = set(a2)

transfers = len(s1-s2) + len(s2-s1)

print("Part 2. Transfers = ", transfers)  # 301
