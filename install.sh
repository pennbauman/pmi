# Install Script
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
install_dir=/usr/share/pmm

sudo cp pmm.sh /bin/pmm
sudo chmod 755 /bin/pmm

sudo mkdir -p $install_dir
sudo cp pmm.py $install_dir
sudo cp colors.py $install_dir
sudo cp help_menu.py $install_dir
sudo cp -r managers $install_dir
