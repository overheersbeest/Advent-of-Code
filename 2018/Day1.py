with open('2018/Day1_input.txt', 'r') as f:
    inputFile = f.readlines()
    inputFile = [int(x) for x in inputFile]
    
    #A
    #print(sum(inputFile))

    #B
    current = 0
    foundRecurring = False
    visitedNumbers = {0}
    while not foundRecurring:
        for adjustment in inputFile:
            current += adjustment
            if current in visitedNumbers:
                foundRecurring = True
                break
            else:
                visitedNumbers.add(current)
    print(current)