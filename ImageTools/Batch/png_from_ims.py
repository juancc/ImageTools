"""
Remove background of all the images in a folder
Images most be in format:
Foreground = name_0.jpg
Background = name_1.jpg

JCA
"""

import os
import argparse
from pathlib import Path

from tqdm import tqdm
import cv2

from ImageTools.png_from_ims import create_png_from_ims
from ImageTools.auxfunc import create_out_dir

parser = argparse.ArgumentParser(
                prog='PNGfromPath',
                description='Remove background of all the images in a folder')

parser.add_argument('path', help='Image path or directory containing images') 
parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.1)
parser.add_argument('-c', '--crop', help='Crop image around largest contour', action='store_true')
parser.add_argument('-b', '--background', help='Keep image background', action='store_true')
parser.add_argument('-u', '--hull', help='Use convex hull for mask generation', action='store_true')



def main(path, crop, threshold, keep_bg=False, hull=False):
    output_dir = create_out_dir(path)
    files = list(Path(path).glob('**/*'))
    names = set([f.name.split('_')[0] for f in files if not f.name.startswith('.')])

    ext = files[0].suffix

    for n in tqdm(names):
        errs = []
        try:
            bck = os.path.join(path, f'{n}_0{ext}')
            fgd = os.path.join(path, f'{n}_1{ext}')

            im0 = cv2.imread(bck)
            im1 = cv2.imread(fgd)

            ret, out = create_png_from_ims(im0, im1, threshold=threshold, crop=crop, keep_bg=keep_bg, hull=hull)
            if ret:
                out_filepath = os.path.join(output_dir, f'{n}_3.png')

                cv2.imwrite(out_filepath, out)
        except Exception as e:
            errs.append(n)

    if errs: print(f' - {len(errs)} files with errors: {errs}')

if __name__ == '__main__':
    args = parser.parse_args()

    main(args.path, args.crop, threshold=float(args.threshold), keep_bg=args.background, hull=args.hull)