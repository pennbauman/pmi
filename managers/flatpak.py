# Flatpak - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import os

import colors
from managers.manager import manager

class flatpak(manager):
    title="Flatpak"

    # Check for updates
    def check(self):
        if not self.ready():
            print(colors.red + "Error: " + self.title + " not enabled.")
            return 1
        if (os.system("flatpak update &> /dev/null") == 256):
            return 8
        return 0
