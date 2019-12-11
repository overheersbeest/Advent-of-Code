imageWidth = 25
imageHeight = 6

with open('2019/Day8_input.txt', 'r') as f:
    inputFile = f.readline().strip()
    numLayers = len(inputFile) / (imageWidth * imageHeight)
    if numLayers % 1 != 0:
        print("ERROR: data incomplete, there is not enough data to create entire layers")
    else:
        numLayers = int(numLayers)
        layersRaw = [[] for x in range(numLayers)]
        imageSize = imageWidth * imageHeight
        minZeros = imageSize
        minZerosIndex = 0
        for layerIndex in range(numLayers):
            layersRaw[layerIndex] = inputFile[imageSize * layerIndex:(imageSize * (layerIndex + 1))]
            zeros = sum(x == '0' for x in layersRaw[layerIndex])
            if zeros < minZeros:
                minZeros = zeros
                minZerosIndex = layerIndex
        
        ones = sum(x == '1' for x in layersRaw[minZerosIndex])
        twos = sum(x == '2' for x in layersRaw[minZerosIndex])
        print(ones * twos)

        outputImageRaw = ['2' for x in range(imageSize)]
        for layerIndex in range(numLayers):
            for pixelIndex in range(imageSize):
                if outputImageRaw[pixelIndex] == '2' and layersRaw[layerIndex][pixelIndex] != '2':
                    outputImageRaw[pixelIndex] = '0' if layersRaw[layerIndex][pixelIndex] == '1' else ' '
        
        outputImage = [[] for x in range(imageHeight)]
        for rowIndex in range(imageHeight):
            outputImage[rowIndex] = outputImageRaw[rowIndex * imageWidth : (rowIndex + 1) * imageWidth]
        
        for row in outputImage:
            print(''.join(row))