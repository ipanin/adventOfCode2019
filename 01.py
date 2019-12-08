import util

data = util.load_int_lines('01_input.txt')

sum = 0
for mass in data:
    sum += (mass // 3) - 2

print("Day 1. Part 1. ", sum) # expected 3282386

sum = 0
for mass in data:
    while (mass := mass // 3 - 2) > 0:
        sum += mass

print("Day 1. Part 2. ", sum) # expected 4920708
