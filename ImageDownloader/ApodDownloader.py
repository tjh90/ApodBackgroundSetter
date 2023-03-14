# Download image from Astronomy Picture of the Day website.

from ImageDownloader.ImageDownloader import ImageDownloader
from bs4 import BeautifulSoup
import requests

class ApodDownloader(ImageDownloader):

    def __init__(self):
        ImageDownloader.__init__(self)
        self.__baseUrl = 'https://apod.nasa.gov/apod/'
        self.__homeUrl = self.__baseUrl + 'astropix.html'

    def downloadPage(self):
        resp = requests.get(self.__homeUrl)
        if 200 == resp.status_code:
            self.setHtml(resp.text)

    def downloadImageFromPage(self):
        if self.getHtml() == None:
            raise RuntimeError('Page has not been downloaded.')

        # Get the image URL by parsing the HTML
        htmlTree = BeautifulSoup(self.getHtml(), 'lxml')
        urlLeaf = htmlTree.find('img')['src']
        imageUrl = self.__baseUrl + urlLeaf

        # Save the image to disk
        extension = '.' + imageUrl.split('.')[-1]
        self.setFilename('img' + extension)
        with open(self.getFilename(), 'wb') as file:
            imgData = requests.get(imageUrl).content
            file.write(imgData)
