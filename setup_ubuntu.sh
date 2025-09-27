#!/bin/bash
set -e
sudo apt update && sudo apt upgrade -y
# Basic build tools
sudo apt install -y build-essential git ffmpeg libsm6 libxext6 python3-full python3-dev python3-venv python3-pip
# Create venv
python3 -m venv deepguard-venv
source deepguard-venv/bin/activate
pip install --upgrade pip
# Install requirements (CPU). If you have CUDA, install appropriate torch separately per https://pytorch.org
pip install -r requirements.txt
# Optionally, install a CUDA-enabled torch. Example for CUDA 11.7 (change per your GPU):
# pip install torch==2.1.0+cu117 torchvision --extra-index-url https://download.pytorch.org/whl/cu117

# Make sure ffmpeg is available
ffmpeg -version || echo "FFmpeg missing"