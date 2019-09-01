# Download a background picture from https://www.apod.nasa.gov

from ImageDownloader.ApodDownloader import ApodDownloader
import os
import subprocess

apod = ApodDownloader()
apod.downloadPage()
apod.downloadImageFromPage()

# Set the image as the background
pathToImage = os.getcwd() + os.sep + apod.getFilename()
subprocess.call(['feh', '--bg-max', pathToImage])
