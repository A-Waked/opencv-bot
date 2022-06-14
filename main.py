import cv2 as cv
import numpy as np
import random

def findClickPositions(needle_img_path, haystack_img_path, threshold=0.07, debug_mode=None):

    haystack_img = cv.imread(haystack_img_path, cv.IMREAD_UNCHANGED)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)

    locations = np.where(result <= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    rectangles = []

    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weight = cv.groupRectangles(rectangles, 1, 0.20)
    # print(rectangles)

    points = []
    if len(rectangles):
        print('Found needle!')
        
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255,0,255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:
            x_rand = 0
            y_rand = 0

            #check if x_rand and y_rand are inside the rectangle. Generarte new random numbers if not
            if debug_mode != 'rectangles':
                while not (x_rand >= x and x_rand <= x + w and y_rand >= y and y_rand <= y + h):
                    x_rand = random.gauss(x + w / 2, w / 4)
                    y_rand = random.gauss(y + h / 2, h / 4)

                x_rand = int(x_rand)
                y_rand = int(y_rand)

            points.append((x_rand, y_rand))
            
            if debug_mode == 'rectangles':    
                top_left = (x, y)
                bottom_right = (x + w, y + h)

                cv.rectangle(haystack_img, top_left, bottom_right, line_color, 1)

            elif debug_mode == 'points':
                cv.drawMarker(haystack_img, (x_rand, y_rand), line_color, cv.MARKER_CROSS, markerSize=10, thickness=1)
            

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            cv.waitKey()

    return points

# points = findClickPositions('needle2.png', 'haystack2.png' ,debug_mode='points')
# print(points)

