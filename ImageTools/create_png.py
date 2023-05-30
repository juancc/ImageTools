"""
Create a PNG image from JPG image

V0 
- Source image with a plain color

JCA
"""

import cv2
import numpy as np

from ImageTools.auxfunc import automatic_contour, draw_contour, show, create_out_dir

def create_png(src, show_change=False, color=(255,255,255)):
    """return a PNG image with automatic background detection"""
    hull, _, hull_center = automatic_contour(src, convex_hull=False)

    alpha = np.zeros(src.shape)
    alpha = draw_contour(alpha, hull, hull_center, color=255, thickness=-1)

    if show_change:
        show(alpha)

    # Remove other pixels of background
    neg_alpha = -1*(alpha/255 -1)
    src[neg_alpha.astype(bool).all()] = color

    return np.dstack([src, alpha[:,:,0]])


if __name__ == '__main__':
    import os
    import argparse
    from pathlib import Path

    from tqdm import tqdm

    parser = argparse.ArgumentParser(
                    prog='ImageTools',
                    description='Apply image transformation to images')

    parser.add_argument('path', help='Image path or directory containing images') 
    parser.add_argument('-s', '--show', help='Show changes on image for visual debugging', action='store_true')

    args = parser.parse_args()
    path = args.path

    if os.path.isdir(path):
        output_dir = create_out_dir(path)
        files = list(Path(path).glob('**/*'))
        for filepath in tqdm(files, total=len(files)):
            err = []
            try:
                im = cv2.imread(str(filepath))

                out = create_png(im, show_change=args.show)
                out_filename = f'{filepath.name.split(".")[0]}.png'
                out_filepath = os.path.join(output_dir, out_filename)

                cv2.imwrite(out_filepath, out)
            except Exception as e:
                err.append(str(filepath))

        if err: print(err)

