#!/usr/bin/env python3
import os,sys

class FerSettings :
    def __init__(self) :
        self.videoCaptureIntervalInSecs = 1
        self.frameCaptureThrottleLimit = 10000

    def VideoCaptureIntervalInSecs(self) :
        return self.videoCaptureIntervalInSecs

    def FrameCaptureThrottleLimitPerVideo(self) :
        return self.frameCaptureThrottleLimit