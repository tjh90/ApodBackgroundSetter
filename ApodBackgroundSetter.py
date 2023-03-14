# Download a background picture from https://www.apod.nasa.gov

from ImageDownloader.ApodDownloader import ApodDownloader
from ImageSetter.LinuxImageSetter import LinuxImageSetter
from ImageSetter.WindowsImageSetter import WindowsImageSetter
from RecentImageFile import RecentImageFile
import os

apod = ApodDownloader()
try:
    apod.downloadPage()
    apod.downloadImageFromPage()
    pathToImage = os.getcwd() + os.sep + apod.getFilename()
except:
    recentImageFile = RecentImageFile(os.getcwd(), 'img')
    pathToImage = recentImageFile.findMostRecentDownload()

# Set the image as the background
if pathToImage is not None:
    if 'nt' == os.name:
        imgSetter = WindowsImageSetter()
    else:
        imgSetter = LinuxImageSetter()

    imgSetter.setImageAsBackground(pathToImage)

    print('Set background image.')
else:
    print('Could not find image to set as backgound.')
