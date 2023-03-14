# Image setting implementation for linux.

from ImageSetter.ImageSetter import ImageSetter

import subprocess

class LinuxImageSetter(ImageSetter):

    def __init__(self):
        ImageSetter.__init__(self)

    def setImageAsBackground(self, pathToImage):
        subprocess.call(['feh', '--bg-max', pathToImage])
