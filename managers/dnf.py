# DNF - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os
from colors import colors

class dnf:
    debug=False
    configured=1

    def __init__(self, config_dir, debug=False):
        if self.debug:
            print("> dnf init")
        self.configured = os.system("cat " + config_dir + "dnf &> /dev/null")
        self.debug = debug

    def ready(self):
        if (self.configured == 1):
            print(colors.yellow + "DNF: Must be configured" + colors.none)
            return False
        else:
            return True

    # Find
    def find(self, package):
        if self.debug:
            print("> dnf find " + package)
        test = os.system("dnf info " + package + " &> /dev/null")
        if (test == 0):
            return True
        else:
            return False

    # Update
    def update(self, package = ""):
        if self.debug:
            print("> dnf update " + package)
        test = self.check(package, True)
        if (test != 8):
            return test
        print(colors.bold + colors.green + "DNF update" + colors.none)
        return (os.system("dnf upgrade"))

    # Check
    def check(self, package = "", quiet = False):
        if self.debug:
            print("> dnf check " + package)
        if not self.ready():
            return 1
        if (package == ""):
            if (os.system("dnf check-update &> /dev/null") == 400):
                if not quiet:
                    print(colors.green + "DNF: Updates available" + colors.none)
                return 8
            else:
                print(colors.yellow + "DNF: No updates available" + colors.none)
                return 0
        else:
            if not self.find(package):
                print(colors.red + "DNF: No package '" + package + "' found" + colors.none)
                return 1
            if (os.system("dnf check-update " + package + " &> /dev/null") == 400):
                if not quiet:
                    print(colors.green + "DNF: Updates available for " + package + colors.none)
                return 8
            else:
                print(colors.yellow + "DNF: No updates available for " + package + colors.none)
                return 0
