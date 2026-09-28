import ctypes
import os
import subprocess


def set_background_image(img_path: str):
    """
    Sets the background image of the application.

    Args:
        imgPath (str): The path to the image file to be set as the background.
    """

    img_abs_path = os.path.abspath(img_path)
    if os.name == "nt":
        _set_windows_background_image(img_abs_path)
    else:
        _set_linux_background_image(img_abs_path)


def _set_windows_background_image(path_to_image):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path_to_image, 0)


def _set_linux_background_image(path_to_image):
    subprocess.call(["feh", "--bg-max", path_to_image])
