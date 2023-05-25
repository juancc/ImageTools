"""
Create a PNG image from JPG image

V0 
- Source image with a plain color

JCA
"""

import cv2
import numpy as np

from ImageTools.auxfunc import automatic_contour, draw_contour, show

def create_png(src):
    """return a PNG image with automatic background detection"""
    hull, _, hull_center = automatic_contour(src, convex_hull=False)

    alpha = np.zeros(src.shape)
    alpha = draw_contour(alpha, hull, hull_center, color=255, thickness=-1)

    return np.dstack([src, alpha[:,:,0]])


if __name__ == '__main__':
    im = cv2.imread('/Users/juanc/Downloads/SASVAR_clear/4.jpg')
    out = create_png(im)
    cv2.imwrite('/Users/juanc/Downloads/out.png', out)
