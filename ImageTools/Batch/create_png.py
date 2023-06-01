"""
Create PNG from images in folder

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
                prog='ImageTools',
                description='Apply image transformation to images')

parser.add_argument('path', help='Image path or directory containing images') 
parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')
parser.add_argument('-c', '--color', help='Background color of the image, available: white, black, green ', default='white')



def main(path):
    output_dir = create_out_dir(path)
    files = list(Path(path).glob('**/*'))
    for filepath in tqdm(files, total=len(files)):
        err = []
        try:
            im = cv2.imread(str(filepath))

            out = create_png(im, show_change=args.show, bck_color=args.color)
            out_filename = f'{filepath.name.split(".")[0]}.png'
            out_filepath = os.path.join(output_dir, out_filename)

            cv2.imwrite(out_filepath, out)
        except Exception as e:
            err.append(str(filepath))

    if err: print(err)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.path

    main(path)