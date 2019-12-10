
def countChildOrbits(parent, orbitsMap, depth):
    if parent not in orbitsMap:
        return 0
    childList = orbitsMap[parent]
    orbitCount = len(childList) #direct orbits
    orbitCount *= depth #indirect orbits to all parents of parents
    for child in childList:
        orbitCount += countChildOrbits(child, orbitsMap, depth + 1)
    return orbitCount

def getPathTowards(target, current, orbitsMap):
    if current not in orbitsMap:
        return None
    childList = orbitsMap[current]
    for child in childList:
        if child == target:
            return [child, current]
        else:
            childResult = getPathTowards(target, child, orbitsMap)
            if childResult != None:
                childResult.append(current)
                return childResult
    
def getPathTo(target, orbitsMap):
    path = getPathTowards(target, "COM", orbitsMap)
    path.reverse()
    return path

with open('2019/Day6_input.txt', 'r') as f:
    inputFile = f.readlines()

    #testInput A
    #inputFile = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L"]

    #testInput B
    #inputFile = ["COM)B","B)C","C)D","D)E","E)F","B)G","G)H","D)I","E)J","J)K","K)L","K)YOU","I)SAN"]

    inputFile = [x.strip().split(')') for x in inputFile]
    orbitsMap = {}

    for inputLine in inputFile:
        if inputLine[0] not in orbitsMap:
            orbitsMap[inputLine[0]] = []
        orbitsMap[inputLine[0]].append(inputLine[1])
    
    #A
    #print(countChildOrbits("COM", orbitsMap, 1))

    #B
    pathToMe = getPathTo("YOU", orbitsMap)
    pathToSanta = getPathTo("SAN", orbitsMap)
    for stepIndex in range(min(len(pathToMe), len(pathToSanta))):
        if pathToMe[stepIndex] != pathToSanta[stepIndex]:
            #paths diverge, calculate distance
            print("distance between santa and you:", len(pathToMe) + len(pathToSanta) - (2 * stepIndex) - 2)
            break