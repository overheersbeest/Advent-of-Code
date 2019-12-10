import math

def getFuelCost(m):
    return math.trunc(m / 3)-2

with open('2019/Day1_input.txt', 'r') as f:
    input = f.readlines()
    input = [int(x) for x in input]
    totalFuelRequired = 0
    for module in input:
        FuelCostToAdd = getFuelCost(module)
        while FuelCostToAdd > 0:
            totalFuelRequired += FuelCostToAdd
            FuelCostToAdd = getFuelCost(FuelCostToAdd)
    print(str(totalFuelRequired))
