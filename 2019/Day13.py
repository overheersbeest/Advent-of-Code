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
                        playerInput = input()
                        if playerInput == "a":
                            newInput = -1
                        elif playerInput == "s":
                            newInput = 0
                        elif playerInput == "d":
                            newInput = 1
                        else:
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

with open('2019/Day13_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.split(',')
    inputFile = [int(x) for x in inputFile]

    #A
    if False:
        program = Program(inputFile[:])
        program.printOutput = False
        output = []
        program.run([], output)
        minX = 0
        maxX = 0
        minY = 0
        maxY = 0
        paintedTiles = {}
        for i in range(0,len(output), 3):
            x = output[i]
            y = output[i+1]
            minX = min(minX, x)
            maxX = max(maxX, x)
            minY = min(minY, y)
            maxY = max(maxY, y)
            paintedTiles[(x, y)] = output[i+2]
        
        blockCount = sum([1 if x == 2 else 0 for x in paintedTiles.values()])
        print(blockCount)
    
    #B
    def drawScreen(tiles, width, height):
        screen = [['.' for x in range(width)] for y in range(height)]
        for x, y in tiles:
            charToPaint = '?'
            tileID = tiles[(x, y)]
            if tileID == 0:
                charToPaint = '.'
            elif tileID == 1:
                charToPaint = '#'
            elif tileID == 2:
                charToPaint = 'X'
            elif tileID == 3:
                charToPaint = '='
            elif tileID == 4:
                charToPaint = '0'
            screen[y][x] = charToPaint
        for row in screen:
            print("".join(row))

    program = Program(inputFile[:])
    program.memory[0] = 2
    program.printOutput = False
    program.pauseOnInput = True
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    joystickInput = [0]*10 + [-1] + [0]*5 + [1,1] + [0]*22 + [-1,-1] + [0]*25 + [1]*4 + [0]*21 + [1]*7 + [0]*11 + [-1] + [0]*36 + [1]*3 + [0]*16 + [-1,-1,-1] + [0]*500 + [-1]*18 + [0]*360 + [1]*10 + [0]*370 + [1]*3 + [0]*3 + [1]*3 + [0]*7
    joystickInput += [0]*160 + [-1]*3 + [0]*30 + [-1]*15 + [0]*125 + [1]*8 + [0]*70 + [1]*14 + [0]*180 + [-1]*10 + [0]*100 + [-1]*9 + [0]*50 + [-1]*8 + [0]*10 + [-1]*4 + [0]*80 + [1]*9 + [0]*70 + [-1]*5 + [0]*10 + [1]*3 + [0]*30 + [-1]*2
    joystickInput += [0]*16 + [1]*4 + [0]*45 + [-1]*2 + [0]*60 + [1]*29 + [0]*29 + [-1]*30 + [0]*10 + [-1]*1 + [1]*31 + [0]*70 + [-1]*1 + [0]*20 + [-1]*33 + [0]*50 + [1]*1 + [0]*80 + [-1]*1 + [0]*30 + [1]*34 + [0]*10 + [-1]*30 + [0]*20
    joystickInput += [1]*26 + [0]*30 + [-1]*9 + [0]*50 + [1]*10 + [0]*241 + [-1]*23 + [0]*45 + [1]*18 + [0]*60 + [-1]*4 + [0]*35 + [-1]*10 + [0]*20 + [1]*1 + [0]*40 + [1]*15 + [0]*40 + [-1]*22 + [0]*30 + [1]*1 + [0]*10 + [1]*25 + [0]*10
    joystickInput += [-1]*30 + [0]*20 + [1]*34 + [0]*8 + [-1]*38 + [0]*5 + [1]*40 + [-1]*38 + [0]*6 + [1]*34 + [0]*10 + [-1]*30 + [0]*14 + [1]*26 + [0]*18 + [-1]*22 + [0]*22 + [1]*18 + [0]*26 + [0]*28
    skipStepNr = len(joystickInput) - 1
    counter = 0
    score = 0
    paintedTiles = {}
    while True:
        output = []
        program.run(joystickInput, output)
        for i in range(0,len(output), 3):
            x = output[i]
            y = output[i+1]
            if x == -1 and y == 0:
                newScore = output[i+2]
                if newScore != score:
                    #print("delta", newScore - score)
                    if newScore == 0:
                        drawScreen(paintedTiles, maxX - minX + 1, maxY - minY + 1)
                        print("score:", score)
                    score = newScore
                    #program.verbose = True
            else:
                minX = min(minX, x)
                maxX = max(maxX, x)
                minY = min(minY, y)
                maxY = max(maxY, y)
                paintedTiles[(x, y)] = output[i+2]
        counter += 1
        if counter > skipStepNr:
            drawScreen(paintedTiles, maxX - minX + 1, maxY - minY + 1)
            print("score:", score)
            print("steps:", counter - skipStepNr - 1)
        if program.lastRunProcessedInput == False:
            #game over
            drawScreen(paintedTiles, maxX - minX + 1, maxY - minY + 1)
            print("score:", score)
            print(counter, skipStepNr, counter - skipStepNr)
            break
        joystickInput = []