# Package Manager Manager
A tool to allow managing packages form multiple package managers simultaneously.

## Install & Configure

	./install.sh

	pmm setup

## Usage

	pmm [manager] [command]

#### Managers
- [DNF](https://fedoraproject.org/wiki/DNF)

- [Flatpak](https://www.flatpak.org/)

Generally if a manager is not specified all are used.

#### Commands
- `version` Prints version number.

- `help` Prints help menu.

- `setup` Setup managers to be used.

- `state` Print the current configurations for all managers.

- `enable` Enable manager or interactively choose managers to enable.

- `disable` Disable manager or interactively choose managers to disable.

- `check` [Unimplemented!] Check for updates.

- `update` [Unimplemented!] Update.

If no commands is specified update is run.

