# Manager Template - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import sys
import os

import colors
import util

class manager:
    name="manager"
    title="Manager Template"
    config_state=0
        #  0 = unconfigured
        #  1 = enabled
        # -1 = disabled
        # -2 = command not found

    # Initialize and check configuration
    def __init__(self):
        self.check_code=-1
        self.check_text=[]
        self.name = self.__class__.__name__
        self.title_formated = "{:<8} : ".format(self.title)
        # Check manager installed
        if not util.has_cmd(self.name):
            self.config_state = -2
            return
        try:
            # Read config
            config = open(util.get_config_dir() + "/config", "r").readlines()
            for line in config:
                line = line.replace(" ", "")
                if (line == self.name + ":enabled\n"):
                    self.config_state=1
                    break
                elif (line == self.name + ":disabled\n"):
                    self.config_state=-1
                    break
        except:
            self.config_state=0

    # Check if enabled and error if not
    def enabled_error(self):
        if (self.config_state == -2):
            print(colors.red + "Error: " + self.title + " isn't even installed" + colors.none)
            sys.exit(1)
        if (self.config_state == -1):
            print(colors.red + "Error: " + self.title + " is disabled" + colors.none)
            sys.exit(1)
        if (self.config_state == 0):
            print(colors.red + "Error: " + self.title + " must be enabled or disabled before use." + colors.none)
            sys.exit(1)



    # Enable manager
    def enable(self):
        if (self.config_state == 1):
            print(self.title + " already enabled.")
        else:
            os.system("sed '/" + self.name + "/d' -i " + util.get_config_dir() + "/config")
            config = open(util.get_config_dir() + "/config", 'a').write(self.name + ":enabled\n")
            print(self.title + " successfully enabled.")

    # Disable manager
    def disable(self):
        if (self.config_state == -1):
            print(self.title + " already disabled.")
        else:
            os.system("sed '/" + self.name + "/d' -i " + util.get_config_dir() + "/config")
            config = open(util.get_config_dir() + "/config", 'a').write(self.name + ":disabled\n")
            print(self.title + " successfully disabled.")


    # Check for updates, setup check data for printing
    def check(self):
        print(colors.violet + self.title + ": check_run() unimplemented" + colors.none)
        sys.exit(1)

    # Print if updates are available and a list of updates if provided
    def check_print(name, available, packages=[]):
        if available:
            print(colors.bold + colors.green + name + "Updates available." + colors.none)
        else:
            print(colors.bold + colors.yellow + name + "No updates available." + colors.none)

        for p in packages:
            print("  " + p)
        if (len(packages) > 0):
            print()
