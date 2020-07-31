# DNF - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import os

import colors
from managers.manager import manager

class dnf(manager):
    title="DNF"

    # Check for updates
    def check(self):
        if not self.ready():
            print(colors.red + "Error: " + self.title + " not enabled.")
            return 1
        if (os.system("dnf check-update &> /dev/null") == 400):
            return 8
        return 0
