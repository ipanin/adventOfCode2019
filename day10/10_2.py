import util
import math

def my_range(start, stop):
    if start < stop:
        return range(start+1, stop)
    else:
        return range(start-1, stop, -1)

def angle(x0: int, y0: int, x1: int, y1: int) -> float:
    dx = x1 - x0
    dy = - (y1-y0) # Decart
    normal_angle = math.atan2(dy, dx)
    angle = math.pi/2 - normal_angle
    if angle < 0:
        angle += math.pi*2
    return angle

class matrix():
    def __init__(self, filename : str):
        self.lines = util.load_str_lines_list(filename)
        self.heigth = len(self.lines)
        self.width = len(self.lines[0])

    def visible(self, x0 : int, y0 : int, x1 : int, y1 : int) -> bool:
        if x1 == x0:
            for y in my_range (y0, y1):
                if self.lines[y][x0] == '#':
                    return False
            return True

        k = (y1-y0) / (x1-x0)
        for x in my_range(x0, x1):
            y = y0 + (x - x0) * k
            if y < 0 or y >= self.heigth:
                return False
            inty = int(round(y, 4))
            if inty == round(y, 4):
                if self.lines[inty][x] == '#':
                    return False
        return True

    def allvisible(self, i0: int, j0 : int) -> dict:
        res = dict()
        for j in range(self.heigth):
            line = self.lines[j]
            for i in range(self.width):
                if line[i] != '#':
                    continue
                if i == i0 and j == j0:
                    continue
                if self.visible(i0, j0, i, j):
                    a = angle(i0, j0, i, j)
                    res[a] = (i, j)
        return res

    def find200th(self, x:int, y:int) -> (int, int):
        visible = self.allvisible(x, y)
        s = sorted(visible.items())
        n=1
        for item in s:
            print(f'The {n} asteroid to be vaporized is at {item[1]} ({item[0]}).')
            n+=1
        key = s[200-1]
        return key[1]


def test2(input_file : str, x, y, expected):
    m = matrix(input_file)
    i, j = m.find200th(x,y)
    result = i*100 + j
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


test2('input_test2.txt', 11, 13, 802)

print("Part 2.")
test2('input.txt', 29, 28, 1707)


