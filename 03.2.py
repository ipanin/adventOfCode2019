import sys
import os
from collections import defaultdict



def load_data():
    f = open('03_input.txt', 'rt')
    line1 = f.readline()
    line2 = f.readline()
    #line1 = "R8,U5,L5,D3" 
    #line2 = "U7,R6,D4,L4"
    #line1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    #line2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

    #line1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    #line2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    data1 = [item for item in line1.split(',')]
    data2 = [item for item in line2.split(',')]
    
    return (data1,data2)

def draw(matrix, data):
    x = 0
    y = 0
    wire_len = 0
    for d in data:
        x, y, wire_len = draw_line(matrix, x, y, wire_len, d)

def draw_line(matrix, x, y, wire_len, d):
    direction = d[0]
    length = int(d[1:])
    if direction == 'R':
        for i in range(length):
            x += 1
            wire_len += 1
            if matrix.get((x,y), 0) == 0:
                matrix[(x,y)] = wire_len
    if direction == 'L':
        for i in range(length):
            x -= 1
            wire_len += 1
            if matrix.get((x, y), 0) == 0:
                matrix[(x, y)] = wire_len
    if direction == 'U':
        for i in range(length):
            y += 1
            wire_len += 1
            if matrix.get((x, y), 0) == 0:
                matrix[(x, y)] = wire_len
    if direction == 'D':
        for i in range(length):
            y -= 1
            wire_len += 1
            if matrix.get((x, y), 0) == 0:
                matrix[(x, y)] = wire_len

    return (x,y, wire_len)

def find_closest(matrix):
    intersections = list(filter(lambda elem: elem[1] > 1, matrix.items()))
    #distances = list(filter(lambda elem: sum([abs(e) for e in elem[0]]), intersections))
    print(intersections)
    distances = [i[1] for i in intersections]
    return min(distances)

def intersect(matrix1, matrix2):
    res = defaultdict(int)
    for i in matrix1.items():
        m2 = matrix2[i[0]]
        if m2 != 0:
            res[i[0]] = i[1] + m2 
    return res

# ----------------------------------------
matrix1 = defaultdict(int)
matrix2 = defaultdict(int)
data1, data2 = load_data()
draw(matrix1, data1)
draw(matrix2, data2)
matrix = intersect(matrix1, matrix2)
res = find_closest(matrix)
print("part 2. Res=", res)
