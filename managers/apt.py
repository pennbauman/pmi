# APT - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager
from package import package

class apt(manager):
    title="APT"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["apt", "list", "--upgradable"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        if (len(text) == 2):
            self.check_code = 0
        else:
            self.check_code = 8
        if self.check_code:
            i=1
            while (i < len(text)-1):
                line = text[i].split()
                print(line)
                old = line[len(line)-1][0:-1]
                name = line[0].split("/")[0]
                self.check_text.append(package(name, self.name, old, line[1]))
                self.width = max(self.width, len(name))
                i += 1

    # Find installed packages, setup data for printing
    def list(self, name=""):
        self.enabled_error()
        cmd = subprocess.run(["apt", "list", "--installed"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
        while (i < len(text)-1):
            line = text[i].split()
            self.list_text.append(package(line[0].split("/")[0], self.name, line[1]))
            self.width = max(self.width, len(line[0].split("/")[0]))
            i += 1
        if (name != ""):
            self.list_find(name)

    # Search for packages to install
    def search(self, term=""):
        self.enabled_error()
        cmd = subprocess.run(["apt", "search", term], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=0
        while not "/" in text[i]:
            i += 1
        while (i < len(text)-1):
            name = text[i].split()[0].split("/")[0]
            self.search_text.append(package(name, self.name, desc=text[i+1][2:]))
            self.width = max(self.width, len(name))
            i += 3
