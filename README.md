# Package Manager Investigator
A tool to allow monitoring packages from multiple package managers simultaneously.

## Install & Configure
Requires root access:

	./install.sh

	pmi setup

## Use

	pmi [manager] [command] [options]

### Managers
- [DNF](https://fedoraproject.org/wiki/DNF)

- [Yum](https://fedoraproject.org/wiki/Yum)

- [Flatpak](https://www.flatpak.org/)

- [npm](https://www.npmjs.com/)

- [pip](https://pypi.org/project/pip/)

If a manager is not specified all are used.

### Commands

`version` Print version number. Accepts `--full` and `--plain`, `--full` is the default.

`help` Print a help menu. Accepts no options.

`setup` Setup PMI and enable or disable managers. Accepts no options.

`status` Check the state of available managers. Accepts no options.

`enable` Enable the specified manager or selected managers. Accepts `--ask` and `--yes` options, `--ask` is the default when a manager is not specified, `--yes` is the default otherwise.

`disable` Disable the specified manager or selected managers. Accepts `--ask` and `--yes` options, `--ask` is the default when a manager is not specified, `--yes` is the default otherwise.

`check` Check for updates, the return code is 8 when updates are available. Accepts with `--full`, `--plain`, `--silent`, and `--count` options, `--full` is the default.

`list` List all installed packages. Accepts with `--full`, `--plain`, and `--count` options, `--full` is the default.

If no command is not specified `check` is run.

### Options
`-a`, `--ask` Ask before preforming changes.

`-y`, `--yes` Preform requested changes without asking.

`-f`, `--full` Print full output with format.

`-p`, `--plain` Print simplified output without formatting.

`-s`, `--silent` Print nothing, useful to get return codes.

`-c`, `--count` Print only the count of packages.
