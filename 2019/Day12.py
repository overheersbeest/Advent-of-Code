import time
import math

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x  + other.x, self.y + other.y, self.z + other.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))
        
    def __str__(self):
        return "<x= %d, y= %d, z=%d>" % (self.x, self.y, self.z)


class Moon:
    def __init__(self):
        self.pos = Vector()
        self.v = Vector()

    def __hash__(self):
        return hash((self.pos, self.v))
    
    def __str__(self):
        return "pos=" + str(self.pos) + ", vel=" + str(self.v)

    def getPotentialEnergy(self):
        return abs(self.pos.x) + abs(self.pos.y) + abs(self.pos.z)

    def getKineticEnergy(self):
        return abs(self.v.x) + abs(self.v.y) + abs(self.v.z)

with open('2019/Day12_input.txt', 'r') as f:
    inputFile = f.readlines()

    #test input
    #inputFile = ["<x=-1, y=0, z=2>","<x=2, y=-10, z=-7>","<x=4, y=-8, z=8>","<x=3, y=5, z=-1>"]
    #inputFile = ["<x=-8, y=-10, z=0>","<x=5, y=5, z=10>","<x=2, y=-7, z=3>","<x=9, y=-8, z=-3>"]

    moons = []
    for line in inputFile:
        line = line[line.index("<") + 1 : line.index(">")]
        segments = line.split(",")
        moon = Moon()
        for segment in segments:
            tokens = segment.split("=")
            component = tokens[0].strip()
            value = int(tokens[1])
            if component == "x":
                moon.pos.x = value
            elif component == "y":
                moon.pos.y = value
            elif component == "z":
                moon.pos.z = value
            else:
                print("ERROR: unknown component \"" + component + "\"")

        moons += [moon]
    
    #A
    if False:
        for timestep in range(1000):
            #update velocities
            for moon1Index in range(len(moons)):
                moon1 = moons[moon1Index]
                for moon2Index in range(moon1Index + 1, len(moons)):
                    moon2 = moons[moon2Index]
                    #x
                    if moon1.pos.x < moon2.pos.x:
                        moon1.v.x += 1
                        moon2.v.x -= 1
                    elif moon1.pos.x > moon2.pos.x:
                        moon1.v.x -= 1
                        moon2.v.x += 1
                    #y
                    if moon1.pos.y < moon2.pos.y:
                        moon1.v.y += 1
                        moon2.v.y -= 1
                    elif moon1.pos.y > moon2.pos.y:
                        moon1.v.y -= 1
                        moon2.v.y += 1
                    #z
                    if moon1.pos.z < moon2.pos.z:
                        moon1.v.z += 1
                        moon2.v.z -= 1
                    elif moon1.pos.z > moon2.pos.z:
                        moon1.v.z -= 1
                        moon2.v.z += 1
            #update positions
            for moon in moons:
                moon.pos += moon.v

        totalEnergy = 0
        for moon in moons:
            potential = moon.getPotentialEnergy()
            kinetic = moon.getKineticEnergy()
            totalEnergy += potential * kinetic
        print(totalEnergy)
    
    #B
    if True:
        startTime = time.time()

        xStates = set()
        yStates = set()
        zStates = set()
        stepsSimulated = 0
        numMoons = len(moons)
        xMultiple = -1#167624#
        yMultiple = -1#231614#
        zMultiple = -1#96236#

        while xMultiple == -1 or yMultiple == -1 or zMultiple == -1:
            #update velocities
            for moon1Index in range(numMoons):
                moon1 = moons[moon1Index]
                otherMoons = moons[moon1Index + 1:]
                #moon1.v.x += sum([1 for moon2 in otherMoons])
                for moon2 in otherMoons:
                    #x
                    deltaX = sorted((-1, moon2.pos.x - moon1.pos.x, 1))[1]
                    moon1.v.x += deltaX
                    moon2.v.x -= deltaX
                    #y
                    deltaY = sorted((-1, moon2.pos.y - moon1.pos.y, 1))[1]
                    moon1.v.y += deltaY
                    moon2.v.y -= deltaY
                    #z
                    deltaZ = sorted((-1, moon2.pos.z - moon1.pos.z, 1))[1]
                    moon1.v.z += deltaZ
                    moon2.v.z -= deltaZ
            #update positions
            for moon in moons:
                moon.pos += moon.v
  
            #x
            if xMultiple == -1:
                xHash = tuple([(moon.pos.x, moon.v.x) for moon in moons])
                if xHash in xStates:
                    print("found x multiple:", stepsSimulated)
                    xMultiple = stepsSimulated
                else:
                    xStates.add(xHash)  
            #y
            if yMultiple == -1:
                yHash = tuple([(moon.pos.y, moon.v.y) for moon in moons])
                if yHash in yStates:
                    print("found y multiple:", stepsSimulated)
                    yMultiple = stepsSimulated
                else:
                    yStates.add(yHash)
            #z
            if zMultiple == -1:
                zHash = tuple([(moon.pos.z, moon.v.z) for moon in moons])
                if zHash in zStates:
                    print("found z multiple:", stepsSimulated)
                    zMultiple = stepsSimulated
                else:
                    zStates.add(zHash)

            stepsSimulated += 1
        
        multiples = [xMultiple, yMultiple, zMultiple]

        def primeFactors(n):
            factors = {}
            while n % 2 == 0:
                if 2 not in factors:
                    factors[2] = 1
                else:
                    factors[2] += 1
                n = n // 2
            for i in range(3,int(math.sqrt(n)) + 1,2):
                while n % i== 0:
                    if i not in factors:
                        factors[i] = 1
                    else:
                        factors[i] += 1
                    n = n // i
            if n > 2:
                factors[n] = 1
            return factors

        factorMaps = [primeFactors(n) for n in multiples]
        mergedFactorMap = {}
        for factorMap in factorMaps:
            for factor in factorMap:
                if factor not in mergedFactorMap:
                    mergedFactorMap[factor] = factorMap[factor]
                elif factorMap[factor] > mergedFactorMap[factor]:
                    mergedFactorMap[factor] = factorMap[factor]

        current = 1
        for factor in mergedFactorMap:
            current *= factor ** mergedFactorMap[factor]

        print(current)

        endTime = time.time()
        print(endTime - startTime, "seconds to run")