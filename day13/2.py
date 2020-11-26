# AoC 2019. Day 13. Care Package
import util
import intcode
import pygame as pg
import keyboard
import collections

kb_buf = collections.deque()

def on_key_left_press(e):
    kb_buf.append(-1)

def on_key_right_press(e):
    kb_buf.append(1)

class ArcadeCabinet:
    def __init__(self, comp):
        self.comp = comp
        self.comp.set_input_fun(self.input_handler)
        self.comp.set_output_fun(self.output_handler)
        self.output_index = 0
        self.output_buffer = [0, 0, 0]
        self.screen = pg.display.set_mode((1200, 800))
        
        keyboard.on_press_key("a", on_key_left_press)
        keyboard.on_press_key("d", on_key_right_press)

    def input_handler(self):
        #time.sleep(1)
        if len(kb_buf) == 0:
            return 0

        return kb_buf.popleft()

    def output_handler(self, value: int):
        self.output_buffer[self.output_index] = value
        self.output_index += 1

        if self.output_index == 3:
            self.output_index = 0
            if self.output_buffer[0] == -1 and self.output_buffer[1] == 0:
                print('Score=', self.output_buffer[2])
            else:
                self.paint(*self.output_buffer)

    def paint(self, x, y, v):
        if v == 0: # empty
            color = (0,0,0)
        elif v == 1: # wall
            color = (255, 255, 255)  # white
        elif v == 2: # block
            color = (255, 0, 0)  # red
        elif v == 3: # paddle
            color = (0, 255, 0)  # green
        elif v == 4: # ball
            color = (255, 255, 0)  # yellow
        else:
            color = (128, 128, 128)  # gray

        re = pg.Rect(x*20, y*20, 20, 20)
        pg.draw.rect(self.screen, color, re)
        pg.display.update()

    def run(self):
        self.comp.execute()

def test2(program):
    program[0] = 2 # 2 coins
    comp = intcode.IntcodeComputer(program)
    game = ArcadeCabinet(comp)
    while True:
        game.run()
        comp.ip = 0  # restart game from same state and score 
        # other solution is to modify game field adding buttom wall

print("Part 2.")
data = util.load_int_list('input.txt')
test2(data) # max score == 8942






