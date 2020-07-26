# Help - Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
from colors import colors

def help_menu(manager = ""):
    if (manager == ""):
        print(colors.bold + "Package Manager Manager Help")
    elif (manager == "dnf"):
        print(colors.bold + "Package Manager Manager DNF Help")



