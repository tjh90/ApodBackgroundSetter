import os
import unittest
from unittest.mock import Mock, patch

import BackgroundSetter

# SPI_SETDESKWALLPAPER, the Win32 SystemParametersInfo action that repaints the wallpaper.
_SPI_SETDESKWALLPAPER = 20

class _FakeWindll:
    '''Stand-in for ctypes.windll so the Windows branch is testable off Windows.'''

    def __init__(self):
        self.user32 = Mock()
        self.user32.SystemParametersInfoW.return_value = 1


class SetBackgroundImageDispatchTest(unittest.TestCase):

    def test_dispatches_to_windows_on_nt(self):
        with patch.object(BackgroundSetter.os, 'name', 'nt'), \
                patch.object(BackgroundSetter, '_set_windows_background_image') as windows, \
                patch.object(BackgroundSetter, '_set_linux_background_image') as linux:
            BackgroundSetter.set_background_image('img.jpg')

        windows.assert_called_once()
        linux.assert_not_called()

    def test_dispatches_to_linux_on_posix(self):
        with patch.object(BackgroundSetter.os, 'name', 'posix'), \
                patch.object(BackgroundSetter, '_set_windows_background_image') as windows, \
                patch.object(BackgroundSetter, '_set_linux_background_image') as linux:
            BackgroundSetter.set_background_image('img.jpg')

        linux.assert_called_once()
        windows.assert_not_called()

    def test_dispatches_to_linux_on_non_nt_names(self):
        for name in ('posix', 'java'):
            with self.subTest(os_name=name), \
                    patch.object(BackgroundSetter.os, 'name', name), \
                    patch.object(BackgroundSetter, '_set_linux_background_image') as linux:
                BackgroundSetter.set_background_image('img.jpg')

                linux.assert_called_once_with(os.path.abspath('img.jpg'))

if __name__ == '__main__':
    unittest.main()
