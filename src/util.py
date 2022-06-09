from typing import List
import cv2
from cv2 import Mat

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

def frames_from_video(video) -> List[Mat]:
    frames = []
    while True:
        ret, frame = video.read()
        if ret == False: break
        frames.append(frame)
    return frames