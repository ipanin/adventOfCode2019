import sys

def has_double(digits):
    prev = digits[0]
    for d in digits[1:]:
        if d == prev:
            return True
        prev = d
    return False


def increasing(digits):
    prev = digits[0]
    for d in digits[1:]:
        if d < prev:
            return False
        prev = d
    return True

start = 109165
finish = 576723
count = 0

for current in range(start, finish+1):
    digits = [int(d) for d in str(current)]
    if has_double(digits) and increasing(digits):
        count +=1

print("Part 1. Res=", count)
