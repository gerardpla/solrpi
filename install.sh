#!/bin/bash

read -p "About to install all required files and system dependencies as root. Proceed? (y/n) " yn
case $yn in
    [Yy]* ) echo "Installing solrpi now (5 steps)";;
    * ) echo "Aborting"; exit;;
esac

echo -e "\nStopping solrpi system service"
sudo systemctl stop solrpi 2> /dev/null

TARGET_DIR=/usr/local/solrpi
sudo mkdir -p $TARGET_DIR
sudo chown $(id -u):$(id -g) $TARGET_DIR

echo -e "\n(1/5) Installing required packages"
sudo apt-get install python3-pip virtualenv -y

echo -e "\n(2/5) Installing runtime venv"
python3 -m venv $TARGET_DIR/.venv

echo -e "\n(3/5) Installing runtime dependencies"
$TARGET_DIR/.venv/bin/python3 -m pip install -r requirements_base.txt -r requirements_runtime.txt

# TODO install generated package using pip?
echo -e "\n(4/5) Installing solrpi application"
cp -r solrpi $TARGET_DIR
cp solrpi_main.py $TARGET_DIR
chmod 664 $TARGET_DIR/solrpi_main.py

echo -e "\n(5/5) Installing solrpi system service"
sudo cp service/solrpi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable solrpi
sudo systemctl restart solrpi

echo -e "\nInstallation DONE. solrpi should be running as system job.\n\nCheck status using:\n   sudo systemctl status solrpi\n"
