#!/bin/bash

echo "Downloading u2net.onnx model..."
wget -O u2net.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
echo "Model downloaded."

echo "Installing Python dependencies..."
pip install -r requirements.txt
