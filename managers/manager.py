# Manager - Template - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os
from colors import colors

class manager:
    debug=False
    configured=1
    name="Template"

    def __init__(self, config_dir, debug=False):
        if self.debug:
            print("> " + self.__class__.__name + " init")
        self.configured = os.system("cat " + config_dir + self.__class__.__name__ + "&> /dev/null")
        self.debug = debug

    def ready(self):
        if (self.configured == 1):
            print(colors.yellow + self.name + ": Must be configured" + colors.none)
            return False
        else:
            return True

    # Find
    def find(self, package):
        print(colors.red + "ERROR: " + self.__class__.__name__ + " find() not implemented" + colors.none)
        return False

    # Update
    def update(self, package = ""):
        print(colors.red + "ERROR: " + self.__class__.__name__ + " update() not implemented" + colors.none)
        return 2

    # Check
    def check(self, package = "", quiet = False):
        print(colors.red + "ERROR: " + self.__class__.__name__ + " update() not implemented" + colors.none)
        return 2
