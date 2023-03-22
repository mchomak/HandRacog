import cv2
import os
import datetime
face_cascade_db = cv2.CascadeClassifier("haarcascades\\haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascades\\haarcascade_eye.xml")
cap = cv2.VideoCapture(0)

def obrabotka_picture(img,faces,img_gray):
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        img_gray_face = img_gray[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(img_gray_face, 1.1, 19)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img, (x+ex, y+ey), (x+ex + ew, y+ey + eh), (255, 0, 0), 2)
    return img

while True:
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    img=obrabotka_picture(img,faces,img_gray)


    cv2.imshow('face',img)
    cv2.waitKey(1)
