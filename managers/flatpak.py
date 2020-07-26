# Flatpak - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os
from colors import colors

class flatpak:
    debug=False
    configured=1

    def __init__(self, config_dir, debug=False):
        if self.debug:
            print("> flatpak init")
        self.configured = os.system("cat " + config_dir + "flatpak &> /dev/null")
        self.debug = debug

    def ready(self):
        if (self.configured == 1):
            print(colors.yellow + "Flatpak: Must be configured" + colors.none)
            return False
        else:
            return True

    # Find
    def find(self, package):
        if self.debug:
            print("> flatpak find " + package)
        test = os.system("flatpak info " + package + " &> /dev/null")
        if (test == 0):
            return True
        else:
            return False

    # Update
    def update(self, package = ""):
        if self.debug:
            print("> flatpak update")
        test = self.check(package, True)
        if (test != 8):
            return test
        print(colors.bold + colors.green + "Flatpak update" + colors.none)
        return(os.system("flatpak update"))

    # Check
    def check(self, package = "", quiet = False):
        if self.debug:
            print("> flatpak check")
        if not self.ready():
            return 1
        if (package == ""):
            if (os.system("flatpak update &> /dev/null") == 1):
                if not quiet:
                    print(colors.green + "Flatpak: Updates available" + colors.none)
                return 8
            else:
                print(colors.yellow + "Flatpak: No updates available" + colors.none)
                return 0
        else:
            if not self.find(package):
                print(colors.red + "Flatpak: No package '" + package + "' found" + colors.none)
                return 1
            if (os.system("flatpak update " + package + " &> /dev/null") == 1):
                if not quiet:
                    print(colors.green + "Flatpak: Updates available for " + package + colors.none)
                return 8
            else:
                print(colors.yellow + "Flatpak: No updates available for " + package + colors.none)
                return 0
