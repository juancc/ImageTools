"""
Calculate and display color histogram

JCA
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def calc_hist(im):
    """Calculate imagecolor histogram of an image
        : param im : (np.array) CV loaded image
    """
    im_hist = [ cv2.calcHist([im], [col_i], None, [256], [0, 256])\
                for col_i, col in enumerate(['b', 'g', 'r']) ]
    im_hist = np.vstack(im_hist)

    # divide per image area
    h, w = im.shape[:2]
    area = h*w
    im_hist /= area

    # Normalize
    # im_hist /= max(im_hist)

    return im_hist

def draw_hist(histogram, color_alpha=0.2)->None:
    """
        Display the color distribution of main classes. 
        The histogram of percentage of pixel count per color of all the images of a class
        Histogram of pixel count / image size per color
    """
    # pixel count per RGB (0-256) per chanel for all the images per category
    # B: [0:256]
    # G: [256:512]
    # R: [512:768]  

    fig = plt.figure() 
    plt.fill_between(np.arange(0, 256, 1), histogram[512:768].T[0] , color='red', alpha=color_alpha)
    plt.fill_between(np.arange(0, 256, 1), histogram[0:256].T[0] , color='blue', alpha=color_alpha)
    plt.fill_between(np.arange(0, 256, 1), histogram[256:512].T[0] , color='green', alpha=color_alpha)
        
    plt.show() 

def show_histogram(im):
    """Calculate and display color histogram"""
    hist = calc_hist(im)
    draw_hist(hist)

if __name__ == '__main__':
    """Use as an independent script"""
    print('Image color histogram')
    import argparse

    parser = argparse.ArgumentParser(
                    prog='ShowHistogram',
                    description='Show color histogram of image')

    parser.add_argument('im_path', help='Image path')


    args = parser.parse_args()

    im = cv2.imread(args.im_path)
    show_histogram(im)