# Package - Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import colors

class package:
    # Initialize package with information
    def __init__(self, name, manager, current_version="", new_version="", desc=""):
        self.name = name
        self.manager = manager
        self.current_version = current_version
        self.new_version = new_version
        self.desc = desc

    def __str__(self):
        return self.name

    # Print update information
    def print_update(self, width=0):
        if (self.manager == "flatpak"):
            print("  " + self.name)
            return
        line = "  {name:<" + str(width) + "} [{current} > {new}]"
        print(line.format(name = self.name, current=self.current_version, new=self.new_version))

    # Print installed package information
    def print_info(self):
        print(self.name + "  [" + self.current_version + "]")
