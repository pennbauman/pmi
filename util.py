# Utility - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
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
        config_dir = os.environ['XDG_CONFIG_HOME'] + "/pmi"
    except:
        try:
            config_dir = os.environ['HOME'] + "/.config/pmi"
        except:
            print(colors.red + "Error: $HOME cannot be determined" + colors.none)
            sys.exit(1)
    return config_dir

def mk_config_dir():
    config_dir = get_config_dir()
    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)

def ask(question):
    while True:
        response = input(question + " [y/n]: ")
        if (response == "y") or (response == "Y"):
            return True
        elif (response == "n") or (response == "N"):
            return False
        else:
            print("  Please response 'y' or 'n'")
