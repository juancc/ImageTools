"""
Create a PNG image from JPG image

V0 
- Source image with a plain color

JCA
"""

import cv2
import numpy as np

from ImageTools.auxfunc import automatic_contour,\
      draw_contour, show, create_out_dir, blend

def create_png(src, show_change=False, color=(255,255,255)):
    """return a PNG image with automatic background detection"""
    hull, _, hull_center = automatic_contour(src, convex_hull=False)

    alpha = np.zeros(src.shape)
    alpha = draw_contour(alpha, hull, hull_center, color=(255,255,255), thickness=-1)

    if show_change:
        show(alpha)

    # Remove other pixels of background
    mask = alpha/255
    bck = np.zeros(src.shape)+255
    src =  blend(bck, src, mask)

    return np.dstack([src, alpha[:,:,0]])


if __name__ == '__main__':
    import os
    import argparse
    from pathlib import Path

    from tqdm import tqdm

    parser = argparse.ArgumentParser(
                    prog='CreatePNG',
                    description='Remove background from image')

    parser.add_argument('path', help='Image path ') 
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')

    args = parser.parse_args()
    path = args.path


    im = cv2.imread(str(path))

    out = create_png(im, show_change=args.show)
    out_filepath = f'{path.split(".")[0]}_out.png'

    cv2.imwrite(out_filepath, out)

