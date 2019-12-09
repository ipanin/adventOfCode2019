# AoC 2019. Day 9. Sensor Boost
import util
import intcode

def run(program, input):
    comp = intcode.IntcodeComputer(program, input)
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
data = util.load_int_list('input.txt')
test(data, [1], [3013554615])

print("Part 2.")
test(data, [2], [50158])


