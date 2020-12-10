# Flatpak - Package Manager Investigator
#   URL: https://github.com/pennbauman/pmi
#   License: GPLv3.0
#   Author:
#     Penn Bauman (pennbauman@protonmail.com)
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
            na = colors.violet + "N/A" + colors.none
            text = cmd.stdout.decode("utf-8").split("\n")
            i = 0
            while (i < len(text)-1):
                line = text[i].split()
                if (len(line) == 0):
                    pass
                elif (line[0][-1:] == ".") and line[0][0:-1].isdigit():
                    self.check_text.append(package(line[1], self.name, na, na))
                i += 1

    # Find installed packages, setup data for printing
    def list(self, name=""):
        self.enabled_error()
        cmd = subprocess.run(["flatpak", "list", "--columns=application"], \
                capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-1):
            line = text[i].split()
            na = colors.violet + "N/A" + colors.none
            self.list_text.append(package(line[0], self.name, na))
            i += 1
        if (name != ""):
            self.list_find(name)

    # Search for packages to install
    def search(self, term=""):
        self.enabled_error()
        cmd = subprocess.run(["flatpak", "search", term, \
                "--columns=application,description"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-1):
            name = text[i].split()[0]
            desc = text[i][len(name) + 1:]
            self.search_text.append(package(name, self.name, desc=desc))
            self.width = max(self.width, len(name))
            i += 1
