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

MIN_AREA = 0.03
MAX_AREA = 0.95

def create_png(src, show_change=False, color=(255,255,255), bck_color='white', min_area=MIN_AREA,\
                max_area=MAX_AREA, convex_hull=False):
    """Return a PNG image with automatic background detection
    : param bck_color: (Str) background color of the image, available: white, black, green 
    : param min_area : (float) Min percentage of area to be considered
    : param max_area : (float) Max percentage of area to be considered. Avoid saving
      images that does not have mask 
    :param convex_hull : (Bool) Get alpha channel with convex hull

    """
    hull, area, hull_center = automatic_contour(src, convex_hull=convex_hull, bck=bck_color)

    if area < np.prod(src.shape[:-1])*min_area or area > np.prod(src.shape[:-1])*max_area:
        return

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

    parser = argparse.ArgumentParser(
                    prog='CreatePNG',
                    description='Remove background from image')

    parser.add_argument('path', help='Image path ') 
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')
    parser.add_argument('-c', '--color', help='Background color of the image, available: white, black, green ', default='white')
    parser.add_argument('-x', '--convex_hull', help='Get alpha channel with convex hull', action='store_true')



    args = parser.parse_args()
    path = args.path

    im = cv2.imread(str(path))

    out = create_png(im, show_change=args.show, bck_color=args.color, convex_hull=args.convex_hull)
    out_filepath = f'{path.split(".")[0]}_out.png'

    cv2.imwrite(out_filepath, out)


