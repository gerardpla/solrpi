#!/bin/bash

read -p "About to deinstall solrpi files, but keeps the system-wide Python packages installed. Proceed? (y/n) " yn
case $yn in
    [Yy]* ) echo "Deinstalling solrpi now (2 steps)";;
    * ) echo "Aborting"; exit;;
esac

TARGET_DIR=/usr/local/solrpi

echo -e "\n(1/2) Deinstalling solrpi service"
sudo systemctl stop solrpi 2> /dev/null
sudo systemctl disable solrpi
sudo rm -rf /etc/systemd/system/solrpi.service
sudo systemctl daemon-reload

echo -e "\n(2/2) Removing solrpi files and runtime environment"
sudo rm -rf $TARGET_DIR

echo -e "\nDeinstallation DONE.\n\nYou can reinstall by executing:\n   make install\n"
