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
