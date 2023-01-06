import sys
from typing import Dict, List, Tuple

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
normal_speed_green    = 'assets/Green-Square/NormalSpeed.mp4'
slow_speed_green      = 'assets/Green-Square/SlowSpeed.mp4'
green_fiducial        = 'assets/Green-Square/templates/Green Fiducial.png'
bigger_green_fiducial = 'assets/Green-Square/templates/Bigger Green Fiducial.png'
normal_green_frame    = 'assets/Green-Square/NormalSpeedFrame.png'
lower_square_green = (40,100,95)
upper_square_green = (75,135,130)

# PATHS FOR SQUAT VIDEOS WITH GREEN CIRCLE FIDUCIAL
green_circle_video       = 'assets/Green-Circle/GreenCircle.mp4'
green_circle_frame       = 'assets/Green-Circle/GreenCircleFrame.png'
circle_template          = 'assets/Green-Circle/templates/CircleTemplate.png'
circle_template2         = 'assets/Green-Circle/templates/CircleTemplate2.png'
isolated_circle_temlpate = 'assets/Green-Circle/templates/IsolatedCircle.png'
lower_circle_green = (50, 100, 130)
upper_circle_green = (90, 150, 180)

# Rowing video
rowing_video = 'assets/Green Circle/Rowing.mp4'   
lower_rowing_green = (40, 90, 90)
upper_rowing_green = (70, 150, 140)


def color_isolated(bgr_img: Mat, lower_color: Tuple, upper_color: Tuple) -> Mat:
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv_img, lower_color, upper_color) 
    return mask

# returns dictionary where keys are the time values and the values are the center points of the circle
def track_green_fiducial(
    path: str, fiducial_radius: int,
    lower_color: Tuple[int, int, int], upper_color: Tuple[int, int, int]
) -> Dict[np.signedinteger, Tuple[int, int]]:
    points = {}
    
    vid = cv2.VideoCapture(path)

    fps = int(vid.get(5))
    print("Frame Rate : ", fps, "frames per second") 
    frame_count = vid.get(7)
    print("Frame count : ", frame_count)

    # keep track of the time passed at each frame
    vid_length = frame_count / fps
    seconds_per_frame = vid_length / frame_count
    time_vals = np.arange(0, vid_length, seconds_per_frame)

    i = 0
    while vid.isOpened():
        success, frame = vid.read()
        if not success: break
        if path == rowing_video:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        curr_time = time_vals[i]

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
            
            if fiducial_radius - 10 <= radius and radius <= fiducial_radius + 10:
                # this block greatly increases the accuracy
                # it either draws the correct circle or nothing :)
                cv2.circle(frame, center, int(radius), (255, 0, 0), 15)
                cv2.circle(frame, center, radius=10, color=(0, 0, 0), thickness=-1)

                points[curr_time] = (x, y)

        cv2.imshow('Contours', frame)
        i += 1
        if cv2.waitKey(1) == ord('q'):
            break
    print(f"num frames analyzed: {i}")
    cv2.destroyAllWindows()
    return points

def test_local_video():
    path = green_circle_video
    if path == green_circle_video:
        lower_color = lower_circle_green
        upper_color = upper_circle_green
        fiducial_radius = 135
    elif path == rowing_video:
        lower_color = lower_rowing_green
        upper_color = upper_rowing_green
        fiducial_radius = 60
    
    point_dict = track_green_fiducial(path, fiducial_radius, lower_color, upper_color)
    
    x_vals, y_vals = [], []
    time_vals = []
    for key, val in point_dict.items():
        if path == green_circle_video and (key < 0.4 or key > 3): continue
        time_vals.append(key)
        x_vals.append(val[0])
        y_vals.append(val[1])
    
    # graph full results
    calc.graph_calculus(
        y_vals, time_vals, fiducial_radius=fiducial_radius,
        isAscending=False, title="Tracking a Barbell During a Squat"
    )
    
    # graph descent (from start to highest y value aka deepst pat of squat)
    max_y_index = y_vals.index(max(y_vals))

    y_descent = y_vals[0 : max_y_index]
    t_descent = time_vals[0 : max_y_index]

    calc.graph_calculus(
        y_descent, t_descent, fiducial_radius=fiducial_radius,
        isAscending=False, title="Tracking a Barbell During the Descent of a Squat"
    )

    # graph ascent (from highest y value aka deepst pat of squat to end)
    y_ascent = y_vals[max_y_index :]
    t_ascent = time_vals[max_y_index : ]

    calc.graph_calculus(
        y_ascent, t_ascent, fiducial_radius=fiducial_radius,
        isAscending=True, title="Tracking a Barbell During the Ascent of a Squat"
    )
    
    calc.check_barpath(x_vals, time_vals, fiducial_radius)

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
# refPt = []
# cropping = False
# def click_and_crop(event, x, y, flags, param):
# 	# grab references to the global variables
# 	global refPt, cropping
# 	# if the left mouse button was clicked, record the starting
# 	# (x, y) coordinates and indicate that cropping is being
# 	# performed
# 	if event == cv2.EVENT_LBUTTONDOWN:
# 		refPt = [(x, y)]
# 		cropping = True
# 	# check to see if the left mouse button was released
# 	elif event == cv2.EVENT_LBUTTONUP:
# 		# record the ending (x, y) coordinates and indicate that
# 		# the cropping operation is finished
# 		refPt.append((x, y))
# 		cropping = False
# 		# draw a rectangle around the region of interest
# 		cv2.rectangle(image, refPt[0], refPt[1], (255, 255, 255), 2)
# 		cv2.imshow("image", image)

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("USAGE: python3 src/main.py <path/to/video/to/analyze>")
    #     print("**Path cannot have spaces within**")
    #     exit(1)

    # path = sys.argv[1]
    # print(f"Path: {path}")

    # vid = cv2.VideoCapture(path)
    # success, image = vid.read()
    # if not success: exit(1)

    # # load the image, clone it, and setup the mouse callback function
    # clone = image.copy()
    # cv2.namedWindow("image")
    # cv2.setMouseCallback("image", click_and_crop)
    # # keep looping until the 'q' key is pressed
    # while True:
    #     # display the image and wait for a keypress
    #     cv2.imshow("image", image)
    #     key = cv2.waitKey(1) & 0xFF
    #     # if the 'r' key is pressed, reset the cropping region
    #     if key == ord("r"):
    #         image = clone.copy()
    #     # if the 'c' key is pressed, break from the loop
    #     elif key == ord("c"):
    #         break
    # # if there are two reference points, then crop the region of interest
    # # from teh image and display it
    #     roi = clone[reffPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    #     cv2.imshow("ROI", roi)
    #     cv2.waitKey(0)
    # # close all open windows
    # cv2.destroyAllWindows()

    
    test_local_video()