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
        self.check_enabled()
        if (os.system("dnf check-update &> /dev/null") == 100):
            return 8
        return 0
