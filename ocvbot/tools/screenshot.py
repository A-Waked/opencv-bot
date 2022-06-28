import argparse
import cv2 as cv
import os
from time import time
from ocvbot.botlib.windowcapture import WindowCapture
from ocvbot.botlib.vision import Vision
from ocvbot.botlib.hsvfilter import HSVFilter

def run(path, needle):
    path = path.replace("\\", "/")  # fix path for windows

    wc = WindowCapture("")

    hsvfilter = HSVFilter()         # TODO fetch parameters from file if it exists

    loop_time = time()

    # screenshot variables
    pos = 0
    neg = 0
    toggle = False
    sps = 30 # denominator of screenshots per second TODO make this dec/inc with +/-
    spsc = 0
    output_size = 1

    # capture window toggles
    filtering = False
    matching = False

    # set path to needle else use placeholder object
    if needle:
        vision = Vision(path+"needles/"+needle+".jpg")
    else:
        vision = Vision()

    vision.init_control_gui()   

    while(True):
        capture = wc.get_screenshot()[1]

        # make positive and negative folders at the path if they dont exist
        if not os.path.exists(path+"/positive"):
            os.makedirs(path+"/positive")
        if not os.path.exists(path+"/negative"):
            os.makedirs(path+"/negative")
             
        if matching:
            # check if a filter exists and apply it
            if os.path.exists(path+"needle_filter.txt"):
                hsvfilter = get_filter(path)

                # apply the filter
                filtered_image = vision.apply_hsv_filter(capture, hsvfilter)
                rectangles = vision.find(filtered_image)
                vision.set_trackbar_positions(hsvfilter)
            else:
                # draw unfiltered image
                # useful for speeding up the process of gathering training data
                rectangles = vision.find(capture)

            capture = vision.draw_rectangles(capture, rectangles)

        if filtering:
            filtered_image = vision.apply_hsv_filter(capture)
            # resize filtered image to half size
            output = cv.resize(filtered_image, (0,0), fx=output_size, fy=output_size)
        else:
            output = cv.resize(capture, (0,0), fx=output_size, fy=output_size)

        cv.imshow('output', output)

        # print("FPS: {}".format(1/(time()-loop_time)))
        loop_time = time()

        key = cv.waitKey(1)
        # q - Quit
        if key == ord('q'):
            cv.destroyAllWindows()
            break

        # r - toggle filter
        elif key == ord('f'):
            # toggle filtering
            filtering = not filtering
        
        # s - save filter to text file
        elif key == ord('s'):
            hsvfilter = vision.get_hsv_filter_from_controls()
            save_filter(path, hsvfilter)

        # l - load filter from text file
        elif key == ord('l'):
            hsvfilter = get_filter(path)
            vision.set_trackbar_positions(hsvfilter)

        # t - toggle template matching
        elif key == ord('t'):
            # toggle template matching
            if needle:
                matching = not matching
            else:
                print("No template folder provided. Run again with -t <path-to-template>")

        # p - save to positive folder
        elif key == ord('p'):
            pos += 1
            cv.imwrite('{}positive/positive-{}.jpg'.format(path,loop_time), capture)
            # print save path
            print("{}. Saved: {}positive-{}.jpg".format(pos,path,loop_time))

        # n - save to negative folder
        elif key == ord('n'):
            cv.imwrite('{}negative/negative-{}.jpg'.format(path,loop_time), capture)
            neg += 1
            print("{}. Saved: {}negative-{}.jpg".format(neg,path,loop_time))

        # \ - toggle auto-screenshot
        elif key == ord('\\'):
            toggle = True

        # TODO add max and min
        # '+' - increase screenshots per second
        elif key == ord('+'):
            sps += 1
            print("SPS: {}".format(sps))

        # '-' - decrease screenshots per second
        elif key == ord('-'):
            sps -= 1
            print("SPS: {}".format(sps))

        # ']' - increase size of window
        elif key == ord(']'):
            output_size += 0.1

        # '[' - decrease size of window
        elif key == ord('['):
            if output_size > 0.2:
                output_size -= 0.1

        # automaticallly save a screenshot
        if toggle == True:
            if spsc == sps:
                if key == ord('\\'):
                    # if toggle is true then switch to false, otherwise switch to true
                    toggle = False
                    print("Auto screenshot disabled")
                cv.imwrite('{}negative/negative-{}.jpg'.format(path,loop_time), capture)
                neg += 1
                print("{}. Saved: {}negative-{}.jpg".format(neg,path,loop_time))
                spsc = 0
            spsc += 1

        

def get_filter(path):
    hsvfilter = HSVFilter()
    
    if os.path.exists(path+"needle_filter.txt"):
        with open(path+"needle_filter.txt", "r") as f:
            hsvfilter.hMin = int(f.readline())
            hsvfilter.sMin = int(f.readline())
            hsvfilter.vMin = int(f.readline())
            hsvfilter.hMax = int(f.readline())
            hsvfilter.sMax = int(f.readline())
            hsvfilter.vMax = int(f.readline())
            hsvfilter.sAdd = int(f.readline())
            hsvfilter.sSub = int(f.readline())
            hsvfilter.vAdd = int(f.readline())
            hsvfilter.vSub = int(f.readline())
            print("Loaded filter from file")
        return hsvfilter
    else:
        return HSVFilter()

def save_filter(path, hsvfilter):
    with open(path+"needle_filter.txt", "w") as f:
        f.write(str(hsvfilter.hMin)+"\n")
        f.write(str(hsvfilter.sMin)+"\n")
        f.write(str(hsvfilter.vMin)+"\n")
        f.write(str(hsvfilter.hMax)+"\n")
        f.write(str(hsvfilter.sMax)+"\n")
        f.write(str(hsvfilter.vMax)+"\n")
        f.write(str(hsvfilter.sAdd)+"\n")
        f.write(str(hsvfilter.sSub)+"\n")
        f.write(str(hsvfilter.vAdd)+"\n")
        f.write(str(hsvfilter.vSub)+"\n")
    print("Filter values saved to needle_filter.txt")