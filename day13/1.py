# AoC 2019. Day 13. Care Package (Arcade Cabinet)
import util
import intcode

class ArcadeCabinet:
    def __init__(self, comp):
        self.comp = comp
        self.comp.set_input_fun(lambda: 0)
        self.comp.set_output_fun(self.output_handler)
        self.screen = dict()
        self.output_index = 0
        self.output_buffer = [0, 0, 0]

    def output_handler(self, value: int):
        self.output_buffer[self.output_index] = value
        self.output_index += 1

        if self.output_index == 3:
            self.output_index = 0
            self.draw_tile(*self.output_buffer)

    def draw_tile(self, x, y, tile):
        self.screen[(x,y)] = tile

    def run(self):
        self.comp.execute()


def test1(program, expected):
    comp = intcode.IntcodeComputer(program)
    game = ArcadeCabinet(comp)
    game.run()

    result = sum([1 for x in game.screen.values() if x == 2])
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")

print("Part 1.")
data = util.load_int_list('input.txt')
test1(data, 173)





