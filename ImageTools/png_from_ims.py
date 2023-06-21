"""
Create PNG from two images: remove background from image difference

JCA
"""
import numpy as np
import cv2

from ImageTools.difference import is_change
from ImageTools.auxfunc import show, draw_contour, get_hull



def create_png_from_ims(bck, fgd, threshold=0.1, show_change=False, color=(255,255,255), crop=False, keep_bg=False):
    """Create a PNG image from two images using their absolute difference.
        : param im0 : (np.array) background
        : param im1 : (np.array) Image to remove background
        : param threshold : (int) Percentage of pixels that changed to be considered a change
        : param show_change : (bool) Show changes on image for visual debugging
        : param color : (tuple) color to replace the background
        : param crop : (bool) crop image arround largest contour
    """
    ret, thresh = is_change(bck, fgd, threshold=threshold, min_change=30)

    # If there is not change return None
    if not ret:
        print('There is not change between the images')
        return False, None
    
    # Dilate to get internal parts
    dilation = cv2.dilate(thresh, (5,5), iterations=1)

    # Find contours to only get the largest one
    contours, hierarchy = cv2.findContours(dilation.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull, hull_area, hull_center, main_contour = get_hull(contours, convex_hull=False)
    
    alpha = np.zeros(fgd.shape)
    alpha = draw_contour(alpha, hull, hull_center, color=255, thickness=-1)[:,:,0]

    if show_change:
        im_change = np.array(fgd)
        im_change[alpha.astype(bool)] = (0,255,0)
        show(im_change)

    # Remove other pixels of background
    if not keep_bg:
        neg_alpha = -1*(alpha/255 -1)
        fgd[neg_alpha.astype(bool)] = color

    # Image with alpha channel
    out = np.dstack([fgd, alpha])

    # Crop around largest contour
    if crop:
        x,y,w,h  = cv2.boundingRect(main_contour)
        if show_change:
            cv2.rectangle(fgd,(x,y),(x+w,y+h),(0,255,0),2)
            show(fgd)
        out = out[y:y+h, x:x+w]

    return True, out



    
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
    parser.add_argument('-c', '--crop', help='Crop image around largest contour', action='store_true')
    parser.add_argument('-b', '--background', help='Keep image background', action='store_true')





    args = parser.parse_args()


    im0 = cv2.imread(args.im0)
    im1 = cv2.imread(args.im1)

    ret, ans = create_png_from_ims(im0, im1, threshold=float(args.threshold), show_change=args.show, crop=args.crop, keep_bg=args.background)

    out_filepath = f'{args.im0.split(".")[0]}_out.png'

    if ret: cv2.imwrite(out_filepath, ans)


