import cv2
import os
import alg
import time
import numpy as np


def read_videos(path, size=None, fps=30):
    """
    read_videos(path, [size=None[, fps=30]]): 讀取影片
    path: 影片路徑, 資料類型 str
    size: 影片解析度大小, 輸入類型 tuple, (width, height), 默認 None 為預設輸入影片解析度大小
    fps: 影片每秒讀取的幀數, 不超過 60, 類型 int, 默認 30
    return video (type: cv2.VideoCapture)
    """

    if not os.path.isfile(path):
        raise IOError('路徑裡不包含影片檔案格式 *.mp4, *.avi')

    if not isinstance(size, tuple) and size is not None:
        raise TypeError('size 輸入資料類型錯誤, 格式為 tuple, (width, height)')

    if not isinstance(fps, int) and (fps > 60 or fps < 0):
        raise TypeError('fps 資料類型或大小錯誤, 格式 int, 範圍 0 < fps <= 60')

    video = cv2.VideoCapture(path)

    if size is not None:
        video.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    video.set(cv2.CAP_PROP_FPS, fps)

    return video


def get_road(cap, frame_time=-1):
    """
    get_road(cap[, frame_time=-1]): 抓取馬路範圍
    cap: 資料類型為 cv2.VideoCapture
    frame_time: 影片每秒讀取幀數, 不超過影片設定的 fps 值, 默認為 -1, 則實質為 fps 值
    """

    while True:
        ret, frame = cap.read()
        if frame_time != -1:
            frame_cnt = 1
            if frame_cnt % frame_time == 0:
                pass  # handle img
            frame_cnt += 1
        else:
            pass  # handle img
    pass  # return or any handle


videos = read_videos('./video/test.mp4')
get_road(videos)