# Install Script - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
install_dir=/usr/share/pmi

sudo cp pmi.sh /bin/pmi
sudo chmod 755 /bin/pmi

sudo mkdir -p $install_dir
sudo cp pmi.py $install_dir
sudo cp colors.py $install_dir
sudo cp util.py $install_dir
sudo cp -r managers $install_dir
