import HandTrackingModule as htm
import autopy
import cv2
import mediapipe as mp
import time
import math
import os
import numpy as np
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280,1080
frameR = 50  # уменьшение окна
smoothening = 7
mod = 'selection_mod'

green=(0,255,0)
perple=(255,0,255)
red=(255,0,0)
blue=(0,0,255)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime,cTime,bud_fps,new_volume = 0,0,0,0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()


def finger_mouser():
    global img,plocX,plocY
    # 2.получаем координаты указ и сред пальцев
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # 3. проверяем подняты ли пальцы
        fingers = detector.fingersUp(1)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(perple), 2)
        # 4. если указ поднят то двигаем мышью
        if fingers[1] == 1 :
            # 5. конвертируем координаты
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            # 6. сглаживание значений
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. двигаем мышью
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (perple), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8. если подянты оба пальца то наживаем мышью
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. растояние между паьцами
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. нажатие мышкой
            if length <= 60:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (green), cv2.FILLED)
                pyautogui.click(clicks=1)

def finger_volume():
    global img,new_volume
    if len(lmList) != 0:
        # 3. проверяем какие пальцы подняты
        fingers = detector.fingersUp(1)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(perple), 2)
        # 4. если больщой и указ подняты то меняем звук
        if fingers[1] == 1:
            # 5. считаем длину между пальцами
            length, img, lineInfo = detector.findDistance(4,8, img,1)
            new_volume=round((length-90)/3)
            if length<100:
                new_volume=0
            if new_volume<=0:
                new_volume=0
            elif new_volume>=100:
                new_volume=100
            print(length)
            # если мезинец опущен меняем громкость
            if fingers[4]==0:
                # 6. изменяем громкость
                print(new_volume)
                volume.SetMasterVolumeLevelScalar(new_volume/100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (green), cv2.FILLED)

    cv2.putText(img, str(int(new_volume)), (1180, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (red), 3)



def window_painter():
    global pTime,lmList,bbox,img
    # 1. ищем ключевые точки
    success, img = cap.read()
    img,lmList,bbox,hand_1,hand_2= detector.findHands(img)
    print('1: '+str(hand_1))
    print('2: ' + str(hand_2))
    #  фпс
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 950), cv2.FONT_HERSHEY_PLAIN, 3,
                (red), 3)
    cv2.putText(img, mod, (20, 900), cv2.FONT_HERSHEY_PLAIN, 3,
                (red), 3)

    # 12. отрисовка картинки
    cv2.imshow("Image", img)
    cv2.waitKey(1)

def main():
    while True:
        window_painter()

main()