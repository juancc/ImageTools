"""
Crop all the images in folder
The crop is cententered and squared

JCA
"""
import os
import argparse

import cv2 as cv
import numpy as np
from tqdm import tqdm

from ImageTools.auxfunc import create_out_dir

# Square side size of the cropped area
SIZE = 100
EXT = 'jpg'

parser = argparse.ArgumentParser(
                    prog = 'Folder Image Cropper',
                    description = 'Crop all images in folder')

parser.add_argument('path', help='Source directory', type=str)
parser.add_argument('-s', '--size', help='Size of the side cropped area', default=SIZE, type=int)


def main(path, size):
    target_path = create_out_dir(path, tag='crop')

    # List of files with errors
    err = []

    for p in tqdm(os.listdir(path)):
        filepath = os.path.join(path, p)
        name = p.split('.')[0]
        target = os.path.join(target_path, name +'.'+ EXT)

        try:
            im = cv.imread(filepath)
            h,w,_ = im.shape
            x_i = int((h - size)/2)
            y_i = int((w - size)/2)

            im = im[x_i:x_i+size, y_i:y_i+size]

            cv.imwrite(target, im)
        except Exception as e:
            err.append(p)

    print(f'Could not crop the next files: {p}')


if __name__ == '__main__': 
    args = parser.parse_args()
    main(args.path, args.size)