import io
import sys

def load_data():
    f = open('05_input.txt', 'rt')
    line = f.readline()
    data = [int(item) for item in line.split(',')]
    return data

def operation(opcode, arg1, arg2):
    if opcode == 1:
        return arg1 + arg2
    if opcode == 2:
        return arg1 * arg2
    if opcode == 7:
        return int(arg1 < arg2)
    if opcode == 8:
        return int(arg1 == arg2)
    

def get_value(program, param, parameter_mode):
    if parameter_mode == 0:
        return program[param]
    elif parameter_mode == 1:
        return param
    else:
        raise Exception(f"Invalid parameter mode {parameter_mode}")


def execute(program_in, input):
    program = program_in.copy()
    ip = 0 # instruction pointer
    prog_len = len(program)
    command_len = { 1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4 }
    while ip < prog_len:
        instruction = f"{program[ip]:05}"
        opcode = int(instruction[-2:])
        parameter_modes = [int(m) for m in instruction[2::-1]]
        if parameter_modes[2] == 1:
            raise Exception(f"Error at {ip}: invalid parameter mode for target. instruction={instruction}")

        if opcode == 99:
            break
        
        cmd_len = command_len[opcode]

        if ip + cmd_len >= prog_len:
            raise Exception(f"IP={ip} out of range {prog_len}")

        if opcode==1 or opcode==2 or opcode==7 or opcode==8: # add or multiply, less than, equals
            arg1 = get_value(program, program[ip+1], parameter_modes[0])
            arg2 = get_value(program, program[ip+2], parameter_modes[1])

            addr_res = program[ip+3]

            res = operation(opcode, arg1, arg2)
            program[addr_res] = res
        elif opcode == 3: # save input int to address arg1
            if parameter_modes[0] == 1:
                raise Exception(f"Error at {ip}: invalid parameter mode for target. instruction={instruction}")
            addr1 = program[ip+1]
            print("Input: ", input)
            program[addr1] = input # TODO can be executed only once
        elif opcode == 4: # output arg1
            arg = get_value(program, program[ip+1], parameter_modes[0])
            print("Output: ", arg)
        elif opcode == 5: # jump-if-true
            arg1 = get_value(program, program[ip+1], parameter_modes[0])
            arg2 = get_value(program, program[ip+2], parameter_modes[1])
            if arg1:
                ip = arg2
                continue
        elif opcode == 6: # jump-if-false
            arg1 = get_value(program, program[ip+1], parameter_modes[0])
            arg2 = get_value(program, program[ip+2], parameter_modes[1])
            if arg1 == 0:
                ip = arg2
                continue
        else:
            raise Exception(f"Error at {ip}: unknown opcode={opcode}. instruction={instruction}")

        ip += cmd_len

    if ip >= prog_len:
        raise Exception(f"No HALT at the end of program")

    return program


def test(program, expected, input):
    result = execute(program, input)
    if result != expected:
        print("Error")
    else:
        print("OK")

test([1,9,10,3,2,3,11,0,99,30,40,50], [3500,9,10,70,2,3,11,0,99,30,40,50], 0)

data = load_data()

print("Part 1.")
execute(data, 1) # expected 13787043

print("Part 2.")
execute(data, 5) # expected 3892695

