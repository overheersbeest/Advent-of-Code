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
        self.verbose = False

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

    def run(self, inputValues, outputValues, ):
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
                    newInput = int(input())
                    self.inputQueue.put(newInput)
                self.setValue(modeMap[0], self.instructionIndex + 1, self.inputQueue.get())
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

with open('2019/Day9_input.txt', 'r') as f:
    inputFile = f.readline()
    inputFile = inputFile.split(',')
    inputFile = [int(x) for x in inputFile]
    
    #test inputs
    #inputFile = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    #inputFile = [1102,34915192,34915192,7,4,7,99,0]
    #inputFile = [104,1125899906842624,99]

    #A
    if False:
        program = Program(inputFile[:])
        #program.verbose = True
        program.printOutput = False
        #print(program.memory)
        output = []
        program.run([1], output)
        print(output)
    
    #B
    if True:
        program = Program(inputFile[:])
        program.printOutput = False
        output = []
        program.run([2], output)
        print(output)