# _*_coding:utf-8 _*_
# Author  : Tao
"""
"""

import os
from PIL import Image
from skimage import color
import numpy as np
import re
import cv2
from easydict import EasyDict as edict
from scipy import misc
from config import *
from utils import *


args = parse_args()
np.random.seed(args.seed)

im_path_list = get_file_path_list(args.imdir)

# resize the maximum side length of the image to 400
# and Aggregate all frames together, as [seq, h, w, c]
h, w, c = np.array(Image.open(im_path_list[0])).shape
frac = min(min(1. * args.max_side / h, 1. * args.max_side / w), 1.0)
if frac < 1.0:
    h, w, c = cv2.resize(np.array(Image.open(im_path_list[0])),
                         (int(frac * w), int(frac * h))).shape

im_seq = np.zeros((len(im_path_list), h, w, c), dtype=np.uint8)

for i in range(len(im_path_list)):
    if frac < 1.0:
        im_seq[i] = cv2.resize(np.array(Image.open(im_path_list[i])), (w, h))
    else:
        im_seq[i] = np.array(Image.open(im_path_list[i]))
print('Total Video Shape: ', im_seq.shape)

