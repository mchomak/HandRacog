import cv2
import mediapipe as mp
import time
import math
import numpy as np

green=(0,255,0)
perple=(255,0,255)
red=(255,0,0)
blue=(0,0,255)

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    # print(id, cx, cy)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
                xList,yList=[],[]
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),(0, 255, 0), 2)


        return img,self.lmList, bbox

    def fingersUp(self,hands):
        fingers,multi_fingers = [],[]
        fingers_1,fingers_2=[],[]
        # большой палец
        if hands==1:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # остальные пальцы
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers

        if hands==2:
            for hand in range(3):
                if hand==1:
                    if self.hand_1!=[]:
                        if self.hand_1[self.tipIds[0]][1] > self.hand_1[self.tipIds[0] - 1][1]:
                            fingers_1.append(1)
                        else:
                            fingers_1.append(0)
                        # остальные пальцы
                        for id in range(1, 5):
                            if self.hand_1[self.tipIds[id]][2] < self.hand_1[self.tipIds[id] - 2][2]:
                                fingers_1.append(1)
                            else:
                                fingers_1.append(0)

                if hand==2:
                    if self.hand_2 != []:
                        if self.hand_2[self.tipIds[0]][1] > self.hand_2[self.tipIds[0] - 1][1]:
                            fingers_2.append(1)
                        else:
                            fingers_2.append(0)
                        # остальные пальцы
                        for id in range(1, 5):
                            if self.hand_2[self.tipIds[id]][2] < self.hand_2[self.tipIds[id] - 2][2]:
                                fingers_2.append(1)
                            else:
                                fingers_2.append(0)

            multi_fingers.append(fingers_1)
            print(multi_fingers)
            print(fingers_1)
            multi_fingers.append(fingers_2)
            print(multi_fingers)
            print(fingers_2)
            return multi_fingers

    def findDistance(self, p1, p2, img, hands,draw=True,r=15, t=3):
        if hands==1:
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]

        if hands==2:
            x1, y1 = self.hand_1[p1][1:]
            x2, y2 = self.hand_2[p2][1:]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (perple), t)
            cv2.circle(img, (x1, y1), r, (perple), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (perple), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (blue), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]




