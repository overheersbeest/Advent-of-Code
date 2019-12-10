import math
import queue

def runProgram(memory, inputQueue, outputValues, overrideInstructionIndex = -1, printOutput = True, pauseOnOutput = False):
    memSize = len(memory)
    instructionIndex = 0
    if overrideInstructionIndex > 0:
        instructionIndex = overrideInstructionIndex
    lastOutput = None
    while instructionIndex < memSize:
        modeMap = ""
        opcode = memory[instructionIndex]
        if opcode >= 100:
            instruction = str(memory[instructionIndex])
            modeMap = instruction[len(instruction)-3::-1]
            opcode = int(instruction[len(modeMap):])
        #perform checks
        numArgs = 0
        if opcode == 1: #add
            numArgs = 3
        elif opcode == 2: #multiply
            numArgs = 3
        elif opcode == 3: #input
            numArgs = 1
        elif opcode == 4: #output
            numArgs = 1
        elif opcode == 5: #jump-if-true
            numArgs = 2
        elif opcode == 6: #jump-if-false
            numArgs = 2
        elif opcode == 7: #less than
            numArgs = 3
        elif opcode == 8: #equals
            numArgs = 3
        elif opcode == 99: #halt
            numArgs = 0
        else:
            print("ERROR: invalid opcode found: ", opcode, " in position ", instructionIndex)
            break
        
        if instructionIndex + numArgs >= memSize:
            print("ERROR: not enough memory to get ", numArgs, " arguments for operation ", opcode, " in position ", instructionIndex)
            break
        if len(modeMap) > numArgs:
            print("ERROR: number of arguments and number of modes provided do not match. args:", numArgs, ", modes: ", len(modeMap), " in position ", instructionIndex)
            break
        elif len(modeMap) < numArgs:
            modeMap += "0" * (numArgs - len(modeMap))
        for arg in range(numArgs):
            if modeMap[arg] == "0" and memory[instructionIndex + 1 + arg] >= memSize:
                print("ERROR: argument ", arg, " out of bounds: ", memory[instructionIndex + arg], " in position ", instructionIndex)
                break
        
        instructionIndexModified = False
        #perform operation
        if opcode == 1: #add
            a = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            b = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
            if modeMap[2] == "0":
                memory[memory[instructionIndex + 3]] = a + b
            else:
                memory[instructionIndex + 3] = a + b
        elif opcode == 2: #multiply
            a = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            b = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
            if modeMap[2] == "0":
                memory[memory[instructionIndex + 3]] = a * b
            else:
                memory[instructionIndex + 3] = a * b
        elif opcode == 3: #input
            if inputQueue.empty():
                print("please provide additional input:")
                newInput = int(input())
                inputQueue.put(newInput)
            memory[memory[instructionIndex + 1]] = inputQueue.get()
        elif opcode == 4: #output
            lastOutput = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            outputValues.append(lastOutput)
            if printOutput:
                print(lastOutput, "printed at", instructionIndex)
            if pauseOnOutput:
                return instructionIndex + numArgs + 1
        elif opcode == 5: #jump-if-true
            param = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            if param != 0:
                instructionIndex = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
                instructionIndexModified = True
        elif opcode == 6: #jump-if-false
            param = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            if param == 0:
                instructionIndex = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
                instructionIndexModified = True
        elif opcode == 7: #less than
            a = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            b = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
            result = 1 if a < b else 0
            if modeMap[2] == "0":
                memory[memory[instructionIndex + 3]] = result
            else:
                memory[instructionIndex + 3] = result
        elif opcode == 8: #equals
            a = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            b = memory[memory[instructionIndex + 2]] if modeMap[1] == "0" else memory[instructionIndex + 2]
            result = 1 if a == b else 0
            if modeMap[2] == "0":
                memory[memory[instructionIndex + 3]] = result
            else:
                memory[instructionIndex + 3] = result
        elif opcode == 99: #halt
            return None
        if instructionIndexModified == False:
            instructionIndex += numArgs + 1

    return None

def getAllPermutations(inputList):
    if len(inputList) == 0:
        return []
    if len(inputList) == 1:
        return [inputList]
    retVal = []
    for i in range(len(inputList)):
       char = inputList[i]
       unusedCharacters = inputList[:i] + inputList[i+1:]
       for remainingPermutation in getAllPermutations(unusedCharacters): 
           retVal.append([char] + remainingPermutation) 
    return retVal 

with open('2019/Day7_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.split(',')
    memory = [int(x) for x in inputFile]
    
    #test inputs
    #memory = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    #memory = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    #memory = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

    #A
    if False:
        maxOutput = 0
        maxOutputPermutation = []
        data = [0,1,2,3,4]
        for permutation in getAllPermutations(data):
            print("")
            print("permutation:", permutation)
            output = 0
            for phase in permutation:
                output = runProgram(memory[:], [phase, output], [])
            if output > maxOutput:
                maxOutput = output
                maxOutputPermutation = permutation
        print("max output:", maxOutput, "at", maxOutputPermutation)

    #test inputs
    #memory = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    #memory = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    #B
    maxOutput = 0
    maxOutputPermutation = []
    data = [5,6,7,8,9]
    for permutation in getAllPermutations(data):
        print("permutation:", permutation)
        permutationInstructionIndices = [0 for x in range(len(permutation))]
        permutationMemories = [memory[:] for x in range(len(permutation))]
        queuedInputs = [queue.Queue() for x in range(len(permutation))]
        for x in range(len(permutation)):
            queuedInputs[x].put(permutation[x])
        queuedInputs[0].put(0)
        ampOutputs = [[] for x in range(len(permutation))]
        halt = False
        while not halt:
            for permutationIndex in range(len(permutation)):
                #print("switching to amp", permutationIndex)
                workingMemory = permutationMemories[permutationIndex]
                inputForRun = queuedInputs[permutationIndex]
                programOutput = ampOutputs[permutationIndex]
                instructionIndex = permutationInstructionIndices[permutationIndex]
                resumePointer = runProgram(workingMemory, inputForRun, programOutput, instructionIndex, printOutput=False, pauseOnOutput=True)
                if resumePointer == None:
                    halt = True
                else:
                    permutationInstructionIndices[permutationIndex] = resumePointer
                queuedInputs[permutationIndex - len(queuedInputs) + 1].put(programOutput[-1])
                #for permutationIndex in range(len(permutation)):
                #    print(permutationMemories[permutationIndex], permutationInstructionIndices[permutationIndex], queuedInputs[permutationIndex].queue, ampOutputs[permutationIndex])

        permutationOutput = ampOutputs[-1][-1]
        if permutationOutput > maxOutput:
            maxOutput = permutationOutput
            maxOutputPermutation = permutation
    print("max output:", maxOutput, "at", maxOutputPermutation)