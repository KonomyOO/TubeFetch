#!/bin/bash

echo "Updating system packages..."
sudo dnf update -y

echo "Installing system dependencies (mpv-libs, aria2)..."
sudo dnf install -y mpv-libs aria2

echo "Creating symbolic link for libmpv.so.1..."
sudo ln -sf /usr/lib64/libmpv.so.2 /usr/lib64/libmpv.so.1

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "All dependencies installed successfully!"
