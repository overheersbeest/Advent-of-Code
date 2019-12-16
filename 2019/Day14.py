import math

class Reaction:
    def __init__(self, output, outputQuantity = 1):
        self.output = output
        self.outputQuantity = outputQuantity
        self.inputQuatities = {}
    
    def getInputsForOutputQuantity(self, targetOutputQuantity):
        reactionsRequired = math.ceil(targetOutputQuantity / self.outputQuantity)
        retVal = {}
        for inputResource in self.inputQuatities:
            retVal[inputResource] = self.inputQuatities[inputResource] * reactionsRequired
        return retVal

def getOreCost(resource, requiredQuantity, allReactions, leftOvers):
    if resource == "ORE":
        return requiredQuantity
    if resource in leftOvers:
        if leftOvers[resource] > requiredQuantity:
            leftOvers[resource] -= requiredQuantity
            return 0
        else:
            requiredQuantity -= leftOvers[resource]
            del leftOvers[resource]
            if requiredQuantity == 0:
                return 0
    reaction = allReactions[resource]
    if reaction == None:
        print("ERROR: no reaction found for", resource)
        return 0
    oreCost = 0
    bulkReactionInputs = reaction.getInputsForOutputQuantity(requiredQuantity)
    if resource in leftOvers:
        print("ERROR: leftOvers[resource] should be empty by now")
    resourcesLeftOver = (math.ceil(requiredQuantity / reaction.outputQuantity) * reaction.outputQuantity) - requiredQuantity
    if resourcesLeftOver > 0:
        leftOvers[resource] = resourcesLeftOver
    for reactionInput in bulkReactionInputs:
        oreCost += getOreCost(reactionInput, bulkReactionInputs[reactionInput], allReactions, leftOvers)
    return oreCost

with open('2019/Day14_input.txt', 'r') as f:
    inputFile = f.readlines()
    allReactions = {}
    for line in inputFile:
        segments = line.split("=>")
        if len(segments) != 2:
            print("ERROR: file format is wrong")
            break
        inputStrings = segments[0].split(",")
        outputSegments = segments[1].strip().split(" ")
        if len(outputSegments) != 2:
            print("ERROR: file format is wrong")
            break
        reaction = Reaction(outputSegments[1].strip(), int(outputSegments[0].strip()))
        for inputString in inputStrings:
            inputSegments = inputString.strip().split(" ")
            if len(inputSegments) != 2:
                print("ERROR: file format is wrong")
                break
            reaction.inputQuatities[inputSegments[1].strip()] = int(inputSegments[0].strip())
        allReactions[reaction.output] = reaction
    
    #A
    leftOvers = {}
    fuelCost = getOreCost("FUEL", 1, allReactions, leftOvers)
    print(fuelCost)

    #B
    oreAvailable = 1000000000000
    #the amount we can guarantee we'll be able to make
    startAmount = math.floor(oreAvailable / fuelCost)
    
    leftOvers = {}
    oreCost = getOreCost("FUEL", startAmount, allReactions, leftOvers)
    fuelProduced = startAmount
    oreAvailable -= oreCost
    power = math.floor(math.log10(oreAvailable))
    while True:
        leftOverBackup = leftOvers.copy()
        oreCost = getOreCost("FUEL", 10**power, allReactions, leftOvers)
        if oreAvailable >= oreCost:
            oreAvailable -= oreCost
            fuelProduced += 10**power
        else:
            leftOvers = leftOverBackup
            if power == 0:
                break
            else:
                power -= 1
    print(fuelProduced)