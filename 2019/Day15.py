import math
import queue

class Program:
    def __init__(self, memory):
        self.instructionIndex = 0
        self.relativeBase = 0
        self.lastOutput = None
        self.memory = memory
        self.memSize = len(memory)
        self.inputQueue = queue.Queue()
        self.printOutput = True
        self.pauseOnOutput = False
        self.pauseOnInput = False
        self.verbose = False
        self.halted = False
        self.lastRunProcessedInput = False

    def expandMemoryIfNeeded(self, mode, index):
        if mode == "0":
            if index >= self.memSize:
                self.memory += [0 for x in range(index - (self.memSize - 1))]
                self.memSize = len(self.memory)
            if self.memory[index] >= self.memSize:
                self.memory += [0 for x in range(self.memory[index] - (self.memSize - 1))]
                self.memSize = len(self.memory)
        elif mode == "1":
            if index >= self.memSize:
                self.memory += [0 for x in range(index - (self.memSize - 1))]
                self.memSize = len(self.memory)
        elif mode == "2":
            if index >= self.memSize:
                self.memory += [0 for x in range(index - (self.memSize - 1))]
                self.memSize = len(self.memory)
            if self.relativeBase + self.memory[index] >= self.memSize:
                self.memory += [0 for x in range(self.relativeBase + self.memory[index] - (self.memSize - 1))]
                self.memSize = len(self.memory)
        else:
            print("ERROR: invalid mode provided:", mode)

    def getValue(self, mode, index):
        self.expandMemoryIfNeeded(mode, index)
        if mode == "0":
            return self.memory[self.memory[index]]
        elif mode == "1":
            return self.memory[index]
        elif mode == "2":
            return self.memory[self.relativeBase + self.memory[index]]
        else:
            print("ERROR: invalid mode provided:", mode)

    def setValue(self, mode, index, value):
        self.expandMemoryIfNeeded(mode, index)
        if mode == "0":
            self.memory[self.memory[index]] = value
        elif mode == "1":
            self.memory[index] = value
        elif mode == "2":
            self.memory[self.relativeBase + self.memory[index]] = value
        else:
            print("ERROR: invalid mode provided:", mode)

    def run(self, inputValues, outputValues):
        self.halted = False
        self.lastRunProcessedInput = False
        for x in inputValues:
            self.inputQueue.put(x)

        pause = False
        while self.instructionIndex < self.memSize:
            modeMap = ""
            opcode = self.memory[self.instructionIndex]
            if opcode >= 100:
                instruction = str(self.memory[self.instructionIndex])
                modeMap = instruction[len(instruction)-3::-1]
                opcode = int(instruction[len(modeMap):])
            
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
            elif opcode == 9: #relative base offset
                numArgs = 1
            elif opcode == 99: #halt
                numArgs = 0
            else:
                print("ERROR: invalid opcode found: ", opcode, " in position ", self.instructionIndex)
                break
            
            if self.instructionIndex + numArgs >= self.memSize:
                print("ERROR: not enough memory to get ", numArgs, " arguments for operation ", opcode, " in position ", self.instructionIndex)
                break
            if len(modeMap) > numArgs:
                print("ERROR: number of arguments and number of modes provided do not match. args:", numArgs, ", modes: ", len(modeMap), " in position ", self.instructionIndex)
                break
            elif len(modeMap) < numArgs:
                modeMap += "0" * (numArgs - len(modeMap))
            
            if self.verbose:
                print("\t", self.instructionIndex, self.memory[self.instructionIndex:self.instructionIndex + numArgs + 1], self.relativeBase)
                for i in range(numArgs):
                    print(self.getValue(modeMap[i], self.instructionIndex + 1 + i))
                print("")

            instructionIndexModified = False
            #perform operation
            if opcode == 1: #add
                a = self.getValue(modeMap[0], self.instructionIndex + 1)
                b = self.getValue(modeMap[1], self.instructionIndex + 2)
                self.setValue(modeMap[2], self.instructionIndex + 3, a + b)
            elif opcode == 2: #multiply
                a = self.getValue(modeMap[0], self.instructionIndex + 1)
                b = self.getValue(modeMap[1], self.instructionIndex + 2)
                self.setValue(modeMap[2], self.instructionIndex + 3, a * b)
            elif opcode == 3: #input
                if self.inputQueue.empty():
                    print("please provide additional input:")
                    #custom inputs
                    newInput = None
                    while newInput == None:
                        try:
                            newInput = int(input())
                        except:
                            newInput = None
                    self.inputQueue.put(newInput)
                self.setValue(modeMap[0], self.instructionIndex + 1, self.inputQueue.get())
                self.lastRunProcessedInput = True
                if self.pauseOnInput:
                    pause = True
            elif opcode == 4: #output
                self.lastOutput = self.getValue(modeMap[0], self.instructionIndex + 1)
                outputValues.append(self.lastOutput)
                if self.printOutput:
                    print(self.lastOutput, "printed at", self.instructionIndex)
                if self.pauseOnOutput:
                    pause = True
            elif opcode == 5: #jump-if-true
                param = self.getValue(modeMap[0], self.instructionIndex + 1)
                if param != 0:
                    self.instructionIndex = self.getValue(modeMap[1], self.instructionIndex + 2)
                    instructionIndexModified = True
            elif opcode == 6: #jump-if-false
                param = self.getValue(modeMap[0], self.instructionIndex + 1)
                if param == 0:
                    self.instructionIndex = self.getValue(modeMap[1], self.instructionIndex + 2)
                    instructionIndexModified = True
            elif opcode == 7: #less than
                a = self.getValue(modeMap[0], self.instructionIndex + 1)
                b = self.getValue(modeMap[1], self.instructionIndex + 2)
                self.setValue(modeMap[2], self.instructionIndex + 3, 1 if a < b else 0)
            elif opcode == 8: #equals
                a = self.getValue(modeMap[0], self.instructionIndex + 1)
                b = self.getValue(modeMap[1], self.instructionIndex + 2)
                self.setValue(modeMap[2], self.instructionIndex + 3, 1 if a == b else 0)
            elif opcode == 9: #relative base offset
               self.relativeBase += self.getValue(modeMap[0], self.instructionIndex + 1)
            elif opcode == 99: #halt
                self.halted = True
                return
            else:
                print("ERROR: invalid opcode found: ", opcode, " in position ", self.instructionIndex)
                break

            if self.verbose:
                print(self.instructionIndex, self.relativeBase)
                for i in range(numArgs):
                    print(self.getValue(modeMap[i], self.instructionIndex + 1 + i))
                print("")
                print("")

            if instructionIndexModified == False:
                self.instructionIndex += numArgs + 1
            if pause:
                return

        return

def getPositionInDirection(startPos, direction, stepSize = 1):
    if direction == 1:#up
        return (startPos[0], startPos[1] + stepSize)
    elif direction == 2:#down
        return (startPos[0], startPos[1] - stepSize)
    elif direction == 3:#left
        return (startPos[0] - stepSize, startPos[1])
    elif direction == 4:#right
        return (startPos[0] + stepSize, startPos[1])

def drawScreen(knownPositions, dronePosition):
    print("")
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    paintedTiles = {}
    for x, y in knownPositions:
        minX = min(minX, x)
        maxX = max(maxX, x)
        minY = min(minY, y)
        maxY = max(maxY, y)
    width = maxX + 1 - minX
    height = maxY + 1 - minY
    screen = [['?' for x in range(width)] for y in range(height)]
    for x, y in knownPositions:
        if (x, y) == dronePosition:
            screen[height - (y - minY) - 1][x - minX] = "D"
        else:
            screen[height - (y - minY) - 1][x - minX] = knownPositions[(x, y)]
    for row in screen:
        print("".join(row))

with open('2019/Day15_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.split(',')
    inputFile = [int(x) for x in inputFile]

    #A
    program = Program(inputFile[:])
    program.printOutput = False
    program.pauseOnOutput = True

    dronePos = (0, 0)
    knownPositions = {}
    knownPositions[dronePos] = "."
    while True:
        output = []

        #custom inputs
        programInput = None
        while programInput == None:
            playerInput = input()
            if playerInput == "w":
                programInput = 1
            elif playerInput == "a":
                programInput = 3
            elif playerInput == "s":
                programInput = 2
            elif playerInput == "d":
                programInput = 4
        
        program.run([programInput], output)
        if len(output) != 1:
            print("ERROR: expected output")
        outputCode = output[0]
        if outputCode == 0:
            #hit a wall
            knownPositions[getPositionInDirection(dronePos, programInput)] = "#"
        elif outputCode == 1 or outputCode == 2:
            #moved a stepw
            dronePos = getPositionInDirection(dronePos, programInput)
            if outputCode == 2:
                #reached Destination
                knownPositions[dronePos] = "X"
                break
            else:
                knownPositions[dronePos] = "."
        else:
            print("ERROR: invalid output")
        drawScreen(knownPositions, dronePos)
    #answer 204

    #B
    #answer 340

#map for reference:
#########################################
#.....#.........#.....#.....#...#.....x.#
###.#.###.###.#.#.###.###.#.#.#.#####.#.#
#...#...#.#...#...#.#...#.#...#.....#.#.#
#.#####.#.#.#######.###.#.#########.#.#.#
#...#.#.#.#.#...#.....#...#.......#.#.#.#
###.#.#.###.#.#.#####.#####.#######.#.#.#
#...#...#...#.#.....#.....#.........#.#.#
#.###.###.###.#####.#.#.###.###########.#
#.#...#...#.....#.....#.#...#.........#.#
#.#.###.#.#.###.#.#######.#########.#.#.#
#.#...#.#.#...#.#.#.....#.....#.....#...#
#.###.###.#####.#.#.###.#####.#.#######.#
#...#.....#.....#.#.#.......#...#...#...#
#.#.#######.#######.#.###########.#.#.###
#.#...#.............#.#.........#.#...#.#
#.###.#.#############.#.#######.#.#####.#
#.#...#.#...........#.#.#...#...#...#...#
###.#####.#########.#.#.#.#.#.#####.#.#.#
#...#...#...#.....#.#.....#.#.....#.#.#.#
#.###.#.###.#.###.#.#######.#####.#.#.###
#...#.#.....#.#.....#S#...#.#...#...#...# S=Start location
#.#.#.#######.#.#####.#.###.###.#####.#.#
#.#.#...#...#.#.#.....#.......#...#...#.#
#.#.###.###.#.###.#####.#####.#.#.#####.#
#.#...#.....#.....#.....#...#.#.#...#...#
#.#.#.#####.###########.#.#.#.#.###.#.#.#
#.#.#.....#...........#.#.#.#...#.#...#.#
###.#.###############.###.#.#####.#####.#
#...#.#.............#.#...#.....#.......#
#.#####.###########.#.#.#######.###.#####
#.#.....#....?????#.#...#.....#...#.#...#
#.#.#####.#.#???###.#####.#.#####.#.###.#
#.#.#O....#.#???#...#...#.#.......#.....# O=Oxygen generator
#.#.#######.#####.#.###.#.#############.#
#.#.........#.....#.....#...#...#.....#.#
#.#########.#.#####.#######.#.#.#.#.###.#
#.....#.....#.#.....#.....#.#.#...#.....#
#.#####.#####.#######.###.#.#.###########
#...........#...........#...#...........#
#########################################


    