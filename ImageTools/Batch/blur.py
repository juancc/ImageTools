"""
Apply Gaussian Blur to all the images on folder

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
                prog='ImageBlur',
                description='Apply Gaussian Blur to all the images on folder')

parser.add_argument('path', help='Image path or directory containing images') 




def main(path, args):
    output_dir = create_out_dir(path)
    files = list(Path(path).glob('**/*'))
    for filepath in tqdm(files, total=len(files)):
        err = []
        try:
            im = cv2.imread(str(filepath))

            out = cv2.GaussianBlur(im,(5,5),0)
            out_filename = f'{filepath.name.split(".")[0]}.png'
            out_filepath = os.path.join(output_dir, out_filename)

            cv2.imwrite(out_filepath, out)
        except Exception as e:
            err.append(str(filepath))

    if err: print(err)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.path

    main(path, args)