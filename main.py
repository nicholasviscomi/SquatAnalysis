from typing import List
import cv2
from cv2 import Mat
import numpy as np

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

# PATHS FOR SQUAT VIDEOS WITH GREEN FIDUCIAL
normal_speed_green = 'assets/Green Square/NormalSpeed.mp4'
slow_speed_green   = 'assets/Green Square/SlowSpeed.mp4'
green_fiducial     = 'assets/Green Square/templates/Green Fiducial.png'

def analysis(path: str, template_path: str):
    vid_capture = cv2.VideoCapture(path, apiPreference=cv2.CAP_MSMF)

    if (vid_capture.isOpened() == False):
        print("Error opening the video file")
        exit(0)
    
    # Get frame rate information
    fps = int(vid_capture.get(5))
    print("Frame Rate : ", fps, "frames per second") 

    # Get frame count
    frame_count = vid_capture.get(7)
    print("Frame count : ", frame_count)

    frames = frames_from_video(vid_capture)
    

    methods = [
        cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, # best ones by far
        cv2.TM_CCORR, cv2.TM_CCORR_NORMED,
        cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED
    ]
    methods = [
        cv2.TM_CCOEFF_NORMED, # best ones by far
        cv2.TM_CCORR_NORMED,
        cv2.TM_SQDIFF_NORMED
    ]
    colors = [
        (255,255,255),
        (0,0,0),
        (255,0,0),
        (0,255,0),
        (0,0,255),
        (255,255,0),
    ]

    template = cv2.imread(template_path, 0)
    t_width, t_height = template.shape   

    for method,color in zip(methods, colors):
        print("==============================")
        print(method)
        i = 1
        for frame in frames:
            frame_copy = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(frame_copy, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            print(f"Frame #: {i}")
            # print(f"Max value: {max_val}")
            # print(f"Min value: {min_val}")
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                # for these 2 methods, min is the best one
                location = min_loc
            else:
                location = max_loc

            cv2.rectangle(
                frame, # write on the original color frame
                location, (location[0] + t_width, location[1]+t_height),
                color,
                thickness=5
            )

            cv2.imshow('Frame', frame)
            i += 1
            if cv2.waitKey(1) == ord('q'):
                break
        print("==============================")
    
    vid_capture.release()
    cv2.destroyAllWindows()

# Problem frames: 40-70, 85-95
    # I think I just need higher quality video

def frames_from_video(video) -> List[Mat]:
    frames = []
    while True:
        ret, frame = video.read()
        if ret == False: break
        frames.append(frame)
    return frames
    

def play_video(path):
    vid = cv2.VideoCapture(path)
    while vid.isOpened():
        ret, frame = vid.read()
        if ret == False: break
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

def show_frame(path):
    vid = cv2.VideoCapture(path)
    ret, frame = vid.read()
    if not ret: return
    cv2.imshow('Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # play_video(normal_speed_green)
    # show_frame(normal_speed_green)
    analysis(normal_speed_green, template_path=green_fiducial)