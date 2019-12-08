import io
import sys

def load_data():
    f = open('07_input.txt', 'rt')
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
    input_pointer = 0
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
            inp = input[input_pointer]
            input_pointer += 1
            #print("Input: ", inp)
            program[addr1] = inp
        elif opcode == 4: # output arg1
            arg = get_value(program, program[ip+1], parameter_modes[0])
            #print("Output: ", arg)
            input[1] = arg
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


def run(program, phase_setting):
    input = [0, 0]
    for i in range(5):
        input[0] = phase_setting[i]
        execute(program, input)

    return input[1]


def test(program, phase_setting, expected):
    result = run(program, phase_setting)
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


def get_next(sett):
    # Шаг 1: найти такой наибольший j {\displaystyle j} j, для которого a j < a j + 1 {\displaystyle a_{j} < a_{j+1}} {\displaystyle a_{j} < a_{j+1}}.
    # Шаг 2: увеличить a j {\displaystyle a_{j}} a_{j}. Для этого надо найти наибольшее l > j {\displaystyle l > j} {\displaystyle l > j}, для которого a l > a j {\displaystyle a_{l} > a_{j}} {\displaystyle a_{l} > a_{j}}. Затем поменять местами a j {\displaystyle a_{j}} a_{j} и a l {\displaystyle a_{l}} {\displaystyle a_{l}}.
    # Шаг 3: записать последовательность a j + 1, . . ., a n {\displaystyle a_{j+1}, ..., a_{n}} {\displaystyle a_{j+1}, ..., a_{n}} в обратном порядке.
    pass

def next_permutation(sequence) -> bool:
    """Поиск очередной перестановки"""
    count = len(sequence)
    i = count
    # Этап № 1
    while True:
        if i < 2:
            return False  # Перебор закончен
        i -= 1
        if sequence[i - 1] < sequence[i]:
            break
    # Этап № 2
    j = count
    while j > i and not (sequence[i - 1] < sequence[j - 1]):
        j -= 1
    sequence[i - 1], sequence[j - 1] = sequence[j - 1], sequence[i - 1]
    # Этап № 3
    j = count
    while i < j - 1:
        j -= 1
        sequence[i], sequence[j] = sequence[j], sequence[i]
        i += 1
    return True

def test_max(program, expected):
    max_signal = 0
    phase_setting = [0, 1, 2, 3, 4]
    for i in range(120):
        res = run(program, phase_setting)
        if res > max_signal:
            max_signal = res
        cont = next_permutation(phase_setting)

    if max_signal != expected:
        print(f"Error, expected={expected}, actual={max_signal}")
    else:
        print("OK")


test([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],  [4, 3, 2, 1, 0], 43210)
test([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0,1,2,3,4], 54321)

test_max([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],  43210)
test_max([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], 54321)

print("Part 1.")
data = load_data()
test_max(data, 359142)
#print(f"Max signal = {max_signal}")

