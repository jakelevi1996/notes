# Useful `bash` commands

This is just a random collection of commands which are useful in Bash. This Gist is expected to grow over time (until I have mastered the whole of Bash). Another useful resource is this [list of Unix commands on Wikipedia](https://en.wikipedia.org/wiki/List_of_Unix_commands#List).

## Viewing the system path

To view the system path (directories in which executables can be run from any other directory without need to specify the path to the executable):

```bash
echo $PATH
```

This will print every directory on the system path, separated by a colon. To print each directory on a new line, use a [shell parameter expansion](https://stackoverflow.com/questions/13210880/replace-one-substring-for-another-string-in-shell-script/13210909):

```bash
echo -e "${PATH//:/'\n'}"
```

To add a new directory to the path ([source](https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path)):

```bash
PATH=$PATH:~/new/dir
```

## Changing access mode

Use `chmod` ("change mode") to change the access of a file or folder. The 3-digit octal number which follows `chmod` and precedes the file/folder which is being modified decides whether reading, writing, and execution is available to the user (the owner that created the file/folder), the group (the users from group that owner is member) and other (all other users) ([source](https://superuser.com/questions/295591/what-is-the-meaning-of-chmod-666)).

## Viewing the Linux distribution details

The command `lsb_release` is used to view details about the current Linux distribution under the Linux Standard Base (LSB), and optionally any LSB modules that the system supports. Using this command with flags `lsb_release -irc` will show the distributer ID of the Linux distribution which is running, the release number of the distribution, and the code name of the distribution, EG:

```
$ lsb_release -irc
Distributor ID: Ubuntu
Release:        18.04
Codename:       bionic
```

## WSL

WSL is the Windows Subsytem for Linux, which "[allows Linux binaries to run in Windows unmodified](https://www.petri.com/bash-out-of-beta-in-windows-10)", by adding a compatability layer which presumably allows Windows to interpret Linux binary [Executable Formats and Application Binary Interfaces](https://stackoverflow.com/questions/2059605/why-an-executable-program-for-a-specific-cpu-does-not-work-on-linux-and-windows).

## Connecting to a serial device using WSL

To connect to a serial device using WSL (see above), the COM port for the serial device must be found in Windows Device Manager. Say the device is connected to COM3, it can be connected to from WSL with a baud rate of 115200 using the following command ([source 1](https://docs.microsoft.com/en-gb/archive/blogs/wsl/serial-support-on-the-windows-subsystem-for-linux), [source 2](https://www.scivision.dev/usb-tty-windows-subsystem-for-linux/)):

```bash
$ sudo chmod 666 /dev/ttyS3 && stty -F /dev/ttyS3 115200 && sudo screen /dev/ttyS3 115200
```

## Seeing available disk space

To see how much disk space is available, use the command `df`. To view the output in a human-readable format which chooses appropriate memory units for each file system (GB, MB, etc.), use the `-h` flag, as in `df -h`.

## Reboot machine

A machine can be rebooted from terminal with the command `sudo reboot`.

## Add user to group

To add a user to a group (which may be necessary for obtaining permissions to complete other tasks), do `sudo usermod -aG groupname username` (see the [`usermod` Man page](https://linux.die.net/man/8/usermod) for a description of the `a` and `G` flags).

```bash
```
