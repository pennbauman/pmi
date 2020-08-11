# npm - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager

class npm(manager):
    title="npm"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["npm", "outdated", "-g"], capture_output=True)
        if (cmd.returncode == 1):
            self.check_code = 8
        else:
            self.check_code = 0
        if self.check_code:
            text = cmd.stdout.decode("utf-8").split("\n")
            i=1
            while (i < len(text)-1):
                self.check_text.append(text[i].split()[0])
                i += 1
