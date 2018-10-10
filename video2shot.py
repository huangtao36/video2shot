# _*_coding:utf-8 _*_
# Author  : Tao
"""
"""

from PIL import Image
import cv2
from config import *
from utils import *
from cpd_auto import cpd_auto


def vid2shots(img_seq, max_shots=5, vmax=0.6, col_bins=40):
    """
    Convert a given video into number of shots
    img_seq: (n,h,w,c): 0-255: np.uint8: RGB
    shot_idx: (k,): start Index of shot: 0-indexed
    shotScore: (k,): First change ../lib/kts/cpd_auto.py return value to
                     scores2 instead of costs (a bug)
    """
    x = np.zeros((img_seq.shape[0], compute_features(img_seq[0], col_bins).size))
    print('Feature Matrix shape:', x.shape)
    for n in range(img_seq.shape[0]):
        x[n] = compute_features(img_seq[n], col_bins)

    k = np.dot(x, x.T)
    shot_idx, _ = cpd_auto(k, max_shots - 1, vmax)
    shot_idx = np.concatenate(([0], shot_idx))
    return shot_idx


if __name__ == '__main__':

    args = parse_args()
    np.random.seed(args.seed)

    project_par_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
    data_root_path = os.path.join(project_par_path,
                                  'Dataset',
                                  'ydata-tvsum50-v1_1',
                                  'sample_video')

    for dir_ in os.listdir(data_root_path):
        args.imdir = os.path.join(data_root_path, dir_)
        if not os.path.isdir(args.imdir):
            continue

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

        # run the algorithm
        shot_index = vid2shots(im_seq, max_shots=args.max_shots, vmax=args.vmax,
                               col_bins=args.col_bins)

        print(args.imdir)
        print(shot_index)
