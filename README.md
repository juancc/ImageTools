# ImageTools
Console tools for image processing. The ImageTools repository contains scripts for perfoming:
- Individual image processing located under ImageTools 
- Batch processing: the scripts perform a transformation of all the images inside a folder and subfolders. The result are placed inside a new folder with the same name as the source directoru plus '_out'. The scripts are located on ImageTools/Batch.

Run the scripts following the next pattern:

`python -m ImageTools.Batch.script_name -A --args /image/path.png `

# Tools
## Create PNG (Alpha-mated images)
Generate a transparency image and save as PNG. Automatic background subtraction from plain colors. Four backround colors: White, black, green and auto. Im auto mode: the foreground detection is based on the most common color of the image. Example auto mode transparency generator:

![alt text](https://github.com/juancc/ImageTools/blob/main/Assets/Img/ex_create_png.jpg?raw=true)

 


## Cropper

## Resize

## PNG from images



