# AoC 2019 Day 8: Space Image Format

import util

def draw_image(image, w, h):
    pos = 0
    for _ in range(h):
        row = ""
        for _ in range(w):
            c = image[pos]
            if c == 2:
                row += ' '
            elif c == 1:
                row += '#'
            elif c == 0:
                row += '.'
            pos += 1
        print(row)

# -----------------------------------------

w = 25
h = 6
data = util.load_int_line('08_input.txt')
layers = list(util.chunks(data, w*h))

min_zero_layer = min(layers, key = lambda layer: layer.count(0))
ones = min_zero_layer.count(1)
twos = min_zero_layer.count(2)

print("Part 1. Result = ", ones*twos) # actual 2975

print("Part 2.")

start_layer = len(layers) - 1
image = layers[start_layer]
for i in reversed(range(start_layer)):
    for j, pixel in enumerate(layers[i]):
        if pixel != 2: # transparent
            image[j] = pixel

draw_image(image, w, h) # actual EHRUE