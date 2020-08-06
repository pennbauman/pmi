# DNF - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import os
import subprocess

import colors
from managers.manager import manager

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
            text = cmd.stdout.decode("utf=8").split("\n")
            i=2
            while (i < len(text)-1):
                self.check_text.append(text[i].split()[0])
                i += 1

    # Preform updates
    def update(self):
        self.enabled_error()
        print(self.name + " update")
        #fw = open("tmpout", "wb")
        #fr = open("tmpout", "r")
        #cmd = subprocess.Popen(["sudo dnf", "upgrade"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #cmd = subprocess.run(["dnf", "upgrade"], capture_output=True)
        #print(cmd.stderr.decode("utf-8"))
        #print(cmd.stdout.decode("utf-8"))
        cmd = subprocess.Popen(["dnf", "upgrade"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #cmd.stdin.write("M1st3r R0b0t0\n".encode("utf-8"))
        print("started")
        if (cmd.poll() == None):
            print("running")
        if cmd.stderr.readable():
            print(cmd.stderr.read())
        else:
            print("No err")
        if cmd.stdout.readable():
            print(cmd.stdout.read())
        else:
            print("No out")
        if (cmd.poll() == None):
            print("running")
            cmd.stdin.write("n\n".encode("utf-8"))
        print(cmd.stderr.read().decode("utf-8"))
        print(cmd.stdout.read().decode("utf-8"))
        if (cmd.poll() == None):
            cmd.stdin.write("n\n".encode("utf-8"))
        print(cmd.stderr.decode("utf-8"))
        print(cmd.stdout.decode("utf-8"))

        #print(cmd.stderr.decode("utf-8"))
        #cmd.stdin.write("M1st3r R0b0t0\n".encode("utf-8"))
        print(cmd.returncode)
        if (cmd.poll() != None):
            print("finished")
        print(cmd.stdout.read())
        print(cmd.returncode)
