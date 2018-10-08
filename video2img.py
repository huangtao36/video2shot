# _*_coding:utf-8 _*_
# Author  : Tao
"""
This code is used to convert video to frame-level images, sampled as 2pfs
"""

import cv2
import os
import time

video_dir = './video'
save_root_path = './imdir'
os.mkdir(save_root_path) if not os.path.exists(save_root_path) else None

st = time.time()

for i, video in enumerate(os.listdir(video_dir)):
    video_num = len(os.listdir(video_dir))
    vidcap = cv2.VideoCapture(video)

    save_path = os.path.join(save_root_path, video.split('.')[0])
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)  # 帧数
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    # print(fps)

    # 这里固定10帧间隔采样，原应按照帧率计算采样间隔的，采样后为 2-3 fps
    for n in range(round(frames / 10)):
        print("共:{0}个视频, 进度:{1}%, 已耗时:{2}s".format(
            video_num,
            round((i + 1) * 100 / video_num),
            round(time.time() - st, 2)), end="\r")

        vidcap.set(cv2.CAP_PROP_POS_FRAMES, n * 10)
        bool_, img = vidcap.read()

        cv2.imwrite(os.path.join(save_path, "%s.png" % str(n)), img)
