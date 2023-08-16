"""
Crop part of the image that changed in two images

JCA
"""

import numpy as np
import cv2

from ImageTools.difference import is_change
from ImageTools.auxfunc import show, draw_contour, get_hull



def crop_change(bck, fgd, threshold=0.1, show_change=False, hull=False,
                        min_change=30, border=0):
    """Create a PNG image from two images using their absolute difference.
        : param im0 : (np.array) background
        : param im1 : (np.array) Image to remove background
        : param threshold : (int) Percentage of pixels that changed to be considered a change
        : param show_change : (bool) Show changes on image for visual debugging
        : param color : (tuple) color to replace the background
        : param crop : (bool) crop image arround largest contour
        : param min_change : (int) Minimum pixel chamge to be considered 
        : param border: (float) Percentage to increase in all directions 

    """
    ret, thresh = is_change(bck, fgd, threshold=threshold, min_change=min_change)

    # If there is not change return None
    if not ret:
        print('There is not change between the images')
        return False, None
    
    # Dilate to get internal parts
    dilation = cv2.dilate(thresh, (5,5), iterations=1)

    # Find contours to only get the largest one
    contours, hierarchy = cv2.findContours(dilation.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hull, hull_area, hull_center, main_contour = get_hull(contours, convex_hull=hull)
    

    if show_change:
        alpha = np.zeros(fgd.shape)
        alpha = draw_contour(alpha, hull, hull_center, color=255, thickness=-1)[:,:,0]
        im_change = np.array(fgd)
        im_change[alpha.astype(bool)] = (0,255,0)
        show(im_change)

    # Crop around largest contour
    x,y,w,h  = cv2.boundingRect(main_contour)
    x_i, y_i, w_i, h_i = x,y,w,h 
    if border:
        dx = border * w/2
        dy = border * h/2
        x = int(max(0, x-dx))
        y = int(max(0, y-dy))

        w = w+2*dx if x+w+2*dx < fgd.shape[1] else fgd.shape[1]-x
        h = h+2*dy if y+h+2*dy < fgd.shape[0] else fgd.shape[0]-y

        w = int(w)
        h = int(h)

    if show_change:
        cv2.rectangle(fgd,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.rectangle(fgd,(x_i,y_i),(x_i+w_i,y_i+h_i),(0,255,0),2)

        show(fgd)
    out = fgd[y:y+h, x:x+w]

    return True, out



    
if __name__ == '__main__':
    """Use as an independent script"""
    import argparse


    parser = argparse.ArgumentParser(
                    prog='CropChange',
                    description='Crop images based the change of of background foreground')

    parser.add_argument('im0', help='Background')
    parser.add_argument('im1', help='Foreground') 

    parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.1)
    parser.add_argument('-m', '--min', help=' Minimum pixel chamge to be considered ', default=30)

    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')
    parser.add_argument('-u', '--hull', help='Use convex hull for mask generation', action='store_true')
    parser.add_argument('-b', '--border', help='Percentage to increase in all directions', default=0)




    args = parser.parse_args()


    im0 = cv2.imread(args.im0)
    im1 = cv2.imread(args.im1)

    ret, ans = crop_change(im0, im1, threshold=float(args.threshold), 
                                   show_change=args.show,
                                   hull=args.hull,
                                   min_change=int(args.min),
                                   border=float(args.border),
                                   )

    out_filepath = f'{args.im0.split(".")[0]}_out.png'

    if ret: cv2.imwrite(out_filepath, ans)