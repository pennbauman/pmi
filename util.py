# Utility - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os
import subprocess

import colors

# Check if has superuser privileges
def is_sudo():
    return os.geteuid() == 0

# Check if system has command
def has_cmd(command):
    return os.system("command -v " + command + "&> /dev/null") == 0

def get_config_dir():
    try:
        config_dir = os.environ['XDG_CONFIG_HOME'] + "/pmm"
    except:
        try:
            config_dir = os.environ['HOME'] + "/.config/pmm"
        except:
            print(colors.red + "Error: $HOME cannot be determined" + colors.none)
            sys.exit(1)
    return config_dir
