from typing import List, Tuple

import cv2
from cv2 import Mat

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors

import util
import calc


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
circle_template2          = 'assets/Green Circle/templates/CircleTemplate2.png'
isolated_circle_temlpate = 'assets/Green Circle/templates/IsolatedCircle.png'
lower_circle_green = (55, 105, 135)
upper_circle_green = (85, 145, 175)


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

def track_green_fiducial(path: str, template_path: str, 
                        lower_color: Tuple[int, int, int], upper_color: Tuple[int, int, int]) -> List[List]:
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
        frame = color_isolated(frame, lower_color, upper_color)

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
    
if __name__ == '__main__':
    # points = track_green_fiducial (
    #     green_circle_video, isolated_circle_temlpate, 
    #     lower_circle_green, upper_circle_green
    # )

    calc.analyze_points([[0,0]])