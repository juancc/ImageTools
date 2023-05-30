"""
Detect changes on a pair of images

JCA
"""
import numpy as np
import cv2

from ImageTools.auxfunc import show

def is_change(im0, im1, threshold=0.1, show_change=False, min_change=30):
    """Detect if there is a change between two images. The change is calculated by the absolute 
    difference between the images. If the change is greater than a value is counted as if the pixel changes.
    Return True if the number of pixels that changed are greated thant the thresh parameter.
    Images most be of the same size!!

        : param im0 : (np.array) 3D matrix of the values of the image
        : param im1 : (np.array) 3D matrix of the values of the image
        : param threshold : (int) Percentage of pixels that changed to be considered a change
        : param show_change : (bool) Show changes on image for visual debugging
        : param min_change : (int) Minimum pixel chamge to be considered 
        : return (Bool): If there is a change in the images
        : return (np.array): Threshold image
    """
    # Check if images have the same dimensions.
    # Raise a ValueError otherwise
    if im0.shape != im1.shape:
        raise ValueError(f'Image dimension most be the same: Image sizes: {im0.shape} and {im0.shape}')
    
    diff = cv2.absdiff(im0, im1)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
                diff, min_change, 255,
                cv2.THRESH_BINARY)[1]/255

    changed = thresh.sum() / np.prod(thresh.shape)

    # Show changes between images
    if show_change:
        im_change = im0
        im_change[thresh.astype(bool)] = (0,255,0)

        show(im_change)
        print(f'{thresh.sum()} pixels changed of {np.prod(thresh.shape)}')

    return changed>threshold, thresh





if __name__ == '__main__':
    """Use as an independent script"""
    import argparse

    parser = argparse.ArgumentParser(
                    prog='IsChange',
                    description='Return if an image is changed')

    parser.add_argument('im0', help='Image 1')
    parser.add_argument('im1', help='Image 2') 

    parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.2)
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')



    args = parser.parse_args()


    im0 = cv2.imread(args.im0)
    im1 = cv2.imread(args.im1)

    ans = is_change(im0, im1, threshold=float(args.threshold), show_change=args.show)
    
    print(f'  Image Changed: {ans}')


