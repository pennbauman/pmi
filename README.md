# Package Manager Investigator
A tool to allow monitoring packages from multiple package managers simultaneously.

## Install & Configure
Requires root access:

	./install.sh

	pmi setup

## Use

	pmi [manager] [command] [subcommand]

### Managers
- [DNF](https://fedoraproject.org/wiki/DNF)

- [Yum](https://fedoraproject.org/wiki/Yum)

- [Flatpak](https://www.flatpak.org/)

Generally if a manager is not specified all are used.

### Commands & Subcommands
- `version` Print version number
    - `message` (Default) Print message with number
    - `number` Print only the version number

- `help` Print this help menu

- `setup` Setup PMI and enable or disable managers

- `status` Check the state of available managers

- `enable` Enable the specified manager or picked managers
    - `ask` (Default when manager is all) Ask before enabling
    - `auto` (Default when manager specified) Do not ask before enabling

- `disable` Disable the specified manager or picked managers
    - `ask` (Default when manager is all) Ask before disabling
    - `auto`(Default when manager specified) Do not ask before disabling

- `check` (Default) Check for updates, return code is 8 when updates are available
    - `silent` Print nothing, for using only the return code
    - `terse` Print only if updates were found or not
    - `list` (Default) Print if updates were found and lists of packages
    - `count` Print the number of packages to update (0 for no updates)

If a command or subcommand is not specified the default is used.
