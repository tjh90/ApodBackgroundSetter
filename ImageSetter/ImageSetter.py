# Abstract image setter.

class ImageSetter:

    methodErrMsg = 'Abstract method not overridden.'

    def __init__(self):
        pass

    # Download the page containing the image
    def setImageAsBackground(self, pathToImage):
        raise NotImplementedError(ImageDownloader.methodErrMsg)
