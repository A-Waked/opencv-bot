import cv2 as cv
import numpy as np
from windowcapture import WindowCapture
from action import Action
from vision import Vision
from hsvfilter import HSVFilter

# points = findClickPositions('needle2.png', 'haystack2.png' ,debug_mode='points')
# print(points)

wc = WindowCapture("", 0)
vision = Vision('needle2.1.jpg')
vision.init_control_gui()
hsv_filter = HSVFilter(hMin=32, sMin=204, vMin=204, hMax=54, sMax=255, vMax=255, sAdd=153, sSub=204, vAdd=5, vSub=153)

while(True):
    capture = wc.get_screenshot()    
    rect = capture[0]
    processed_image = vision.apply_hsv_filter(capture[1], hsv_filter)
    rectangles = vision.find(processed_image, threshold=0.09)
    output_image = vision.draw_points(capture[1], vision.get_click_points(rectangles))
    # output_image = vision.draw_rectangles(capture[1], rectangles)

    cv.imshow('output', output_image)
    # cv.imshow('input', processed_image)
    # print(points)
    # cv.imshow('Computer Vision', capture[1])

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break