# Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os
from colors import colors
from help_menu import help_menu


version="0.3"
debug=False
config_dir=sys.argv[1]


# Check if has superuser privileges
def issudo():
    return os.geteuid() == 0
# Check if system has command
def hascmd(command):
    return os.system("command -v " + command + "&> /dev/null") == 0

managers = {}
if hascmd("dnf"):
    from managers.dnf import dnf
    managers["dnf"] = dnf(config_dir, debug)
if hascmd("flatpak"):
    from managers.flatpak import flatpak
    managers["flatpak"] = flatpak(config_dir, debug)



# Global Variables
command=""
manager=""
#remote=""
package=""



# Functions
def find(package):
    for m in managers:
        if managers[m].find(package):
            return True
    return False

def update():
    if debug:
        print("> update " + str(package))
    if not issudo():
        print(colors.red + "ERROR: This command must be run with superuser privileges" + colors.none)
        sys.exit(1)
    if (manager == ""):
        if (package == ""):
            for m in managers:
                managers[m].update()
        else:
            for m in managers:
                if managers[m].find(package):
                    managers[m].update(package)
    else:
        if (package == ""):
            managers[manager].update()
        else:
            managers[manager].update(package)

def check():
    if debug:
        print("> check " + str(package))
    result = 0
    if (manager == ""):
        if (package == ""):
            for m in managers:
                r = managers[m].update()
                if (r == 8):
                    result = 8
        else:
            if not find(package):
                for m in managers:
                    managers[m].check(package)
                return 1
            else:
                for m in managers:
                    if managers[m].find(package):
                        r = managers[m].check(package)
                        if (r == 8):
                            result = 8
    else:
        if (package != ""):
            r = managers[manager].update()
            if (r == 8):
                result = 8
    return result



# Main Program
i = 2
while (i < len(sys.argv)):
    if (sys.argv[i][0:1] == "-"):
        if (sys.argv[i] == "--dnf"):
            manager = "dnf"
        elif (sys.argv[i] == "--flatpak"):
            manager = "flatpak"
        else:
            print("unknown option '" + sys.argv[i] + "'")
            sys.exit()
    else:
        if (command == ""):
            command = sys.argv[i]
        elif (package == ""):
            if debug:
                print("package: " + sys.argv[i])
            package = sys.argv[i]
        else:
            print(colors.red + "ERROR: Too many command provided" + colors.none)
            sys.exit(1)
    i += 1

if (command == ""):
    command = "update"

if (command == "version"):
    print("Package Manager Manager : v" + version)
    sys.exit()
elif (command == "help"):
    help_menu(manager)
    sys.exit()
elif (command == "configure"):
    if (manager == ""):
        print(colors.red + "ERROR: Manager must be provided to configure" + colors.none)
    else:
        if (os.system("echo '' > " + config_dir + manager) == 0):
            print(colors.green + manager + " condigured" + colors.none)
            sys.exit(0)
        else:
            sys.exit(1)

elif (command == "update"):
    update()

elif (command == "check"):
    sys.exit(check())

#elif (command == "search"):
#elif (command == "install"):
#elif (command == "remove"):
#elif (command == "info"):
#elif (command == "list"):

#elif (command == "manager"):
#elif (command == "source"):
