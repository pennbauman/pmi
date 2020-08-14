# Flatpak - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager
from package import package

class flatpak(manager):
    title="Flatpak"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["flatpak", "update"], capture_output=True)
        if (cmd.returncode == 1):
            self.check_code = 8
        else:
            self.check_code = 0
        if self.check_code:
            text = cmd.stdout.decode("utf-8").split("\n")
            i=3
            while (i < len(text)-3):
                line = text[i].split()
                na = colors.violet + "N/A" + colors.none
                self.check_text.append(package(line[1], self.name, na, na))
                i += 1

    # Find installed packages, setup data for printing
    def list(self):
        self.enabled_error()
        cmd = subprocess.run(["flatpak", "list"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-1):
            line = text[i].split()
            na = colors.violet + "N/A" + colors.none
            self.list_text.append(package(line[0], self.name, na))
            i += 1
