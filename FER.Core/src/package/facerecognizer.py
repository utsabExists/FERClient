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

def GetSortedDirectoryList(imgdir) :
    dirnames = []
    for dirname in os.listdir(imgdir):
        tokens = dirname.split('_')
        res = (dirname, int(tokens[1]))
        dirnames.append(res)

    dirnames.sort(key = lambda x: x[1])
    return dirnames

def AnalyzeImage(imageDirectory, outputDirPath) :
    listOp = []
    print ("Process images files")
    fHelperImageGenerated = False
    dirnames = GetSortedDirectoryList(imageDirectory)
    for dirnameTup in dirnames:
        dirname = dirnameTup[0]
        dirpath = os.path.join(imageDirectory, dirname)
        if os.path.isdir(dirpath):
            imgfile = os.path.join(dirpath, 'faces.jpg')
            if (os.path.isfile(imgfile)) :
                print("Processing : ---------------" + imgfile + "---------------------")
                imgObj = imageObject(imgfile)
                if (not fHelperImageGenerated) :
                    fHelperImageGenerated = imgObj.generateFaceHelperImage(outputDirPath)
                faces = imgObj.getFaces()
                imgNames = ''
                expressions = ''

                # TODO : check why face detection is failing
                if len(faces) == 0 :
                    print ("[WARNING] : No face detected in ",imgfile)
                    continue

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