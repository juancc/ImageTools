# ImageTools
Console tools for image processing. The ImageTools repository contains scripts for perfoming:
- Individual image processing located under ImageTools 
- Batch processing: the scripts perform a transformation of all the images inside a folder and subfolders. The result are placed inside a new folder with the same name as the source directoru plus '_out'. The scripts are located on ImageTools/Batch.

Run the scripts following the next pattern:

```bash
python -m ImageTools.Batch.script_name -A --args /image/path.png
```

# Tools
## Create PNG (Alpha-mated images)
Generate a transparency image and save as PNG. Automatic background subtraction from plain colors. Four backround colors: White, black, green and auto. Im auto mode: the foreground detection is based on the most common color of the image. Example auto mode transparency generator:

![alt text](https://github.com/juancc/ImageTools/blob/main/Assets/Img/ex_create_png.png?raw=true)

 ### Usage
```bash
python -m ImageTools.Batch.png_from_ims  [-s] [-c COLOR] [-x] path
```

### Positional arguments:
> __path:__     Image path or directory containing images

### Optional arguments:
> __-s__, --show &emsp;&emsp;&emsp;       Show changes on image for visual debugging
> 
> __-c COLOR__, --color     Background color of the image, available: white, black, green or auto
>
> __-x__, --convex_hull        Get alpha channel with convex hull



## Cropper
Batch crop part of all the images located in a folder and subfolders. There are available 4 ways to crop the images:
- Square centered: crop a square centered of the image with a specified size 
- Y-axis range: crop a range of the image in the y-axis
- X-axis range: crop a range of the image in the x-axis
- Automatic: crop arrount the largest blob in the alpha channel

Image cropper examples:

![alt text](https://github.com/juancc/ImageTools/blob/main/Assets/Img/ex_cropper.png?raw=true)


### Usage: 
```bash
python -m ImageTools.Batch.cropper [-s SIZE] [-y YRANGE] [-x XRANGE] [-q QUALITY] [-a] path
```

### Positional arguments:
>  __path__ :     Source directory

### Optional arguments:
>  __-s SIZE__, --size               Size of the side cropped area centered on the image
>  
>  __-y YRANGE__, --yrange     Range of image in y axis (y_init, y_final)
>  
>  __-x XRANGE__, --xrange     Range of image in x axis (x_init, x_final)
>  
>  __-q QUALITY__, --quality    Output file image quality
>  
>  __-a__, --auto                        Crop automatic based alpha channel



## Resize
Scale all the images inside folder and subfolders. This script creates a new folder in the same location with the same name plus '_resized'. 

### Usage:
```bash
python -m ImageTools.Batch.ImageResize [-h] [-s SCALE] [-q QUALITY] path
```

### Positional arguments:
>  __path__                                       Image path or directory containing images

### Optional arguments:
>  __-s SCALE__, --scale               Scale both widht and height
>                        
>  __-q QUALITY__, --quality        Output file image quality
>                        

## PNG from images
Generate a transparency image by removing the background using two images (Background and Foreground) and save as PNG. 


