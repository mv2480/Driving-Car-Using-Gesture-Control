import pyautogui as key
import cv2
import time
import numpy as np
import math


color = [[0,121,145,6,255,255]]
x = 2
def masking(colors, img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    point = []
    lower = np.array(colors[0][0:3])
    upper = np.array(colors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) ==2:
        cv2.drawContours(imgContour, contours[0], -1, (255, 0, 0), 3)
        peri = cv2.arcLength(contours[0], True)
        approx = cv2.approxPolyDP(contours[0], 0.02 * peri, True)
        objCor = len(approx)
        x1, y1, w1, h1 = cv2.boundingRect(approx)

        cv2.drawContours(imgContour, contours[1], -1, (255, 0, 0), 3)
        peri = cv2.arcLength(contours[1], True)
        approx = cv2.approxPolyDP(contours[1], 0.02 * peri, True)
        objCor = len(approx)
        x2, y2, w2, h2 = cv2.boundingRect(approx)
        cv2.line(imgContour,(int(x1+w1/2),int(y1+h1/2)),(int(x2+w2/2),int(y2+h2/2)),(255,0,0),2)
        angle = AngleBtw2Points((int(x1+w1/2),int(y1+h1/2)),(int(x2+w2/2),int(y2+h2/2)))
        a , b = midpoint((int(x1+w1/2),int(y1+h1/2)),(int(x2+w2/2),int(y2+h2/2)))
        distance = math.sqrt((((int(x1+w1/2) - int(x2+w2/2)) ** 2) + ((int(y1+h1/2) - int(y2+h2/2)) ** 2)))
        cv2.circle(imgContour,(int(a),int(b)),int(distance/2),(255,0,0),4)
        cv2.circle(imgContour, (int(a), int(b)), 10, (255, 0, 0), cv2.FILLED)
        if (angle < -15) and (angle > -120):
            cv2.putText(imgContour, 'Right', (420, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)
            key.keyDown('d')
            print('d')
        elif (angle > -165) and (angle < -120)  :
            cv2.putText(imgContour, 'Left', (150, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)
            key.keyDown('a')
            print('a')
        if ((angle > -15) and (angle < 0)) or ((angle > -180) and (angle < -165)):
            key.keyUp('d')
            print('a')
            print('d')
            key.keyUp('a')
        if distance > 320:
            if x == 0:
                cv2.putText(imgContour, 'Reverse', (250, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)
            else:
                cv2.putText(imgContour, 'Forward', (250, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)
            key.keyDown('w')
            print('w')
        elif distance < 150:
            cv2.putText(imgContour, 'Stop', (250, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 4)
            key.keyDown('s')
            print('s')
        if ((distance < 350 and distance > 150) or (distance < 350 and distance > 150)):
            key.keyUp('w')
            print('w')
            print('s')
            key.keyUp('s')


        print(angle)
        print(distance)



def midpoint(p1, p2):
    return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return math.degrees(math.atan2(changeInY,changeInX))

def gear(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    Gear = ['R','N','1st','2nd','3rd','4th']
    global x
    if len(contours) == 1:
        cv2.drawContours(imgContour, contours[0], -1, (255, 0, 0), 3)
        peri = cv2.arcLength(contours[0], True)
        approx = cv2.approxPolyDP(contours[0], 0.02 * peri, True)
        objCor = len(approx)
        x1, y1, w1, h1 = cv2.boundingRect(approx)
        cv2.putText(imgContour,'Gear-',(310,80),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,0),4)
        cv2.putText(imgContour, Gear[x], (520, 80), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 4)
        cv2.circle(imgContour,(int(x1+w1/2),int(y1)),10,(255,0,0),cv2.FILLED)
        if (int(x1+w1/2)>475 and int(y1)>325) and (int(x1+w1/2)<575 and int(y1)<425) :
            if x > 0 :
                x = x - 1
            key.keyDown("down")
            time.sleep(1)
            key.keyUp("down");
            cv2.rectangle(imgContour, (490, 340), (560, 410), (255, 0, 0), cv2.FILLED)
        else:
            cv2.rectangle(imgContour,(475,325),(575,425),(255,0,0),cv2.FILLED)
        if (int(x1+w1/2)>475 and int(y1)>175) and (int(x1+w1/2)<575 and int(y1)<275) :
            cv2.rectangle(imgContour, (490, 190), (560, 260), (255, 0, 0), cv2.FILLED)
            if x<5:
                x = x + 1
            key.keyDown("up")
            time.sleep(1)
            key.keyUp("up");
        else:
            cv2.rectangle(imgContour, (475, 175), (575, 275), (255, 0, 0), cv2.FILLED)



cap =cv2.VideoCapture(0)

while True:
    success , img = cap.read()
    imgContour = img.copy()
    mask = masking(color,img)
    getContours(mask)
    gear(mask)
    cv2.imshow("mask",mask)
    cv2.imshow("contour", imgContour)
    ky = cv2.waitKey(1)
    if ky == ord('q'):
        break
