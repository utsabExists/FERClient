#!/usr/bin/env python3
import os,sys

class FerSettings :
    def __init__(self) :
        self.videoCaptureIntervalInSecs = 60
        self.frameCaptureThrottleLimit = 7

    def VideoCaptureIntervalInSecs(self) :
        return self.videoCaptureIntervalInSecs

    def FrameCaptureThrottleLimitPerVideo(self) :
        return self.frameCaptureThrottleLimit