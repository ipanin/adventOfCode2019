import sys

def has_double(digits):
    prev = digits[0]
    count = 1
    for d in digits[1:]:
        if d == prev:
            count +=1
        else:
            if count == 2:
                return True
            prev = d
            count = 1

    if count == 2:
        return True

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

print("Part 2. Res=", count)
