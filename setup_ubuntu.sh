{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs26 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 #!/bin/bash\
set -e\
sudo apt update && sudo apt upgrade -y\
# Basic build tools\
sudo apt install -y build-essential git ffmpeg libsm6 libxext6 python3-venv python3-pip\
# Create venv\
python3 -m venv deepguard-venv\
source deepguard-venv/bin/activate\
pip install --upgrade pip\
# Install requirements (CPU). If you have CUDA, install appropriate torch separately per https://pytorch.org\
pip install -r requirements.txt\
# Optionally, install a CUDA-enabled torch. Example for CUDA 11.7 (change per your GPU):\
# pip install torch==2.1.0+cu117 torchvision --extra-index-url https://download.pytorch.org/whl/cu117\
\
# Make sure ffmpeg is available\
ffmpeg -version || echo "FFmpeg missing"\
}