# Package Manager Manager
#   Penn Bauman (pennbauman@protonmail.com)
#   https://github.com/pennbauman/pmm
import sys
import os

import util
import colors

# Globals
VERSION="0.5"
DEBUG=False
HELP=colors.bold + "Package Manager Manager" + colors.none + "\n\
\n\
Usage:\n\
  pmm [manager] [command] [subcommand]\n\
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
  setup     : Setup PMM and enable or disable managers\n\
  status    : Check the state of available managers\n\
  enable    : Enable the specified manager or picked managers\n\
    ask       : (Default when manager is all) Ask before enabling\n\
    auto      : (Default when manager specified) Do not ask before enabling\n\
\n\
  disable   : Disable the specified manager or picked managers\n\
    ask       : (Default when manager is all) Ask before disabling\n\
    auto      : (Default when manager specified) Do not ask before disabling\n\
\n\
  check     : (Defualt) Check for updates, return code is 8 when updates are available\n\
    silent    : Print nothing, for using only the return code\n\
    terse     : Print only if updates were found or not\n\
    list      : (Default) Print if updates were found and lists of packages\n\
    count     : Print the number of packages to update (0 for no updates)\n\
\n\
  update    : !!Unimplemented!!"


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
manager=""
command=""
options=[]
if (len(sys.argv) > 2):
    if sys.argv[2] in managers or (sys.argv[2] == "all"):
        manager = sys.argv[2]
        if (len(sys.argv) > 3):
            command = sys.argv[4]
        if (len(sys.argv) > 4):
            options = sys.argv[4:]
    else:
        command = sys.argv[2]
        if (len(sys.argv) > 3):
            options = sys.argv[3:]
# Check default option
if (manager == ""):
    manager = "all"
if (command == ""):
    command = "check"
if DEBUG:
    print("M: '%s', C: '%s', O: %s" % (manager, command, options))
    print("Config: " + util.get_config_dir())



# Print version
if (command == "version"):
    if (len(options) > 0) and (options[0] == "ask"):
        print(VERSION)
    else:
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
        if util.ask("Enable " + managers[m].title):
            managers[m].enable()
        else:
            if util.ask("Disable " + managers[m].title):
                managers[m].disable()
    print()
    print("PMM is now configured.")
    print("If you need more information run 'pmm help'.")
    sys.exit(0)
# Print status of all manager (config file)
#   Print status for indivigual managers? when we get more complex configs?
if (command == "status"):
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
if (command == "enable"):
    if (manager == "all"):
        for m in managers:
            if (len(options) > 0) and (options[0] == "auto"):
                managers[m].enable()
            else:
                if managers[m].ready():
                    managers[m].enable()
                else:
                    if util.ask("Enable " + managers[m].title):
                        managers[m].enable()
    else:
        if (len(options) > 0) and (options[0] == "ask"):
            if util.ask("Enable " + managers[manager].title):
                managers[manager].enable()
        else:
            managers[manager].enable()
    sys.exit(0)
# Disable specific manager, or enter interactive disabler
if (command == "disable"):
    if (manager == "all"):
        for m in managers:
            if (len(options) > 0) and (options[0] == "auto"):
                managers[m].disable()
            else:
                if (managers[m].config_state == -1):
                    managers[m].disable()
                else:
                    if util.ask("Disable " + managers[m].title):
                        managers[m].disable()
    else:
        if (len(options) > 0) and (options[0] == "ask"):
            if util.ask("Disable " + managers[manager].title):
                managers[manager].disable()
        else:
            managers[manager].disable()
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
        print(colors.yellow + "Warning: Both Yum and DNF installed, will be duplicates." + colors.none)


# Check for available updates
if (command == "check"):
    if (len(options) == 0):
        options = ["list"]
    if (manager == "all"):
        fin = 0
        count = 0
        for m in managers.values():
            if (m.config_state < 1):
                continue
            result = m.check()
            if (m.check_code == 8):
                fin = 8
            if (options[0] == "terse") or (options[0] == "list"):
                if (m.check_code == 8):
                    print(colors.green + m.title_formated + "Updates available." + colors.none)
                else:
                    print(colors.yellow + m.title_formated + "No updates available." + colors.none)
            if (options[0] == "silent"):
                pass
            elif (options[0] == "terse"):
                pass
            elif (options[0] == "list"):
                if (m.check_code == 8):
                    for p in m.check_text:
                        print("  " + p)
            elif (options[0] == "count"):
                count += len(m.check_text)
            else:
                print(colors.red + "Error: unkown check subcommand '" + options[0] + "'" + colors.none)
                sys.exit(1)
        if (options[0] == "count"):
            print(count)
        sys.exit(fin)
    else:
        managers[manager].check()
        if (options[0] == "terse") or (options[0] == "list"):
            if (managers[manager].check_code == 8):
                print(colors.green + managers[manager].title_formated + "Updates available." + colors.none)
            else:
                print(colors.yellow + managers[manager].title_formated + "No updates available." + colors.none)
        if (options[0] == "terse"):
            pass
        elif (options[0] == "list"):
            if (managers[manager].check_code == 8):
                for p in managers[manager].check_text:
                    print("  " + p)
        elif (options[0] == "count"):
            print(len(managers[manager].check_text))
        else:
            print(colors.red + "Error: unkown check subcommand '" + options[0] + "'" + colors.none)
            sys.exit(1)
        sys.exit(managers[manager].check_code)


# Update packages
if (command == "update"):
    print(colors.violet + "!!Unimplemented 'update'!!" + colors.none)
    if not DEBUG:
        sys.exit(1)
    if not util.is_sudo():
        print(colors.red + "Error: This command must be run with superuser privileges" + colors.none)
        #sys.exit(1)
    if (manager == "all"):
        for m in managers.values():
            if (m.config_state < 1):
                continue
            m.update()
    else:
        managers[manager].update()
    sys.exit(0)

# Error out if command is not found
print(colors.red + "Error: Unknown command '" + command + "'" + colors.none)
sys.exit(1)
