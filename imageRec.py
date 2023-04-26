import cv2
import numpy as np
from PySide6.QtCore import Signal, Slot, Qt, QThread

class PerspectiveTransform():
    def __init__(self, image, imageNum=0):
        super().__init__()
        self.image = image
        self.imageNum = imageNum
        self.refPt = []

    def run(self):
        self.perspective_transform(self.image.copy())

    def perspective_transform(self, image):
        cv2.namedWindow('image1')
        cv2.setMouseCallback('image1', self.find_point_image)

        # plots and shows reference points and image1 for perspective transform
        while True:
            cv2.imshow('image1', self.image)

            # allows for user to do the next perspective transform by pressing ESC
            if cv2.waitKey(20) & 0xFF == 27:
                print("exit")
                cv2.destroyAllWindows()
                # adds image from perspective transform to results
                new_image = self.four_point_transform(image, np.float32(self.refPt))

                # destroys the window when three images have been made for the photomosaic

                cv2.imwrite(f'Images\perspectiveImg{self.imageNum}.png', new_image)
                return 

    # does perspective transform on image
    def four_point_transform(self, image, pts):
        # obtain a consistent order of the points and unpack them
        # individually
        (tl, tr, br, bl) = pts

        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        # compute the perspective transform matrix and then apply it
        matrix = cv2.getPerspectiveTransform(pts, dst)
        warped = cv2.warpPerspective(image, matrix, (maxWidth, maxHeight))

        # return the warped image
        return warped
    
    def find_point_image(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            self.refPt.append([x, y])


def seagrass(image, image2):
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
