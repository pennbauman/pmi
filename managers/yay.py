# yay - Package Manager Investigator
#   URL: https://github.com/pennbauman/pmi
#   License: GPLv3.0
#   Author:
#     Penn Bauman (pennbauman@protonmail.com)
import os
import subprocess

import colors
from managers.manager import manager
from package import package

class yay(manager):
    title="Yay"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["yay", "-Qu"], capture_output=True)
        if (cmd.stdout.decode("utf-8") != ""):
            self.check_code = 8
        else:
            self.check_code = 0
        if self.check_code:
            text = cmd.stdout.decode("utf-8").split("\n")
            i=0
            while (i < len(text)-1):
                line = text[i].split()
                self.check_text.append(package(line[0], self.name, line[1], line[3]))
                self.width = max(self.width, len(line[0]))
                i += 1

    # Find installed packages, setup data for printing
    def list(self, name=""):
        self.enabled_error()
        cmd = subprocess.run(["yay", "-Q"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=0
        while (i < len(text)-1):
            line = text[i].split()
            self.list_text.append(package(line[0], self.name, line[1]))
            self.width = max(self.width, len(line[0]))
            i += 1
        if (name != ""):
            self.list_find(name)

    # Search for packages to install
    def search(self, term=""):
        self.enabled_error()
        cmd = subprocess.run(["yay", "-Ss", term], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=0
        while (i < len(text)-1):
            line1 = text[i].split()
            name = line1[0].split("/")[1]
            i += 1
            line2 = text[i][4:]
            self.search_text.append(package(name, self.name, desc=line2))
            self.width = max(self.width, len(name))
            i += 1
