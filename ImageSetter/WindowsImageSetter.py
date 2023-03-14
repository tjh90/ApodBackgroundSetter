# Image setting implementation for windows.

from ImageSetter.ImageSetter import ImageSetter

import ctypes

class WindowsImageSetter(ImageSetter):

    def __init__(self):
        ImageSetter.__init__(self)

    def setImageAsBackground(self, pathToImage):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, pathToImage , 0)
