import cv2

face_cascade_db = cv2.CascadeClassifier("haarcascades\\haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
number=0
filename=('D:/model_fotos/'+str(number)+'.png')

while True:
    success, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+224,y+224), (0,255,0), 2)
        img_gray_face = img_gray[y:y+h,x:x+w]
        image = img[y:y + 224, x:x + 224]

    isWritten=cv2.imwrite(('D:/model_fotos/'+str(number)+'.png'),image)
    if isWritten:
        print('seved',number)
    cv2.imshow('image', image)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    number=number+1