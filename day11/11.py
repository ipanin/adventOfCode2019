# AoC 2019. Day 11. Painting robot.
import util
import intcode

# This implementation doesn't execute program to calculate output, it has predefined output values
class FakeComp:
    def __init__(self, output_data):
        self.output_data = output_data
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
        for item in self.output_data:
            self.output_fun(item)

VECTOR = [(0,-1), (1,0), (0,1), (-1,0)] # up, right, buttom, left

class RobotOnField:
    def __init__(self, comp):
        self.comp = comp
        self.comp.set_input_fun(self.get_field_color)
        self.comp.set_output_fun(self.output_handler)
        self.field = dict() # painted panels (x,y)/color; color 0=black, 1=white
        self.robo_pos = (0, 0) # position x,y
        self.robo_dir = 0 # robot direction. 0=up, 1=right, 2=buttom, 3=left
        self.paint_state = True
    
    def get_field_color(self):
        # get field color
        return self.field.get(self.robo_pos, 0) # 0=black by default

    def output_handler(self, value : int):
        # paint or move
        if self.paint_state:
            self.paint(value)
        else:
            self.move(value)
        
        self.paint_state = not self.paint_state

    def paint(self, value: int):
        self.field[self.robo_pos] = value

    def move(self, value: int):
        if value == 0: # turn left
            self.robo_dir = (self.robo_dir - 1) % 4 # correctly works for negative values
        elif value == 1: # turn right
            self.robo_dir = (self.robo_dir + 1) % 4
        else:
            raise Exception("Invalid turn command: " + str(value))
        
        # move forward
        dx, dy = VECTOR[self.robo_dir]
        self.robo_pos = (self.robo_pos[0] + dx, self.robo_pos[1] + dy)


    def run(self):
        self.comp.execute()


def test0(fake_output, expected_painted_panel_count: int):
    comp = FakeComp(fake_output)
    robo = RobotOnField(comp)
    robo.run()

    result = len(robo.field.keys())
    if result != expected_painted_panel_count:
        print(f"Error, expected painted panel count={expected_painted_panel_count}, actual={result}")
    else:
        print("OK")


def test1(program, expected_painted_panel_count: int):
    comp = intcode.IntcodeComputer(program)
    robo = RobotOnField(comp)
    robo.run()

    result = len(robo.field.keys())
    if result != expected_painted_panel_count:
        print(f"Error, expected painted panel count={expected_painted_panel_count}, actual={result}")
    else:
        print("OK")

def test2(program):
    comp = intcode.IntcodeComputer(program)
    robo = RobotOnField(comp)
    robo.field[(0,0)] = 1 # start from white panel
    robo.run()

    # print(robo.field.keys()) 
    # all keys >= 0
    w = max(p[0] for p in robo.field.keys()) + 1
    h = max(p[1] for p in robo.field.keys()) + 1
    util.draw_image(robo.field, w, h) # BCKFPCRA

test0([1,0, 0,0, 1,0, 1,0, 0,1, 1,0, 1,0], 6)

print("Part 1.")
data = util.load_int_list('input.txt')
test1(data, 2255)

print("Part 2.")
test2(data)
