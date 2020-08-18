# DNF - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import os
import subprocess

import colors
from managers.manager import manager
from package import package

class dnf(manager):
    title="DNF"

    # Check for updates, setup check data for printing
    def check(self):
        self.enabled_error()
        cmd = subprocess.run(["dnf", "check-update"], capture_output=True)
        if (cmd.returncode == 100):
            self.check_code = 8
        else:
            self.check_code = 0
        if self.check_code:
            pack_cmd = subprocess.run(["dnf", "list", "installed"], capture_output=True)
            pack_cmd = pack_cmd.stdout.decode("utf-8").split("\n")
            pack_info = {}
            i=1
            while (i < len(pack_cmd)-1):
                p = pack_cmd[i].split()
                pack_info[p[0]] = p[1]
                i += 1

            text = cmd.stdout.decode("utf-8").split("\n")
            i=2
            while (i < len(text)-1):
                line = text[i].split()
                self.check_text.append(package(line[0], self.name, pack_info[line[0]], line[1]))
                self.width = max(self.width, len(line[0]))
                i += 1

    # Find installed packages, setup data for printing
    def list(self, name=""):
        self.enabled_error()
        cmd = subprocess.run(["dnf", "list", "installed"], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=1
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
        cmd = subprocess.run(["dnf", "search", term], capture_output=True)
        text = cmd.stdout.decode("utf-8").split("\n")
        i=0
        while (i < len(text)-1):
            if (text[i][0:2] == "=="):
                pass
            else:
                line = text[i].split(" : ")
                self.search_text.append(package(line[0], self.name, desc=line[1]))
                self.width = max(self.width, len(line[0]))
            i += 1
