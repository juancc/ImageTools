"""
Apply image transformations to images 

JCA
"""
import os
import argparse
from pathlib import Path

from tqdm import tqdm
import cv2

from ImageTools.create_png import create_png

parser = argparse.ArgumentParser(
                    prog='ImageTools',
                    description='Apply image transformation to images')

parser.add_argument('path', help='Image path or directory containing images') 
parser.add_argument('-p', '--png', help='Create PNG image', action='store_true')

def main(path, png):

    if os.path.isdir(path):
        output = path.split(os.sep)[-1]+'_out'

        output_dir = os.path.join(os.sep.join(path.split(os.sep)[:-1]), output)
        os.makedirs(output_dir, exist_ok=True)
        print(f'    - Output directory: {output_dir}')
        files = list(Path(path).glob('**/*'))
        for filepath in tqdm(files, total=len(files)):
            err = []
            try:
                im = cv2.imread(str(filepath))

                if png:
                    out = create_png(im)

                    out_filename = f'{filepath.name.split(".")[0]}.png'
                    out_filepath = os.path.join(output_dir, out_filename)

                    cv2.imwrite(out_filepath, out)
            except Exception as e:
                err.append(str(filepath))

            if err: print(err)

        
    

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.path, args.png)