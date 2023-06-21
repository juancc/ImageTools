"""
Crop all the images in folder
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


from ImageTools.auxfunc import create_out_dir
from ImageTools.cropper import cropper


parser = argparse.ArgumentParser(
                    prog = 'Folder Image Cropper',
                    description = 'Crop all images in folder')

parser.add_argument('path', help='Source directory', type=str)
parser.add_argument('-s', '--size', help='Size of the side cropped area centered on the image', 
                    default=None)
parser.add_argument('-y', '--yrange', help='Range of image in y axis (y_init,y_final)', 
                    default=None)
parser.add_argument('-q', '--quality', help='Output file image quality', default=90)


def main(path, size, y_range, quality):
    output_dir = create_out_dir(path, tag='crop')

    # List of files with errors
    err = []
    files = list(Path(path).glob('**/*'))

    for filepath in tqdm(files, total=len(files)):
        try:
            im = cropper(filepath, size=size, y_range=y_range)

            out_filename = f'{filepath.name.split(".")[0]}.png'
            out_filepath = os.path.join(output_dir, out_filename)

            cv2.imwrite(out_filepath, im,  [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)])
        except Exception as e:
            err.append(filepath.name)

    print(f'Could not crop the next files: {err}')


if __name__ == '__main__': 
    args = parser.parse_args()

    # If size provided crop will be square centered on the image
    size = int(args.size) if args.size else None
    y_range = literal_eval(args.yrange) if args.yrange else None

    main(args.path, size, y_range, args.quality)