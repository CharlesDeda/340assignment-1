import cv2
import numpy as np
from matrixMult import matrixMult

def getScaledImageAndSize(image):
    # Image Dimensions
    numRows = image.shape[0]  # height of image
    numCols = image.shape[1]  # width of image

    # Scaling Factor to determine image size
    scalingFactor = 1.5

    # Image size scaled
    scaledSize = int(scalingFactor * max(numRows, numCols))

    # Center original image in new image by using offsets
    scaledImage = np.zeros((scaledSize, scaledSize, 3), np.float32)
    return scaledImage, scaledSize

def rotate(scaledImage, scaledSize, angle):
    numRows = iImage.shape[0]  # height of image
    numCols = iImage.shape[1]  # width of image

    #
    ###Create an empty image of scaledSize
    rotatedImage = np.zeros((scaledSize, scaledSize, 3), np.float32)
    scaledSize2 = scaledSize // 2

    offsetb = (scaledSize - numRows) // 2
    offseta = (scaledSize - numCols) // 2
    print("size: ", numRows, numCols)

    ### iterate through pixels and change colors
    for b in range(numRows):  # height of the image, y coordinates
        for a in range(numCols):  # width of the image, x coordinates
            scaledImage[b + offsetb][a + offseta] = iImage[b][a]
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

            blueValueInitial = scaledImage[i][j][0]
            greenValueInitial = scaledImage[i][j][1]
            redValueInitial = scaledImage[i][j][2]

            finalError = (r2 - r0 + r3 - r1) / scaledSize * rotations
            if (r0 >= scaledSize or r1 >= scaledSize) or (r0 < 0 or r1 < 0):
                continue
            rotatedImage[i][j] = scaledImage[r1][r0]  # finalPoint logic

            redValueFinal = rotatedImage[i][j][0]
            greenValueFinal = rotatedImage[i][j][1]
            blueValueFinal = rotatedImage[i][j][2]
            colorError = np.sqrt((redValueFinal - redValueInitial) ** 2 + (greenValueFinal - greenValueInitial) ** 2 + (
                    blueValueFinal - blueValueInitial) ** 2)
            colorCorrection += colorError

    return rotatedImage, colorCorrection, finalError


iImage = cv2.imread("fallen-angel.jpg")
output = getScaledImageAndSize(iImage)
(scaledImage, scaledSize) = output
(rotatedImage, colorCorrection, finalError) = rotate(scaledImage, scaledSize, 90)

#display image
cv2.imshow("Copied image", rotatedImage / 255.0) #ensure image is /255 to display properly
cv2.imwrite("savedimage.png", rotatedImage)
cv2.waitKey(0) #pauses program until enter key is hit
cv2.destroyAllWindows() #stops all programs imshow
