#!/usr/bin/env python3
import pyautogui 
import cv2 
import numpy as np
import os
from deepface import DeepFace
import matplotlib.pyplot as plt
from package.fersettings import FerSettings

# cv2 Camera Properties
# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)


def GetFrameRate(videoParam) :
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
    if int(major_ver)  < 3 :
        fps = videoParam.get(cv2.cv.CV_CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = videoParam.get(cv2.CAP_PROP_FPS)
        print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    return int(fps)

def CaptureFromVideo(videofile, outputDir, fersettings) :
    # Read the video from specified path 
    cam = cv2.VideoCapture(videofile) 
    fps = GetFrameRate(cam)
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
    currentSec = 0
    currCount = 0
    while(True): 
        
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret: 
            # if video is still left continue creating images
            currCount = currCount + 1
            name = 'frame_' + str(int(currentSec))
            imgdir = os.path.join(outputDir, name)
            if (not os.path.isdir(imgdir)) :
                os.mkdir(imgdir)

            filename = os.path.join(imgdir, 'faces.jpg')
            print ('Creating...' + name) 
    
            # writing the extracted images 
            cv2.imwrite(filename, frame) 
    
            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += (fps * fersettings.VideoCaptureIntervalInSecs())
            currentSec += fersettings.VideoCaptureIntervalInSecs()
            cam.set(1, currentframe)
        else: 
            break

        if (currCount == fersettings.FrameCaptureThrottleLimitPerVideo()) :
            break
    
    # Release all space and windows once done 
    cam.release()
    cv2.destroyAllWindows()
    return True



