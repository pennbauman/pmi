# Package Manager Investigator
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmi
import sys
import os

import util
import colors
from managers.manager import manager

# Globals
VERSION="0.6"
DEBUG=False
HELP=colors.bold + "Package Manager Investigator" + colors.none + "\n\
\n\
Usage:\n\
  pmi [manager] [command] [subcommand]\n\
\n\
Managers:\n\
  all       : (Default) Run command for all mangers\n\
  dnf       : Fedora DNF\n\
  flatpak   : Flatpak\n\
\n\
Commands:\n\
  version   : Print version number\n\
    message   : (Default) Print message with number\n\
    number    : Print only the version number\n\
\n\
  help      : Print this help menu\n\
  setup     : Setup PMI and enable or disable managers\n\
  status    : Check the state of available managers\n\
  enable    : Enable the specified manager or picked managers\n\
    ask       : (Default when manager is all) Ask before enabling\n\
    auto      : (Default when manager specified) Do not ask before enabling\n\
\n\
  disable   : Disable the specified manager or picked managers\n\
    ask       : (Default when manager is all) Ask before disabling\n\
    auto      : (Default when manager specified) Do not ask before disabling\n\
\n\
  check     : (Defualt) Check for updates, return code is 8 when updates are\n\
              available\n\
    silent    : Print nothing, for using only the return code\n\
    terse     : Print only if updates were found or not\n\
    list      : (Default) Print a lists of out of date packages\n\
      formatted : (Default) Print manager heads and the list packages\n\
      plain     : Print only this of packages\n\
    count     : Print the number of packages to update (0 for no updates)"


# Import Managers
managers = {}
if util.has_cmd("dnf"):
    from managers.dnf import dnf
    managers['dnf'] = dnf()
if util.has_cmd("yum"):
    from managers.yum import yum
    managers['yum'] = yum()
if util.has_cmd("flatpak"):
    from managers.flatpak import flatpak
    managers['flatpak'] = flatpak()


# Parse command line options
args=["", ""]
if (len(sys.argv) > 1):
    if sys.argv[1] in managers or (sys.argv[1] == "all"):
        args[1] = sys.argv[1]
        if (len(sys.argv) > 2):
            args[0] = sys.argv[2]
        if (len(sys.argv) > 3):
            args = args + sys.argv[3:]
    else:
        args[0] = sys.argv[1]
        if (len(sys.argv) > 2):
            args = args + sys.argv[2:]
# Check default option
if (args[1] == ""):
    args[1] = "all"
if (args[0] == ""):
    args[0] = "check"
if DEBUG:
    print("M: '%s', C: '%s', O: %s" % (args[1], args[0], args[2:]))
    print("Config: " + util.get_config_dir())



# Print version
if (args[0] == "version"):
    if (len(args) == 2):
        args.append("message")
    if (args[2] == "message"):
        print("Package Manager Investigator : v" + VERSION)
    elif (args[2] == "number"):
        print(VERSION)
    else:
        print(colors.red + "Error: unkown 'version' subcommand '" + args[2] + "'" + colors.none)
    sys.exit(0)

# Print Help Menu
#   Varies based on manager?
if (args[0] == "help") or (args[0] == "-help") or (args[0] == "--help"):
    print(HELP)
    sys.exit(0)

# Preform interactive setup
if (args[0] == "setup"):
    print(colors.bold + "Package Manager Investigator Setup" + colors.none)
    print("Enable any managers you want to use.")
    print()
    for m in managers:
        if util.ask("Enable " + managers[m].title):
            managers[m].enable()
        else:
            if util.ask("Disable " + managers[m].title):
                managers[m].disable()
    print()
    print("PMI is now configured.")
    print("If you need more information run 'pmi help'.")
    sys.exit(0)

# Print status of all managers (config file)
#   Print status for indivigual managers? when we get more complex configs?
if (args[0] == "status"):
    for m in managers.values():
        state = m.config_state
        if (state == 1):
            print(colors.green + m.title_formated + "Enabled" + colors.none)
        elif (state == 0):
            print(colors.red + m.title_formated + "None" + colors.none)
        elif (state == -1):
            print(colors.yellow + m.title_formated + "Disabled" + colors.none)
    sys.exit(0)
# Enable specific manager, or enter interactive enabler
if (args[0] == "enable"):
    if (args[1] == "all"):
        if (len(args) == 2):
            args.append("ask")
        for m in managers:
            if (args[2] == "auto"):
                managers[m].enable()
            elif (args[2] == "ask"):
                if managers[m].ready():
                    managers[m].enable()
                else:
                    if util.ask("Enable " + managers[m].title):
                        managers[m].enable()

            else:
                print(colors.red + "Error: unkown 'enable' subcommand '" + args[2] + "'" + colors.none)
    else:
        if (len(args) == 2):
            args.append("auto")
        if (args[2] == "auto"):
            managers[args[1]].enable()
        elif (args[2] == "ask"):
            if util.ask("Enable " + managers[args[1]].title):
                managers[args[1]].enable()
        else:
            print(colors.red + "Error: unkown 'enable' subcommand '" + args[2] + "'" + colors.none)
    sys.exit(0)
# Disable specific manager, or enter interactive disabler
if (args[0] == "disable"):
    if (args[1] == "all"):
        if (len(args) == 2):
            args.append("ask")
        for m in managers:
            if (args[2] == "auto"):
                managers[m].disable()
            elif (args[2] == "ask"):
                if (managers[m].config_state == -1):
                    managers[m].disable()
                else:
                    if util.ask("Disable " + managers[m].title):
                        managers[m].disable()
            else:
                print(colors.red + "Error: unkown 'disable' subcommand '" + args[2] + "'" + colors.none)
    else:
        if (len(args) == 2):
            args.append("auto")
        if (args[2] == "auto"):
            managers[args[1]].disable()
        elif (args[2] == "ask"):
            if util.ask("Disable " + managers[args[1]].title):
                managers[args[1]].disable()
        else:
            print(colors.red + "Error: unkown 'disable' subcommand '" + args[2] + "'" + colors.none)

    sys.exit(0)


# Check for unconfigured managers
unconfigured = False
for m in managers:
    if (managers[m].config_state == 0):
        print(colors.red + "Error: " + managers[m].title + " must be enabled or disabled before use." + colors.none)
        unconfigured = True
if unconfigured:
    sys.exit(1)

# Check if duplicate managers are inabled
if "dnf" in managers and "yum" in managers:
    if (managers["yum"].config_state == 1) and (managers["yum"].config_state == 1):
        print(colors.yellow + "Warning: Both Yum and DNF installed, they will act as duplicates." + colors.none)


# Check for available updates
if (args[0] == "check"):
    if (len(args) == 2):
        args.append("list")
    if (args[2] == "list") and (len(args) == 3):
        args.append("formatted")
    if (args[1] == "all"):
        fin = 0
        count = 0
        for m in managers.values():
            if (m.config_state < 1):
                continue
            result = m.check()
            if (m.check_code == 8):
                fin = 8
            if (args[2] == "silent"):
                pass
            elif (args[2] == "terse"):
                manager.check_print(m.title_formated, (m.check_code == 8))
            elif (args[2] == "list"):
                if (args[3] == "formatted"):
                    manager.check_print(m.title_formated, (m.check_code == 8), m.check_text)
                elif (args[3] == "plain"):
                    if (m.check_code == 8):
                        for p in m.check_text:
                            print(p)
                else:
                    print(colors.red + "Error: unkown 'check list' subcommand '" + args[3] + "'" + colors.none)
            elif (args[2] == "count"):
                count += len(m.check_text)
            else:
                print(colors.red + "Error: unkown 'check' subcommand '" + args[2] + "'" + colors.none)
                sys.exit(1)
        if (args[2] == "count"):
            print(count)
        sys.exit(fin)
    else:
        managers[args[1]].check()

        if (args[2] == "terse"):
            manager.check_print(managers[args[1]].title_formated, (managers[args[1]].check_code == 8))
        elif (args[2] == "list"):
            if (args[3] == "formatted"):
                manager.check_print(managers[args[1]].title_formated, (managers[args[1]].check_code == 8), managers[args[1]].check_text)
            elif (args[3] == "plain"):
                if (managers[args[1]].check_code == 8):
                    for p in managers[args[1]].check_text:
                        print(p)
            else:
                print(colors.red + "Error: unkown 'check list' subcommand '" + args[3] + "'" + colors.none)
        elif (args[2] == "count"):
            print(len(managers[args[1]].check_text))
        else:
            print(colors.red + "Error: unkown 'check' subcommand '" + args[2] + "'" + colors.none)
            sys.exit(1)
        sys.exit(managers[args[1]].check_code)

# Error out if command is not found
print(colors.red + "Error: Unknown command '" + args[0] + "'" + colors.none)
print("  For more information run 'pmi help'")
sys.exit(1)
