"""
Create PNG from two images: remove background from image difference

JCA
"""
import numpy as np
import cv2

from ImageTools.difference import is_change
from ImageTools.auxfunc import show, draw_contour, get_hull



def create_png_from_ims(bck, fgd, threshold=0.1, show_change=False, color=(255,255,255)):
    """Create a PNG image from two images using their absolute difference.
        : param im0 : (np.array) background
        : param im1 : (np.array) Image to remove background
        : param threshold : (int) Percentage of pixels that changed to be considered a change
        : param show_change : (bool) Show changes on image for visual debugging
        : param color : (tuple) color to replace the background
    """
    ret, thresh = is_change(bck, fgd, threshold=threshold, min_change=30)

    # If there is not change return None
    if not ret:
        print('There is not change between the images')
        False, None
    
    # Dilate to get internal parts
    dilation = cv2.dilate(thresh, (5,5), iterations=1)

    # Find contours to only get the largest one
    contours, hierarchy = cv2.findContours(dilation.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull, hull_area, hull_center = get_hull(contours, convex_hull=False)
    
    alpha = np.zeros(fgd.shape)
    alpha = draw_contour(alpha, hull, hull_center, color=255, thickness=-1)[:,:,0]

    if show_change:
        im_change = np.array(fgd)
        im_change[alpha.astype(bool)] = (0,255,0)
        show(im_change)

    # Remove other pixels of background
    neg_alpha = -1*(alpha/255 -1)
    fgd[neg_alpha.astype(bool)] = color

    return True, np.dstack([fgd, alpha])



    
if __name__ == '__main__':
    """Use as an independent script"""
    import argparse


    parser = argparse.ArgumentParser(
                    prog='PNGfromIMS',
                    description='Create PNG from two images: remove background from image difference')

    parser.add_argument('im0', help='Background')
    parser.add_argument('im1', help='Foreground') 

    parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.1)
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')


    args = parser.parse_args()


    im0 = cv2.imread(args.im0)
    im1 = cv2.imread(args.im1)

    ret, ans = create_png_from_ims(im0, im1, threshold=float(args.threshold), show_change=args.show)
    if ret: cv2.imwrite('/Users/juanc/Downloads/out.png', ans)


