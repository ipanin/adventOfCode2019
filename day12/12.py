# AoC 2019. Day 12. The N-Body Problem
import util

class Moon():
    def __init__(self, pos):
        self.pos = pos.copy()
        self.vel = [0,0,0]
    
    def apply_velocity(self):
        for dim in range(3):
            self.pos[dim] += self.vel[dim]

    def potential(self):
        return sum([abs(x) for x in self.pos])
    
    def kinetic(self):
        return sum([abs(x) for x in self.vel])

    def energy(self):
        return self.potential() * self.kinetic()
    
    def __str__(self):
        return f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>"

def apply_gravity(A, B):
    for dimention in range(3):
        if A.pos[dimention] < B.pos[dimention]:
            A.vel[dimention] += 1
            B.vel[dimention] -= 1
        elif A.pos[dimention] > B.pos[dimention]:
            A.vel[dimention] -= 1
            B.vel[dimention] += 1

def test1(positions, steps: int, expected_energy: int):
    moons = list()
    for p in positions:
        moons.append(Moon(p))

    for step in range(steps):
        for i in range(len(moons)):
            for j in range(0,i):
                apply_gravity(moons[i], moons[j])

        #print(f"\nAfter {step+1} steps:")
        for m in moons:
            m.apply_velocity()
            #print(m)
        

    result = sum([m.energy() for m in moons])
    if result != expected_energy:
        print(f"Error, expected={expected_energy}, actual={result}")
    else:
        print("OK")

def test2(positions, expected_steps: int):
    moons = list()
    for p in positions:
        moons.append(Moon(p))

    step = 0
    while (1==1):
        for i in range(len(moons)):
            for j in range(0,i):
                apply_gravity(moons[i], moons[j])

        #print(f"\nAfter {step+1} steps:")
        for m in moons:
            m.apply_velocity()
        #    print(m)

        step += 1
        if positions == [m.pos for m in moons]:
            break
        if step % 1000000 == 0:
            print(f'step = {step/1000000}M', )

    result = step + 1 # why?

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

# too long 
# test2([[-8,-10,0], [5,5,10], [2,-7,3], [9,-8,-3]], 4686774924)



