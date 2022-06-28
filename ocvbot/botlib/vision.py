import cv2 as cv
import numpy as np
import random
from ocvbot.botlib.hsvfilter import HSVFilter

class Vision:
    TRACKBAR_WINDOW = "Trackbars"

    # properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    def __init__(self, needle_img_path = None, method = cv.TM_SQDIFF_NORMED):
        if needle_img_path is not None:
            self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)
            self.needle_w = self.needle_img.shape[1]
            self.needle_h = self.needle_img.shape[0]
            self.method = method
            # self.method = cv.TM_CCOEFF_NORMED

    def find(self, haystack_img, threshold=0.07, max_results=10):
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        locations = np.where(result <= threshold)
        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weight = cv.groupRectangles(rectangles, 1, 0.20)

        if len(rectangles) > max_results:
            rectangles = rectangles[:max_results]

        return rectangles

    def draw_rectangles(self, haystack_img, rectangles):
        if rectangles is None:
            return haystack_img
        else:
            line_color = (255, 0, 0)
            line_type = cv.LINE_4

            for (x, y, w, h) in rectangles:
                top_left = (x, y)
                bottom_right = (x + w, y + h)

                cv.rectangle(haystack_img, top_left, bottom_right, line_color, 1)

            return haystack_img
    
    def draw_points(self, haystack_img, points):
        if points is None:
            # print("No points")
            return haystack_img
        else:
            marker_color = (255,0,0)
            line_color = (255, 0, 0)
            marker_type = cv.MARKER_CROSS

            for (x, y) in points:
                cv.drawMarker(haystack_img, (x, y), line_color, cv.MARKER_CROSS, markerSize=10, thickness=1)

            return haystack_img

    def get_click_points(self, rectangles):
        points = []
        
        x_rand = 0
        y_rand = 0

        for (x, y, w, h) in rectangles:            
            #check if x_rand and y_rand are inside the rectangle. Generarte new random numbers if not
            while not (x_rand >= x and x_rand <= x + w and y_rand >= y and y_rand <= y + h):
                x_rand = random.gauss(x + w / 2, w / 4)
                y_rand = random.gauss(y + h / 2, h / 4)

            
            x_rand = int(x_rand)
            y_rand = int(y_rand)

            points.append((x_rand, y_rand))  


        return points
        
    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        def nothing(x):
            pass

        # cv scale for HSV - Hue (0 - 179) Saturation (0 - 255) Value (0 - 255)
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)

        # default values
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

        # button for resetting trackbars without using qt

    def set_trackbar_positions(self, hsv_filter):
        # update trackbar when applying existing filter
        cv.setTrackbarPos('HMin', self.TRACKBAR_WINDOW, hsv_filter.hMin)
        cv.setTrackbarPos('SMin', self.TRACKBAR_WINDOW, hsv_filter.sMin)
        cv.setTrackbarPos('VMin', self.TRACKBAR_WINDOW, hsv_filter.vMin)
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, hsv_filter.hMax)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, hsv_filter.sMax)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, hsv_filter.vMax)
        cv.setTrackbarPos('SAdd', self.TRACKBAR_WINDOW, hsv_filter.sAdd)
        cv.setTrackbarPos('SSub', self.TRACKBAR_WINDOW, hsv_filter.sSub)
        cv.setTrackbarPos('VAdd', self.TRACKBAR_WINDOW, hsv_filter.vAdd)
        cv.setTrackbarPos('VSub', self.TRACKBAR_WINDOW, hsv_filter.vSub)

    def get_hsv_filter_from_controls(self):
        hsv_filter = HSVFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)

        return hsv_filter
    
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # use filter values from trackbars
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        #  set min and max values for each channel
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])

        # add to saturation up to a max of 255
        hsv[:, :, 1] = np.maximum(hsv[:, :, 1] + hsv_filter.sAdd, hsv_filter.sSub)

        # add to value up to a max of 255
        hsv[:, :, 2] = np.maximum(hsv[:, :, 2] + hsv_filter.vAdd, hsv_filter.vSub)

        # apply filter
        mask = cv.inRange(hsv, lower, upper)                    # pixels in range are 1 (white), others are 0 (black)
        filtered_image = cv.bitwise_and(hsv, hsv, mask=mask)    # apply mask to original image

        # convert back to BGR
        img = cv.cvtColor(filtered_image, cv.COLOR_HSV2BGR)

        return img