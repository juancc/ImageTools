"""
Generate transparency image using COCO segmentation labels

JCA
"""
import os
import argparse
from pathlib import Path
import json

import numpy as np
import cv2
from tqdm import tqdm
from pycocotools import mask as cocomask

from ImageTools.auxfunc import create_out_dir, show, blend


parser = argparse.ArgumentParser(
                prog='PNGfromPath',
                description='Remove background of all the images in a folder')


parser.add_argument('ann_path', help='COCO annotation file in JSON format')
parser.add_argument('im_path', help='Directory containing images') 
parser.add_argument('-r', '--rle', help='Segmentation in RLE (Run Lenght Encode) format', action='store_true')



def main(ann_path, im_path, rle=False):

    output_dir = create_out_dir(im_path)

    # Image files
    files = list(Path(im_path).glob('**/*'))

    # Annotation file
    with open(ann_path, 'r') as f:
        ann = json.load(f)
    
    # Get image IDS. Create a dict {im_filename: id, ...}
    im_ids = {}
    for im_data in ann['images']:
        iid = im_data['id']
        file_name = im_data['file_name']

        im_ids[file_name] = iid

    # Get segmentation by ID
    segments_id = {}
    for seg_data in ann['annotations']:
        iid = seg_data['image_id']
        segmentation = seg_data['segmentation']

        segments_id[iid] = segmentation

    err = []
    for filepath in tqdm(files, total=len(files)):
        try:
            im = cv2.imread(str(filepath))

            name = filepath.name
            # get image ID
            iid = im_ids[name]
        
            # Get segmentation and generate mask
            seg = segments_id[iid]
            alpha = np.zeros(im.shape)

            fr_obj = cocomask.frPyObjects([seg], im.shape[0], im.shape[1])
            maskedArr = cocomask.decode(fr_obj)
            contours, _ = cv2.findContours(maskedArr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            alpha = cv2.drawContours(image=alpha, contours=contours, contourIdx=-1, 
                                    color=(255,255,255), thickness=-1, lineType=cv2.LINE_AA)

            # Remove other pixels of background
            mask = alpha/255
            bck = np.zeros(im.shape) +255
            im =  blend(bck, im, mask)

            # Save PNG
            out = np.dstack([im, alpha[:,:,0]])
            out_filepath = os.path.join(output_dir, f'{name.split(".")[0]}.png')
            cv2.imwrite(out_filepath, out)

        except Exception as e:
            err.append(name)
            continue


  
    
    if err: print(f'Error reading {len(err)} images')


if __name__ == '__main__':
    args = parser.parse_args()
    ann_path = args.ann_path
    im_path = args.im_path
    rle = args.rle


    main(ann_path, im_path, rle=rle)