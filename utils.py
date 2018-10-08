# _*_coding:utf-8 _*_
# Author  : Tao
"""
This Code is ...
"""
import os
import re
import numpy as np
from skimage import color


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


def color_hist(im, col_bins):
    """
    Get color histogram descriptors for RGB and LAB space.
    Input: im: (h,w,c): 0-255: np.uint8
    Output: descriptor: (col_bins*6,)
    """
    assert im.ndim == 3 and im.shape[2] == 3, "image should be rgb"
    arr = np.concatenate((im, color.rgb2lab(im)), axis=2).reshape((-1, 6))
    desc = np.zeros((col_bins * 6,), dtype=np.float)
    for i in range(3):
        desc[i * col_bins:(i + 1) * col_bins], _ = np.histogram(
            arr[:, i], bins=col_bins, range=(0, 255))
        desc[i * col_bins:(i + 1) * col_bins] /= np.sum(
            desc[i * col_bins:(i + 1) * col_bins]) + (
                np.sum(desc[i * col_bins:(i + 1) * col_bins]) < 1e-4)

    # noinspection PyUnboundLocalVariable
    i += 1
    desc[i * col_bins:(i + 1) * col_bins], _ = np.histogram(
        arr[:, i], bins=col_bins, range=(0, 100))
    desc[i * col_bins:(i + 1) * col_bins] /= np.sum(
        desc[i * col_bins:(i + 1) * col_bins]) + (
            np.sum(desc[i * col_bins:(i + 1) * col_bins]) < 1e-4)
    for i in range(4, 6):
        desc[i * col_bins:(i + 1) * col_bins], _ = np.histogram(
            arr[:, i], bins=col_bins, range=(-128, 127))
        desc[i * col_bins:(i + 1) * col_bins] /= np.sum(
            desc[i * col_bins:(i + 1) * col_bins]) + (
                np.sum(desc[i * col_bins:(i + 1) * col_bins]) < 1e-4)
    return desc


def compute_features(im, col_bins):
    """
    Compute features of images: RGB histogram + SIFT
    im: (h,w,c): 0-255: np.uint8
    feat: (d,)
    """
    col_hist = color_hist(im, col_bins=col_bins)

    return col_hist


if __name__ == '__main__':
    get_file_path_list('./cache')
