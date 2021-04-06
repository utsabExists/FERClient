#!/usr/bin/env python3
import os, sys
import cv2
from deepface import DeepFace

class imageObject :
    def __init__(self, imagepath) :
        self.imagepath = imagepath

    def getFaces(self) :
        image = cv2.imread(self.imagepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

        print("[INFO] Found {0} Faces!".format(len(faces)))
        #return faces, image
        faceObjectList = []
        index = 1
        for (x, y, w, h) in faces :
            name = 'face' + str(index)
            facImg = image[y:y+h, x:x+w]
            fobj = faceObject(facImg, name)
            faceObjectList.append(fobj)
            index = index + 1

        return faceObjectList

    def generateFaceHelperImage(self, dirpath) :
        image = cv2.imread(self.imagepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SIMPLEX

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))

        if (len(faces) == 0) :
            return False

        index = 1
        for (x, y, w, h) in faces :
            facename = 'face' + str(index)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, facename, (x + 8, y + 28), font, 1,(255,255,255),2)
            index = index + 1
            
        imgpath = os.path.join(dirpath, 'face_helper.jpg')
        status = cv2.imwrite(imgpath, image)
        if (not status) :
            print ("Failed to generate helper image.")
            return False
        
        return True

class faceObject :
    def __init__(self, faceimg, name) :
        self.name = name
        self.faceImg = faceimg

    def getName(self) :
        return self.name

    def saveAsImage(self, dirpath) :
        if (not os.path.isdir(dirpath)) :
            os.mkdir(dirpath)

        imgname = self.name + '.jpg'
        imgpath = os.path.join(dirpath, imgname)
        status = cv2.imwrite(imgpath, self.faceImg)
        if (not status) :
            print ("ERROR : Failed to write image")

    def getExpression(self) :
        try :
            predictions = DeepFace.analyze(self.faceImg, enforce_detection = False)
            return predictions['dominant_emotion']
        except :
            return "N/A"

# imagepath = "C:\\github\\FERClient\\data\\sample3_output\\images\\frame_40.jpg"
# imgObj = imageObject(imagepath)
# faceObjectList = imgObj.getFaces()
# for faceObject in faceObjectList:
#     faceObject.saveAsImage("C:\\github\\FERClient\\data\\sample3_output\\images\\detect\\")
#     print (faceObject.getExpression())
#     #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     #cropImg = img[y:y+h, x:x+w]
#     #status = cv2.imwrite('faces_detected.jpg', cropImg)
#     #print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
#     #print (type(img))