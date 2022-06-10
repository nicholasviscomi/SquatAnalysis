from re import template
from typing import List, Tuple

import cv2
from cv2 import Mat

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors

import util


# have the user input the template, aka the barbell
# track that template through every frame of the video
# find a way to turn the change in pixels into a change in real distance 
    # can you just do the calcualtions on change in # of pixels rather than a distance?
# do some math and pretty graphs!

# PATHS FOR BASIC SQUAT VIDEOS
squat_video1     = 'assets/SquatVideo.mp4'
squat_video2     = 'assets/SquatVideo2.mp4'
plate_template1  = 'assets/PlateTemplate.png'
plate_template2  = 'assets/PlateTemplate2.png'
plate_template3  = 'assets/PlateTemplate3.png'
barbell_template = 'assets/BarbellTemplate.png'

# PATHS FOR SQUAT VIDEOS WITH GREEN SQUARE FIDUCIAL
normal_speed_green    = 'assets/Green Square/NormalSpeed.mp4'
slow_speed_green      = 'assets/Green Square/SlowSpeed.mp4'
green_fiducial        = 'assets/Green Square/templates/Green Fiducial.png'
bigger_green_fiducial = 'assets/Green Square/templates/Bigger Green Fiducial.png'
normal_green_frame    = 'assets/Green Square/NormalSpeedFrame.png'
lower_square_green = (40,100,95)
upper_square_green = (75,135,130)

# PATHS FOR SQUAT VIDEOS WITH GREEN CIRCLE FIDUCIAL
green_circle_video       = 'assets/Green Circle/GreenCircle.mp4'
circle_template          = 'assets/Green Circle/templates/CircleTemplate.png'
isolated_circle_temlpate = 'assets/Green Circle/templates/IsolatedCircle.png'
lower_circle_green = (60, 110, 140)
upper_circle_green = (80, 140, 170)


def analysis(path: str, template_path: str):
    vid_capture = cv2.VideoCapture(path)

    if (vid_capture.isOpened() == False):
        print("Error opening the video file")
        exit(0)
    
    # Get frame rate information
    fps = int(vid_capture.get(5))
    print("Frame Rate : ", fps, "frames per second") 

    # Get frame count
    frame_count = vid_capture.get(7)
    print("Frame count : ", frame_count)

    # methods = [
    #     cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, # best ones by far
    #     cv2.TM_CCORR, cv2.TM_CCORR_NORMED,
    #     cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED
    # ]
    # colors = [
    #     (255,255,255),
    #     (0,0,0),
    #     (255,0,0),
    #     (0,255,0),
    #     (0,0,255),
    #     (255,255,0),
    # ]
    frames = util.frames_from_video(vid_capture)
        
def color_isolated(bgr_img: Mat, lower_color: Tuple, upper_color: Tuple) -> Mat:
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv_img, lower_color, upper_color) 
    result = cv2.bitwise_and(rgb_img, rgb_img, mask=mask) # mashes the 2 images together

    return result

def track_green_fiducial(path: str, template_path: str) -> List[List]:
    # get video strem and template set up
    vid_capture = cv2.VideoCapture(path)

    if (vid_capture.isOpened() == False):
        print("Error opening the video file")
        exit(0)

    points = []
    
    template = cv2.cvtColor(cv2.imread(template_path), cv2.COLOR_BGR2RGB)
    t_width, t_height, _ = template.shape   
    
    method = cv2.TM_CCORR

    i = 0
    while vid_capture.isOpened:
        if i % 10 != 0: 
            i += 1
            continue

        # get frame and template ready
        ret, frame = vid_capture.read()
        if not ret: break
        original = frame
        frame = color_isolated(frame, lower_square_green, upper_square_green)

        # match it and draw the rectangle
        match = cv2.matchTemplate(frame, template, method) # for this, cv2.TM_CCORR worked best
        _, _, _, max_loc = cv2.minMaxLoc(match)
        cv2.rectangle(
            original, max_loc, 
            (max_loc[0] + t_width, max_loc[1] + t_height),
            color=(255,255,255),
            thickness=5
        )
        points.append([max_loc[0], max_loc[1]])
        cv2.imshow('Frame', original)
        i += 1
        if cv2.waitKey(1) == ord('q'):
            break
    
    vid_capture.release()
    cv2.destroyAllWindows()
    return points

#doesn't work because there are some random pixels that get caught first
def track_first_green_pixel(path: str) -> List[List]:
    vid = cv2.VideoCapture(path)
    if vid.isOpened() == False:
        print("Error opening video")
        return

    tracking_points = []

    num_frame = 1
    while vid.isOpened():
        ret, frame = vid.read()
        if ret == False: 
            print("No more frames to retrieve")
            break
        frame = color_isolated(frame, lower_square_green, upper_square_green)
        # util.display(frame)

        if num_frame % 5 != 0: 
            # reduce frame rate to lessen number of computations done
            num_frame += 1
            continue

        if num_frame == 120:
            return tracking_points

        # will be set with the previous location of the first green pixel 
        # so that only the surrounding area is searched and not the whole image

        starting_x, starting_y = 0,0 
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for y in range(starting_y, len(hsv_frame)):
            for x in range(starting_x, len(hsv_frame[0])):
                # because of the green isolation, everything else is (0,0,0)
                # find first pixel with saturation greater than 100
                if hsv_frame[y][x][1] >= 100: 
                    print(f"Frame #{num_frame}: non-black pixel @ row {y}, col {x}")
                    cv2.circle(frame, center=(x, y), radius=5, color=(255,255,255), thickness=-1)
                    cv2.imshow('Frame', frame)
                    if cv2.waitKey(1) == ord('q'):
                        return tracking_points

                    tracking_points.append([y, x])

                    # gives the next iteration an idea of where to start
                    if y > 200:
                        starting_y = y - 100
                    if x > 200:
                        starting_x = x - 100
                    break
            else:
                # once the inner for loop is exited, this will run
                # it will go to the line below, and break out of the upper loop
                continue
            break
        
        num_frame += 1

    return tracking_points

#doesn't work
def track_circle_fiducial(path: str, template_path: str):
    
    template = cv2.imread(template_path)
    # template = color_isolated(template, lower_circle_green, upper_circle_green)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)

    vid = cv2.VideoCapture(path)
    while vid.isOpened():
        success, frame = vid.read()
        if not success: break

        frame = color_isolated(frame, lower_circle_green, upper_circle_green)

        # try using template matching on the isolated green circle

        cv2.imshow('Frame', frame)
        cv2.waitKey(0)
        break
            # if cv2.waitKey(1) == ord('q'):
            #     break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    track_green_fiducial(normal_speed_green, bigger_green_fiducial)