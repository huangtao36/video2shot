# _*_coding:utf-8 _*_
# Author  : Tao
"""
This code is used to convert video to frame-level images, sampled as 2pfs
"""
from __future__ import unicode_literals
import cv2
import os
import time
import random
import json
import h5py
from load_tvsum_utils import load_tvsum, get_summary


def sample_tvsum_video(video_dir, save_root_path, data_root_path):

    st = time.time()
    print("Load tvsum annotation data...")
    video_dic = load_tvsum(data_root_path=data_root_path, scale=True)
    print("用时: {0}s".format(time.time() - st))

    # st = time.time()

    os.mkdir(save_root_path) if not os.path.exists(save_root_path) else None
    f = h5py.File(os.path.join(save_root_path, 'sample_anno.h5'), 'w')

    for key in video_dic:
        video_name = key
        fps = video_dic[key]['fps']
        frames = video_dic[key]['frames']
        user_score = video_dic[key]['user_score']
        avg_score = video_dic[key]['avg_score']

        internal = ((fps + 1) // 2)
        # 每秒取两帧，随机取
        select = []
        for n in range(round(frames // internal)):
            # 这里最后的1-2秒内的帧不会被选择到，因为取整的问题，
            # 考虑到视频最后1-2秒的信息量一般不大，可认为是合理的
            select_num = (n * internal) + random.randint(0, internal)
            select.append(select_num)

        video_file = os.path.join(video_dir, video_name + '.mp4')
        video_capture = cv2.VideoCapture(video_file)

        save_path = os.path.join(save_root_path, video_name)
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        sample_score = []
        serial_number = 0
        for n in select:
            sample_score.append(avg_score[n])

            video_capture.set(cv2.CAP_PROP_POS_FRAMES, n)
            bool_, img = video_capture.read()

            if bool_:
                cv2.imwrite(os.path.join(save_path, '%s.png' % str(serial_number)), img)

            serial_number += 1
        video_dic[key]['avg_score'] = sample_score

        subgroup = f.create_group(video_name)
        subgroup.create_dataset('sample_scores', data=sample_score)
    f.close()


if __name__ == '__main__':
    project_par_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
    data_root_path = os.path.join(project_par_path, 'Dataset', 'ydata-tvsum50-v1_1')

    video_path = os.path.join(data_root_path, 'video')

    save_root_path = os.path.join(data_root_path, 'sample_video')

    sample_tvsum_video(video_path, save_root_path, data_root_path)
