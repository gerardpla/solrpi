#!/bin/bash

echo "This file has not yet been tested. ABORTING for your own good."
exit 1

echo "Some commands are executed with sudo rights. Please enter your password if prompted:"

echo "raspi-config"

set -e

# See https://www.raspberrypi.com/documentation/computers/configuration.html
# 0=enable, 1=disable
sudo raspi-config nonint do_hostname "solrpi"
sudo raspi-config nonint do_boot_splash 1
# disable camera
sudo raspi-config nonint do_camera 1
# enable SSH (should be enabled already, so just in case...)
sudo raspi-config nonint do_ssh 0
# disable VNC
sudo raspi-config nonint do_vnc 1
# disable SPI (used for PiFace)
sudo raspi-config nonint do_spi 1
# enable I2C (GPIO PINs used for LED board)
sudo raspi-config nonint do_i2c 0
# disable serial port 
# (0: Enable console over serial port, 1: Disable serial port, 2: Enable serial port)
sudo raspi-config nonint do_serial 1
# disable temperature sensor PINs
sudo raspi-config nonint do_onewire 1
# disable remote GPIO control
sudo raspi-config nonint do_rgpio 1

# Performance settings
sudo raspi-config nonint do_change_locale en_US.UTF-8 UTF-8
sudo raspi-config nonint do_change_timezone Europe/Zurich
sudo raspi-config nonint do_wifi_country CH

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
dpkg-reconfigure locales

echo "Updating OS"
sudo apt update -y
sudo apt full-upgrade -y
sudo apt clean

sudo apt install python3.11-venv
