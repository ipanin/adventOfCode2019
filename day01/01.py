# AoC 2019 Day 1: The Tyranny of the Rocket Equation
import util

data = util.load_int_lines('01_input.txt')

sum = 0
for mass in data:
    sum += (mass // 3) - 2

# What is the sum of the fuel requirements for all of the modules on your spacecraft?
print("Day 1. Part 1. ", sum) # expected 3282386

sum = 0
for mass in data:
    while (mass := mass // 3 - 2) > 0:
        sum += mass

# What is the sum of the fuel requirements for all of the modules on your spacecraft 
# when also taking into account the mass of the added fuel?
print("Day 1. Part 2. ", sum) # expected 4920708
