import cv2 as cv
import numpy as np

image = cv.imread("imgs/img1.png")
image2 = cv.imread("imgs/img2.png")

width = 8
height = 8
resize = (width, height)

lowerGreen = np.array([0, 100, 0])
upperGreen = np.array([100, 255, 100])

greenMask = cv.inRange(image, lowerGreen, upperGreen)
greenMask2 = cv.inRange(image2, lowerGreen, upperGreen)

greenMaskFinal = cv.resize(greenMask, resize)
greenMaskFinal2 = cv.resize(greenMask2, resize)

greenMaskFinal = greenMaskFinal.astype(np.int32)
greenMaskFinal2 = greenMaskFinal2.astype(np.int32)

difference = greenMaskFinal2 - greenMaskFinal

newAlive = 0
newDead = 0

for i in range(len(difference)):
    for j in range(len(difference[i])):
        if difference[i][j] == 255:
            newAlive += 1
        elif difference[i][j] == -255:
            newDead += 1

theRealFinal1 = np.array([["" for i in range(8)] for j in range(8)])
theRealFinal2 = np.array([["" for i in range(8)] for j in range(8)])

for i in range(len(greenMaskFinal)):
    for j in range(len(greenMaskFinal[i])):
        if greenMaskFinal[i][j] == 255:
            theRealFinal1[i][j] = "A"
        elif greenMaskFinal[i][j] == 0:
            theRealFinal1[i][j] = "D"

for i in range(len(greenMaskFinal2)):
    for j in range(len(greenMaskFinal2[i])):
        if greenMaskFinal2[i][j] == 255:
            theRealFinal2[i][j] = "A"
        elif greenMaskFinal2[i][j] == 0:
            theRealFinal2[i][j] = "D"


print(str(newAlive) + " corals went dead to alive")
print(str(newDead) + " corals went from alive to dead")

cv.imshow('Mask', greenMask)
cv.waitKey(0)
cv.imshow('Mask2', greenMask2)
cv.waitKey(0)
