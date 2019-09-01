# Abstract image downloader class.

class ImageDownloader:

    methodErrMsg = 'Abstract method not overridden.'

    def __init__(self):
        self.__filename = None
        self.__html = None

    # Download the page containing the image
    def downloadPage(self):
        raise NotImplementedError(ImageDownloader.methodErrMsg)

    # Download the image from the page
    def downloadImageFromPage(self):
        raise NotImplementedError(ImageDownloader.methodErrMsg)

    def getFilename(self):
        return self.__filename

    def setFilename(self, filename):
        self.__filename = filename

    def getHtml(self):
        return self.__html

    def setHtml(self, html):
        self.__html = html
