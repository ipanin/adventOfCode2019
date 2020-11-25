# AoC 2019. Day 12. The N-Body Problem
import util
from math import gcd
from functools import reduce

def move(initial_pos, steps:int):
    pos = initial_pos.copy()
    vel = [0,0,0,0]

    for step in range(steps):
        for i in range(4):
            for j in range(0,i):
                #apply_gravity(moons[i], moons[j])
                if pos[i] < pos[j]:
                    vel[i] += 1; vel[j] -= 1
                elif pos[i] > pos[j]:
                    vel[i] -= 1; vel[j] += 1

        # apply velocity
        for i in range(4):
            pos[i] += vel[i] 

    return (pos, vel)

def test1(positions, steps: int, expected_energy: int):
    pp = []
    vv = []
    for dimention in range(3):
        start_pos = [p[dimention] for p in positions]
        pos_after, vel_after = move(start_pos, steps)
        pp.append(pos_after)
        vv.append(vel_after)

    energy = 0
    for m in range(4):
        kin = pot = 0
        for dimention in range(3):
            pot += abs(pp[dimention][m])
            kin += abs(vv[dimention][m])
        energy += kin*pot

    result = energy
    if result != expected_energy:
        print(f"Error, expected={expected_energy}, actual={result}")
    else:
        print("OK")

   
def find_period(initial_pos):
    pos = initial_pos.copy()
    vel = [0,0,0,0]
    step = 0
    while (1==1):
        for i in range(4):
            for j in range(0,i):
                #apply_gravity(moons[i], moons[j])
                if pos[i] < pos[j]:
                    vel[i] += 1; vel[j] -= 1
                elif pos[i] > pos[j]:
                    vel[i] -= 1; vel[j] += 1

        for i in range(4):
            pos[i] += vel[i] # apply velocity

        step += 1
        if pos == initial_pos:
            break
        if step % 1000000 == 0:
            print(f'step = {step/1000000}M')
    
    return step + 1 # why +1?

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_n(args):
    return reduce(lcm, args)

def test2(positions, expected_steps: int):
    periods = []
    for dim in range(3):
        pos = [p[dim] for p in positions]
        periods.append(find_period(pos))

    #print(periods)
    result = lcm_n(periods)
    if result != expected_steps:
        print(f"Error, expected={expected_steps}, actual={result}")
    else:
        print("OK")


print("Part 1.")
test1([[-1,0,2], [2,-10,-7], [4,-8,8], [3,5,-1]], 10, 179)
test1([[-8,-10,0], [5,5,10], [2,-7,3], [9,-8,-3]], 100, 1940)
test1([[-19,-4,2], [-9,8,-16], [-4,5,-11], [1,9,-13]], 1000, 8287) # my task

print("Part 2.")
test2([[-1,0,2], [2,-10,-7], [4,-8,8], [3,5,-1]], 2772)
test2([[-8,-10,0], [5,5,10], [2,-7,3], [9,-8,-3]], 4686774924)
test2([[-19,-4,2], [-9,8,-16], [-4,5,-11], [1,9,-13]], 528250271633772) # my task



