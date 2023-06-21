"""
Image cropper
Area specifications:
 - size: The crop is cententered and squared
 - yrange: Range of the image in the y axis


JCA
"""
import os
import argparse
from pathlib import Path
from ast import literal_eval

import cv2
import numpy as np
from tqdm import tqdm


def cropper(filepath, size=None, y_range=None):
    """Crop image in different modes:
        :param size: Squared centered on the image with side as size
        :param y_range: (yi,yf) range of the image in y axis 
    """
    im = cv2.imread(str(filepath), cv2.IMREAD_UNCHANGED)
    h,w,_ = im.shape
    if size:
        xi = int((h - size)/2)
        yi = int((w - size)/2)

        im = im[yi:yi+size, xi:xi+size]
    elif y_range:
        im = im[y_range[0]:y_range[1], 0:w]

    else:
        print('Area to crop not provided')
        exit()
    
    return im


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog = 'Folder Image Cropper',
                    description = 'Crop all images in folder')

    parser.add_argument('path', help='Source file', type=str)
    parser.add_argument('-s', '--size', help='Size of the side cropped area centered on the image', 
                        default=None)
    parser.add_argument('-y', '--yrange', help='Range of image in y axis (y_init,y_final)', 
                        default=None)
    parser.add_argument('-q', '--quality', help='Output file image quality', default=90)


    args = parser.parse_args()

    # If size provided crop will be square centered on the image
    size = int(args.size) if args.size else None
    y_range = literal_eval(args.yrange) if args.yrange else None

    im = cropper(args.path, size=size, y_range=y_range)

    out_filepath = f'{args.path.split(".")[0]}_crop.png'


    cv2.imwrite(out_filepath, im, [int(cv2.IMWRITE_JPEG_QUALITY), int(args.quality)])