# Yum - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager

class yum(manager):
    title="Yum"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["yum", "check-update"], capture_output=True)
        if (cmd.returncode == 100):
            self.check_code = 8
        else:
            self.check_code = 0
        if self.check_code:
            text = cmd.stdout.decode("utf=8").split("\n")
            i=2
            while (i < len(text)-1):
                self.check_text.append(text[i].split()[0])
                i += 1
