# FERClient SetUp
This repo hosts code for facial expression recognition

1.  pip install numpy
2.  pip install pyautogui
3.  pip install opencv-python
4.  pip install opencv-contrib-python
5.  pip install matplotlib
6.  pip install tensorflow - 
    Note: tensorflow is more stable with python version 3.8. 
    If you have higher version - try the following
    (python -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl)
        OR
    pip install pip install tf-nightly (unstable preview build but it works with all versions of python)

7. pip install deepface

Install visual studio code (preffered IDE)

# Usage 

1. Run the following command

    .\main.py "v=<path to video file>"

    Ex: .\main.py v="C:\github\FERClient\data\sample2.mp4"

    The above will generate a out put directory with name sample2_output in the same location as the video file. Inside that it will have a images directory containing all the frames of the video in .jpg format and an expression_output.json having facial expression of each of the frames.

    NOTE: imageCapturethrottleLimit is set to 4, so only first 4 frames from video will be processed.