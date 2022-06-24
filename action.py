import win32gui
import win32con
import win32api
import time
import random
from ctypes import windll


# Note: for some reason using WindowFromPoint works out fine
#       shouldn't need to change handle after initilization

# Uses position releative to the whole desktop
# Specify offset given by windowcapture
class Action:
    def __init__(self, offset_x, offset_y, x, y):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.handle = self.get_win_handle((x, y))

    def left_click(self, pos):
        client_pos = win32gui.ScreenToClient(self.handle, pos)
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp) 
        time.sleep((random.gauss(105, 32))/1000)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
    
    def right_click(self, pos, option = 0):
        # TODO implement left click after right click menu
        client_pos = win32gui.ScreenToClient(self.handle, pos)
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, tmp) 
        time.sleep((random.gauss(105, 32))/1000)
        win32api.SendMessage(self.handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON, tmp)

    def mouse_move(self, pos):
        client_pos = win32gui.ScreenToClient(self.handle, pos)
        tmp = win32api.MAKELONG(client_pos[0], client_pos[1])
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)
        time.sleep((random.gauss(105, 32))/1000)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)
            
    def keystroke(self, key):
        vk_key = self.char2key(key)
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_KEYDOWN, vk_key, 0)
        time.sleep((random.gauss(105, 32))/1000)
        win32api.SendMessage(self.handle, win32con.WM_KEYUP, vk_key, 0)

    def get_curpos(self):
        return win32gui.GetCursorPos()

    # does the job for now, better to keep a dictionary
    def char2key(self, c):
        result = windll.User32.VkKeyScanW(ord(str(c)))
        shift_state = (result & 0xFF00) >> 8
        vk_key = result & 0xFF

        return vk_key
    
    @staticmethod
    def get_win_handle(pos):
        handle = win32gui.WindowFromPoint(pos)
        # print the name of the handle
        print(win32gui.GetWindowText(handle))
        return win32gui.WindowFromPoint(pos)

'''
Usage:
    click = action(0, 0, 497, 1280)
    click.left_click((498, 1280))
    or
    click.keystroke('1')
'''

