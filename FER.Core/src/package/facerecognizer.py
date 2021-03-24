import pyautogui 
import cv2 
import numpy as np
import os
from deepface import DeepFace
import matplotlib.pyplot as plt
import json

def AnalyzeImage(imageDirectory) :

    listOp = []
    for filename in os.listdir(imageDirectory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            imgfile = os.path.join(imageDirectory, filename)
            if (os.path.isfile(imgfile)) :
                print("Processing : ---------------" + imgfile + "---------------------")
                img = cv2.imread(imgfile)
                plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                predictions = DeepFace.analyze(img)
                result = (filename, predictions['dominant_emotion'])
                listOp.append(result)
        else:
            continue
    return listOp

def WriteToOutputFile(listOp, outputFile) :
    # listOp is expected to have tuple items  like [imagename, expression]
    data = {}
    data['Results'] = []
    # NOTE : if file already exists it will be overriden
    # if (os.path.exists(filename)) :
    #     with open(filename) as json_file:
    #         data = json.load(json_file)

    for item in listOp :
        data['Results'].append({
            'ImgName': item[0],
            'Expression': item[1],
            })

    with open(outputFile, 'w') as outfile:
        json.dump(data, outfile, indent = 2)