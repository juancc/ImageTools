"""
Create PNG from two images: remove background from image difference

JCA
"""

from ImageTools.difference import is_change
from ImageTools.auxfunc import show


def create_png_from_ims(im0, im1, threshold=0.1, show_change=False):
    """Create a PNG image from two images using their absolute difference.
        : param im0 : (np.array) 3D matrix of the values of the image
        : param im1 : (np.array) 3D matrix of the values of the image
        : param threshold : (int) Percentage of pixels that changed to be considered a change
        : param show_change : (bool) Show changes on image for visual debugging
    """
    ret, thresh = is_change(im0, im1, threshold=threshold, show_change=show_change)

    # If there is not change return None
    if not ret:
        print('There is not change between the images')
        return
    

    
if __name__ == '__main__':
    """Use as an independent script"""
    import argparse

    import cv2

    parser = argparse.ArgumentParser(
                    prog='PNGfromIMS',
                    description='Create PNG from two images: remove background from image difference')

    parser.add_argument('im0', help='Image 1')
    parser.add_argument('im1', help='Image 2') 

    parser.add_argument('-t', '--threshold', help='Percentage of pixels that changed to be considered a change', default=0.2)
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')


    args = parser.parse_args()


    im0 = cv2.imread(args.im0)
    im1 = cv2.imread(args.im1)

    ans = create_png_from_ims(im0, im1, threshold=float(args.threshold), show_change=args.show)
