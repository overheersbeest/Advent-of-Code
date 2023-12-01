import re

def GetCalibrationValue_PartOne(line):
    first = None
    last = None
    for char in line:
        if str.isnumeric(char):
            last = int(char)
            if first == None:
                first = last
    return first*10 + last

def GetCalibrationValue_PartTwo(line):
    matches = re.findall('(\d)|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine)', line)

    def GetNum(match):
        if len(match[0]) > 0:
            return int(match[0])
        else:
            for i in range(1, 10):
                if (len(match[i]) > 0):
                    return i

    return GetNum(matches[0]) * 10 + GetNum(matches[len(matches)-1])

with open('2023/Day1_input.txt', 'r') as f:
    input = f.readlines()
    partOne = 0
    partTwo = 0
    for line in input:
        partOne += GetCalibrationValue_PartOne(line)
        partTwo += GetCalibrationValue_PartTwo(line)
    print("Part 1: " + str(partOne))
    print("Part 2: " + str(partTwo))
