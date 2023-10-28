import cv2
import numpy as np

framewidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameHeight)

cammidw = int (framewidth/2)
cammidh = int (frameHeight/2)

def empty(a):
    pass


cv2.namedWindow("Parameters")

cv2.resizeWindow("Parameters",1640, 240)
cv2. createTrackbar ("Threshold1","Parameters",23,255, empty)
cv2.createTrackbar ("Threshold2","Parameters",20,255, empty)
cv2.createTrackbar ("Area","Parameters",5000, 30000, empty)

def stackImages (scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray [0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray [0][0]. shape[0]

    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0]. shape[:2]:
                    imgArray[x][y] = cv2.resize (imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape [1], imgArray[0][0].shape [0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2. cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
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
                imgArray[x] = cv2.resize(imgArray [x], (imgArray [0].shape [1], imgArray [0].shape [0]), None, scale, scale) 
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtcolor(imgArray [x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour,imgDist):
    _,contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area> areaMin:
            cv2.drawContours (imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            x , y , w, h = cv2.boundingRect (approx)
            midh = int ((h/2)+y)
            midw = int ((w/2)+x)
            
            offsetx = (cammidw-midw)
            offsety = (cammidh-midh)

            cv2.rectangle(imgContour, (x ,y ), (x +w, y + h ) , (0, 255, 0), 5)
            cv2.circle(imgContour, (midw , midh ), 5 , (0, 255, 0), -1)
            cv2.circle(imgContour, (cammidw , cammidh ), 10 , (255, 255, 0), 6)


            cv2.putText (imgContour, "Points: " + str (len (approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
              (0, 255, 0), 2)
            cv2.putText (imgContour, "Area: " + str(int (area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            (0, 255, 0),2)
            

            cv2.rectangle(imgDist, (x ,y ), (x +w, y + h ) , (0, 255, 0), 5)
            cv2.circle(imgDist, (midw , midh ), 5 , (255, 255, 0), -1)
            cv2.circle(imgDist, (cammidw , cammidh ), 10 , (255, 255, 0), 6)
            
            cv2.arrowedLine(imgDist, (cammidw+150 ,cammidh+150 ), (midw+150, midh+150 ) , (0, 255, 0), 5)
            
            cv2.putText (imgDist, "X Axis Offset: " + str(int (offsetx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            (0, 255, 0),2)
            cv2.putText (imgDist, "Y Axis Offset: " + str(int (offsety)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
            (0, 255, 0),2)


while True:
    
    success,img = cap.read()
    img = cv2.flip(img,0)
    
    imgContour= img.copy() 
    imgDist= img.copy() 

    imgBlur = cv2.GaussianBlur (img, (7, 7), 1)
    imgGray = cv2.cvtColor (imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")
    imgCanny = cv2. Canny (imgGray, threshold1, threshold2)
    kernel = np.ones ((5, 5))
    imgDil = cv2. dilate (imgCanny, kernel, iterations=1)
    
    getContours(imgDil,imgContour,imgDist)

    imgStack = stackImages (0.8,([img, imgGray, imgCanny],
                                  [imgDil,imgContour,imgContour]))


    cv2. imshow ("Distance", imgDist)


    cv2. imshow ("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
