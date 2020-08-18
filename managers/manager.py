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
        self.name = self.__class__.__name__
        self.title_formated = "{:<8} : ".format(self.title)

        self.width = 0

        self.check_code=-1
        self.check_text=[]

        self.list_text=[]
        self.search_text=[]
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
            util.error(self.title + " isn't even installed", False)
        if (self.config_state == -1):
            util.error(self.title + " is disabled", False)
        if (self.config_state == 0):
            util.error(self.title + " must be enabled or disabled before use.")


    # Enable manager
    def enable(self):
        if (self.config_state == 1):
            print(self.title + " already enabled.")
        else:
            if os.path.isfile(util.get_config_dir() + "/config"):
                os.system("sed '/" + self.name + "/d' -i " + util.get_config_dir() + "/config")
                config = open(util.get_config_dir() + "/config", 'a').write(self.name + \
                        ":enabled\n")
            else:
                util.mk_config_dir()
                config = open(util.get_config_dir() + "/config", 'w').write(self.name + \
                        ":enabled\n")
            print(self.title + " successfully enabled.")

    # Disable manager
    def disable(self):
        if (self.config_state == -1):
            print(self.title + " already disabled.")
        else:
            if os.path.isfile(util.get_config_dir() + "/config"):
                os.system("sed '/" + self.name + "/d' -i " + util.get_config_dir() + "/config")
                config = open(util.get_config_dir() + "/config", 'a').write(self.name + \
                        ":disabled\n")
            else:
                util.mk_config_dir()
                config = open(util.get_config_dir() + "/config", 'w').write(self.name + \
                        ":disbled\n")
            print(self.title + " successfully disabled.")


    # Check for updates, setup check data for printing
    def check(self):
        print(colors.violet + self.title + ": check() unimplemented" + colors.none)
        sys.exit(1)

    # Print if updates are available and a list of updates if provided
    def check_print(self):
        if (self.check_code == 8):
            print(colors.bold + colors.yellow + self.title_formated + "Updates available" + colors.none)
        else:
            print(colors.bold + self.title_formated + "No updates available" + colors.none)
        for p in self.check_text:
            p.print_update(self.width)


    # Find installed packages, setup data for printing
    def list(self, name=""):
        print(colors.violet + self.title + ": list() unimplemented" + colors.none)
        sys.exit(1)

    # Search through packages by string
    def list_find(self, name):
        new_text = []
        l = len(name)
        for p in self.list_text:
            if name in p.name.lower():
                #i = p.name.lower().find(name)
                #p.name = p.name[0:i] + colors.green + p.name[i:i+l] + \
                        #colors.none + p.name[i+l:]
                new_text.append(p)
        self.list_text = new_text

    # Print list of installed packages
    def list_print(self):
        print(colors.bold + self.title_formated + "Installed Packages" + colors.none)
        if (len(self.list_text) == 0):
            print("  no packages found")
        for p in self.list_text:
            p.print_info(self.width)

    # Search for packages to install
    def search(self, term):
        print(colors.violet + self.title + ": search() unimplemented" + colors.none)
        sys.exit(1)

    # Print search results
    def search_print(self):
        print(colors.bold + self.title_formated + "Search Results" + colors.none)
        if (len(self.search_text) == 0):
            print("  no packages found")
        for p in self.search_text:
            p.print_search(self.width)
