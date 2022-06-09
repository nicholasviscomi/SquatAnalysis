from typing import List

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

# PATHS FOR SQUAT VIDEOS WITH GREEN FIDUCIAL
normal_speed_green = 'assets/Green Square/NormalSpeed.mp4'
slow_speed_green   = 'assets/Green Square/SlowSpeed.mp4'
green_fiducial     = 'assets/Green Square/templates/Green Fiducial.png'
normal_green_frame = 'assets/Green Square/NormalSpeedFrame.png'

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

    frames = frames_from_video(vid_capture)
    

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

    template = cv2.imread(template_path)
    t_width, t_height, _ = template.shape   

    
    i = 1; method = cv2.TM_CCORR
    for i in range(0, len(frames) - 1, 3): # 60fps it too much
        # get frame and template ready
        frame = green_isolated(frames[i])
        template = cv2.cvtColor(cv2.imread(green_fiducial), cv2.COLOR_BGR2RGB)
        t_width, t_height, _ = template.shape

        # match it and draw the rectangle
        match = cv2.matchTemplate(frame, template, method) # for this, cv2.TM_CCORR worked best
        _, _, _, max_loc = cv2.minMaxLoc(match)
        cv2.rectangle(
            frame, max_loc, 
            (max_loc[0] + t_width, max_loc[1] + t_height),
            color=(255,255,255),
            thickness=5
        )

        cv2.imshow('Frame', frame)
        i += 1
        if cv2.waitKey(1) == ord('q'):
            break
    
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
    

def green_isolated(bgr_img: Mat) -> Mat:
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv_img, (40,100,95), (70,130,125))
    result = cv2.bitwise_and(rgb_img, rgb_img, mask=mask) # mashes the 2 images together
    # plt.subplot(1, 2, 1)
    # plt.imshow(mask, cmap="gray")
    # plt.subplot(1, 2, 2)
    # plt.imshow(result)
    # plt.show()

    return result


if __name__ == '__main__':
    # util.play_video(normal_speed_green)
    # util.show_frame(normal_speed_green)

    analysis(normal_speed_green, template_path=green_fiducial)

    # img = cv2.imread(normal_green_frame)
    # img = green_isolated(img)

    # template = cv2.cvtColor(cv2.imread(green_fiducial), cv2.COLOR_BGR2RGB)
    # t_width, t_height, _ = template.shape

    # plt.subplot(1, 2, 1)
    # plt.imshow(img)
    # plt.subplot(1, 2, 2)
    # plt.imshow(template)
    # plt.show()

    # match = cv2.matchTemplate(img, template, cv2.TM_CCORR) # for this, cv2.TM_CCORR worked best
    # _, _, _, max_loc = cv2.minMaxLoc(match)
    # cv2.rectangle(
    #     img, max_loc, 
    #     (max_loc[0] + t_width, max_loc[1] + t_height),
    #     color=(255,255,255),
    #     thickness=5
    # )

    # cv2.imshow('Figure', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    



# def rgb_splitter(image):
#     rgb_list = ['Reds','Greens','Blues']
#     _, ax = plt.subplots(1, 3, figsize=(15,5), sharey = True)
#     for i in range(3):
#         ax[i].imshow(image[:,:,i], cmap = rgb_list[i])
#         ax[i].set_title(rgb_list[i], fontsize = 15)
#     plt.show()

# original = plt.imread(path)
# # plt.figure(num=None, figsize=(8, 6), dpi=80)
# # plt.imshow(original)
# # plt.show()
# # rgb_splitter(original)

# # original[:,:,0] = r; original[:,:,0] = g, etc.
# green_filtered = (original[:,:,0] < 100) & (original[:,:,1] > 10) & (original[:,:,2] < 110)
# plt.figure(num=None, figsize=(8, 6), dpi=80)
# green_square_new = original.copy()
# green_square_new[:, :, 0] = green_square_new[:, :, 0] * green_filtered
# green_square_new[:, :, 1] = green_square_new[:, :, 1] * green_filtered
# green_square_new[:, :, 2] = green_square_new[:, :, 2] * green_filtered
# plt.imshow(green_square_new)
# plt.show()