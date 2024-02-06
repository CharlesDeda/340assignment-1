import cv2
import numpy as np
from matrixMult import matrixMult

def getSize(image, scale):
    return int(scale * max(image.shape[0], image.shape[1]))

def createEmptyImage(size):
    return np.zeros((size, size, 3), np.float32)

def rotate(iImage, oImage, angle):
    numRows = iImage.shape[0]  # height of image
    numCols = iImage.shape[1]  # width of image
    scaledSize = getSize(oImage, 1)
    scaledSize2 = scaledSize // 2

    ###Create an empty image of scaledSize
    rotatedImage = np.zeros((scaledSize, scaledSize, 3), np.float32)

    offsetb = (scaledSize - numRows) // 2
    offseta = (scaledSize - numCols) // 2
    print("size: ", numRows, numCols)

    ### iterate through pixels and change colors
    for b in range(numRows):  # height of the image, y coordinates
        for a in range(numCols):  # width of the image, x coordinates
            oImage[b + offsetb][a + offseta] = iImage[b][a]

    colorCorrection = 0
    rotations = 1
    rotationMatrix = np.array([[np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(-angle))],
                        [np.sin(np.deg2rad(angle)), np.cos(np.deg2rad(angle))]])

    for i in range(scaledSize):  # height of the image, y coordinates
        for j in range(scaledSize):  # width of the image, x coordinates
            # newEmptyIm must be the image we saved so that we can rotate THAT image
            imageMatrix = np.array([[j - scaledSize2], [i - scaledSize2]])
            # image2[i][j] = image1[i-scaledSize2][j-scaledSize2] #shifted
            rotatedPoint = matrixMult(rotationMatrix, imageMatrix)  # rotatedPoint logic to get matrix of new points
            r0 = int(rotatedPoint[0][0]) + scaledSize2
            r1 = int(rotatedPoint[1][0]) + scaledSize2
            r2 = rotatedPoint[0][0] + scaledSize2
            r3 = rotatedPoint[1][0] + scaledSize2

            blueValueInitial = oImage[i][j][0]
            greenValueInitial = oImage[i][j][1]
            redValueInitial = oImage[i][j][2]

            finalError = (r2 - r0 + r3 - r1) / scaledSize * rotations
            if (r0 >= scaledSize or r1 >= scaledSize) or (r0 < 0 or r1 < 0):
                continue
            rotatedImage[i][j] = oImage[r1][r0]  # finalPoint logic

            redValueFinal = rotatedImage[i][j][0]
            greenValueFinal = rotatedImage[i][j][1]
            blueValueFinal = rotatedImage[i][j][2]
            colorError = np.sqrt((redValueFinal - redValueInitial) ** 2 + (greenValueFinal - greenValueInitial) ** 2 + (
                    blueValueFinal - blueValueInitial) ** 2)
            colorCorrection += colorError
    colorCorrection/= (378 * 600)
    return rotatedImage, colorCorrection, finalError

def main():
    iImage = cv2.imread("fallen-angel.jpg")
    oImage = createEmptyImage(getSize(iImage, 1.5))

    degrees = int(input("Degrees to rotate by?"))
    rotations = int(input("How many rotations?"))

    for rotation in range(1, rotations + 1):
        angle = degrees * rotation
        (rotatedImage, colorCorrection, finalError) = rotate(iImage, oImage, angle)
        print(colorCorrection, "CC")
        print()
        print(finalError, "FE")
        #display image
        cv2.imshow("Copied image", rotatedImage / 255.0) #ensure image is /255 to display properly
        cv2.imwrite(f'{angle}.png', rotatedImage)
        cv2.waitKey(0) #pauses program until enter key is hit
        cv2.destroyAllWindows() #stops all programs imshow

main()