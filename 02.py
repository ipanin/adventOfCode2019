import io
import sys

def load_data():
    f = open('02_input.txt', 'rt')
    line = f.readline()
    data = [int(item) for item in line.split(',')]
    return data

def operation(opcode, arg1, arg2):
    if opcode == 1:
        return arg1 + arg2
    if opcode == 2:
        return arg1 * arg2
    return -1 # unknown opcode

def execute(program):
    ip = 0 # instruction pointer
    prog_len = len(program)
    while ip < prog_len:
        opcode = program[ip]
        if opcode == 99:
            break

        if ip + 3 >= prog_len:
            raise Exception(f"IP={ip} out of range {prog_len}")

        addr1 = program[ip+1]
        addr2 = program[ip+2]
        addr_res = program[ip+3]
        res = operation(opcode, program[addr1], program[addr2])
        if res < 0:
            raise Exception(f"Error at {ip}: unknown opcode={opcode}. addr1={addr1}, addr2={addr2}, addr_res={addr_res}")
        program[addr_res] = res
        ip += 4
    
    return program


def test(input, expected):
    result = execute(input)
    if result != expected:
        print("Error")
    else:
        print("OK")

test([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70,2,3,11,0,99,30,40,50])

data = load_data()
noun = 65  # 12
verb = 33  # 2
data[1] = noun 
data[2] = verb 
output = execute(data)
print(output)  # 3790689
target = 19690720
if output[0] == target:
    print("Part 2. Result = ", 100 * noun + verb)

