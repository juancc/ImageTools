"""
Auxiliar functions for image tools

JCA
"""
import os

import cv2
import numpy as np


def auto_thresh(im):
    """Get threshold mask fore remove background of an image based 
    the mean and STD from each channel"""
    hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
        
    hue_std = np.std(hsv[:,:,0])
    hue_mean = np.mean(hsv[:,:,0])
    sat_std = np.std(hsv[:,:,1])
    sat_mean = np.mean(hsv[:,:,1])
    val_std = np.std(hsv[:,:,2])
    val_mean = np.mean(hsv[:,:,2])


    min = np.array([hue_mean - hue_std, sat_mean - sat_std, val_mean - val_std],np.uint8)
    max = np.array([hue_mean + hue_std, sat_mean + sat_std, val_mean + val_std],np.uint8)
    th = cv2.inRange(hsv, min, max)

    th = cv2.bitwise_not(th)
    return th



def automatic_contour(im, bck='white', convex_hull=True, **kwargs):
    """Contour is calculated automatic for images witout information
    Return object contour, area and centroid base background-object segmentation
        :param im: (np.array) image loaded for cv2
        :param bck: (int) background type (0:black, 1:white, 2:mixed)
        :convex_hull: (Bool) use convex hull for segmentation
    """
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    if bck == 'black':
        hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
        min = np.array([0, 0, 0],np.uint8)
        max = np.array([255, 170, 170],np.uint8)

        th = cv2.inRange(hsv, min, max)
        th = cv2.bitwise_not(th)

        # ret, th = cv2.threshold(gray, 0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    elif bck == 'white':
        hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)

        min = np.array([0, 30, 30],np.uint8)
        max = np.array([255, 255, 255],np.uint8)
        th = cv2.inRange(hsv, min, max)


    elif bck == 'green':
        # in LAB there are 2 color channels and 1 brightness channel:
        #   L-channel: Brightness value in the image
        #   A-channel: Red and green color in the image
        #   B-channel: Blue and yellow color in the image
        lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)
        a_channel = lab[:,:,1]
        th = cv2.threshold(a_channel,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        th = cv2.bitwise_not(th)

    elif bck=='auto':
        th = auto_thresh(im)

        
    # blur = cv2.GaussianBlur(gray,(3,3),0)
    dilation = cv2.dilate(th, (5,5), iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return get_hull(contours, convex_hull=convex_hull)


def get_hull(contours, convex_hull=True):
    """Return the largest contour"""
    hull = None
    hull_area = 0
    hull_center = None
    # Only consider the larges convex hull of the image
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)
        if M['m00'] > hull_area:
            im_hull = cv2.convexHull(c) if convex_hull else c

            hull = im_hull 
            hull_area = M['m00']

            # calculate x,y coordinate of center
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            hull_center = (cX, cY)
            
    return hull, hull_area, hull_center
    


def draw_contour(im, hull, hull_center, color=(0, 255, 0), thickness=2):
    """Draw contours"""
    cv2.drawContours(image=im, contours=[hull], contourIdx=-1, color=color, thickness=thickness, lineType=cv2.LINE_AA)
    # cv2.circle(im, hull_center, 8, (0, 255, 0), -1)
    return im


def show(im, window='window'):
    """Shortcut for display image with Opencv"""
    cv2.imshow(window,im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def create_out_dir(path, tag='out'):
    output = path.split(os.sep)[-1]+f'_{tag}'

    output_dir = os.path.join(os.sep.join(path.split(os.sep)[:-1]), output)
    os.makedirs(output_dir, exist_ok=True)
    print(f'    - Output directory: {output_dir}')

    return output_dir


def blend(im1, im2, alpha):
    """Alpha blend"""
    return (1-alpha)*im1 + alpha*im2