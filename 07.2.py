import io
import sys
from queue import Queue
import threading

class IntcodeComputer:
    def __init__(self, program, input):
        self.program = program.copy()
        self.prog_len = len(self.program)
        self.ip = 0  # instruction pointer
        self.input = Queue(1024)
        self.input.put(input) # more than 1?
        self.name = input
        self.command_len = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
    
    def connect_output(self, output):
        self.output = output

    def get_input(self):
        return self.input

    def execute(self):
        while self.ip < self.prog_len:
            instruction = f"{self.program[self.ip]:05}"
            opcode = int(instruction[-2:])
            parameter_modes = [int(m) for m in instruction[2::-1]]
            if parameter_modes[2] == 1:
                raise Exception(
                    f"[{self.name}] Error at {self.ip}: invalid parameter mode for target. instruction={instruction}")

            if opcode == 99:
                break

            cmd_len = self.command_len[opcode]

            if self.ip + cmd_len >= self.prog_len:
                raise Exception(f"[{self.name}] IP={self.ip} out of range {self.prog_len}")

            self.ip = self.step(self.ip, opcode, parameter_modes, cmd_len)

        if self.ip >= self.prog_len:
            raise Exception(f"[{self.name}] No HALT at the end of self.program")

        #print(f"[{self.name}] Exit")

    def step(self, ip, opcode, parameter_modes, cmd_len):
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:  # add or multiply, less than, equals
            arg1 = IntcodeComputer.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = IntcodeComputer.get_value(self.program, self.program[ip+2], parameter_modes[1])

            addr_res = self.program[ip+3]

            res = IntcodeComputer.operation(opcode, arg1, arg2)
            self.program[addr_res] = res
        elif opcode == 3:  # save input int to address arg1
            if parameter_modes[0] == 1:
                raise Exception(f"[{self.name}] Error at {ip}: invalid parameter mode 1 for target. opcode={opcode}")
            addr1 = self.program[ip+1]
            #if self.input.qsize() == 0:
            #    print(f"[{self.name}] Wait input")
            inp = self.input.get()
            #print(f"[{self.name}] Input: {inp}")
            self.program[addr1] = inp
        elif opcode == 4:  # output arg1
            arg = IntcodeComputer.get_value(self.program, self.program[ip+1], parameter_modes[0])
            #print(f"[{self.name}] Output: {arg}")
            self.output.put_nowait(arg)
        elif opcode == 5:  # jump-if-true
            arg1 = IntcodeComputer.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = IntcodeComputer.get_value(self.program, self.program[ip+2], parameter_modes[1])
            if arg1:
                return arg2
        elif opcode == 6:  # jump-if-false
            arg1 = IntcodeComputer.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = IntcodeComputer.get_value(self.program, self.program[ip+2], parameter_modes[1])
            if arg1 == 0:
                return arg2
        else:
            raise Exception(f"[{self.name}] Error at {ip}: unknown opcode={opcode}.")

        return ip + cmd_len

    @staticmethod
    def get_value(program, param, parameter_mode):
        if parameter_mode == 0:
            return program[param]
        elif parameter_mode == 1:
            return param
        else:
            raise Exception(f"Invalid parameter mode {parameter_mode}")

    @staticmethod
    def operation(opcode, arg1, arg2):
        if opcode == 1:
            return arg1 + arg2
        if opcode == 2:
            return arg1 * arg2
        if opcode == 7:
            return int(arg1 < arg2)
        if opcode == 8:
            return int(arg1 == arg2)

# ----------------------------------------------------------------------------

def load_data():
    f = open('07_input.txt', 'rt')
    line = f.readline()
    data = [int(item) for item in line.split(',')]
    return data

def run(program, phase_setting):
    amplifiers = []
    for i in range(5):
        amplifiers.append(IntcodeComputer(program, phase_setting[i]))

    for i in range(5):
        amplifiers[i].connect_output(amplifiers[(i+1) % 5].get_input())

    amplifiers[0].get_input().put(0)

    threads = []
    for a in amplifiers:
        thread1 = threading.Thread(target=a.execute)
        thread1.start()
        threads.append(thread1)

    for t in threads:
        t.join()

    return amplifiers[4].output.get()


def test(program, phase_setting, expected):
    result = run(program, phase_setting)
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


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


def test_max(program, phase_setting_in, expected):
    max_signal = 0
    phase_setting = phase_setting_in.copy()
    for i in range(120):
        res = run(program, phase_setting)
        if res > max_signal:
            max_signal = res
        cont = next_permutation(phase_setting)

    if max_signal != expected:
        print(f"Error, expected={expected}, actual={max_signal}")
    else:
        print("OK")


#test([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],  [4, 3, 2, 1, 0], 43210)
#test([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0,1,2,3,4], 54321)
test([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], [9,8,7,6,5], 139629729)

#test_max([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [0,1,2,3,4], 43210)
#test_max([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0,1,2,3,4], 54321)
test_max([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], [5, 6, 7, 8, 9], 139629729)

print("Part 2.")
data = load_data()
test_max(data, [5, 6, 7, 8, 9], 4374895)
#print(f"Max signal = {max_signal}")

