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
    sum += int(mass / 3) - 2

print(sum)