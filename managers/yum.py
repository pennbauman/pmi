# Yum - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import os

import colors
from managers.manager import manager

class yum(manager):
    title="Yum"

    # Check for updates
    def check(self):
        self.check_enabled()
        if (os.system("yum check-update &> /dev/null") == 100):
            return 8
        return 0
