import argparse
import os
import importlib
import cv2 as cv # TODO remove this when done testing
from ocvbot.botlib.windowcapture import WindowCapture
from ocvbot.botlib.vision import Vision # TODO remove this when done testing

parser = argparse.ArgumentParser()

# screenshot tool args
parser.add_argument('-s', '--screenshot', help='launch screenshot tool. Put \'?\' for temp file', required=False)
# parser.add_argument('-f', '--screenshot-filter', help='launch screenshot tool with HSV filter tool', required=False, action='store_true')
parser.add_argument('-t', '--template-match', help='Draw rectangles using template matching', required=False)

# bot args
parser.add_argument('-b', '--bot', help='start bot', required=False)
parser.add_argument('-d', '--debug', help='open debug window', required=False, action='store_true')

args = parser.parse_args()

if args.bot:
    # takes the bot name through the bot argument and runs it from the scripts directory
    bot = args.bot
    try :
        bot_module = importlib.import_module("ocvbot.scripts." + bot)
        bot_module.run(args)
    except ImportError as e:
        print("Error: " + str(e))
        exit()

elif args.screenshot:
    if args.screenshot == '?':
        screenshot_path = os.getcwd()+"\\ocvbot\scripts\\temp\\"
        
    else:
        screenshot_path = os.getcwd()+"\\ocvbot\scripts\\"+args.screenshot+"\\"
    
    from ocvbot.tools.screenshot import run
    run(screenshot_path, args.template_match)

else:
    # Testing - Remove later
    cascade = cv.CascadeClassifier('ocvbot/scripts/cascading_bot/cascade/cascade.xml')
    vision = Vision()
    
    while True:
        capture = WindowCapture("").get_screenshot()[1]
        rectangles = cascade.detectMultiScale(capture)
        vision.draw_rectangles(capture, rectangles)
        cv.imshow('output', capture)

        key = cv.waitKey(1)
        if key == ord('q'):
            cv.destroyAllWindows()
            break


    #----------------------------------------

    # print("Error: no arguments given")
    # exit()


