import torchvision
import torch
import torchvision
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import json
import ezdxf


print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())

import sys
# import sys
# sys.path.append("..")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

def show_anns(anns):
    if len(anns) == 0:
        return
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    ax = plt.gca()
    ax.set_autoscale_on(False)

    img = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 4))
    img[:,:,3] = 0
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.concatenate([np.random.random(3), [0.35]])
        img[m] = color_mask
    ax.imshow(img)

    
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    


def contours_to_svg(contours, output_filename, image_size):
    with open(output_filename, 'w') as svg_file:
        svg_file.write('<svg width="{0}" height="{1}" xmlns="http://www.w3.org/2000/svg">\n'.format(image_size[1], image_size[0]))
        
        for contour in contours:
            points = ' '.join([f'{point[0][0]},{point[0][1]}' for point in contour])
            svg_file.write(f'<polyline points="{points}" style="fill:none;stroke:black;stroke-width:1" />\n')
        
        svg_file.write('</svg>')
    print(f"SVG file saved as {output_filename}")


sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

mask_generator = SamAutomaticMaskGenerator(sam)

############### using SAM ############ 

image = cv2.imread('4.png')
masks = mask_generator.generate(image)
blank_image = np.zeros((image.shape[0], image.shape[1], image.shape[2]), dtype=np.uint8)

all_contours = []
##### dxf approach #### 
doc = ezdxf.new(dxfversion='R2010')
msp = doc.modelspace()

for mask in masks:
    # Convert boolean array to uint8
    binary_mask_uint8 = (mask['segmentation'] * 255).astype(np.uint8)

    # Find contours
    contours, hierarchy = cv2.findContours(binary_mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        ## to make sure contour is closed ####
        if not np.array_equal(contour[0], contour[-1]):
            first_point_reshaped = contour[0].reshape(1, 1,2) 
            contour = np.vstack([contour, first_point_reshaped])  

        #### to dxf ####       
        points = contour.reshape(-1, 2).tolist()
        msp.add_lwpolyline(points)
        all_contours.append(contour)
    

#### dxf approach ##### 
dxf_filename = "contours_upd.dxf"
doc.saveas(dxf_filename)

cv2.drawContours(image, all_contours, -1, (0, 255, 0), 2)

# Resize the image to fit the screen
screen_resolution = 1024, 768  # Example screen resolution; adjust as needed
scale_width = screen_resolution[0] / image.shape[1]
scale_height = screen_resolution[1] / image.shape[0]
scale = min(scale_width, scale_height)
window_width = int(image.shape[1] * scale)
window_height = int(image.shape[0] * scale)

resized_image = cv2.resize(image, (window_width, window_height))
cv2.imshow('Contours', resized_image)
cv2.waitKey(0)  # Wait for a key press to close the image window
cv2.destroyAllWindows()