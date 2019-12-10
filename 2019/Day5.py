import math

def runProgram(memory, inputValues):
    nextInputIndex = 0

    memSize = len(memory)
    instructionIndex = 0
    lastOperationWasOutput = False
    lastOutput = 0
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
            if nextInputIndex >= len(inputValues):
                print("please provide additional input:")
                newInput = int(input())
                inputValues.append(newInput)
            memory[memory[instructionIndex + 1]] = inputValues[nextInputIndex]
            nextInputIndex += 1
        elif opcode == 4: #output
            lastOutput = memory[memory[instructionIndex + 1]] if modeMap[0] == "0" else memory[instructionIndex + 1]
            print(lastOutput, "printed at", instructionIndex)
        elif opcode == 5: #jump-if-ture
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
            if lastOperationWasOutput:
                return lastOutput
            break
        lastOperationWasOutput = opcode == 4
        if instructionIndexModified == False:
            instructionIndex += numArgs + 1

    return memory[0]

with open('2019/Day5_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.split(',')
    memory = [int(x) for x in inputFile]
    
    #A
    #print(runProgram(memory[:], [1]))

    #tests
    #print(runProgram([3,9,8,9,10,9,4,9,99,-1,8], [])) #equal to 8, position mode
    #print(runProgram([3,9,7,9,10,9,4,9,99,-1,8], [])) #less than to 8, position mode
    #print(runProgram([3,3,1108,-1,8,3,4,3,99], [])) #equal to 8, immediate  mode
    #print(runProgram([3,3,1107,-1,8,3,4,3,99], [])) #less than to 8, immediate  mode
    #print(runProgram([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [])) #is false, position mode
    #print(runProgram([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [])) #is false, immediate mode
    #print(runProgram([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], [])) #compare to 8, outputs 999, 1000, or 1001
    #B
    print(runProgram(memory[:], [5]))