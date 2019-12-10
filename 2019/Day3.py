import math

with open('2019/Day3_input.txt', 'r') as f:
    input = f.readlines()
    input = [x.split(',') for x in input]
    
    #input = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],['U62','R66','U55','R34','D71','R55','D58','R83']]
    #input = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]

    XRange = [0, 0]
    YRange = [0, 0]
    for wireIndex in range(0, len(input)):
        pos = [0, 0]
        for operation in input[wireIndex]:
            stepLength = int(operation[1:])
            if operation.startswith('U'):
                pos[1] += stepLength
                YRange[1] = max(YRange[1], pos[1])
            elif operation.startswith('D'):
                pos[1] -= stepLength
                YRange[0] = max(YRange[0], pos[1])
            elif operation.startswith('R'):
                pos[0] += stepLength
                XRange[1] = max(XRange[1], pos[0])
            elif operation.startswith('L'):
                pos[0] -= stepLength
                XRange[0] = max(XRange[0], pos[0])
    
    root = [XRange[0], YRange[0]]
    mapWidth = XRange[0] + 1 + XRange[1]
    mapHeight = YRange[0] + 1 + YRange[1]
    map = [[0] * mapHeight for i in range(mapWidth)]

    minDistance = -1
    for wireIndex in range(0, len(input)):
        pos = [x for x in root]
        stepNr = 0
        marker = 1 << wireIndex
        for operation in input[wireIndex]:
            stepLength = int(operation[1:])
            delta = [0, 0]
            if operation.startswith('U'):
                delta = [0, 1]
            elif operation.startswith('D'):
                delta = [0, -1]
            elif operation.startswith('R'):
                delta = [1, 0]
            elif operation.startswith('L'):
                delta = [-1, 0]

            for i in range(stepLength):
                pos[0] += delta[0]
                pos[1] += delta[1]
                stepNr += 1

                if wireIndex == 0:
                    if map[pos[0]][pos[1]] == 0 or stepNr < map[pos[0]][pos[1]]:
                       map[pos[0]][pos[1]] = stepNr
                elif map[pos[0]][pos[1]] != 0:
                    distance = map[pos[0]][pos[1]] + stepNr
                    print("found intersection on ", pos[0], ", ", pos[1], ": distance=", distance)
                    if minDistance == -1 or distance < minDistance:
                        minDistance = distance
                
            #    map[pos[0]][pos[1]] += marker
            #    if map[pos[0]][pos[1]] == 3:
            #        distance = abs(pos[0] - root[0]) + abs(pos[1] - root[1])
            #        print("found intersection on ", pos[0], ", ", pos[1], ": distance=", distance)
            #        if minDistance == -1 or distance < minDistance:
            #            minDistance = distance
    
    print(minDistance)