# importing the required packages 
import pyautogui 
import cv2 
import numpy as np
import os
from deepface import DeepFace
import matplotlib.pyplot as plt

def CaptureFromVideo(videofile, outputDir) :
    imageCapturethrottleLimit = 4
    # Read the video from specified path 
    cam = cv2.VideoCapture(videofile) 
    
    try: 
        
        # creating a folder named data 
        if not os.path.exists(outputDir): 
            os.makedirs(outputDir) 
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data')
        return False
    
    # frame 
    currentframe = 0
    
    while(True): 
        
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret: 
            # if video is still left continue creating images
            name = 'frame' + str(currentframe) + '.jpg'
            filename = os.path.join(outputDir, name)
            print ('Creating...' + name) 
    
            # writing the extracted images 
            cv2.imwrite(filename, frame) 
    
            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else: 
            break

        if (imageCapturethrottleLimit == currentframe) :
            break
    
    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows()
    return True

#videofile = "C:\\github\\FERClient\\data\\sample2.mp4"
#CaptureFromVideo(videofile)

# directory = ".\gen-temp"
# listOp = []
# for filename in os.listdir(directory):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         imgfile = os.path.join(directory, filename)
#         if (os.path.isfile(imgfile)) :
#             print("Processing : ---------------" + imgfile + "---------------------")
#             img = cv2.imread(imgfile)
#             plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#             predictions = DeepFace.analyze(img)
#             listOp.append(predictions['dominant_emotion'])
#     else:
#         continue

# img = cv2.imread("./gen-temp/frame0.jpg")
# print('before showing image')
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# print('after showing image')
# predictions = DeepFace.analyze(img)
# print(predictions['dominant_emotion'])



