# Install Script - Package Manager Investigator
#   URL: https://github.com/pennbauman/pmi
#   License: GPLv3.0
#   Author:
#     Penn Bauman (pennbauman@protonmail.com)
install_dir=/usr/share/pmi

sudo cp pmi.sh /bin/pmi
sudo chmod 755 /bin/pmi

sudo mkdir -p $install_dir
sudo cp pmi.py $install_dir
sudo cp colors.py $install_dir
sudo cp util.py $install_dir
sudo cp package.py $install_dir
sudo cp -r managers $install_dir
