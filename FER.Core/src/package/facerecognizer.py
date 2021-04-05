#!/usr/bin/env python3
import pyautogui 
import cv2 
import numpy as np
import os
from deepface import DeepFace
import matplotlib.pyplot as plt
import json
from package.imageObject import imageObject
from package.imageObject import faceObject

def GetElapsedTimeFromImgName(filename) :
    tokens = filename.split('_')
    if (len(tokens) != 2) :
        return 'N/A'

    return tokens[1]

def AnalyzeImage(imageDirectory) :
    listOp = []
    print ("Process images files")
    index = 0
    for dirname in os.listdir(imageDirectory):
        dirpath = os.path.join(imageDirectory, dirname)
        if os.path.isdir(dirpath):
            imgfile = os.path.join(dirpath, 'faces.jpg')
            if (os.path.isfile(imgfile)) :
                print("Processing : ---------------" + imgfile + "---------------------")
                imgObj = imageObject(imgfile)
                faces = imgObj.getFaces()
                imgNames = ''
                expressions = ''

                # TODO : check why face detection is failing
                if len(faces) == 0 :
                    print ("ERROR : Face detection failed for ",imgfile)
                    expressions = expressions + ',' + "NA"
                    imgNames = imgNames + ',' + "NA"

                for face in faces :
                    face.saveAsImage(dirpath)
                    imgNames = imgNames + ',' + face.getName()
                    expressions = expressions + ',' + face.getExpression()

                elapsedTimeInSecs = GetElapsedTimeFromImgName(dirname)
                result = (imgNames, elapsedTimeInSecs, expressions)
                listOp.append(result)
                index = index+1
        else:
            continue
    return listOp

def WriteToOutputFile(listOp, outputFile) :
    # listOp is expected to have tuple items  like [imagename, timestamp, expression]
    data = {}
    data['Results'] = []

    for item in listOp :
        data['Results'].append({
            'ImgName': item[0],
            'TimeInSecs':item[1],
            'Expression': item[2],
            })

    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, indent = 2)