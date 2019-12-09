# AoC 2019. Day 9. Sensor Boost
import util
from queue import Queue
#import threading

class IntcodeComputer:
    def __init__(self, program, input_values, name="Main"):
        self.program = util.GrowingList(program) #.copy()
        self.ip = 0  # instruction pointer
        self.relative_base = 0
        self.input = Queue(1024)
        self.output = self.input

        for i in input_values:
            self.input.put(i)

        self.name = name

        self.command_len = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
        
    
    def connect_output(self, output):
        self.output = output

    def get_input(self):
        return self.input

    def execute(self):
        while self.ip < len(self.program): # TODO extend
            inst = self.program[self.ip]
            instruction = f"{inst:05}"
            opcode = int(instruction[-2:])
            parameter_modes = [int(m) for m in instruction[2::-1]]
            if parameter_modes[2] == 1: # TODO
                raise Exception(
                    f"[{self.name}] Error at {self.ip}: invalid parameter mode for target. instruction={instruction}")

            if opcode == 99:
                break

            cmd_len = self.command_len[opcode]

            self.ip = self.step(self.ip, opcode, parameter_modes, cmd_len)

        if self.ip >= len(self.program):
            raise Exception(f"[{self.name}] No HALT at the end of self.program")

        #print(f"[{self.name}] Exit")

    def step(self, ip, opcode, parameter_modes, cmd_len):
        if opcode == 1 or opcode == 2 or opcode == 7 or opcode == 8:  # add or multiply, less than, equals
            arg1 = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = self.get_value(self.program, self.program[ip+2], parameter_modes[1])
            addr = self.get_addr (self.program, self.program[ip+3], parameter_modes[2])

            res = IntcodeComputer.operation(opcode, arg1, arg2)
            self.program[addr] = res
        elif opcode == 3:  # save input int to address arg1
            if parameter_modes[0] == 1:
                raise Exception(f"[{self.name}] Error at {ip}: invalid parameter mode 1 for target. opcode={opcode}")
            
            addr = self.get_addr(self.program, self.program[ip+1], parameter_modes[0])
            #if self.input.qsize() == 0:
            #    print(f"[{self.name}] Wait input")
            inp = self.input.get()
            # print(f"[{self.name}] Input: {inp}")
            self.program[addr] = inp
        elif opcode == 4:  # output arg1
            arg = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            # print(f"[{self.name}] Output: {arg}")
            self.output.put_nowait(arg)
        elif opcode == 5:  # jump-if-true
            arg1 = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = self.get_value(self.program, self.program[ip+2], parameter_modes[1])
            if arg1:
                return arg2
        elif opcode == 6:  # jump-if-false
            arg1 = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            arg2 = self.get_value(self.program, self.program[ip+2], parameter_modes[1])
            if arg1 == 0:
                return arg2
        elif opcode == 9: # adjusts the relative base
            arg = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            self.relative_base += arg
        else:
            raise Exception(f"[{self.name}] Error at {ip}: unknown opcode={opcode}.")

        return ip + cmd_len

    def get_value(self, program, param, parameter_mode):
        if parameter_mode == 1: # immediate
            return param
        else:
            addr = self.get_addr(program, param, parameter_mode)
            return program[addr]

    def get_addr(self, program, param, parameter_mode):
        if parameter_mode == 0: # address
            return param
        elif parameter_mode == 1: # immediate
            raise Exception(f"[{self.name}] Error at {self.ip}: invalid parameter mode 1 for target.")
        elif parameter_mode == 2: # relative address
            address = self.relative_base + param
            if address <  0:
                raise Exception(f"[{self.name}] Error: negative address. relative_base={self.relative_base}, param={param}")
            return address
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

    def get_output_values(self):
        result = []
        while not self.output.empty():
            result.append(self.output.get_nowait())
        return result

# ----------------------------------------------------------------------------

def load_data():
    f = open('day09\\input.txt', 'rt')
    line = f.readline()
    data = [int(item) for item in line.split(',')]
    return data

def run(program, input):
    comp = IntcodeComputer(program, input)
    comp.execute()
    return comp.get_output_values()


def test(program, input, expected):
    result = run(program, input)
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


test([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], [], [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
test([1102,34915192,34915192,7,4,7,99,0], [], [1219070632396864])
test([104,1125899906842624,99], [], [1125899906842624])

print("Part 1.")
data = load_data()
test(data, [1], [3013554615])

print("Part 2.")
test(data, [2], [50158])


