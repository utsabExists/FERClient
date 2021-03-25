import os, sys
from package.fersettings import FerSettings

def GetVideoFilePathFromArgs(argvs) :
    videofilePath = ''
    for item in argvs :
        arg = item.split('=')
        if (len(arg) == 2 and arg[0] == 'v') :
            return True, arg[1]

    return False, ''

def GetOutputDirName(filepath) :
    rootpath = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    dirName = filename.rsplit( ".", 1 )[ 0 ] + "_output"
    dirPath = os.path.join(rootpath, dirName)
    return dirPath

res, videopath = GetVideoFilePathFromArgs(sys.argv)
outputDirPath = GetOutputDirName(videopath)
print(outputDirPath)

ferSettings = FerSettings()
from package.imgextractor import *
imageOutputDir = os.path.join(outputDirPath, "images")
ret = CaptureFromVideo(videopath, imageOutputDir, ferSettings)
if (not ret) :
    print("Image capture failed, skipping next steps")
    exit(0)

from package.facerecognizer import *
resultList = AnalyzeImage(imageOutputDir)
outputFilePath = os.path.join(outputDirPath, "expression_output.json")
WriteToOutputFile(resultList, outputFilePath)
