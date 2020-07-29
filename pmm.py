# Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os

import util
import colors

VERSION="0.3"
DEBUG=True

# Import Managers
managers = {}
if util.has_cmd("dnf"):
    from managers.dnf import dnf
    managers['dnf'] = dnf()
if util.has_cmd("flatpak"):
    from managers.flatpak import flatpak
    managers['flatpak'] = flatpak()

# Parse command line options
manager=""
command=""
options=[]
if (len(sys.argv) > 1):
    if sys.argv[1] in managers:
        manager = sys.argv[1]
        if (len(sys.argv) > 2):
            command = sys.argv[2]
        if (len(sys.argv) > 3):
            options = sys.argv[3:]
    else:
        command = sys.argv[1]
        if (len(sys.argv) > 2):
            options = sys.argv[2:]
if (command == ""):
    command = "update"
if DEBUG:
    print("M: '%s', C: '%s', O: %s" % (manager, command, options))

# Print version
if (command == "version"):
    print("Package Manager Manager : v" + VERSION)
    sys.exit(0)
# Print Help Menu
#   Varies based on manager?
if (command == "help"):
    print(colors.bold + "Package Manager Manager Help" + colors.none)
    print(colors.violet + "> Add text\n" + colors.none)
    sys.exit(0)
# Print state of all manager (config file)
#   Print state for indivigual managers? when we get more complex configs?
if (command == "state"):
    try:
        config = open(util.get_config_dir() + "/config", 'r').readlines()
        for line in config:
            print(line.replace("\n", ""))
    except:
        print(colors.red + "Error: PMM must be configed" + colors.none)
        sys.exit(1)
    sys.exit(0)
# Preform interactive setup
if (command == "setup"):
    print(colors.bold + "Package Manager Manager Setup" + colors.none)
    print(colors.violet + "> Add text\n" + colors.none)
    command = "enable"
# Enable specific manager, or enter interactive enabler
if (command == "enable"):
    if (manager == ""):
        for m in managers:
            if managers[m].ready():
                managers[m].enable()
            else:
                while True:
                    response = input("Configure " + m + "? [y/n]: ")
                    if (response == "y") or (response == "Y"):
                        managers[m].enable()
                        break
                    elif (response == "n") or (response == "N"):
                        break
                    else:
                        print("  Invalid response")
    else:
        manager[manager].enable()
    sys.exit(0)
# Disable specific manager, or enter interactive disabler

# Check for available updates

# Update packages

