{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import torch\
import numpy as np\
import cv2\
from pytorch_grad_cam import GradCAM\
from pytorch_grad_cam.utils.image import show_cam_on_image\
\
def gradcam_heatmap(model, target_layer, input_tensor, orig_image):\
    """\
    Generate a Grad-CAM heatmap.\
    Args:\
        model: PyTorch model (e.g., ArtifactDetector.backbone)\
        target_layer: model layer to visualize (e.g., model.backbone.blocks[-1])\
        input_tensor: Preprocessed image tensor (1,C,H,W)\
        orig_image: Original RGB image as np.ndarray (H,W,3) scaled [0,255]\
    Returns:\
        heatmap (np.ndarray): RGB overlay of suspicious regions\
    """\
    cam = GradCAM(model=model, target_layers=[target_layer], use_cuda=torch.cuda.is_available())\
    grayscale_cam = cam(input_tensor=input_tensor)[0, :]\
    rgb_img = orig_image.astype(np.float32) / 255.0\
    cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)\
    return cam_image}