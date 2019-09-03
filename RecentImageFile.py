# Find the most recently modified image file of a given name in a given directory.

import os

class RecentImageFile:

    validExtensions = ['.bmp', '.gif', '.jpeg', '.jpg', '.png']

    def __init__(self, dirPath, fileName):
        self.__dirPath = dirPath
        self.__fileName = fileName

    def findMostRecentDownload(self):
        imgFiles = list(filter(self.__filterFiles, os.listdir()))
        if len(imgFiles) == 0:
            # No images found.
            return None
        elif len(imgFiles) == 1:
            # Return the only image file found.
            return imgFiles[0]
        else:
            # Return the most recently modified image file.
            modTime = 0
            recentImg = None
            for imgFile in imgFiles:
                if os.stat(imgFile).st_mtime > modTime:
                    modTime = os.stat(imgFile).st_mtime
                    recentImg = imgFile

            return recentImg

    def __filterFiles(self, file):
        for ext in RecentImageFile.validExtensions:
            if self.__fileName + ext == file:
                return True
        return False