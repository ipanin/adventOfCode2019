# Intcode computer ver 1.9
import util
from queue import Queue
import time

class IntcodeComputer:
    def __init__(self, program, name="Main"):
        self.name = name
        self.program = util.GrowingList(program)  # .copy()
        self.ip = 0  # instruction pointer
        self.relative_base = 0
        self.command_len = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
        self.input_fun = lambda: 0
        self.output_fun = lambda x: print("OUTPUT: " + str(x))

    def set_input_fun(self, f): 
        self.input_fun = f
    def set_output_fun(self, f): 
        self.output_fun = f
    def read_input(self) -> int:
        return self.input_fun()
    def write_output(self, value: int):
        self.output_fun(value)
    
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
            #time.sleep(1)

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
            inp = self.read_input()
            # print(f"[{self.name}] Input: {inp}")
            self.program[addr] = inp
        elif opcode == 4:  # output arg1
            arg = self.get_value(self.program, self.program[ip+1], parameter_modes[0])
            # print(f"[{self.name}] Output: {arg}")
            self.write_output(arg)
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
