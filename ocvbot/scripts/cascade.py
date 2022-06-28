import argparse
import cv2 as cv
import os
from time import time
from ocvbot.botlib.windowcapture import WindowCapture

def run(args):
    wc = WindowCapture("")

    while(True):
        capture = wc.get_screenshot()[1]    
        
        cv.imshow('output', capture)

        loop_time = time()

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

