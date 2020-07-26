#!/bin/sh
# Runner - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm

if [ -z $XDG_CONFIG_HOME ]; then
	condig_dir=$XDG_CONFIG_HOME/.config/pmm
else
	condig_dir=$HOME/.config/pmm
fi
if [ -d $config_dir ]; then
	config_dir=/usr/share/pmm
fi

python3.8 /usr/share/pmm/pmm.py $config_dir $@
