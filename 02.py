import io
import sys

def load_data():
    f = open('02_input.txt', 'rt')
    line = f.readline()
    #line = "1,9,10,3,2,3,11,0,99,30,40,50"
    data = [int(item) for item in line.split(',')]
    return data

def operation(op, arg1, arg2):
    if op == 1:
        return arg1 + arg2
    if op == 2:
        return arg1 * arg2
    return -1

def execute(program):
    pos = 0
    halt = False
    while not halt:
        op = program[pos]
        if op == 99:
            break
        addr1 = program[pos+1]
        addr2 = program[pos+2]
        addr_res = program[pos+3]
        res = operation(op, program[addr1], program[addr2])
        if res < 0:
            raise Exception(f"Error at {pos}: op={op}, addr1={addr1}, addr2={addr2}, addr_res={addr_res}")
        program[addr_res] = res
        pos += 4
    
    return program


def test(input, expected):
    #data = [int(item) for item in input_line.split(',')]
    result = execute(input)
    if result != expected:
        print("Error")
    else:
        print("OK")

test([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70,2,3,11,0,99,30,40,50])

data = load_data()
noun = 65
verb = 33
print ("part 2=", 100 * noun + verb)
data[1] = 65 #12
data[2] = 33 #2
result = execute(data)
print(result)  # 3790689
#target = 19 690 720
