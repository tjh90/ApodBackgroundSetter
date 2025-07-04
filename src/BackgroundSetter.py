import ctypes
import os
import subprocess

def SetBackgroundImage(imgPath: str):
    """
    Sets the background image of the application.

    Args:
        imgPath (str): The path to the image file to be set as the background.
    """

    imgAbsPath = os.path.abspath(imgPath)
    if os.name == 'nt':
        _SetWindowsBackgroundImage(imgAbsPath)
    else:
        _SetLinuxBackgroundImage(imgAbsPath)

def _SetWindowsBackgroundImage(pathToImage):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pathToImage , 0)

def _SetLinuxBackgroundImage(pathToImage):
    subprocess.call(['feh', '--bg-max', pathToImage])
