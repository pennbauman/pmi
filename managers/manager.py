# Manager Template - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
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
        if not util.has_cmd(self.name):
            config_state = -2
            return
        try:
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

    # Check if manager is configured
    def ready(self):
        return (self.config_state > 0)

    # Enable manager
    def enable(self):
        if (self.config_state < 0):
            print(colors.violet + "Unimplemented manager.enable()" + colors.none)
        if (self.config_state == 0):
            config = open(util.get_config_dir() + "/config", 'a')
            config.write(self.name + ":enabled\n")
            config.close()
            print(colors.green + self.title + " successfully enabled." + colors.none)
        else:
            print(self.title + " already enabled.")
    #def check()
    #def config()
