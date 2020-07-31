# Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os

import util
import colors

# Globals
VERSION="0.4"
DEBUG=False
HELP=colors.bold + "Package Manager Manager" + colors.none + "\n\
\n\
Usage:\n\
  pmm [manager] [command]\n\
\n\
Managers:\n\
  all (defualt)    : Run command for all mangers\n\
  dnf              : Fedora DNF\n\
  flatpak          : Flatpak\n\
\n\
Commands:\n\
  version          : Print version number\n\
  help             : Print this help menu\n\
  setup            : Setup PMM and enable or disable managers\n\
  state            : Check the state of available managers\n\
  enable           : Enable the specified manager or picked managers\n\
  disable          : Disable the specified manager or picked managers\n\
  check            : Check for updates\n\
  update (default) : Upcoming\
"

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
# Check default option
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
    print(HELP)
    sys.exit(0)
# Preform interactive setup
if (command == "setup"):
    print(colors.bold + "Package Manager Manager Setup" + colors.none)
    print("Enable any managers you want to use.")
    print()
    for m in managers:
        if util.ask("Enable " + managers[m].get_title()):
            managers[m].enable()
        else:
            if util.ask("Disable " + managers[m].get_title()):
                managers[m].disable()
    print()
    print("PMM is now configured.")
    print("If you need more information run 'pmm help'.")
    sys.exit(0)
# Print state of all manager (config file)
#   Print state for indivigual managers? when we get more complex configs?
if (command == "state"):
    try:
        config = open(util.get_config_dir() + "/config", 'r').readlines()
        for line in config:
            parts = line.replace("\n", "").split(":")
            print("%-8s : %s" % (managers[parts[0]].get_title(), parts[1]))
    except:
        print(colors.red + "Error: PMM must be configured." + colors.none)
        print("Run 'pmm setup' to configure.")
        sys.exit(1)
    sys.exit(0)
# Enable specific manager, or enter interactive enabler
if (command == "enable"):
    if (manager == ""):
        for m in managers:
            if managers[m].ready():
                managers[m].enable()
            else:
                if util.ask("Enable " + managers[m].get_title()):
                    managers[m].enable()
    else:
        managers[manager].enable()
    sys.exit(0)
# Disable specific manager, or enter interactive disabler
if (command == "disable"):
    if (manager == ""):
        for m in managers:
            if (managers[m].state() == -1):
                managers[m].disable()
            else:
                if util.ask("Disable " + managers[m].get_title()):
                    managers[m].disable()
    else:
        managers[manager].disable()
    sys.exit(0)

# Check for available updates
if (command == "check"):
    if (manager == ""):
        fin = 0
        for m in managers:
            result = managers[m].check()
            if (result == 8):
                print(colors.green, end='')
                print("%-8s : Updates available" % (managers[m].get_title()))
                print(colors.none, end='')
                fin = 8
            else:
                print(colors.yellow, end='')
                print("%-8s : No updates available" % (managers[m].get_title()))
                print(colors.none, end='')
        sys.exit(fin)
    else:
        result = managers[manager].check()
        if (result == 8):
            print(colors.green + managers[manager].get_title() + " : Updates available." + colors.none)
        else:
            print(colors.yellow + managers[manager].get_title() + " : No updates available." + colors.none)
        sys.exit(result)
# Update packages
if (command == "update"):
    print(colors.violet + "Unimplemented $ pmm update" + colors.none)
    sys.exit(1)

