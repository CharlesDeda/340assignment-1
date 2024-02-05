#Charles Deda
#CSC-340
#1/12/24
from matrixMult import matrixMult
#from rotationFunc import rotationFunc
import cv2
import numpy
import numpy as np



def main():
    image = cv2.imread("fallen-angel.jpg")
    (imageWithBlackBorders, scaledSize) = applyBlackBorders(image, 1.5)
    rotatedImage = imageWithBlackBorders

    for rotation in range(1,3):
        rotatedImage = rotatedImage(imageWithBlackBorders, 45, 3, scaledSize)
        cv2.imwrite("finalImage.png", rotatedImage)

    cv2.imshow("Copied image", rotatedImage / 255.0)  # ensure image is /255 to display properly
    return




# #read in image from opencv
#
#     ###get size of an image
#     size1 = 378
#     size2 = 600
    #
def applyBlackBorders(image, scalingFactor):
    numRows = image.shape[0] #height of image
    numCols = image.shape[1] #width of image
    #Scaling Factor to determine image size
    #Max Dimensions
    maxDim = max(numRows, numCols)
    #Image size scaled
    scaledSize = int(scalingFactor * maxDim)
    #Center original image in new image by using offsets
    offsetb = (scaledSize - numRows) // 2
    offseta = (scaledSize - numCols) // 2
    print("size: ", numRows, numCols)
    #
    ###Create an empty image of scaledSize
    emptyIm = np.zeros( (scaledSize, scaledSize, 3), np.float32)
    image2 = np.zeros( (scaledSize, scaledSize, 3), np.float32)


    ### iterate through pixels and change colors
    for b in range(numRows): # height of the image, y coordinates
       for a in range(numCols): # width of the image, x coordinates
           emptyIm[b + offsetb][a + offseta] = image[b][a]
    return emptyIm, scaledSize

#image2 = rotationFunc(cv2.imread("fallen-angel.jpg"), 45, 2)
def rotateImage(image, angle, rotations, scaledSize):
    scaledSize2 = scaledSize // 2
    rotationMatrix = np.array([[np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(-angle))], [np.sin(np.deg2rad(angle)), np.cos(np.deg2rad(angle))]])
    sum = 0
    #iterate through pixels and change colors
    #for rotation in range(0, rotations):
    for i in range(scaledSize): # height of the image, y coordinates
        for j in range(scaledSize): # width of the image, x coordinates
            #newEmptyIm must be the image we saved so that we can rotate THAT image
            imageMatrix = np.array([[j-scaledSize2],[i-scaledSize2]])
            #image2[i][j] = image1[i-scaledSize2][j-scaledSize2] #shifted
            rotatedPoint = matrixMult(rotationMatrix, imageMatrix) #rotatedPoint logic to get matrix of new points
            r0 = int(rotatedPoint[0][0])+scaledSize2
            r1= int(rotatedPoint[1][0])+scaledSize2
            r2 = rotatedPoint[0][0]+scaledSize2
            r3 = rotatedPoint[1][0]+scaledSize2

            blueValueInitial = image[i][j][0]
            greenValueInitial = image[i][j][1]
            redValueInitial = image[i][j][2]

            finalError = (r2-r0 + r3-r1) / scaledSize * rotations
            if (r0 >= scaledSize or r1 >= scaledSize) or (r0 < 0 or r1 < 0):
                 continue
            image2[i][j] = image[r1][r0] #finalPoint logic

            redValueFinal = image2[i][j][0]
            greenValueFinal = image2[i][j][1]
            blueValueFinal = image2[i][j][2]
            colorError = np.sqrt((redValueFinal - redValueInitial) ** 2 + (greenValueFinal - greenValueInitial) ** 2 + (
                    blueValueFinal - blueValueInitial) ** 2)
            sum+= colorError
            image[i][j] = image2[i][j]

    return image2
    # print(finalError)
    # print(scaledSize*rotations)
    # print(sum/(378*600))

#display image
# cv2.imshow("Copied image", image2/255.0) #ensure image is /255 to display properly
# cv2.imwrite("savedimage.png", image2)
# cv2.waitKey(0) #pauses program until enter key is hit
# cv2.destroyAllWindows() #stops all programs imshow

main()