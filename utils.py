# _*_coding:utf-8 _*_
# Author  : Tao
"""
This Code is ...
"""
import os
import re


def get_file_path_list(indir):
    """
    It reads filname containing input pattern recursively if indir exists
    """

    assert os.path.exists(indir), 'indir is not exits.'

    img_file_list = os.listdir(indir)
    img_file_list = sorted(img_file_list,
                           key=lambda k: int(re.match(r'(\d+)', k).group()))
    img_list = []
    for i, img in enumerate(img_file_list):
        if '.png' in img:
            path_ = os.path.join(indir, img)
            img_list.append(path_)
    return img_list


if __name__ == '__main__':
    get_file_path_list('./cache')
