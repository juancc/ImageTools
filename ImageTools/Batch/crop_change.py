"""
Crop part of the images that changes using two images: background and foreground

JCA
"""

import os
import argparse
from pathlib import Path

from tqdm import tqdm
import cv2

from ImageTools.crop_change import crop_change
from ImageTools.auxfunc import create_out_dir

parser = argparse.ArgumentParser(
                prog='PNGfromPath',
                description='Remove background of all the images in a folder')

parser.add_argument('path', help='Image path or directory containing images') 
parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.1)
parser.add_argument('-m', '--min', help=' Minimum pixel chamge to be considered ', default=30)
parser.add_argument('-u', '--hull', help='Use convex hull for mask generation', action='store_true')



def main(path, threshold, min_change, hull=False):
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

            ret, out = crop_change(im0, im1, threshold=threshold, hull=hull,
                                            min_change=int(min_change))
            if ret:
                out_filepath = os.path.join(output_dir, f'{n}_3.png')

                cv2.imwrite(out_filepath, out)
        except Exception as e:
            errs.append(n)

    if errs: print(f' - {len(errs)} files with errors: {errs}')

if __name__ == '__main__':
    args = parser.parse_args()

    main(args.path,float(args.threshold), args.min, hull=args.hull)