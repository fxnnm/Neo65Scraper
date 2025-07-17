#!/bin/bash

# Ubuntu Server Setup Script for Neo65 Scraper
echo "Setting up Neo65 Scraper on Ubuntu Server..."

# Update package list
sudo apt update

# Install Python3 and pip if not already installed
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install -y google-chrome-stable

# Create virtual environment
python3 -m venv venv

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the scraper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the scraper: python3 scraper.py"
