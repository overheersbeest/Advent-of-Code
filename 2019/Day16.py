import time
import math

def getNonZeroMultipliers(pattern, writeIndex, maxIndex):
    retVal = set()
    segmentWidth = writeIndex + 1
    repeatWidth = len(pattern) * segmentWidth
    repeats = math.ceil((maxIndex + 1) / repeatWidth)
    for p in range(len(pattern)):
        mult = pattern[p]
        if mult != 0:
            for r in range(repeats):
                for s in range(segmentWidth):
                    if p == 0 and r == 0 and s == 0:
                        continue
                    realIndex = (r * repeatWidth) + (p * segmentWidth) + s - 1
                    if realIndex <= maxIndex:
                        retVal.add(realIndex)
    return retVal

def getMultiplier(pattern, writeIndex, readIndex):
    return pattern[((readIndex + 1) // (writeIndex + 1)) % len(pattern)]

def getSourceIndices(resultIndices, indexSet, elementLength):
    newIndicesToEvaluate = []
    for writeIndex in resultIndices:
        if writeIndex not in indexSet:
            indexSet.add(writeIndex)
            newIndicesToEvaluate.append(writeIndex)
        for readIndex in range(elementLength):
            multiplier = getMultiplier(pattern, writeIndex,readIndex)
            if multiplier != 0:
                if readIndex not in indexSet:
                    indexSet.add(readIndex)
                    newIndicesToEvaluate.append(readIndex)
    if len(newIndicesToEvaluate) > 0:
        getSourceIndices(newIndicesToEvaluate, indexSet, elementLength)

with open('2019/Day16_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.strip()
    pattern = [0, 1, 0, -1]

    #testInput
    #inputFile = "12345678"
    #inputFile = "80871224585914546619083218645595"
    #inputFile = "19617804207202209144916044189917"
    #inputFile = "69317163492948606335995924319873"
    inputFile = "03036732577212944063491565474664"
    #inputFile = "02935109699940807407585447034323"
    #inputFile = "03081770884921959731165446850517"

    #A
    if False:
        element = [int(x) for x in inputFile]
        phaseCount = 100
        elementLength = len(element)
        for phase in range(phaseCount):
            nextElement = element
            for writeIndex in range(elementLength):
                value = 0
                for readIndex in range(elementLength):
                    value += getMultiplier(pattern, writeIndex, readIndex) * element[readIndex]
                value = abs(value) % 10
                nextElement[writeIndex] = value
            element = nextElement
            #print("".join([str(x) for x in element]))
        print("".join([str(x) for x in element[:8]]))

    #B
    if True:
        element = [int(x) for x in inputFile]
        messageOffset = int("".join([str(x) for x in element[:7]]))
        elementLength = len(element) * 10000

        startTime = time.time()

        #multipliers cache
        indicesNeeded = set()
        indicesToAdd = range(messageOffset, messageOffset+8)
        while len(indicesToAdd) > 0:
            additionList = indicesToAdd[:]
            indicesToAdd = []
            for index in additionList:
                indicesNeeded.add(index)
                requiredindices = getNonZeroMultipliers(pattern, index, elementLength)
                print("added", len(requiredindices), "to set")
                for requiredIndex in requiredindices:
                    if requiredIndex not in indicesNeeded:
                        indicesToAdd.append(requiredindices)
            print("loop finished,", len(indicesToAdd), "to go.")
        
        #simplify element to only include values that affect the final signal
        simplifiedElement = []
        indexMap = list(indicesNeeded)
        indexMap.sort()
        for index in indexMap:
            simplifiedElement.append(element[index % len(element)])
        element = simplifiedElement
        elementLength = len(element)

        #multMap cache
        multMap = {}
        for simplifiedWriteIndex in range(elementLength):
            actualWriteIndex = indexMap[simplifiedWriteIndex]
            multMap[simplifiedWriteIndex] = {}
            for simplifiedReadIndex in range(elementLength):
                multMap[simplifiedWriteIndex][simplifiedReadIndex] = getMultiplier(pattern, actualWriteIndex, indexMap[simplifiedReadIndex])

        endTime = time.time()
        print(endTime - startTime, "seconds to run")
        
        phaseCount = 100
        for phase in range(phaseCount):
            nextElement = element
            for writeIndex in range(elementLength):
                value = 0
                for readIndex in range(elementLength):
                    value += multMap[(writeIndex, readIndex)] * element[readIndex]
                value = abs(value) % 10
                nextElement[writeIndex] = value
            element = nextElement
            print(phase)
        print("".join([str(x) for x in element[messageOffset:messageOffset+8]]))
