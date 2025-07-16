#!/bin/bash

# Ubuntu Server Setup Script for Neo65 Scraper
echo "Setting up Neo65 Scraper on Ubuntu Server..."

# Update package list
sudo apt update

# Install Python3 and pip if not already installed
sudo apt install -y python3 python3-pip python3-venv

# Install Firefox (headless version)
sudo apt install -y firefox

# Install geckodriver for Selenium
echo "Installing geckodriver..."
GECKODRIVER_VERSION="v0.34.0"
wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver
rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# Create virtual environment
python3 -m venv venv

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the scraper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the scraper: python3 scraper.py"
