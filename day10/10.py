import util

def my_range(start, stop):
    if start < stop:
        return range(start+1, stop)
    else:
        return range(start-1, stop, -1)

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

    def calc(self, i0: int, j0 : int) -> int:
        res = 0
        for j in range(self.heigth):
            line = self.lines[j]
            for i in range(self.width):
                if line[i] != '#':
                    continue
                if i == i0 and j == j0:
                    continue
                if self.visible(i0, j0, i, j):
                    res += 1
        return res

    def findbest(self) -> dict:
        maxi = 0
        maxj = 0
        maxa = 0  # asteroids

        for j in range(self.heigth):
            line = self.lines[j]
            for i in range(self.width):
                if line[i] == '#':
                    res = self.calc(i, j)
                    if res > maxa:
                        maxi = i
                        maxj = j
                        maxa = res

        print(f'Best pos ({maxi}, {maxj}), Asteroids = {maxa}')
        return {'x':maxi, 'y': maxj, 'asteroids': maxa}

def test(input_file : str, expected:dict):
    m = matrix(input_file)
    result = m.findbest()
    if result != expected:
        print(f"Error, expected={expected}, actual={result}")
    else:
        print("OK")


test('input_test2.txt', {'x': 11, 'y': 13, 'asteroids': 210})

print("Part 1.")
test('input.txt', {'x': 29, 'y': 28, 'asteroids': 256})


