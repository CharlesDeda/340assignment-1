#Charles Deda
#CSC-340
#1/12/24

import cv2
import numpy as np

#read in image from opencv
image = cv2.imread("cones1.png")
print("image loaded")
#display image (show takes 2 params)
#cv2.imshow("This is an image", image)
#cv2.waitKey(0) #pauses program until enter key is hit
#cv2.destroyAllWindows() #stops all programs imshow

#relative path example
###image  = cv2/imread("imgscones1_inFolder.png")

###get size of an image
size1 = 375
size2 = 500

numRows = image.shape[0] #height of image
numCols = image.shape[1] #width of image
#Scaling Factor to determine image size
scalingFactor = 1.3
#Max Dimensions
maxDim = max(numRows, numCols)
#Image size scaled
scaledSize = int(scalingFactor * maxDim)
#Center original image in new image by using offsets
offseti = (scaledSize - numRows) // 2
offsetj = (scaledSize - numCols) // 2
print("size: ", numRows, numCols)

###Create an empty image of scaledSize
emptyIm = np.zeros( (scaledSize, scaledSize, 3), np.float32)


# iterate through pixels and change colors
for i in range(numRows): # height of the image, y coordinates
    for j in range(numCols): # width of the image, x coordinates
        emptyIm[i + offseti][j + offsetj] = image[i][j]



#display image
cv2.imshow("Copied image", emptyIm/255.0) #ensure image is /255 to display properly
cv2.imwrite("savedimage.png", emptyIm)
cv2.waitKey(0) #pauses program until enter key is hit
cv2.destroyAllWindows() #stops all programs imshow
