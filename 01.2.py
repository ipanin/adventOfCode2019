import io
import sys
data = []
f = open('01_input.txt', 'rt')
for line in f.readlines():
    x = line.rstrip('\n')
    if len(x):
        data.append(int(x))

print(data[0])
sum = 0
for mass in data:
    fuel = mass
    while fuel > 0:
        fuel = int(fuel / 3) - 2
        if fuel > 0:
            sum += fuel

print(sum)
