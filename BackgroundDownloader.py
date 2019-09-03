# Download a background picture from https://www.apod.nasa.gov

from ImageDownloader.ApodDownloader import ApodDownloader
from RecentImageFile import RecentImageFile
import os
import subprocess

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
    subprocess.call(['feh', '--bg-max', pathToImage])
    print('Set background image.')
else:
    print('Could not find image to set as backgound.')
