"""
Resize images in folder structure

JCA
"""
import os
import argparse
from pathlib import Path

from tqdm import tqdm
import numpy as np
import cv2

from ImageTools.create_png import create_png
from ImageTools.auxfunc import  create_out_dir


parser = argparse.ArgumentParser(
                prog='ImageResize',
                description='Resize all the images on folder')

parser.add_argument('path', help='Image path or directory containing images')
parser.add_argument('-s', '--scale', help='Scale both widht and height', default=None)
parser.add_argument('-q', '--quality', help='Output file image quality', default=90)





def main(path, quality, scale=None):
    output_dir = create_out_dir(path, tag='resized')
    files = list(Path(path).glob('**/*'))
    for filepath in tqdm(files, total=len(files)):
        err = []
        try:
            im = cv2.imread(str(filepath), cv2.IMREAD_UNCHANGED)

            if scale:
                scale = float(scale)
                width = int(im.shape[1] * scale)
                height = int(im.shape[0] * scale)
                dim = (width, height)
            
                # resize image
                out = cv2.resize(im, dim)
            # TODO:
            # Implement other scale input types
            else:
                print('Not scale provided')
                exit()



            out_filename = f'{filepath.name.split(".")[0]}.png'
            out_filepath = os.path.join(output_dir, out_filename)

            cv2.imwrite(out_filepath, out, [int(cv2.IMWRITE_JPEG_QUALITY), int(quality)])
        except Exception as e:
            err.append(str(filepath))

    if err: print(err)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.path
    scale = args.scale

    main(path, args.quality, scale=scale)

