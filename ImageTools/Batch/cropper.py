"""
Crop all the images in folder
The crop is cententered and squared

JCA
"""
import os
import argparse
from pathlib import Path

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
parser.add_argument('-q', '--quality', help='Output file image quality', default=90)

def main(path, size, quality):
    output_dir = create_out_dir(path, tag='crop')

    # List of files with errors
    err = []
    files = list(Path(path).glob('**/*'))

    for filepath in tqdm(files, total=len(files)):
        try:
            im = cv.imread(str(filepath), cv.IMREAD_UNCHANGED)
            h,w,_ = im.shape
            x_i = int((h - size)/2)
            y_i = int((w - size)/2)

            im = im[x_i:x_i+size, y_i:y_i+size]

            out_filename = f'{filepath.name.split(".")[0]}.png'
            out_filepath = os.path.join(output_dir, out_filename)

            cv.imwrite(out_filepath, im,  [int(cv.IMWRITE_JPEG_QUALITY), int(quality)])
        except Exception as e:
            err.append(filepath.name)

    print(f'Could not crop the next files: {err}')


if __name__ == '__main__': 
    args = parser.parse_args()
    main(args.path, args.size, args.quality)