import HandTrackingModule as htm
import autopy
import cv2
import mediapipe as mp
import time
import keyboard
import os
import math

wCam, hCam = 1980,1080
frameR = 50  # уменьшение окна
smoothening = 7
mod = 'selection_mod'

header=cv2.imread('img_tub.jpg')
header_w=1920
header_h=250
header = cv2.resize(header, (header_w,header_h), interpolation = cv2.INTER_AREA)

# координаты кнопок
kolvo_button=5
one_button=header_w/kolvo_button
moving_button=[[0,0],[one_button,header_h]]
size_button=[[one_button,0],[one_button*2,header_h]]
turn_button=[[one_button*2,0],[one_button*3,header_h]]
paint_button=[[one_button*3,0],[one_button*4,header_h]]
save_button=[[one_button*4,0],[one_button*5,header_h]]

image=cv2.imread('cat.jpg')
wenth,haith=200,200
wenth2,haith2=wenth,haith
image = cv2.resize(image, (wenth,haith), interpolation = cv2.INTER_AREA)
image_point1=[0,0]
image_point2=[wenth,haith]
picx1, picy1=500,500
picx2,picy2=picx1+wenth,picy1+haith

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
number=0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

def find_twohand_distanse():
    global img,image,wenth,haith
    if len(lmList) != 0:
        fingers = detector.fingersUp(2)
        print(fingers)
        if fingers[1]!=[]:
            if fingers[0][1]==1 and fingers[1][1]:
                print('uvelichenie razmera')
                length, img, lineInfo = detector.findDistance(4, 8, img, 1)
                length=round(length)
                print(length)

def moving_mod(picx1,picx2,picy1,picy2):
    global wenth2,haith2,image
    if len(lmList) != 0:
        print('1')
        fingers = detector.fingersUp(1)
        if fingers[1]==1:
            print('2')
            x1, y1 = lmList[8][1:]
            # вычисляем координаты картинки
            if x1>frameR and y1>frameR:
                print('3')
                if x1<wCam - frameR and y1<hCam - frameR:
                    print('4')
                    if picx2-picx1==wenth2 and picy2-picy1==haith2:
                        print('5 :)')
                        picx1, picy1 = x1, y1
                        picx2, picy2 = x1 + wenth2, y1 + haith2

    return picx1,picx2,picy1,picy2

def size_mod(picx1,picx2,picy1,picy2):
    global img, mod,image,wenth2,haith2
    # делаем необходимые провреки
    if len(lmList) != 0:
        fingers = detector.fingersUp(1)
        if fingers[0] == 1 and fingers[1] == 1:
            length, img, lineInfo = detector.findDistance(4,8, img,1)
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (green), cv2.FILLED)
            uvelich=length/200
            buf_x=picx1+round(wenth*uvelich)
            buf_y=picy1 +round(haith*uvelich)
            if buf_x<=wCam and buf_y<=hCam:
                # расчитываем координаты
                wenth2=round(wenth*uvelich)
                haith2=round(haith*uvelich)
                print(wenth2,haith2)
                picx2=picx1+wenth2
                picy2 = picy1 + haith2
                print(picx1,picx2,picy1,picy2)
                # изменяем размер объекта
                image = cv2.resize(image, (wenth2, haith2), interpolation=cv2.INTER_AREA)

    return picx1,picx2,picy1,picy2

def turn_mod():
    global img,image,rotate
    if len(lmList) != 0:
        fingers = detector.fingersUp(1)

        if fingers[1]==1:
            (h, w, d) = image.shape
            print(h, w, d)
            center_x=int(wenth/2)
            center_y=int(haith/2)
            print(center_x,center_y)
            x2, y2 = lmList[8][1:]

            if x2-center_x!=0:
                angle_hend=(y2-center_y)/(x2-center_x)
                print(angle_hend)
                angle_hend=math.atan(angle_hend)
                print(angle_hend)
                angle_hend=math.degrees(angle_hend)
                angle_hend=round(angle_hend)
                print(angle_hend)
                M = cv2.getRotationMatrix2D((center_x,center_y), -1, 1.0)
                image = cv2.warpAffine(image, M, (wenth, haith))

def reset_mod():
    if len(lmList) != 0:
        fingers = detector.fingersUp(1)
        if fingers[1] == 1:
            print(":)")

def raschet_frame(number,image):
    global img,  first_point, second_point, tree_point, four_point, picx1, picx2, picy1, picy2, image_point1, image_point2, wenth2, haith2
    if number==1:
        line_lenth = second_point[1] - tree_point[1]
        otrezok = tree_point[0] - picx1
        picx1 = tree_point[0]
        image_point1[0] = image_point1[0] + otrezok
        image = image[image_point1[1]:image_point2[1], image_point1[0]:image_point2[0]]
        image_point2[0] = image_point2[0] - otrezok
        image_point1[0] = 0
        wenth2 = image_point2[0] - image_point1[0]
        haith2 = image_point2[1] - image_point1[1]

    elif number==2:
        line_lenth = second_point[0] - tree_point[0]
        otrezok = picy2-tree_point[1]
        picy2 = tree_point[1]
        image_point2[1] = image_point2[1] - otrezok
        image = image[image_point1[1]:image_point2[1], image_point1[0]:image_point2[0]]
        image_point2[1] = image_point2[1] - otrezok
        image_point2[1] = 0
        wenth2 = image_point2[0] - image_point1[0]
        haith2 = image_point2[1] - image_point1[1]

    return image

def frame_mod(image):
    global img,number,first_point, second_point,tree_point,four_point,picx1,picx2,picy1,picy2,image_point1,image_point2,wenth2,haith2
    if len(lmList) != 0:
        fingers = detector.fingersUp(1)
        if fingers[1] == 1:
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img, 1)
                cx, cy = lineInfo[4], lineInfo[5]
                if length<=60:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (green), cv2.FILLED)
                    if number==0:
                        first_point=[cx,cy]
                        number=number+1

                    elif number==1:
                        second_point=[cx,cy]
                        tree_point=[second_point[0],first_point[1]]
                        four_point=[first_point[0],second_point[1]]

            if number==1:
                if fingers[1] == 1 and fingers[2] == 0:
                    number = number + 1

        if first_point != [] and second_point != []:
            cv2.rectangle(img, first_point, second_point, (perple), 2)
            if fingers[1] == 1 and fingers[2] == 0:
                if (second_point[0]<picx1 and first_point[0]<picx1) or (second_point[1]<picy1 and first_point[1]<picy1):
                    pass
                else:
                    # проверяем какая точка пресекает
                    if first_point[0]<picx1:
                        # первая точка слева
                        if first_point[1]<picy1 or first_point[1]>picy2:
                            # первая точка сверху
                            if picx1<second_point[0]<picx2:
                                # вторая точка посередине
                                if second_point[1]>picy2 or second_point[1]<picy1:
                                    # вторая точка снизу
                                    image=raschet_frame(1,image)

                    elif picy1 < first_point[1] < picy2:
                        # первая точка посередине
                        if first_point[0]>picx2 or first_point[0]<picx1:
                            # первая точка справа
                            if second_point[1]>picy2:
                                # вторая точка снизу
                                if second_point[0]<picx1 or second_point[0]>picx2:
                                    # вторая точка слева
                                    image = raschet_frame(2, image)


                    # elif first_point[1]<picy1:
                    #
                    # elif first_point[1]>picy2:

    return image

def check_mod():
    global img, mod
    if mod!='frame':
        if len(lmList) != 0:
            fingers = detector.fingersUp(1)
            if fingers[1] == 1 and fingers[2]==1:
                length, img, lineInfo = detector.findDistance(8, 12, img, 1)
                if length <= 60:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (green), cv2.FILLED)
                    mod='selection_mod'

def selection_mod():
    global img,mod
    # проверяем руки
    if len(lmList) != 0:
        fingers = detector.fingersUp(1)
        if fingers[1]==1 and fingers[2]==1:
            length, img, lineInfo = detector.findDistance(8, 12, img, 1)
            cx,cy=lineInfo[4],lineInfo[5]
            if length <= 60:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (green), cv2.FILLED)
                # проверяем корды пальцев
                if cy>=0 and cy<=moving_button[1][1]:
                    if cx>=0 and cx<=header_w:
                        if cx>=moving_button[0][0] and cx<=moving_button[1][0]:
                            mod='moving'
                        elif cx>=size_button[0][0] and cx<=size_button[1][0]:
                            mod = 'size'
                        elif cx>=turn_button[0][0] and cx<=turn_button[1][0]:
                            mod = 'turn'
                        elif cx>=paint_button[0][0] and cx<=paint_button[1][0]:
                            mod = 'frame'
                        elif cx>=save_button[0][0] and cx<=save_button[1][0]:
                            mod = 'save'
                        else:
                            mod = 'selection_mod'
    return mod

def key_cheker():
    global mod
    if keyboard.is_pressed('1'):
        mod='moving'
    elif keyboard.is_pressed('2'):
        mod = 'size'
    elif keyboard.is_pressed('3'):
        mod = 'turn'
    elif keyboard.is_pressed('4'):
        mod = 'frame'
    elif keyboard.is_pressed('5'):
        mod = 'save'
    elif keyboard.is_pressed('9'):
        mod = 'selection_mod'
    elif keyboard.is_pressed('0'):
        reset_mod()
    return mod

def img_mod():
    global mod,picx1,picx2,picy1,picy2,number,first_point, second_point,image
    check_mod()
    mod=selection_mod()
    mod=key_cheker()
    if mod!='selection_mod':
        # рисуем облать действия
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (perple), 2)
    if mod=='moving':
        print('moving')
        picx1,picx2,picy1,picy2=moving_mod(picx1,picx2,picy1,picy2)
        print(picx1,picx2,picy1,picy2)
    elif mod=='size':
        print('size')
        picx1,picx2,picy1,picy2=size_mod(picx1,picx2,picy1,picy2)
    elif mod=='turn':
        print('turn')
        turn_mod()
    elif mod=='frame':
        print('frame')
        image=frame_mod(image)
    elif mod=='save':
        print('save')
    elif mod=='selection_mod':
        number=0
        first_point,second_point=[],[]
    else:
        pass

    img[0:header_h, 0:header_w] = header


def window_painter():
    global pTime,lmList,bbox,img,image
    # 1. ищем ключевые точки
    success, img = cap.read()
    img,lmList, bbox= detector.findHands(img)
    img_mod()
    #  фпс
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 900), cv2.FONT_HERSHEY_PLAIN, 3,
                (red), 3)
    cv2.putText(img, mod, (20, 950), cv2.FONT_HERSHEY_PLAIN, 3,
                (red), 3)
    # 12. отрисовка картинки
    # try:
    img[picy1:picy2, picx1:picx2] = image
    # except ValueError:
    #     pass

    try:
        cv2.imshow("Image", img)
    except ValueError:
        pass
    cv2.waitKey(1)

def main():
    while True:
        window_painter()

main()