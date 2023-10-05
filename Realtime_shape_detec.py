import cv2
import numpy as np

framewidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameHeight)

def empty(a):
    pass


cv2.namedWindow("Parameters")

cv2.resizewindow("Parameters"1640, 240)
cv2. createTrackbar ("Threshold1","Parameters",23,255, empty)
c2.createTrackbar ("Threshold2","Parameters",20,255, empty)
cv2.createTrackbar ("Area","Parameters",5000, 30000, empty)

def stackImages (scale, imgArray.):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray [0], list)
    width = imeArrav[0][0].shape[1]
    height = imgArray [0][0]. shape[0]

    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0]. shape[:2]:
                    imgArray[x][y] = cv2.resize (imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x](y], (imgArray[0][0].shape [1], imgArray[0][0].shape [0]), None, scale, scale)
                if len(imgArray[×][y]. shape) == 2; imgArray [×][y]= cv2. cvtColor(imgArray[×][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), p.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray [x] = cv2.resize(imgArray [x], (0, 0), None, scale, scale)
            else:
                imgArray[×] = cv2.resize(imgArray [x], (imgArray [0].shape [1], imgArray [0].shape [0]), None, scale, scale) 
            if len(imgArray[x].shape) == 2; imgArray[×] = cv2.cvtcolor(imgArray [x], cv2.COLOR _GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
success, img = cap.read()

imgBlur = cv2.GaussianBlur (img, (7, 7), 1)
imgGray = cv2.cvtColor (imgBlur, cV2.COLOR_BGR2GRAY)

threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")
imgCanny = cv2. Canny (imgGray, threshold1, threshold2)
kernel = np.ones ((5, 5))
imgDil = cv2. dilate (imgCanny, kernel, iterations=1)

ingstack = stackImages (O.8 ([Iimg, imgGrav, imgCanny],
                              [imgDil,imgDil,imgDil]))

cv2. imshow ("Result", imgStack)
if cv2.waitkey (1) & 0xFF == ord('q'):
    break