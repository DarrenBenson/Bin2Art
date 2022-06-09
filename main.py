import os
import mmap
from numpy import ceil, sqrt
from PIL import Image

def getOutputFilename(inputFileName):
    baseFileName = os.path.splitext(inputFileName)[0]
    return baseFileName + ".png"

def loadFileData(filename):
    with open(filename, mode="rb") as file:
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as fileData:
            return fileData.read()

def generateImage(fileName):
    outputFileName = getOutputFilename(inputFileName)
    fileData = loadFileData(fileName)
    pixelDimention = int(ceil(sqrt(len(fileData) / 3)))
    outputImage = Image.new("RGBA", (pixelDimention, pixelDimention), "black")
    pixelCount = 0
    for x in range(pixelDimention):
        for y in range(pixelDimention):       
            rgbValue = [0, 0, 0]
            for i in range(3):            
                rgbValue[i] = fileData[pixelCount]
                if pixelCount < len(fileData) - 1:
                    pixelCount += 1
            outputImage.putpixel((x,y),(rgbValue[0], rgbValue[1], rgbValue[2]))
    resizedImage = outputImage.resize((1920, 1920), Image.Resampling.BOX)
    resizedImage.save(outputFileName, "PNG")


inputFileName = "Chuckie Egg.tap"
generateImage(inputFileName)