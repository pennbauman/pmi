#!/bin/sh
# Test Runner - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
if [ -z $XDG_CONFIG_HOME ]; then
	config_dir=$XDG_CONFIG_HOME/.config/pmm
else
	config_dir=$HOME/.config/pmm
fi
#if [ ! -d $config_dir ]; then
	#mkdir -p $config_dir
#fi
#echo $config_dir
python3.8 pmm.py $config_dir $@
