import math

def runProgram(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb
    
    memSize = len(memory)
    opcodePosition = 0
    while opcodePosition < memSize:
        opcode = memory[opcodePosition]
        #perform checks
        numArgs = 0
        if opcode == 1:
            numArgs = 3
        elif opcode == 2:
            numArgs = 3
        elif opcode == 99:
            numArgs = 0
        else:
            print("ERROR: invalid opcode found: ", opcode, " in position ", opcodePosition)
            break
        
        if opcodePosition + numArgs >= memSize:
            print("ERROR: not enought memory to get ", numArgs, " arguments for operation ", opcode)
            break
        for arg in range(1, numArgs):
            if memory[opcodePosition + arg] >= memSize:
                print("ERROR: argument ", arg, " out of bounds: ", memory[opcodePosition + arg])
                break

        #perform operation
        if opcode == 1:
            memory[memory[opcodePosition + 3]] = memory[memory[opcodePosition + 1]] + memory[memory[opcodePosition + 2]]
        elif opcode == 2:
            memory[memory[opcodePosition + 3]] = memory[memory[opcodePosition + 1]] * memory[memory[opcodePosition + 2]]
        elif opcode == 99:
            break
        opcodePosition += numArgs + 1

    return memory[0]

with open('2019/Day2_input.txt', 'r') as f:
    input = f.readline()
    input = input.split(',')
    memory = [int(x) for x in input]
    
    #A
    #print(runProgram(memory, 12, 2))
    
    #B
    target = 19690720
    targetFound = False
    for noun in range(0, 100):
        for verb in range(0, 100):
            result = runProgram(memory[:], noun, verb)
            if result == target:
                print("Success: ", (100*noun) + verb)
                targetFound = True
                break
        if targetFound:
            break
    print("run complete")
