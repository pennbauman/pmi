# Package Manager Investigator
#   URL: https://github.com/pennbauman/pmi
#   License: GPLv3.0
#   Author:
#     Penn Bauman (pennbauman@protonmail.com)
import sys
import os

import util
import colors
from managers.manager import manager

# Globals
VERSION="1.2.4"
DEBUG=False
HELP=colors.bold + "Package Manager Investigator" + colors.none + "\n\
Usage:\n\
  pmi [manager] [command] [options]\n\
\n\
Package Managers:\n\
  all          : Run command for all mangers, this the default\n\
  dnf          : DNF for Fedora\n\
  yum          : Yum for Fedora, CentOS, and RHEL\n\
  pacman       : Pacman for archlinux\n\
  yay          : Yet Another Yogurt archlinux AUR helper\n\
  apt          : APT for Debian and Ubuntu\n\
  flatpak      : Flatpak\n\
  npm          : Node.js package manager\n\
  pip          : Python package manager\n\
\n\
Commands:\n\
  version      : Print version number\n\
                  Accepts --full and --plain\n\
                  --full is the default\n\
  help         : Print this help menu\n\
                  Accepts no options\n\
  setup        : Setup PMI and enable or disable managers\n\
                  Accepts no options\n\
  status       : Check the state of available managers\n\
                  Accepts no options\n\
  enable       : Enable the specified manager or selected managers\n\
                  Accepts --ask and --yes options\n\
                  --ask is the default when a manager is not specified\n\
                  --yes is the default otherwise\n\
  disable      : Disable the specified manager or selected managers\n\
                  Accepts --ask and --yes options\n\
                  --ask is the default when a manager is not specified\n\
                  --yes is the default otherwise\n\
  check        : Check for updates, the return code is 8 when updates are available\n\
                  This command is fun if no command is specified\n\
                  Accepts with --full, --plain, --silent, and --count options\n\
                  --full is the default\n\
  list         : List all installed packages\n\
                  Accepts with --full, --plain, and --count options\n\
                  --full is the default\n\
                  If a package name is provided to this command it will only list \n\
                   package including that name\n\
  search       : Search for packages to install based to provided search term\n\
                  Accepts --full and --plain\n\
                  --full is the default\n\
\n\
Options:\n\
  -a, --ask    : Ask before preforming changes\n\
  -y, --yes    : Preform requested changes without asking\n\
  -f, --full   : Print full output with format\n\
  -p, --plain  : Print simplified output without formatting\n\
  -s, --silent : Print nothing, useful to get return codes\n\
  -c, --count  : Print only the count of packages\n\
"


# Import Managers
managers = {}
# System package managers
if util.has_cmd("dnf"):
    from managers.dnf import dnf
    managers['dnf'] = dnf()
if util.has_cmd("yum"):
    from managers.yum import yum
    managers['yum'] = yum()
if util.has_cmd("pacman"):
    from managers.pacman import pacman
    managers['pacman'] = pacman()
if util.has_cmd("yay"):
    from managers.yay import yay
    managers['yay'] = yay()
if util.has_cmd("apt"):
    from managers.apt import apt
    managers['apt'] = apt()
# Sandboxed package managers
if util.has_cmd("flatpak"):
    from managers.flatpak import flatpak
    managers['flatpak'] = flatpak()
# Language package managers
if util.has_cmd("npm"):
    from managers.npm import npm
    managers['npm'] = npm()
if util.has_cmd("pip"):
    from managers.pip import pip
    managers['pip'] = pip()


# List of possible main commands
available_cmds = {
        "version", "setup", "status", "enable", "disable", # tools commands
        "check", "list", "search" # manager commands
    }
help_cmds = {"help", "-help", "--help", "-h", "--h"}
# List of possible options (and their abbreviations)
available_opts = {
        "-a":"ask", "--ask":"ask", "-y":"yes", "--yes":"yes",
        "-f":"full", "--full":"full", "-p":"plain", "--plain":"plain",
        "-s":"silent", "--silent":"silent", "-c":"count", "--count":"count",
    }
# Setup arguements list
args=[
        "", # command
        "", # manager
        [], # options
        ""  # package
    ]

# Parse command line options
i=1
while (i < len(sys.argv)):
    if sys.argv[i] in help_cmds:
        args[0] = "help"
    elif sys.argv[i] in available_cmds:
        args[0] = sys.argv[i]
    elif (sys.argv[i] in managers) or (sys.argv[i] == "all"):
        args[1] = sys.argv[i]
    elif sys.argv[i][0] == "-":
        if not sys.argv[i] in available_opts:
            util.error("Unknown option '" + sys.argv[i] + "'")
        args[2].append(sys.argv[i])
    else:
        if (args[0] == ""):
            util.error("Unknown command '" + sys.argv[i] + "'")
        if (args[3] == ""):
            args[3] = sys.argv[i]
        else:
            util.error("Invalid extra input '" + args[3] + "'", False)
    i += 1


# Check if default command should be used
if (args[0] == ""):
    args[0] = "check"
# Defualt to all managers
if (args[1] == ""):
    args[1] = "all"


# Check for package provided to tool commands
if (args[0] == "version") or (args[0] == "setup") or (args[0] == "status") or \
        (args[0] == "enable") or (args[0] == "disable"):
    if (args[3] != ""):
        util.error("Invalid input for " + args[0] + " command '" + args[3] + "'", \
                False)

# Check invalid options
if (args[0] == "version"):
    for o in args[2]:
        if (available_opts[o] == "full") or (available_opts[o] == "plain"):
            pass
        else:
            util.error("Invalid options for " + args[0] + " command '" + o + "'")
if (args[0] == "setup") or (args[0] == "status"):
    if (len(args[2]) > 0):
        util.error("Invalid options for " + args[0] + " command '" + args[2][0] \
                + "'")
if (args[0] == "enable") or (args[0] == "disable"):
    for o in args[2]:
        if (available_opts[o] == "ask") or (available_opts[o] == "yes"):
            pass
        else:
            util.error("Invalid options for " + args[0] + " command '" + o + "'")
if (args[0] == "check"):
    for o in args[2]:
        if (available_opts[o] == "full") or (available_opts[o] == "plain"):
            pass
        elif (available_opts[o] == "silent") or (available_opts[o] == "count"):
            pass
        else:
            util.error("Invalid options for " + args[0] + " command '" + o + "'")
if (args[0] == "list"):
    for o in args[2]:
        if (available_opts[o] == "full") or (available_opts[o] == "plain"):
            pass
        elif (available_opts[o] == "count"):
            pass
        else:
            util.error("Invalid options for " + args[0] + " command '" + o + "'")


# Check conflicting options
for o1 in args[2]:
    for o2 in args[2]:
        opt1 = available_opts[o1]
        opt2 = available_opts[o2]
        if ((opt1 == "ask") and (opt2 == "yes")) or \
                ((opt1 == "full") and (opt2 == "plain")) or \
                ((opt1 == "full") and (opt2 == "silent")) or \
                ((opt1 == "full") and (opt2 == "count")) or \
                ((opt1 == "plain") and (opt2 == "silent")) or \
                ((opt1 == "plain") and (opt2 == "count")) or \
                ((opt1 == "silent") and (opt2 == "count")):
            util.error("Conflicting options '" + o1 + "' and '" + o2 + "'")
            sys.exit(1)

# Set all options to their code
i=0
while (i < len(args[2])):
    args[2][i] = available_opts[args[2][i]]
    i += 1

if (args[1] != "all"):
    managers = {args[1]:managers[args[1]]}


if DEBUG:
    print("Cmd: '%s', Mng: '%s', Opt: %s, Pkg: '%s'" % (args[0], args[1], args[2], args[3]))
    print("Config: " + util.get_config_dir())



# Print version
if (args[0] == "version"):
    if "plain" in args[2]:
        print(VERSION)
    else:
        print("Package Manager Investigator : v" + VERSION)
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
    for m in managers.values():
        if (args[1] == "all"):
            if (m.config_state == 1):
                pass
            elif "yes" in args[2]:
                m.enable()
            else:
                if util.ask("Enable " + m.title):
                    m.enable()
        else:
            if "ask" in args[2]:
                if util.ask("Enable " + m.title):
                    m.enable()
            else:
                m.enable()
    sys.exit(0)
# Disable specific manager, or enter interactive disabler
if (args[0] == "disable"):
    for m in managers.values():
        if (args[1] == "all"):
            if (m.config_state == -1):
                pass
            elif "yes" in args[2]:
                m.disable()
            else:
                if util.ask("Disable " + m.title):
                    m.disable()
        else:
            if "ask" in args[2]:
                if util.ask("Disable " + m.title):
                    m.disable()
            else:
                m.disable()
    sys.exit(0)


# Check for unconfigured managers
unconfigured = False
for m in managers.values():
    if (m.config_state == 0):
        m.enabled_error()

# Check for disabled manager being specified
if (args[1] != "all"):
    if (managers[args[1]].config_state < 0):
        managers[args[1]].enabled_error()

# Check if duplicate managers are inabled
if "dnf" in managers and "yum" in managers:
    if (managers["dnf"].config_state == 1) and (managers["yum"].config_state == 1):
        print(colors.yellow + "Warning: Both Yum and DNF enabled, they will act as duplicates." + colors.none)
if "pacman" in managers and "yay" in managers:
    if (managers["pacman"].config_state == 1) and (managers["yay"].config_state == 1):
        print(colors.yellow + "Warning: Both Pacman and Yay enabled, they will act as duplicates." + colors.none)


# Check for available updates
if (args[0] == "check"):
    fin = 0
    count = 0
    for m in managers.values():
        if (m.config_state < 1):
            continue
        result = m.check()
        if (m.check_code == 8):
            fin = 8
        if "silent" in args[2]:
            pass
        elif "count" in args[2]:
            count += len(m.check_text)
        elif "plain" in args[2]:
            for p in m.check_text:
                print(p)
        else:
            m.check_print()
    if "count" in args[2]:
        print(count)
    sys.exit(fin)

# List installed packages
if (args[0] == "list"):
    count = 0
    for m in managers.values():
        if (m.config_state < 1):
            continue
        m.list(args[3])
        if "count" in args[2]:
            count += len(m.list_text)
        elif "plain" in args[2]:
            for p in m.list_text:
                print(p)
        else:
            m.list_print()
    if "count" in args[2]:
        print(count)
    sys.exit(0)

# Search for packages to install
if (args[0] == "search"):
    if (args[3] == ""):
        util.error("Search command requires an arguement", False)
    for m in managers.values():
        if (m.config_state < 1):
            continue
        m.search(args[3])
        if "plain" in args[2]:
            for p in m.search_text:
                print(p)
        else:
            m.search_print()
    sys.exit(0)


# Error out if command is not found
util.error("Unknown command '" + args[0] + "'")
sys.exit(1)
