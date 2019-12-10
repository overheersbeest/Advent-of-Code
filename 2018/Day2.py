with open('2018/Day2_input.txt', 'r') as f:
    inputFile = f.readlines()
    inputFile = [line.strip() for line in inputFile]

    #test input
    #inputFile = ["abcdef","bababc","abbcde","abcccd","aabcdd","abcdee","ababab"]
    #inputFile = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]

    #A
    if False:
        countDoubles = 0
        countTriples = 0
        for line in inputFile:
            letterCounts = {}
            for char in line:
                if char not in letterCounts:
                    letterCounts[char] = 0
                letterCounts[char] += 1
            foundDouble = False
            foundTriple = False
            for letter in letterCounts:
                count = letterCounts[letter]
                if count == 2:
                    foundDouble = True
                elif count == 3:
                    foundTriple = True
            if foundDouble:
                countDoubles += 1
            if foundTriple:
                countTriples += 1
        print(countDoubles * countTriples)

    #B
    if True:
        for ignoreIndex in range(len(inputFile[0])):
            stringSet = set()
            for line in inputFile:
                setLine = line[:ignoreIndex] + line[ignoreIndex+1:]
                if setLine in stringSet:
                    print(setLine)
                else:
                    stringSet.add(setLine)