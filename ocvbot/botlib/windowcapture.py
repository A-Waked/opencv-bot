import cv2 as cv
import numpy as np
import os
import win32gui
import win32ui
import win32con
import win32api


'''
Class used for window capture.
Two method can be used for window capture. 
1. Window capture with window name.
2. Window capturing the whole screen
    - This currently only supports the main monitor screen
    - Can be used when pairing with an external tool that shows the game state to avoid capturing from
      two different windows
'''
class WindowCapture:
    def __init__(self, window_name, monitor = 0):
        if window_name:
            # grab the handle for the window from the name
            self.hwnd = win32gui.FindWindow(None, window_name)

            if not self.hwnd:
                raise Exception("Window not found")
        else:
            # get the handle for the desktop
            # TODO make this work for specified monitor
            self.hwnd = win32gui.GetDesktopWindow()

        self.monitor = monitor

    def get_screenshot(self) -> np.ndarray:
        # capture the whole window
        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        width = right - left
        height = bottom - top
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        bmpinfo = saveBitMap.GetInfo()
        bmpdata = saveBitMap.GetBitmapBits(True)
        im = np.frombuffer(bmpdata, dtype='uint8')
        im = im.reshape(bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)

        # get window position on desktop to offset clicks later
        rect = win32gui.GetWindowRect(self.hwnd)

        # remove the alpha channel
        im = im[:, :, :3]
        im = np.ascontiguousarray(im)
        # convert to cv_bgr
        # im = cv.cvtColor(im, cv.COLOR_BGRA2BGR)

        # clean up
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

        # return the image and the window position
        return rect,im


# wc = WindowCapture(None, 1)

# while(True):
#     capture = wc.get_screenshot()    
#     rect = capture[0]
#     cv.imshow('Computer Vision', capture[1])

#     if cv.waitKey(1) == ord('q'):
#         cv.destroyAllWindows()
#         break

    