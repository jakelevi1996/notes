# Useful `bash` commands

This is just a random collection of commands which are useful in Bash. This Gist is expected to grow over time (until I have mastered the whole of Bash). Another useful resource is this [list of Unix commands on Wikipedia](https://en.wikipedia.org/wiki/List_of_Unix_commands#List). Hyperlinked bash commands in general lead to relevant Man (manual) pages.

## Changing the bash prompt

The bash prompt can be changed by simply setting a new value to the `PS1` variable; here is an example using WSL:

```
PS C:\Users\Jake\Documents> bash
jake@Jakes-laptop:/mnt/c/Users/Jake/Documents$ PS1="$ "
$ echo test
test
$ date
Fri Apr 24 18:17:17 BST 2020
$
```

In order to change the prompt back to its previous value, store the value in a different variable before changing it:

```
PS C:\Users\Jake\Documents> bash
jake@Jakes-laptop:/mnt/c/Users/Jake/Documents$ DEFAULT=$PS1
jake@Jakes-laptop:/mnt/c/Users/Jake/Documents$ PS1="$ "
$ date
Fri Apr 24 18:25:49 BST 2020
$ PS1=$DEFAULT
jake@Jakes-laptop:/mnt/c/Users/Jake/Documents$
```

## Clear the console window

The console window can be cleared using the command `clear`.

## Iterating through files which match a file pattern

It is possible to iterate through files which match a file pattern by using a `for`/`in`/`do`/`done` loop, using the `*` syntax as a wildcard character for string comparisons, and using the `$` syntax to access the loop-variable ([source](https://stackoverflow.com/a/2305537/8477566)). For example, the following loop will print out all the files whose names start with `cnn_mnist_`:

```
for FILE in cnn_mnist_*; do echo $FILE; done
```

## `git`-moving files in a loop

The example above about "iterating through files which match a file pattern" can be modified to `git`-move all the files that start with `cnn_mnist_` into a subfolder called `cnn_mnist`. The `-n` flag tells `git` to do a "dry-run" (showing what will happen/checking validity of the command without actually executing the command); remove the `-n` flag to to actually perform the `git mv` command:

```
for FILE in cnn_mnist_*; do git mv -n $FILE cnn_mnist/$FILE; done
```

The following will do the above, but removing the `cnn_mnist_` from the start of each string using a bash parameter expansion:

```
for FILE in cnn_mnist_*; do NEW_FILE=${FILE//cnn_mnist_/}; git mv -n $FILE cnn_mnist/$NEW_FILE; done
```

## Search for files anywhere

To search for a file `file_to_search_for` in the directory `path/to/search`, use the [`find`](https://linux.die.net/man/1/find) command, EG:

```
sudo find path/to/search -name file_to_search_for
```

Note that the `find` command will automatically search recursively through subdirectories; sudo must be used to allow access to restricted directories. Patterns can be used, EG to search for any filename ending or file extension, but it may be necessary to put the `names` argument in single-quotes, to prevent a wildcard expansion to be applied before the program is called, as described in [this Stack Overflow answer](https://stackoverflow.com/a/6495536/8477566):

```
sudo find path/to/search -name 'file_to_search_for*'
```

Similarly, to check for Python scripts or shared object files:

```
sudo find path/to/search -name '*.py'
sudo find path/to/search -name '*.so'
```

To search the entire filesystem, replace `path/to/search` with `/`; this can be useful to check if a library is installed anywhere on the system, and return the location of that library, in case it is not on the system path (if it is on the system path, it can be found with [`which`](https://linux.die.net/man/1/which)).

## Connect to a WiFi network from the command line

As described in Part 3 of [this Stack Overflow answer](https://askubuntu.com/a/16588/1078405), a WiFi network can be easily connected to from the command line using the `nmcli` command:

```
nmcli dev wifi connect ESSID_NAME password ESSID_PASSWORD
```

To simply view a list of available WiFi networks:

```
nmcli dev wifi
```

## View the hostname

```
echo $HOSTNAME
```

## Viewing the properties of a file

The `file` command can be used to view the properties of a file, EG whether a shared library is 32-bit or 64-bit, and which platform it was compiled for:

```
$ file lib.c
lib.c: ASCII text, with CRLF line terminators
$ file lib.dll
lib.dll: PE32 executable (DLL) (console) Intel 80386, for MS Windows
$ file lib64.dll
lib64.dll: PE32+ executable (DLL) (console) x86-64, for MS Windows
```

## Viewing and editing the system path

To view the system path (directories in which executables can be run from any other directory without need to specify the path to the executable):

```bash
echo $PATH
```

This will print every directory on the system path, separated by a colon. To print each directory on a new line, there are multiple options; one option is to use a global (`g`) regular-expression substitution (`s`) using the Unix program [`sed`](https://en.wikipedia.org/wiki/Sed) (short for Stream EDitor) as follows, where `:` is the regular expression to be matched, and `\n` is what it is to be replaced with:

```bash
echo $PATH | sed 's/:/\n/g'
```

Another option is to use a [shell parameter expansion](https://stackoverflow.com/questions/13210880/replace-one-substring-for-another-string-in-shell-script/13210909):

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

To open a Windows path in WSL, open a Windows command prompt (Powershell or CMD) in that location, and run `bash` (with no arguments).

## Connecting to a serial device using WSL

To connect to a serial device using WSL (see above), the COM port for the serial device must be found in Windows Device Manager. Say the device is connected to COM3, it can be connected to from WSL with a baud rate of 115200 using the following command ([source 1](https://docs.microsoft.com/en-gb/archive/blogs/wsl/serial-support-on-the-windows-subsystem-for-linux), [source 2](https://www.scivision.dev/usb-tty-windows-subsystem-for-linux/)):

```bash
sudo chmod 666 /dev/ttyS3 && stty -F /dev/ttyS3 115200 && sudo screen /dev/ttyS3 115200
```

## Seeing available disk space

To see how much disk space is available, use the command `df`. To view the output in a human-readable format which chooses appropriate memory units for each file system (GB, MB, etc.), use the `-h` flag:

```
df -h
```

## View filesize

The command `ls` will list files and subdirectories in the directory that is specified as an argument (with no argument, the current directory is used by default). The `-l` flag is used to specify a long-list format, which gives extra data such as permissions, file-size in bytes, time of last edit, and more. The option `--block-size MB` can be used with the `-l` flag to specify file-sizes in megabytes. In this case, a single filename can be used as the main argument to `ls`, in which case only the details for the specified file will be listed. In summary, the syntax for viewing the size of a file in megabytes is:

```
ls -l --block-size MB path/to/file
```

## Reboot machine

A machine can be rebooted from terminal using `reboot`:

```
sudo reboot
```


## [Shutdown](https://youtu.be/MQOG5BkY2Bc) machine

A machine can be shut down from terminal using [`shutdown`](https://youtu.be/MQOG5BkY2Bc):

```
sudo shutdown now
```

This is useful for example for a [Coral Dev Board](https://coral.ai/products/dev-board/); as stated at the bottom of the [getting started guide](https://coral.ai/docs/dev-board/get-started/), the power cable should not be removed from the Dev Board while the device is still on, because this risks corrupting the system image if any write-operations are in progress. The Dev Board can be safely shutdown by calling in terminal `sudo shutdown now`; when the red LED on the Dev Board turns off, the power cable can be unplugged.

## Add user to group

To add a user to a group (which may be necessary for obtaining permissions to complete other tasks), use [`usermod`](https://linux.die.net/man/8/usermod):

```
sudo usermod -aG groupname username
```

## Check if user is part of a group

To see the groups of which a user is a member of, use the [`id`](http://man7.org/linux/man-pages/man1/id.1.html) command:
```
id -nG username
```

To see if the user is a member of a particular group, pipe the output from the `id` command into `grep` followed by the name of the relevant group; if the user is a member of this group, then a line of text from the output of `id` containing the name of that group will be printed; otherwise nothing will be printed. NB this can be used as an `if` condition, EG ([source](https://stackoverflow.com/questions/18431285/check-if-a-user-is-in-a-group)):

```bash
if id -nG "$USER" | grep -qw "$GROUP"; then echo $USER belongs to $GROUP; fi
```

NB the `q` and `w` flags are being used to make `grep` quiet, and only match whole words.

## View directory contents in a single column

To view directory contents in a single column (as opposed to the default table view of `ls`), using the `-1` flag (as in numerical one, not a letter L or I):

```
ls -1
```