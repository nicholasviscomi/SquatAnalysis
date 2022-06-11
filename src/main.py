from typing import List, Tuple

import cv2
from cv2 import Mat

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors

import util
import calc
import imutils

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
green_circle_frame       = 'assets/Green Circle/GreenCircleFrame.png'
circle_template          = 'assets/Green Circle/templates/CircleTemplate.png'
circle_template2         = 'assets/Green Circle/templates/CircleTemplate2.png'
isolated_circle_temlpate = 'assets/Green Circle/templates/IsolatedCircle.png'
lower_circle_green = (50, 100, 130)
upper_circle_green = (90, 150, 180)


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
    return mask

def track_green_fiducial(
    path: str, lower_color: Tuple[int, int, int], upper_color: Tuple[int, int, int]
) -> List[List]:
    points = []
    
    vid = cv2.VideoCapture(path)
    i = 0 
    while vid.isOpened():
        if i % 10 != 0:
            i += 1
            continue
        
        success, frame = vid.read()
        if not success: break
        
        mask = color_isolated(frame, lower_color, upper_color)

        edged = cv2.Canny(mask, 100, 200)
        items = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(items)

        center = None

        if len(contours) > 0:
		# find the largest contour in the mask, then use it to compute 
        # the minimum enclosing circle and its center
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            center = (int(x), int(y))
            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                cv2.circle(frame, center, int(radius), (255, 255, 255), 10)
                cv2.circle(frame, center, radius=10, color=(255, 255, 255), thickness=-1)

                points.append([x, y])

        cv2.imshow('Contours', frame)
        i += 1
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()
    return points
    
if __name__ == '__main__':
    points = track_green_fiducial (
        green_circle_video, lower_circle_green, upper_circle_green
    )

    calc.analyze_points(points)