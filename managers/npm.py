# npm - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager
from package import package

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
                line = text[i].split()
                self.check_text.append(package(line[0], self.name, line[1], line[3]))
                self.width = max(self.width, len(line[0]))
                i += 1

    # Find installed packages, setup data for printing
    def list(self, name=""):
        self.enabled_error()
        cmd = subprocess.run(["npm", "list", "-g", "--depth=0"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-2):
            line = text[i].split()[1].split("@")
            if (line[0] == "(empty)"):
                break
            self.list_text.append(package(line[0], self.name, line[1]))
            self.width = max(self.width, len(line[0]))
            i += 1
        if (name != ""):
            self.list_find(name)

    # Search for packages to install
    def search(self, term=""):
        self.enabled_error()
        cmd = subprocess.run(["npm", "search", term], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-1):
            line = text[i].split("|")
            self.search_text.append(package(line[0], self.name, desc=line[1]))
            self.width = max(self.width, len(line[0]))
            i += 1
