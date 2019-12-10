# AoC 2019 Day 8: Space Image Format
import util
from PIL import Image

def draw_text_image(image, w, h):
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
                row += '-'
            pos += 1
        print(row)

def draw_image(image, w, h):
    img = Image.new('RGB', (w, h), "blue") # Create a new black image
    pixels = img.load() # Create the pixel map
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            c = image[y*w + x]
            if c == 0: # black
                pixels[x, y] = (0, 0, 0)
            if c == 1: # white

                pixels[x, y] = (255,255,255)

    img.resize((w*50, h*50)).show()
# -----------------------------------------

w, h = 25, 6
input = util.load_number_string_list('08_input.txt')
layers = list(util.chunks(input, w*h))

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

# What message is produced after decoding your image?
draw_text_image(image, w, h) # actual EHRUE
draw_image(image, w, h) # actual EHRUE
