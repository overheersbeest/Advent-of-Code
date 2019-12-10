import time

startTime = time.time()

minPass = 265275
maxPass = 781584

def getValidNumberString(number):
    numberList = list(str(number))
    increasedNumber = False
    prevDigit = int(numberList[0])
    for c in range(len(numberList)):
        if increasedNumber:
            numberList[c] = str(prevDigit)
        else:
            char = numberList[c]
            digit = int(char)
            if digit < prevDigit:
                digit = prevDigit
                increasedNumber = True
                numberList[c] = str(digit)
        prevDigit = digit
    #we can't go lower than this number, now we just have to check for double digits
    foundDouble = False
    while not foundDouble:
        for c in range(len(numberList) - 1):
            a = numberList[c]
            b = numberList[c+1]
            if a == b:
                #these are double digits, now let's make sure it isn't part of a larger set
                #look to the left
                if c == 0 or numberList[c-1] != a:
                    #look to the right
                    if c == len(numberList) - 2 or numberList[c+2] != a:
                        foundDouble = True
                        break
        #there isn't a double, so we increase the number to the next double (always in the last two digits)
        if not foundDouble:
            numberList = increment(numberList)
    return numberList

def increment(numberList):
    number = int("".join(numberList))
    number += 1
    return getValidNumberString(number)

currentNumberList = getValidNumberString(minPass)
count = 0
while int("".join(currentNumberList)) <= maxPass:
    count += 1
    currentNumberList = increment(currentNumberList)
print(count)
endTime = time.time()

print(endTime - startTime, "seconds to run")