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

def AnalyzeImage(imageDirectory, outputDirPath) :
    listOp = []
    print ("Process images files")
    fgenerateHelperImage = True
    for dirname in os.listdir(imageDirectory):
        dirpath = os.path.join(imageDirectory, dirname)
        if os.path.isdir(dirpath):
            imgfile = os.path.join(dirpath, 'faces.jpg')
            if (os.path.isfile(imgfile)) :
                print("Processing : ---------------" + imgfile + "---------------------")
                imgObj = imageObject(imgfile)
                if (fgenerateHelperImage) :
                    imgObj.generateFaceHelperImage(outputDirPath)
                    fgenerateHelperImage = False
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
        else:
            continue
    return listOp

def WriteToOutputFile(listOp, outputFile) :
    # listOp is expected to have tuple items  like [imagename, timestamp, expression]
    data = {}
    data['Results'] = []

    for item in listOp :
        imgnamelist = item[0].split(',')
        exprlist = item[2].split(',')
        assert(len(imgnamelist) == len(exprlist))
        merged_list = [(imgnamelist[i], exprlist[i]) for i in range(0, len(imgnamelist))]
        expr = []
        for elem in merged_list :
            if elem[0] == '' or elem[1] == '':
                continue
            expr.append({
                'ImgName': elem[0],
                'Expression':elem[1]
            })

        data['Results'].append({
            'TimeInSecs':item[1],
            'Expressions': expr,
            })

    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, indent = 2)