# 2DArchDraw-Segmentation-to-CAD
This tool automates the conversion of 2D architectural and commercial drawings into CAD formats. Using the Segmented Anything Model (SAM), it segments rooms and walls from top-view images, then accurately transforms these segments into CAD-ready formats. 
## Features

- Utilizes the SAM for precisely segment 2d architectural and commercial drawings.
- Converts segmented contours directly into CAD format, making the digital drafting process more efficient.
- Automated process from image input to CAD file output, reducing manual drawing and conversion time.

## Prerequisites

Before you run this application, ensure you have the following installed:
- Python 3.6 or newer
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- Torch and torchvision
- ezdxf

Install the required dependencies using requirements.txt file

```sh
pip install -r requirements.txt
```

## Installation
- Clone this repository to your local machine.
- Ensure all prerequisites are installed and all the libraries are already installed. 
- Download the required SAM model checkpoint file (sam_vit_h_4b8939.pth) and place it in the project's root directory. It can be downloaded from here https://github.com/facebookresearch/segment-anything?tab=readme-ov-file .

## Usage
To run the segmentation and conversion process, execute the script with the following command: 
```sh
python main.py
```
make sure the image is loaded in my case 4.png .   

## Output
The script outputs a CAD file (contours_upd.dxf) with the segmented architectural drawing contours. Additionally, it displays the segmented contours overlaid on the original image for visual verification.







