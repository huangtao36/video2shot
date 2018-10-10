# _*_coding:utf-8 _*_
# Author  : Tao
"""
This Code is ...
"""
import argparse


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(
        description='Creates a tracker using deepmatch and epicflow')

    parser.add_argument(
        '-out', dest='outdir',
        help='Directory to save output.',
        default='./outdir', type=str)
    parser.add_argument(
        '-imdir', dest='imdir',
        help='Directory containing video images. Will be read ' +
        'alphabetically. Default is random Imagenet train video.',
        default='./imdir', type=str)
    parser.add_argument(
        '-fgap', dest='frameGap',
        help='Gap between frames while running tracker. Default 0.',
        default=0, type=int)
    parser.add_argument(
        '-n', dest='max_shots',
        help='Max number of shots to break into. Default 5.',
        default=50, type=int)
    parser.add_argument(
        '-d', dest='col_bins',
        help='Number of bins in RGBLAB histogram. Default 40. ',
        default=40, type=int)
    parser.add_argument(
        '-v', dest='vmax',
        help='Parameter for KTS, lower value means more clips. Default 0.6.',
        default=0.6, type=float)
    parser.add_argument(
        '-seed', dest='seed',
        help='Random seed for numpy and python.', default=2905, type=int)
    parser.add_argument(
        '-max_side', dest='max_side',
        help='Maximum side length of the picture.', default=400, type=int)

    args = parser.parse_args()
    return args
