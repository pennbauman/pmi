# Package Manager Manager
A tool to allow managing packages form multiple package managers simultaneously.

## Install & Configure

	./install.sh

	pmm configure

## Usage

	pmm [command] [options] [package]

#### Commands
If run with no commands update is used.

`update` Updates all packages or the specified package.

`check` Check for updates for all packages or the specified package. Has a exit status of 8 if updates are available.

#### Options

`--dnf` Specify the DNF package manager.

`--flatpak` Specify the Flatpak package manager.

