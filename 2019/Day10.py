import math

with open('2019/Day10_input.txt', 'r') as f:
    inputFile = f.readlines()
    inputFile = [x.strip() for x in inputFile]

    #inputFile = [".#..#",".....","#####","....#","...##"]
    #inputFile = ["......#.#.","#..#.#....","..#######.",".#.#.###..",".#..#.....","..#....#.#","#..#....#.",".##.#..###","##...#..#.",".#....####"]
    #inputFile = ["#.#...#.#.",".###....#.",".#....#...","##.#.#.#.#","....#.#.#.",".##..###.#","..#...##..","..##....##","......#...",".####.###."]
    #inputFile = [".#..#..###","####.###.#","....###.#.","..###.##.#","##.##.#.#.","....###..#","..#.#..#.#","#..#.#.###",".##...##.#",".....#.#.."]
    #inputFile = [".#..##.###...#######","##.############..##.",".#.######.########.#",".###.#######.####.#.","#####.##.#.##.###.##","..#####..#.#########","####################","#.####....###.#.#.##","##.#################","#####.##.###..####..","..######..##.#######","####.##.####...##..#",".#####..#.######.###","##...#.##########...","#.##########.#######",".####.#.###.###.#.##","....##.##.###..#####",".#.#.###########.###","#.#.#.#####.####.###","###.##.####.##.#..##"]
    
    for row in inputFile:
        print(row)

    def getClockwiseAngleFromTop(v):
        angle = math.degrees(math.atan2(v[0], -v[1]))
        if angle < 0:
            angle += 360
        return angle

    #A
    maxSightlines = 0
    bestPosition = [-1, -1]
    bestSightlineMap = {}
    mapHeight = len(inputFile)
    mapWidth = len(inputFile[0])
    for rowIndex in range(mapHeight):
        row = inputFile[rowIndex]
        for columnIndex in range(mapWidth):
            #count visible asteroids
            blockedSightlines = {}
            if row[columnIndex] == '.':
                    continue
            visionMap = [["." for x in range(mapWidth)] for y in range(mapHeight)]
            for searchRowIndex in range(mapHeight):
                searchRow = inputFile[searchRowIndex]
                for searchColumnIndex in range(mapWidth):
                    if searchRow[searchColumnIndex] == '.':
                        continue
                    deltaX = searchColumnIndex - columnIndex 
                    deltaY = searchRowIndex - rowIndex

                    if deltaX == 0 and deltaY == 0:
                        visionMap[searchRowIndex][searchColumnIndex] = "0"
                        continue
                    
                    angle = getClockwiseAngleFromTop([deltaX, deltaY])
                    if angle not in blockedSightlines:
                        #we can see a new asteroid
                        blockedSightlines[angle] = [[deltaX, deltaY]]
                        visionMap[searchRowIndex][searchColumnIndex] = "+"
                    else:
                        blockedSightlines[angle] += [[deltaX, deltaY]]
                        visionMap[searchRowIndex][searchColumnIndex] = "-"
            sightlines = len(blockedSightlines)
            
            #print(columnIndex, ",", rowIndex)
            #for visionRow in visionMap:
            #    print("[" + "".join(visionRow) + "]")
            #print("score:", sightlines)
            if sightlines > maxSightlines:
                maxSightlines = sightlines
                bestPosition = [columnIndex, rowIndex]
                bestSightlineMap = blockedSightlines
    
    print(maxSightlines, "at", bestPosition)

    #B
    allSightlinesList = [[key, bestSightlineMap[key]] for key in bestSightlineMap]
    
    def sortSightlines(sightline):
        return sightline[0]

    def sortTargets(target):
        return abs(target[0])

    allSightlinesList.sort(key=sortSightlines)
    for sightline in allSightlinesList:
        sightline[1].sort(key=sortTargets)
    
    print(allSightlinesList)

    asteroidsToGo = 200
    while len(allSightlinesList) > 0:
        if asteroidsToGo > len(allSightlinesList):
            asteroidsToGo -= len(allSightlinesList)
            for sightline in allSightlinesList:
                sightline[1] = sightline[1][1:]
            #clean up
            allSightlinesList = [sightline for sightline in allSightlinesList if len(sightline[1]) > 0]
        else:
            targetDelta = allSightlinesList[asteroidsToGo - 1][1][0]
            print(bestPosition[0] + targetDelta[0], bestPosition[1] + targetDelta[1])
            break