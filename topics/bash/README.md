# Notes on `bash`

This is just a random collection of commands which I have found useful in Bash. This Gist is expected to grow over time (until I have mastered the whole of Bash). Another useful resource is this [list of Unix commands on Wikipedia](https://en.wikipedia.org/wiki/List_of_Unix_commands#List). Hyperlinked bash commands in general lead to relevant Man (manual) pages.

## Contents

- [Notes on `bash`](#notes-on-bash)
  - [Contents](#contents)
  - [Run, control and view detached processes using `screen`](#run-control-and-view-detached-processes-using-screen)
  - [`ssh`](#ssh)
    - [Passwordless `ssh` terminals](#passwordless-ssh-terminals)
    - [Scripting individual `ssh` commands](#scripting-individual-ssh-commands)
    - [Displaying graphical user interfaces over `ssh` using Xming](#displaying-graphical-user-interfaces-over-ssh-using-xming)
    - [Jump over intermediate `ssh` connections using `ProxyJump`](#jump-over-intermediate-ssh-connections-using-proxyjump)
    - [Enable `ssh` server on remote machine](#enable-ssh-server-on-remote-machine)
    - [Automatically run commands after connection over SSH](#automatically-run-commands-after-connection-over-ssh)
  - [Synchronise remote files and directories with `rsync`](#synchronise-remote-files-and-directories-with-rsync)
  - [Useful commands for running experiments on a server](#useful-commands-for-running-experiments-on-a-server)
  - [Package management with `apt`](#package-management-with-apt)
    - [What's the difference between `apt` and `apt-get`?](#whats-the-difference-between-apt-and-apt-get)
    - [What's the difference between `apt update`, `apt upgrade`, `apt full-upgrade`, and `apt-get dist-upgrade`?](#whats-the-difference-between-apt-update-apt-upgrade-apt-full-upgrade-and-apt-get-dist-upgrade)
    - [Checking the version of an installed `apt` package using `apt list`](#checking-the-version-of-an-installed-apt-package-using-apt-list)
    - [Uninstalling packages and their dependencies](#uninstalling-packages-and-their-dependencies)
  - [List files in a directory ordered by date with `ls -halt`](#list-files-in-a-directory-ordered-by-date-with-ls--halt)
  - [Use `git push` with an authentication token](#use-git-push-with-an-authentication-token)
  - [View the Linux distribution name and version number using `lsb_release`](#view-the-linux-distribution-name-and-version-number-using-lsb_release)
  - [Download VSCode](#download-vscode)
  - [Multiline `bash` commands](#multiline-bash-commands)
  - [Get the current date and time and generate timestamped filenames with `date`](#get-the-current-date-and-time-and-generate-timestamped-filenames-with-date)
  - [Display date and time in `bash` history using `HISTTIMEFORMAT`](#display-date-and-time-in-bash-history-using-histtimeformat)
  - [Calculate running times of commands using `time`](#calculate-running-times-of-commands-using-time)
  - [Run script in the current shell environment using `source`](#run-script-in-the-current-shell-environment-using-source)
  - [Seeing available disk space (using `df`) and disk usage (using `du`)](#seeing-available-disk-space-using-df-and-disk-usage-using-du)
  - [View the return code of the most recent command using `$?`](#view-the-return-code-of-the-most-recent-command-using-)
  - [Use stdout from one command as a command-line argument in another using `$()` notation](#use-stdout-from-one-command-as-a-command-line-argument-in-another-using--notation)
  - [Serial communication using `minicom`](#serial-communication-using-minicom)
  - [Change users using `su`](#change-users-using-su)
  - [Finding access permissions using `stat`](#finding-access-permissions-using-stat)
  - [Changing access permissions using `chmod`](#changing-access-permissions-using-chmod)
  - [Change ownership of a file using `chown`](#change-ownership-of-a-file-using-chown)
  - [Recursively find word counts of all files with a particular file ending](#recursively-find-word-counts-of-all-files-with-a-particular-file-ending)
  - [View all of the most recent bash commands using `history`](#view-all-of-the-most-recent-bash-commands-using-history)
  - [View the full path to a file using `realpath`](#view-the-full-path-to-a-file-using-realpath)
  - [Fixing `$'\r': command not found` error when running a bash script in WSL using `dos2unix`](#fixing-r-command-not-found-error-when-running-a-bash-script-in-wsl-using-dos2unix)
  - [Extract (unzip) a `.tar.gz` file using `tar -xvzf`](#extract-unzip-a-targz-file-using-tar--xvzf)
  - [Compress (zip) a file or directory using `tar -czvf`](#compress-zip-a-file-or-directory-using-tar--czvf)
  - [Viewing available memory and swap files using `free`](#viewing-available-memory-and-swap-files-using-free)
  - [View running processes using `ps aux`](#view-running-processes-using-ps-aux)
  - [Useful `grep` commands](#useful-grep-commands)
  - [Useful `gcc` flags (including profiling with `gprof`)](#useful-gcc-flags-including-profiling-with-gprof)
  - [Counting the number of lines in a file using `wc`](#counting-the-number-of-lines-in-a-file-using-wc)
  - [Viewing the first/last `n` lines of a file using `head`/`tail`](#viewing-the-firstlast-n-lines-of-a-file-using-headtail)
  - [Changing the bash prompt](#changing-the-bash-prompt)
  - [Clear the console window using `clear`](#clear-the-console-window-using-clear)
  - [Iterating through files which match a file pattern](#iterating-through-files-which-match-a-file-pattern)
  - [Recursively `git add`-ing files (including files hidden by `.gitignore`)](#recursively-git-add-ing-files-including-files-hidden-by-gitignore)
  - [`git`-moving files in a loop](#git-moving-files-in-a-loop)
  - [Iteratively and recursively `git`-moving files one directory up](#iteratively-and-recursively-git-moving-files-one-directory-up)
  - [Search for files anywhere using `find`](#search-for-files-anywhere-using-find)
  - [Connect to a WiFi network from the command line using `nmcli`](#connect-to-a-wifi-network-from-the-command-line-using-nmcli)
  - [View the hostname and IP address using `hostname`](#view-the-hostname-and-ip-address-using-hostname)
  - [Viewing the properties of a file using `file`](#viewing-the-properties-of-a-file-using-file)
  - [Viewing and editing the system path](#viewing-and-editing-the-system-path)
  - [WSL](#wsl)
  - [Connecting to a serial device using WSL](#connecting-to-a-serial-device-using-wsl)
  - [View filesize using `ls -l`](#view-filesize-using-ls--l)
  - [Reboot/restart machine using `reboot`](#rebootrestart-machine-using-reboot)
  - [Shutdown machine](#shutdown-machine)
  - [Add user to group](#add-user-to-group)
  - [Check if user is part of a group](#check-if-user-is-part-of-a-group)
  - [View directory contents in a single column](#view-directory-contents-in-a-single-column)
  - [Storing `git` credentials](#storing-git-credentials)
  - [Automatically providing password to `sudo`](#automatically-providing-password-to-sudo)
  - [Sort `$PATH` and remove duplicates](#sort-path-and-remove-duplicates)
  - [Get the absolute path to the current `bash` script and its directory using `$BASH_SOURCE`](#get-the-absolute-path-to-the-current-bash-script-and-its-directory-using-bash_source)
  - [Create an `alias`](#create-an-alias)
  - [Create a symbolic link using `ln -s`](#create-a-symbolic-link-using-ln--s)
  - [Find CPU details (including model name) using `lscpu`](#find-cpu-details-including-model-name-using-lscpu)
  - [Change default shell](#change-default-shell)
  - [Add directory to the `$PATH` environment variable](#add-directory-to-the-path-environment-variable)
- [Alias `python` to `python3`](#alias-python-to-python3)

## Run, control and view detached processes using `screen`

TLDR:

```bash
# Reset logging output directory
rm -rf  ~/screen_output
mkdir   ~/screen_output
ls      ~/screen_output
ls      ~/screen_output -halt
# Run command (detach by pressing `ctrl+a` and then `d`)
TEST_NAME="insert_test_name_here"; screen -S ${TEST_NAME} -L -Logfile ~/screen_output/${TEST_NAME}.txt python3 scripts/SCRIPT_NAME.py --ARG_1 VAL_1 --ARG_2
# Run command in detached mode
TEST_NAME="insert_test_name_here"; screen -dmS ${TEST_NAME} -L -Logfile ~/screen_output/${TEST_NAME}.txt python3 scripts/SCRIPT_NAME.py --ARG_1 VAL_1 --ARG_2
# List running screen processes
screen -ls
# Attach to process (can use `pid.test_name` copied from `screen -ls`, or just `pid` or just `test_name`)
screen -r pid.test_name
# Kill detached process (can use `pid.test_name` copied from `screen -ls`, or just `pid` or just `test_name`)
screen -XS pid.test_name quit
```

Full tutorial:

- Say you have a long-running script, and you want to start the script running on the server, disconnect from the server without stopping the script, and later reconnect to the server and view the output from the script in real time
- As an example, consider a script that prints the current date and time once per second, which can be created as follows:

```bash
echo "while true; do date; sleep 1; done" > temp_script.sh && chmod +x temp_script.sh
```

- The script can be launched with the GNU program `screen` as follows:

```bash
screen bash temp_script.sh
```

- The output from the script will be printed to the terminal
- To detach from the screen process without killing the process, use the shortcut `ctrl a + d` (it doesn't matter if `ctrl` is still being pressed or not when `d` is pressed)
- To list currently running `screen` sessions, use the following command, which prints a list of screen sessions, each starting with an ID number:

```bash
screen -list
```

- To reattach to the screen session, use the following command (replacing `$ID_NUMBER` with the ID number of the screen session printed by `screen -list`, and entering a valid password if prompted):

```bash
screen -r $ID_NUMBER
```

- To resume a `screen` session "only when it’s unambiguous which one to attach", use the following command ([source](https://www.gnu.org/software/screen/manual/screen.html)):

```bash
screen -R
```

- To "resume the first appropriate detached screen session", use the following command ([source](https://www.gnu.org/software/screen/manual/screen.html)):

```bash
screen -RR
```

- To start a named session, use the `-S` flag, for example:

```bash
screen -S temp_session bash temp_script.sh
```

- After detaching from the session, it can be reattached to using its name (instead of its ID number) as follows:

```bash
screen -r temp_session
```

- To kill a session while it is attached, use the shortcut `ctrl + c` as usual
- To kill a detached session, use the following command (replacing the session name with its ID number if the session is unnamed or if there are multiple sessions with the same name)

```bash
screen -XS temp_session quit
```

- Note that an active `screen` session will continue to run after closing the terminal window (or `ssh` session) from which the screen command was started
- This means that any new (or old) terminal window (or `ssh` session) can be used to reattach to the session at a later point in time
- This is true regardless of whether the process is attached or detached when the terminal window or (`ssh` session) is killed, as long as the `screen` session itself is not actively terminated (IE using `ctrl + c` while the process is attached, or `screen -XS temp_session quit` while the process is detached)
- To start a session in detached mode, use the `-dm` flags, for example:

```bash
screen -dmS temp_session bash temp_script.sh
```

- To log the output to `stdout` from the `screen` session to a text file, use the flags `-L -Logfile $OUTPUT_FILENAME` (note that `screen` might log to the output file slowly, EG once every 10 seconds), for example:

```bash
screen -dmS temp_session -L -Logfile screen_output.txt bash temp_script.sh
```

- To view the output to the log file while it is being updated in real time, use the `tail` command with the `-f` flag, for example:

```bash
tail -f screen_output.txt
```

- To run a command after launching a detached `screen` session in a single command, use the syntax `--` to specify an end to the command line arguments for `screen`, for example (note that firstly the following example is a bit pointless because the output could be viewed simply by not launching the session in detached mode instead of afterwards opening the log file `tail`, and secondly the sleep is included because there may be a delay in creating the log file):

```bash
screen -dmS temp_session -L -Logfile screen_output.txt bash temp_script.sh -- && sleep 1 && tail -f screen_output.txt
```

- Environment variables can be set with the usual syntax by including the environment name and value before the `screen` command (the process launched by `screen` will inherit all environment variables from the parent process), as follows (after first modifying the dummy script to also print the value of the environment variable)

```bash
echo "while true; do date; echo \$CUDA_VISIBLE_DEVICES; sleep 1; done" > temp_script.sh && chmod +x temp_script.sh

CUDA_VISIBLE_DEVICES=7 screen -S temp_session -L -Logfile screen_output.txt bash temp_script.sh
```

- Environment variables can also be included in the arguments to screen (such as the session name, log file, and command arguments), for example:

```bash
VAR_1=hello_world VAR_2=another_variable VAR_3=yet_another_variable
screen -S temp_session_$VAR_1 -L -Logfile screen_output_$VAR_2.txt bash temp_script.sh --arg $VAR_3
```

- To embed environment variables in the middle of strings (not just at the ends), put the variable names in curly braces (not brackets):

```bash
screen -S temp_session_${VAR_1}_${VAR_2} -L -Logfile screen_output_${VAR_2}_${VAR_3}.txt bash temp_script.sh --arg ${VAR_3}_${VAR_1}
```

A good approach for organising commands, session names and log files is to set a `$TEST_NAME` environment variable based on the arguments that will be passed to the command, and then using `$TEST_NAME` to set the `screen` session name, log file (in a dedicated subdirectory to avoid clogging up the home directory), and potentially to pass as an argument to the command itself, for example:

```bash
mkdir ~/screen_output
DEVICE=2 SEED=3 GAME="IPD" TEST_NAME="unique_test_name_for_game_${GAME}_seed_${SEED}"
echo ${TEST_NAME}
CUDA_VISIBLE_DEVICES=${DEVICE} screen -S ${TEST_NAME} -L -Logfile ~/screen_output/${TEST_NAME}.txt python3 ~/dir_name/src/python_script.py --game ${GAME} --seed ${SEED} --output_dir output_dir_name/${TEST_NAME}
```

To set an environment variable *and use it* in a single line, separate setting the environment variable from the rest of the command using a semicolon:

```bash
TEST_NAME="insert_test_name_here"; screen -S ${TEST_NAME} -L -Logfile ~/screen_output/${TEST_NAME}.txt python3 scripts/SCRIPT_NAME.py --ARG_1 VAL_1 --ARG_2
```

- If running `screen` returns the error `mkdir: cannot create directory ‘/run/screen’: Permission denied`, use the following commands (with `sudo` privelages), which should fix the problem:

```bash
sudo mkdir /run/screen
sudo chmod 777 /run/screen/
```

## `ssh`

To open a terminal session on a remote Linux device on a local network, use the following command on the host device:

```
ssh username@hostname
```

After using this command, `ssh` should ask for the password for the specified user on the remote device.

If `stdout` is not being flushed over `ssh`, this problem can be fixed by passing the `-t` command to `ssh`, EG `ssh -t username@hostname` ([source](https://serverfault.com/a/437739/620693))

### Passwordless `ssh` terminals

To configure `ssh` to not request a password when connecting, use the following commands on the local device, replacing `$(UNIQUE_ID)` with a string which is unique to `username@hostname` (the password for `ssh-keygen` can be left blank, whereas the correct password for `username@hostname` needs to be entered when running `ssh-copy-id`):

```
ssh-keygen  -f ~/.ssh/id_rsa_$(UNIQUE_ID)
ssh-copy-id -i ~/.ssh/id_rsa_$(UNIQUE_ID) username@hostname
```

Now `username@hostname` can be connected to over `ssh` without needing to enter a password, using the command `ssh -i ~/.ssh/id_rsa_$(UNIQUE_ID) username@hostname`. To automate this further such that the path to the SSH key doesn't need to be entered when using `ssh`, edit `~/.ssh/config` using the following command:

```
nano ~/.ssh/config
```

Enter the following configuration, replacing `$(SHORT_NAME_FOR_REMOTE_USER)` with a short name which is unique to `username@hostname`:

```
Host $(SHORT_NAME_FOR_REMOTE_USER)
   User username
   Hostname hostname
   IdentityFile ~/.ssh/id_rsa_$(UNIQUE_ID)
```

Save and exit `nano`. `username@hostname` can now be connected to over `ssh` using the following command, without being asked for a password ([source](https://stackoverflow.com/a/41135590/8477566)):

```
ssh $(SHORT_NAME_FOR_REMOTE_USER)
```

This should also allow `rsync` to run without requesting a password, again by replacing `username@hostname` with `$(SHORT_NAME_FOR_REMOTE_USER)`.

If the above steps don't work and `ssh` still asks for a password, the following tips may be useful:
- Make sure that the `~` and `~/.ssh` directories and the `~/.ssh/authorized_keys` file on the remote machine have the correct permissions ([source 1](https://superuser.com/a/925859/1098000)) ([source 2](https://serverfault.com/a/271054/620693)) ([source 3](https://askubuntu.com/a/90465/1078405)):
  - `~` should not be writable by others. Check with `stat ~` and fix with `chmod go-w ~`
  - `~/.ssh` should have `700` permissions. Check with `stat ~/.ssh` and fix with `chmod 700 ~/.ssh`
  - `~/.ssh/authorized_keys` should have `644` permissions. Check with `stat ~/.ssh/authorized_keys` and fix with `chmod 644 ~/.ssh/authorized_keys`
- If the permissions were wrong and have been changed and passwordless `ssh` still doesn't work, consider restarting the `ssh` service with `service ssh restart` ([source](https://superuser.com/a/925859/1098000))
- Make sure that the line `PubkeyAuthentication yes` is present in `/etc/ssh/sshd_config` on the remote device, and not commented out with a `#` (as in `#PubkeyAuthentication yes`) ([source](https://superuser.com/a/904667/1098000)).
- Call `ssh-copy-id` with the `-f` flag on the local device
- Consider checking the permissions of the `id_rsa` files on the local machine ([source 1](https://serverfault.com/a/434498/620693)) ([source 2](https://unix.stackexchange.com/a/36687/421710))

If the `ssh-copy-id` command isn't available (EG if you're trying to configure SSH for Cygwin on Windows), a straightforward (albeit slightly manual) solution is to:

- Use the `ssh-keygen  -f ~/.ssh/id_rsa_$(UNIQUE_ID)` command as before (in Windows)
- Open the public key file `~/.ssh/id_rsa_$(UNIQUE_ID).pub` (note that it should be the `.pub` file containing the public key, not `~/.ssh/id_rsa_$(UNIQUE_ID)` containing the private key)
- Copy the contents of the public key file (EG `ssh-rsa AAAAB...o45upDR= jake@Jakes-laptop`)
- SSH into the remote machine
- Paste the contents of the public key file into the end of `~/.ssh/authorized_keys`

### Scripting individual `ssh` commands

To run individual commands on a remote device over `ssh` without opening up an interactive terminal, use the following syntax (the quotation marks can be ommitted if there are no space characters between the quotation marks):

```
ssh username@hostname "command_name arg1 arg2 arg3"
```

It may be found that commands in `~/.bashrc` on the remote device are not run when using the above syntax to run single commands over `ssh` on the remote device, which might be a problem EG if `~/.bashrc` adds certain directories to `$PATH` which are needed by the commands which are being run over `ssh`. This might be because the following lines are present at the start of `~/.bashrc` on the remote device:

```
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac
```

These lines cause `~/.bashrc` to exit if it's not being run interactively, which is the case when running single commands over `ssh`. To solve this problem, either put whichever commands that need to be run non-interactively in `~/.bashrc` before the line `case $- in`, or comment out the lines from `case $- in` to `esac` (inclusive) on the remote device ([source](https://serverfault.com/a/1062611/620693)).

### Displaying graphical user interfaces over `ssh` using Xming

From WSL on a Windows PC, it is possible to display graphical user interfaces which are running on a remote Linux device using X11 forwarding. To do so:

- Install Xming on the Windows machine from [here](https://sourceforge.net/projects/xming/)
- Make sure Xming is running on the Windows machine (there should be an icon for Xming in the icon tray in the Windows taskbar when Xming is running)
- Use the `-X` flag when connecting over `ssh`, EG `ssh -X username@hostname`
- Test that X11 forwarding is running succesfully by entering the command `xclock` in the `ssh` terminal, which should cause a clock face to appear on the Windows machine
- If this doesn't work, it may be necessary to use the command `export DISPLAY=localhost:0.0` in WSL, and/or to add this command to the bottom of `~/.bashrc` (EG using the command `echo "export DISPLAY=localhost:0.0" >> ~/.bashrc`) and restart the WSL terminal
- If an error message is displayed from the remote machine saying `connect localhost port 6000: Connection refused`, then make sure that Xming is running on the local machine

### Jump over intermediate `ssh` connections using `ProxyJump`

- Sometimes it is desirable to connect to `username@hostname` over `ssh`, but to do so it is necessary to first connect to `username_proxy@hostname_proxy` over `ssh`, and from `username_proxy@hostname_proxy` connect to `username@hostname` over `ssh`
- This can be automated by adding entries into `~/.ssh/config` (see section "[Passwordless `ssh` terminals and commands](#passwordless-ssh-terminals)" above) for `username@hostname` and `username_proxy@hostname_proxy` with aliases `shortname` and `shortname_proxy`, and under the configuration for `shortname`, add the line `ProxyJump shortname_proxy` (following the indentation of the lines above)
- Now, when using the command `ssh shortname`, `ssh` will automatically connect to `shortname_proxy` first, and from `shortname_proxy` connect to `shortname` over `ssh`
- Note that if using `ssh-keygen` and `ssh-copy-id` to log into `username@hostname` without a password (described above), then an entry for `username@hostname` should first be added to `~/.ssh/config` on the local machine (including the `ProxyJump` entry described above), then `ssh-keygen` and `ssh-copy-id` should be used on the local machine (not from `username_proxy@hostname_proxy`) to enable passwordless access to `username@hostname` directly from the local machine

### Enable `ssh` server on remote machine

Install `ssh` server using the following command ([source](https://askubuntu.com/q/1161579/1078405)):

```
sudo apt install openssh-server
```

Activate the `ssh` server ([source](https://www.siteground.co.uk/kb/connection-refused-error-ssh/)):

```
sudo service ssh start
```

### Automatically run commands after connection over SSH

- To automatically run a command on a remote machine after connection over SSH, append that command to the end of `~/.profile`
- This can be useful, for example, to automatically load a virtual environment when connecting to a server using the VS Code "Remote SSH" extension
  - Note that after updating `~/.profile`, it may be necessary to run the "Remote-SSH: Kill Current VS Code Server" command from within the VS Code Remote Window, and then restart the VS Code Remote Window, to prevent the VS Code Server from using a cached version of `~/.profile` ([source](https://stackoverflow.com/a/67403476/8477566))

## Synchronise remote files and directories with `rsync`

To synchronise a local directory with a remote directory, use the following command:

```
rsync -Chavz /path/to/local/dir username@hostname:~/path/to/remote
```

Description of flags:

Flag | Meaning
--- | ---
`-C` | Automatically ignore common temporary files, version control files, etc
`-h` | Use human-readable file sizes (EG `65.49K bytes` instead of `65,422 bytes`)
`-a` | Sync recursively and preserves symbolic links, special and device files, modification times, groups, owners, and permissions
`-v` | Verbose output is printed to `stdout`
`-z` | Compress files (EG text files) to reduce network transfer

([source 1](https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories)) ([source 2](https://linux.die.net/man/1/rsync))

- To configure `rsync` to not request a password when synchronising directories, follow the instructions in the previous section "[Passwordless `ssh` terminals and commands](#passwordless-ssh-terminals)".
- `rsync` can be used with the `--delete` option to delete extra files in the remote directory that are not present in the local directory ([source](https://askubuntu.com/a/665918/1078405)).
- To ignore certain files (EG hidden files, `.pyc` files), use the `--exclude $PATTERN` flag
  - Multiple `--exclude` flags can be included in the same command, EG `rsync -Chavz . hostname:~/target_dir --exclude ".*" --exclude "*.pyc"`
- To copy the contents of the *current directory on the local machine to* a subdirectory of the home directory called `target_dir` on the remote machine, use the command `rsync -Chavz . hostname:~/target_dir` (note *no* `/` character after `target_dir`)
- To copy the contents of a subdirectory of the home directory on the remote machine called `target_dir` *to the current directory on the local machine*, use the command `rsync -Chavz hostname:~/target_dir/ .` (note that there *is* a `/` character after `target_dir`)
- To ignore existing files (useful when synchronising from a server to the local machine after running an experiment remotely, without overwriting recent changes on the local machine), use the flag `--ignore-existing` ([source 1](https://unix.stackexchange.com/questions/67539/how-to-rsync-only-new-files), [source 2](https://linux.die.net/man/1/rsync))
- Summary of commands to synchronise files between the current directory and `~/dir/to/sync` on the remote machine, with all flags described above, ignoring hidden and `.pyc` files and not overwriting recent changes on the local machine:

```
rsync -Chavz . hostname:~/dir/to/sync  --exclude ".*" --exclude "*.pyc"
rsync -Chavz hostname:~/dir/to/sync/ . --exclude ".*" --exclude "*.pyc" --ignore-existing
```

## Useful commands for running experiments on a server

```bash
wc      -l      ~/.ssh/config
head    -n50    ~/.ssh/config

ssh HOSTNAME
exit

ssh HOSTNAME screen -ls

ssh HOSTNAME nvidia-smi

ssh HOSTNAME_1 nvidia-smi; ssh HOSTNAME_2 nvidia-smi

ssh HOSTNAME_1 nvidia-smi --loop=1 > .temp.txt
ssh HOSTNAME_1 ps -o user= -p 9318
ssh HOSTNAME_1 grep USERNAME /etc/passwd

ssh HOSTNAME ls             screen_output
ssh HOSTNAME wc     -l      screen_output/TEST_NAME.txt
ssh HOSTNAME tail   -n100   screen_output/TEST_NAME.txt

rsync -Chavz . HOSTNAME:~/PROJECT_DIR       --exclude ".*" --exclude "*.pyc" --exclude "*.egg-info"
rsync -Chavz ../OTHER_PROJECT HOSTNAME:~    --exclude ".*" --exclude "*.pyc" --exclude "*.egg-info"
rsync -Chavz HOSTNAME:~/PROJECT_DIR/ .      --exclude ".*" --exclude "*.pyc" --ignore-existing

cd ~/jutility
git pull
cd ~/PROJECT_DIR

scp HOSTNAME:~/screen_output/TEST_NAME.txt ./results

rm -rf  ~/screen_output
mkdir   ~/screen_output
ls      ~/screen_output
ls      ~/screen_output -halt

TEST_NAME="insert_test_name_here"; screen -S ${TEST_NAME} -L -Logfile ~/screen_output/${TEST_NAME}.txt python3 scripts/SCRIPT_NAME.py --ARG_1 VAL_1 --ARG_2
```

## Package management with `apt`

From the Wikipedia page ["APT (software)"](https://en.wikipedia.org/wiki/APT_(software)):

> Advanced package tool, or APT, is a free-software user interface that works with core libraries to handle the installation and removal of software on Debian, and Debian-based Linux distributions.

(Note that Ubuntu is a Debian-based Linux distribution).

### What's the difference between `apt` and `apt-get`?

([Source](https://askubuntu.com/a/446484/1078405))

> `apt-get` may be considered as lower-level and "back-end", and support other APT-based tools. `apt` is designed for end-users (human) and its output may be changed between versions.
>
> Note from apt(8):
>
> The `apt` command is meant to be pleasant for end users and does not need to be backward compatible like apt-get(8).

### What's the difference between `apt update`, `apt upgrade`, `apt full-upgrade`, and `apt-get dist-upgrade`?

([Source](https://askubuntu.com/a/222352/1078405))

- `apt update` updates `apt`'s package lists, which allows `apt` to know the newest available version of each package and its dependencies, and ensures that the newest available versions are used whenever installing or upgrading any new or existing packages (although note that `apt update` doesn't install, modify or upgrade any new or existing packages)
- `apt upgrade` updates all possible existing packages to the newest available versions that `apt` knows about from its package lists (which are updated with `apt update`) without removing any existing packages (EG if they are conflicting) or installing any new packages
- `apt full-upgrade` is equivalent to `apt-get dist-upgrade` ([source](https://superuser.com/a/1557279/1098000))
- `apt-get dist-upgrade` does everything that `apt-get upgrade` does and additionally intelligently handles dependencies, including removing obsolete packages and adding new packages when necessary

These commands can be combined using `&&`, for example:

```
sudo apt-get update && sudo apt-get dist-upgrade
```

As described in [this Stack Overflow answer](https://askubuntu.com/a/226213/1078405), as to why you would ever want to use `apt-get upgrade` instead of `apt-get dist-upgrade`:

> Using upgrade keeps to the rule: under no circumstances are currently installed packages removed, or packages not already installed retrieved and installed. If that's important to you, use `apt-get upgrade`. If you want things to "just work", you probably want `apt-get dist-upgrade` to ensure dependencies are resolved

### Checking the version of an installed `apt` package using `apt list`

To view the version of a installed package which is available through `apt` (Advanced Package Tool), use the command `apt list <package-name>` for a concise description, or `apt show <package-name>` for a more verbose output (see also `apt policy <package-name>`).

To view a list of all installed packages, use the command

```
apt list --installed
```

This list can be very large, so it might be sensible to redirect the output into a text file. To do this and then display the first 100 lines of the text file:

```
apt list --installed > aptlistinstalled.txt && head -n100 aptlistinstalled.txt
```

To achieve the same thing but without saving to a text file:

```
apt list --installed | head -n100
```

To list all installed packages which contain the string "`cuda`":

```
apt list --installed | grep cuda
```

### Uninstalling packages and their dependencies

([Source](https://askubuntu.com/a/187891/1078405))

- `apt-get remove packagename` will remove the binaries for `packagename`, but not its configuration files, data files (including those in users' home directories), or dependencies that were installed along with `packagename`
- `apt-get purge packagename` or `apt-get remove --purge packagename` (both commands are equivalent) will remove a package **and its configuration files** (useful for starting over with a package in case its configuration has become messed up), but not its data files (including those in users' home directories), or dependencies that were installed along with `packagename`
- `apt-get autoremove` removes all packages which were installed as a dependency of some package which is no longer present (useful after removing a package which had installed dependencies which are no longer needed)

Note that some packages are dummy packages, meaning they require very little installation except for several other packages which are installed as dependencies, and those dependencies are not always removed by running `apt autoremove`. Approaches for removing dependencies not removed by `autoremove` include:

- Check the output from `apt install packagename`/`apt-get install packagename` (if available) for all packages listed under the line `The following NEW packages will be installed:` and remove them manually
- Parse `/var/log/apt/term.log` to extract all dependencies that were installed when `packagename` was installed and remove them manually
- Run the command `apt show packagename`, and manually remove any packages listed as dependencies in the output from `apt show packagename` (and any dependencies of those dependencies, etc)
- Run the command `apt list --installed | grep packagename` to view any installed packages which contain `packagename` in their name, which are likely to be dependencies of `packagename`, and remove all such packages (and any dependencies of those packages, etc)

## List files in a directory ordered by date with `ls -halt`

Use the flags `-halt` with the `ls` command to list files, dates, and human readable file sizes in a directory ordered by date. "`ls -halt` is for `human readable`, `show hidden`, `print details`, `sort by date`" ([source](https://superuser.com/questions/147027/how-can-i-sort-the-output-of-ls-by-last-modified-date#comment821579_147030)). For example:

```
ls ~/screen_output -halt
```

## Use `git push` with an authentication token

```sh
git remote get-url origin
# https://github.com/${USERNAME}/${REPO_NAME}.git
git remote set-url origin https://git:${TOKEN_STR}@github.com/${USERNAME}/${REPO_NAME}.git
git push
```

To generate an authentication token for a GitHub repository:

- Go to account settings (not repistory settings) by clicking profile picture in top right corner, then "Settings"
- Click "Developer settings", "Personal access tokens", "Fine-grained tokens", "Generate new token"
- Enter "Token name"
- Optional: change "Expiration" to a date or "No expiration"
- Under "Repository access", select either "All repositories" or "Only select repositories"
- Click "Repository permissions", and next to "Contents", change "Access:" to "Read and write"
- Click "Generate token" and "Generate token"
- Copy and use the token

Notes:

- For setting authentication tokens to use with GitHub, `git:${TOKEN_STR}` can be replaced with `${USERNAME}:${TOKEN_STR}`, where `${USERNAME}` is the GitHub username, however using `git` instead of `${USERNAME}` works for GitHub, and also generalises to other remote repositories, EG those hosted on Overleaf, for which the username is an email address, which is not a valid URL component

## View the Linux distribution name and version number using `lsb_release`

The command `lsb_release` is used to view details about the current Linux distribution under the [Linux Standard Base (LSB)](https://en.wikipedia.org/wiki/Linux_Standard_Base), and optionally any LSB modules that the system supports. `lsb_release` accepts flags in order to display various different details (EG the distributer ID of the Linux distribution which is running, the release number of the distribution, the code name of the distribution, etc), but to simply display all details use the `-a` flag, EG:

```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.2 LTS
Release:        18.04
Codename:       bionic
```

## Download VSCode

[Source](https://code.visualstudio.com/docs/setup/linux)

```
sudo apt update
sudo apt upgrade
sudo snap install --classic code # or code-insiders
```

## Multiline `bash` commands

Option 1: backticks

```bash
# Run command
cmd_name        \
  subcmd_name   \
  --arg1 v1     \
  --arg2 v2 v3  \
  --flag
```

Option 2: [`bash` arrays](https://www.gnu.org/software/bash/manual/html_node/Arrays.html) ([source](https://superuser.com/a/1711721/1098000))

```bash
# Define command
cmd=(
  cmd_name
  subcmd_name
  --arg1 v1
  --arg2 "v2 v3"
  --flag
)
# Display command
echo "${cmd[@]}"
# Run command
"${cmd[@]}"
```

## Get the current date and time and generate timestamped filenames with `date`

The command `date` can be used to print the current date and time on the command line, or to get a string variable containing the current date and time which can be used in future commands, for example:

```
$ date
Fri Feb 11 14:53:37 GMT 2022
$ echo $(date) > ~/temp.txt
$ cat ~/temp.txt
Fri Feb 11 14:53:39 GMT 2022
```

It can also be used to generate a timestamped filename on the command line, for example:

```
$ mkdir ./temp && cd ./temp
$ ls
$ echo "Hello, world!" > "Info $(date '+%Y-%m-%d %H-%M-%S').txt"
$ ls
'Info 2022-09-06 13-35-13.txt'
```

## Display date and time in `bash` history using `HISTTIMEFORMAT`

Using the command `history 10` will display the last 10 `bash` commands that were used, but not when they were used (date and time). To include this information in the bash history in the current bash terminal, use the command `export HISTTIMEFORMAT="| %Y-%m-%d %T | "`. Note that using the command `history 10` will now display the date and time of commands that were used both before and after setting `HISTTIMEFORMAT`. To make this behaviour persist in future bash terminals, use the following commands ([source](https://stackoverflow.com/a/41975189/8477566)):

```
echo 'export HISTTIMEFORMAT="| %Y-%m-%d %T | "' >> ~/.bash_profile
source ~/.bash_profile
```

Example:

```
$ history 5
   94  | 2022-05-17 15:48:24 | ls /
   95  | 2022-05-17 15:48:28 | df -h
   96  | 2022-05-17 15:48:33 | cd ~
   97  | 2022-05-17 15:48:36 | ps
   98  | 2022-05-17 15:48:40 | history 5
```

## Calculate running times of commands using `time`

Prepend a `bash` command with `time` to print the running time of that command, EG `time ls /`. Note that arguments to the command being timed don't need to be placed in quotation marks (as is the case with running commands over `ssh`). `time` displays 3 statistics, which are described below ([source](https://stackoverflow.com/a/556411/8477566)):

- `real`: wall clock time, from start to finish of the command being run, including time that the process spends being blocked
- `user`: amount of CPU time spent in user-mode code (outside the kernel), NOT including time that the process spends being blocked, summed over all CPU cores
- `sys`: amount of CPU time spent in the kernel within the process (IE CPU time spent in system calls within the kernel, as opposed to library code, which is still running in user-space), NOT including time that the process spends being blocked, summed over all CPU cores

Note that `time` can be used to time multiple sequential commands, including commands which are themselves being timed using `time`, by placing those commands in brackets. For example:

```
$ time (time ps && time ls /etc/cron.daily)
  PID TTY          TIME CMD
 1035 tty1     00:00:00 bash
 1156 tty1     00:00:00 bash
 1157 tty1     00:00:00 ps

real    0m0.024s
user    0m0.000s
sys     0m0.016s
apport  apt-compat  bsdmainutils  dpkg  logrotate  man-db  mdadm  mlocate  passwd  popularity-contest  ubuntu-advantage-tools  update-notifier-common

real    0m0.026s
user    0m0.000s
sys     0m0.016s

real    0m0.052s
user    0m0.000s
sys     0m0.031s
```

## Run script in the current shell environment using `source`

Given a script called `./script`, running the command `source script` will run `script` in the current shell environment. This means that any environment variables etc set in `script` will persist in the current shell. This is different from running `./script` or `bash script` or `bash ./script`, which will execute the commands in `script` in a new shell environment, so any changes to the shell environment made by `script` will not persist in the current shell (EG if `script` changes an environment variable or sets a new one, the value of that environment variable will not persist once `script` has finished running).

This can be useful EG if making a change to `~/.bashrc` (`bashrc` stands for "Bash Run Commands", which are run every time a bash shell is started) using `nano`, and wanting to apply those changes to the current shell without closing it and starting a new one:

```
$ nano ~/.bashrc
$ # <Make changes to the shell in the nano text editor>
$ source ~/.bashrc
```

## Seeing available disk space (using `df`) and disk usage (using `du`)

To see how much disk space is available, use the command `df`. To view the output in a human-readable format which chooses appropriate memory units for each file system (GB, MB, etc.), use the `-h` flag:

```
df -h
```

To see the size of a file or directory, use the `du` command (`du` stands for disk usage) (again, use the `-h` flag for human-readable format). This program can accept multiple files and/or directories in a single command:

```
du -h file1 [file2 dir1 dir2 etc]
```

If a directory is given to `du`, `du` will recursively search through the directory and print the size of all files in the directory. To only print the total size of the directory, use the `-s` flag (short for `--summarize`).

`du` can also accept wildcards. For example, to print the sizes of all files and directories in the user's home directory (printing the size of directories, but not the files and subdirectories within), use the following command:

```
du -sh ~/*
```

Note that this is different to `du -sh ~` or `du -sh ~/`, which would only print the size of the home directory.

To print the sizes of all directories in the root directory (note that this command runs surprisngly quickly compared to searching through the filesystem on Windows):

```
sudo du -sh /*
```

To sort the output from `du`, pipe the input into `sort`, and [as described here](https://serverfault.com/a/156648/620693), if using the `-h` flag for `du`, then also provide the `-h` flag to `sort`, so that `sort` will sort according to human-readable file-sizes, as shown below:

```
du -sh /path/to/dir/* | sort -h
```

To view the `N` biggest file-sizes, pipe the output from the previous command into `tail`, for example:

```
du -sh /path/to/dir/* | sort -h | tail -n10
```

## View the return code of the most recent command using `$?`

View the return code of the most recent command run in the current `bash` process using the following command:

```
echo $?
```

It is also possible to use `$?` as a regular `bash` variable, EG it can be compared in logical conditions.

## Use stdout from one command as a command-line argument in another using `$()` notation

The stdout from one command can be used as a command-line argument in another using `$()` notation, as shown in the following examples:

```
$ echo $(ls -p)
gui_testing_data/ gui_test.py package.json package-lock.json README.md requirements.txt src/
$ wc -l $(ls -p | grep -v "/")
    39 gui_test.py
    24 package.json
  9671 package-lock.json
     9 README.md
     0 requirements.txt
  9743 total
```

The next example automatically finds the name of the serial device to use with `minicom`:

```
$ minicom --device $(ls -d /dev/serial/by-id/*) --baudrate 115200
```

(Note that the `-p` flag in `ls -p` is used "to append / indicator to directories", so that this can be piped into the `grep -v "/"` which removes all directories from the list, and the `-d` flag is used along with the `*` wildcard to print the full path to the serial device, instead of the relative path to `/dev/serial/by-id/`)

## Serial communication using `minicom`

To install `minicom`:

```
sudo apt-get update
sudo apt install minicom
```

To use `minicom` with a device whose name is `$DEVICE_NAME` in the `/dev/` folder and with a baud-rate of `$BAUD_RATE`:

```
minicom --device /dev/$DEVICE_NAME --baudrate $BAUD_RATE
```

## Change users using `su`

To change to the root user, use the command `sudo su`. This can alleviate some permission problems that are not solved even by using the `sudo` command. To return to the previous user, either use the command `sudo <username>`, or just use the command `exit`, EG:

```
$ tail -n1 /etc/iproute2/rt_tables
103 vlan3
$ sudo echo "105 vlan5" >> /etc/iproute2/rt_tables
bash: /etc/iproute2/rt_tables: Permission denied
$ sudo su
root# echo "105 vlan5" >> /etc/iproute2/rt_tables
root# exit
exit
$ tail -n1 /etc/iproute2/rt_tables
105 vlan5
```

## Finding access permissions using `stat`

Use the `stat` command to find the status of a file, including its access permissions, EG:

```
$ stat /etc/iproute2/rt_tables
  File: /etc/iproute2/rt_tables
  Size: 87              Blocks: 0          IO Block: 512    regular file
Device: 2h/2d   Inode: 1125899908643251  Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2019-05-21 15:43:05.544609577 +0100
Modify: 2018-01-29 16:08:52.000000000 +0000
Change: 2020-02-06 15:48:13.093754700 +0000
 Birth: -
```

For the permissions (next to `access`):
- As described in [Unix file types on Wikipedia](https://en.wikipedia.org/wiki/Unix_file_types):
  - The first character describes the file type
- As described in the [`chmod` man page](https://ss64.com/bash/chmod.html):
  - The next three characters (characters 2-4) describe read/write/execute permissions for the user who owns the file
  - The next three characters (characters 5-7) describe read/write/execute permissions for other users in the file's group
  - The next three characters (characters 8-10) describe read/write/execute permissions for other users NOT in the file's group

Therefore, `-rw-r--r--` says that this is a regular file, which is readable and writeable for the user who owns the file, and readable for everyone else.

## Changing access permissions using `chmod`

Use `chmod` ("change mode") to change the access permissions of a file or folder. As described in the [`chmod` man page](https://ss64.com/bash/chmod.html), the access permissions can be specified using letters (as described above in "Finding access permissions using `stat`") or in octal.

Alternatively, `chmod` can be used in symbolic mode, EG:
- `chmod u+x file` to make a file executable by the user/owner
- `chmod a+r file` to allow read permission to everyone
- `chmod a-x file` to deny execute permission to everyone
- `chmod go+rw file` to make a file readable and writable by the group and others

The examples above are taken from the [`chmod` man page](https://ss64.com/bash/chmod.html).

To make a file executable for all users, use the command `chmod +x /path/to/file`.

## Change ownership of a file using `chown`

Change the ownership of a file or directory using `chown`. If changing ownership of a directory, use the `-R` flag to also recursively change ownership of all subdirectories within that directory ([source](https://unix.stackexchange.com/a/119836/421710)). Example:

```
$ sudo chown username:groupname filename
$ sudo chown -R username:groupname dirname
$ sudo chown -R jake:jake dirname
```

## Recursively find word counts of all files with a particular file ending

The following command can be used to recursively find line counts of all files with a particular file ending (in this case `.py` for Python), excluding all files in the `venv` directory (or more specifically, any files containing the substring `venv` in their path). This is achieved by using a `$` character in the regular expression to match a line-ending, and using `\` to escape the `.` character. The sum of the line counts for all matching words is displaying at the bottom:

```
find |  grep "\.py$" | grep -v venv | xargs wc -l
```

TODO: turn this into a slightly more sophisticated Python scripy that accepts command line arguments specifying what filename ending to look for, and specifically ignoring directories containg the excluded words, and not filenames as well

## View all of the most recent bash commands using `history`

The `history` command prints out all of the previously recorded bash commands ([source](https://askubuntu.com/a/359125/1078405)). To view the most recent bash commands, the output from `history` can be piped into `tail`. For example, to print the 20 most recent bash commands:

```
history | tail -n20
```

To search for a specific command, the output from `history` can be piped into `grep`, EG:

```
$ history | grep realpath
  493  realpath ~
  505  history | grep realpath
```

## View the full path to a file using `realpath`

To view the full path to a file, use the `realpath` command, EG:

```
$ realpath ~
/home/jol
```

## Fixing `$'\r': command not found` error when running a bash script in WSL using `dos2unix`

As described [here](https://askubuntu.com/a/1046371/1078405), this is because of a carriage return used in DOS-style line endings. The problem can be solved as follows:

```
sudo apt-get update
sudo apt-get install dos2unix
dos2unix name_of_shell_script.sh
./name_of_shell_script.sh
```

## Extract (unzip) a `.tar.gz` file using `tar -xvzf`

A `.tar.gz` file can be unzipped easily in `bash` on Linux or in WSL.

To extract a file or direcrory ([source](https://askubuntu.com/a/25348/1078405)):

```bash
tar -xvzf compressed_file_name.tar.gz
```

To extract into a particular directory:

```bash
tar -xvzf compressed_file_name.tar.gz -C output_dir_name
```

Description of flags:

> - `x`: tar can collect files or extract them. x does the latter.
> - `v`: makes tar talk a lot. Verbose output shows you all the files being extracted.
> - `z`: tells tar to decompress the archive using gzip
> - `f`: this must be the last flag of the command, and the tar file must be immediately after. It tells tar the name and path of the compressed file.
> - `C`: means change to the directory specified by the following argument (NB this directory must already exist, if it doesn't then first create it using `mkdir`)

## Compress (zip) a file or directory using `tar -czvf`

A `.tar.gz` file can be created easily in `bash` on Linux or in WSL.

To zip up a file ([source](https://www.howtogeek.com/248780/how-to-compress-and-extract-files-using-the-tar-command-on-linux/)):

```
tar -czvf name-of-archive.tar.gz /path/to/directory-or-file
```

> Here’s what those switches actually mean:
>
> - `c`: Create an archive.
> - `z`: Compress the archive with gzip.
> - `v`: Display progress in the terminal while creating the archive, also known as "verbose" mode. The v is always optional in these commands, but it’s helpful.
> - `f`: Allows you to specify the filename of the archive.


## Viewing available memory and swap files using `free`

The `free` command can be used to view available RAM, RAM usage, and available/used memory in swap files. More information about how to create a swap file can be found in [this tutorial](https://linuxize.com/post/create-a-linux-swap-file/). The `-h` flag can be used with the `free` command to produce a more human-readable output:

```
$ free -h
              total        used        free      shared  buff/cache   available
Mem:            15G        8.8G        6.8G         17M        223M        6.9G
Swap:           29G         56M         29G
```

## View running processes using `ps aux`

`ps` and `top` are two commands which can be used to view running processes, their CPU usage, process ID, etc. They differ mainly in that "`top` is mostly used interactively", while "`ps` is designed for non-interactive use (scripts, extracting some information with shell pipelines etc.)", as described [in this Stack Overflow answer](https://unix.stackexchange.com/a/62186/421710) (see [here](https://superuser.com/questions/451344/difference-between-ps-output-and-top-output) for more differences).

One thing to notice in `top` is that some processes are suffixed by `d` to denote that they are daemon processes ([as described here](https://unix.stackexchange.com/a/72590)), and some processes are prefixe by `k` to denote that they are kernel threads ([as described here](https://superuser.com/a/1087716/1098000)).

When using `ps`, the following flags are useful, as described [here](https://unix.stackexchange.com/a/106848/421710):

- `a` - show processes for all users
- `u` - display the process's user/owner
- `x` - also show processes not attached to a terminal

It is often useful to pipe the output from `ps` into `grep` to narrow down the list of processes to those of interest, for example:

```
ps aux | grep -i cron
```

## Useful `grep` commands

`grep` stands for **G**lobal (-ly search for a) **R**egular **E**xpression (and) **P**rint (the results). It is especially useful for filtering the outputs of other command-line tools or files. Here are some useful features of `grep` (`TODO`: make this into a separate Gist?):

- The `-v` ("in**v**ert") flag can be used print only the lines which **don't** contain the specified string (this is the opposite of the normal behaviour of grep, which prints out lines which do contain the specified string). This can be useful when piping together `grep` commands, to include some search queries and exclude others, EG in the command `sudo find / | grep tensorrt | grep -v cpp`

  - Hint: put the inverted expression before the non-inverted expression to get the results of the non-inverted expression highlighted in the bash terminal output, if this feature is available and preferred

- The `-i` flag can be used for case-**i**nsensitive pattern-matching, IE `grep -i foo` will match `foo`, `FOO`, `fOo`, etc.

- `grep` can be used to search for strings within a file, using the syntax `grep <pattern> <file>` ([source](https://stackoverflow.com/a/48492465/8477566))

- The outputs from grep can be used as the input to a program which doesn't usually accept inputs from `stdin` using the `xargs` command, EG `find | grep svn | xargs rm -rfv` will recursively delete all files and folders in the current directory that contain the string `svn` (good riddance!) (the `-v` flag will also cause `rm` to be verbose about every file and folder which it deletes)

- ...

## Useful `gcc` flags (including profiling with `gprof`)

Flag | Meaning
--- | ---
`-H` | "Print the full path of include files in a format which shows which header includes which" (note that the header file paths are printed to `stderr`) ([source](https://stackoverflow.com/a/18593344/8477566))
`-M` | "Output a rule suitable for `make` describing the dependencies of the main source file. The preprocessor outputs one make rule containing the object file name for that source file, a colon, and the names of all the included files" (the dependencies include both the header files and source files) ([source 1](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#Preprocessor-Options), [source 2](https://stackoverflow.com/a/42513/8477566))
`-MM` | "Like `-M` but do not mention header files that are found in system header directories" ([source](https://gcc.gnu.org/onlinedocs/gcc/Preprocessor-Options.html#Preprocessor-Options))
`-fsanitize=address -fsanitize=undefined -fsanitize=float-divide-by-zero -fno-sanitize-recover` | "Enable AddressSanitizer, a fast memory error detector", and other useful Program Instrumentation Options ([source 1](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html)) ([source 2](https://man7.org/linux/man-pages/man1/gcc.1.html)). Note that it is necessary "to add `-fsanitize=address` to compiler flags (both `CFLAGS` and `CXXFLAGS`) and linker flags (`LDFLAGS`)" ([source](https://stackoverflow.com/a/40215639/8477566))
`-pg` | "From the man page of `gcc`": "Generate extra code to write profile information suitable for the analysis program `gprof`. You must use this option when compiling the source files you want data about, **and you must also use it when linking**." After compiling and linking using the `-pg` flags, execute the program, EG `./name_of_exe`, which should produce a file called `gmon.out`, and then use `gprof` to generate formatted profiling information as follows: `gprof name_of_exe gmon.out > analysis.txt` ([source](https://www.thegeekstuff.com/2012/08/gprof-tutorial/))
` -Xlinker -Map=output.map ` | Use these flags while linking to generate a map file called `output.map`, describing the data and instruction memory usage in the executable ([source](https://stackoverflow.com/a/38961713/8477566))

## Counting the number of lines in a file using `wc`

Use the program `wc` (which is a mandatory UNIX command, and stands for "word count") can be used to count the number of words, lines, characters, or bytes in a file. To count the number of lines in a file, use the `-l` flag, for example in the file `/etc/dhcp/dhclient.conf`:

```
wc -l /etc/dhcp/dhclient.conf
```

`wc` can also accept a list of files as separate arguments (separated by spaces).

As described on [the Wikipedia page for `wc`](https://en.wikipedia.org/wiki/Wc_(Unix)#Usage), the `-l`flag prints the line count, the `-c` flag prints the byte count, the `-m` flag prints the character count, the `-L` flag prints the length of the longest line (GNU extension), and the `-w` flag prints the word count. Example:

```
$ wc -l /etc/dhcp/dhclient.conf
54 /etc/dhcp/dhclient.conf
$ wc -w /etc/dhcp/dhclient.conf
207 /etc/dhcp/dhclient.conf
$ wc -c /etc/dhcp/dhclient.conf
1735 /etc/dhcp/dhclient.conf
$ wc -m /etc/dhcp/dhclient.conf
1735 /etc/dhcp/dhclient.conf
```

The `wc -l` command is useful for counting the number of lines in a file before printing the first or last N lines of the file using the `head` or `tail` commands (see below), where N ≤ the number of lines in the file.

## Viewing the first/last `n` lines of a file using `head`/`tail`

To view the first n lines of a text file, use the `head` command with the `-n` flag, EG:

```
$ head -n5 /etc/dhcp/dhclient.conf
# Configuration file for /sbin/dhclient.
#
# This is a sample configuration file for dhclient. See dhclient.conf's
#       man page for more information about the syntax of this file
#       and a more comprehensive list of the parameters understood by
```

Similarly, use the `tail` command to view the last n lines of a text file.

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

## Clear the console window using `clear`

The console window can be cleared using the command `clear`.

## Iterating through files which match a file pattern

It is possible to iterate through files which match a file pattern by using a `for`/`in`/`do`/`done` loop, using the `*` syntax as a wildcard character for string comparisons, and using the `$` syntax to access the loop-variable ([source](https://stackoverflow.com/a/2305537/8477566)). For example, the following loop will print out all the files whose names start with `cnn_mnist_`:

```
for FILE in cnn_mnist_*; do echo $FILE; done
```

## Recursively `git add`-ing files (including files hidden by `.gitignore`)

To recursively add all files in the current directory and all its subdirectories, use the following command (the `-f` flag instructs `git` to add files even if they included in `.gitignore`, which is useful EG for committing specific images):

```
git add ** -f
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

## Iteratively and recursively `git`-moving files one directory up

Following the examples above, to recursively `git`-move all files and folders in the current directory up by one directory (the `-n` flag is included here again to perform a dry run; remove the `-n` flag to perform an actual `git`-move command):

```
for FILE in ./*; do git mv -n $FILE ../$FILE; done
```

Note that `git` will recursively move the contents of any subdirectories by default.

## Search for files anywhere using `find`

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

Note that an alternative to using the `-name` flag is to pipe the output from `find` into `grep`, EG:

```
sudo find / | grep nvcc
```

Unlike using `-name`, `grep` will match the search query anywhere in the filename or directory (instead of an exact filename), without further modifications.

To only return paths to files from `find` and not include paths to directories, use the `-type f` option, EG:

```
sudo find / -type f | grep nvcc | grep -v docker  | wc -l
```

If no args are passed to `find` then it will recursively search through the current directory and print out the names of all files and subdirectories, EG `find | grep svn`.

## Connect to a WiFi network from the command line using `nmcli`

As described in Part 3 of [this Stack Overflow answer](https://askubuntu.com/a/16588/1078405), a WiFi network can be easily connected to from the command line using the `nmcli` command:

```
nmcli device wifi connect ESSID_NAME password ESSID_PASSWORD
```

To simply view a list of available WiFi networks:

```
nmcli device wifi
```

To view a list of *all* available internet connections (ethernet, wifi, etc):

```
nmcli device
```

Note that when running `nmcli` commands, `device`, `dev`, and `d` are all synonymous, and can be used interchangeably.

## View the hostname and IP address using `hostname`

To view the hostname, use the following command:

```
hostname
```

An alternative command is:

```
echo $HOSTNAME
```

To view the IP address, use the following command (see [this Stack Overflow answer](https://stackoverflow.com/a/13322549/8477566) for details):

```
hostname -I
```

## Viewing the properties of a file using `file`

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

## WSL

WSL is the Windows Subsytem for Linux, which "[allows Linux binaries to run in Windows unmodified](https://www.petri.com/bash-out-of-beta-in-windows-10)", by adding a compatability layer which presumably allows Windows to interpret Linux binary [Executable Formats and Application Binary Interfaces](https://stackoverflow.com/questions/2059605/why-an-executable-program-for-a-specific-cpu-does-not-work-on-linux-and-windows).

To open a Windows path in WSL, open a Windows command prompt (Powershell or CMD) in that location, and run `bash` (with no arguments).

## Connecting to a serial device using WSL

To connect to a serial device using WSL (see above), the COM port for the serial device must be found in Windows Device Manager. Say the device is connected to COM3, it can be connected to from WSL with a baud rate of 115200 using the following command ([source 1](https://docs.microsoft.com/en-gb/archive/blogs/wsl/serial-support-on-the-windows-subsystem-for-linux), [source 2](https://www.scivision.dev/usb-tty-windows-subsystem-for-linux/)):

```bash
sudo chmod 666 /dev/ttyS3 && stty -F /dev/ttyS3 115200 && sudo screen /dev/ttyS3 115200
```

## View filesize using `ls -l`

The command `ls` will list files and subdirectories in the directory that is specified as an argument (with no argument, the current directory is used by default). The `-l` flag is used to specify a long-list format, which gives extra data such as permissions, file-size in bytes, time of last edit, and more. The option `--block-size MB` can be used with the `-l` flag to specify file-sizes in megabytes. In this case, a single filename can be used as the main argument to `ls`, in which case only the details for the specified file will be listed. In summary, the syntax for viewing the size of a file in megabytes is:

```
ls -l --block-size MB path/to/file
```

## Reboot/restart machine using `reboot`

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

## Storing `git` credentials

As stated in [this StackOverflow answer](https://stackoverflow.com/a/52298381/8477566) to the question entitled [Visual Studio Code always asking for git credentials](https://stackoverflow.com/q/34400272/8477566), a simple but non-ideal solution to the problem is to use the following command:

```
git config --global credential.helper store
```

Note that this method is unsafe, because the credentials are stored in plain text in the file `~/.git-credentials`, and these credentials can become compromised if the system becomes hacked. Another solution, as stated in [this answer](https://stackoverflow.com/a/34627954/8477566), is to use the `git` credential helper to store the credentials in memory with a timeout (default is 15 minutes), EG:

```
git config --global credential.helper 'cache --timeout=3600'
# Set the cache to timeout after 1 hour (setting is in seconds)
```

Yet another solution, as stated in [this answer to a post on Reddit](https://www.reddit.com/r/vscode/comments/832xbj/how_to_stop_the_git_login_popup_in_vscode/dvf94cb?utm_source=share&utm_medium=web2x&context=3), is to use "Git Credential Manager Core (GCM Core)", as described in [these instructions](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git).

[This StackOverflow answer](https://stackoverflow.com/a/15382950/8477566) provides instructrions for how to unset the `git` credentials, using the following command:

```
git config --global --unset credential.helper
```

Note that the command `rm ~/.git-credentials` should also be used after the above command in order to delete the saved credentials.

This answer also states that:

> You may also need to do `git config --system --unset credential.helper` if this has been set in the system configuration file (for example, Git for Windows 2).

## Automatically providing password to `sudo`

As stated in [this StackOverflow answer](https://superuser.com/a/67766/1098000), `sudo` can be used with the `-S` switch, which causes `sudo` to read the password from `stdin`:

```
echo <password> | sudo -S <command>
```

## Sort `$PATH` and remove duplicates

These Python commands can be used on Linux to organise `$PATH` into alphabetical order and remove duplicates, and print the result to `stdout`:

```python
import os

path_list = os.getenv("PATH").split(":")
no_final_slash = lambda s: s[:-1] if (s[-1] == "/") else s
unique_path_set = set(no_final_slash(os.path.abspath(p)) for p in path_list)
sorted_unique_path_list = sorted(unique_path_set, key=lambda s: s.lower())

print("*** Separated by newlines ***")
print("\n".join(sorted_unique_path_list))
print("*** Separated by colons ***")
print(":".join(sorted_unique_path_list))
```

## Get the absolute path to the current `bash` script and its directory using `$BASH_SOURCE`

Use the variable `$BASH_SOURCE` to get the path to the current `bash` script. Use this with `realpath` and `dirname` to get the absolute path of the script, and its parent directory. For example:

```bash
X1=$BASH_SOURCE
X2=$(realpath $BASH_SOURCE)
X3=$(dirname $(realpath $BASH_SOURCE))
echo $X1
echo $X2
echo $X3
```

## Create an `alias`

Use `alias` to create an alias, EG `alias gcc-7=gcc`. This means that every time `bash` tries to use the command `gcc-7`, instead it will replace `gcc-7` with `gcc` (but the rest of the command will remain unchanged). This might be useful EG if a shell script assumes that `gcc-7` is installed, and keeps trying to call this version specifically with the command `gcc-7`, but instead a later version of `gcc` is installed that works equally well. Instead of installing an earlier version of `gcc`, using the command `alias gcc-7=gcc` will mean that every call to `gcc-7` is replaced with an equivalent call to `gcc`. This can be placed in `~/.bashrc` (short for `bash` Run Commands, which is run every time `bash` starts up) using the command `echo "alias gcc-7=gcc" >> ~/.bashrc`, and then either restarting the console, or running `source ~/.bashrc`.

```bash
echo "alias gcc-7=gcc" >> ~/.bashrc
```

## Create a symbolic link using `ln -s`

Use `ln` with the `-s` flag to create a symbolic link. This could be useful EG in the scenario described above in the context of `alias`, if `alias` is not working because the commands are not being run in `bash` (this might be the case in a `makefile` which uses `sh` instead of `bash`, see [here](https://unix.stackexchange.com/a/217245/421710)). Instead of using `alias gcc-7=gcc`, an alternative is to use `sudo ln -s /usr/bin/gcc /usr/bin/gcc-7`, which creates a symbolic link in `/usr/bin/` from `gcc-7` to `gcc`, which is more likely to be portable between different shells (not just `bash`).

```bash
sudo ln -s /usr/bin/gcc /usr/bin/gcc-7
```

## Find CPU details (including model name) using `lscpu`

Example:

```
$ lscpu
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              8
On-line CPU(s) list: 0-7
Thread(s) per core:  2
Core(s) per socket:  4
Socket(s):           1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               126
Model name:          Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz
Stepping:            5
CPU MHz:             1498.000
CPU max MHz:         1498.0000
BogoMIPS:            2996.00
Virtualization:      VT-x
Hypervisor vendor:   Windows Subsystem for Linux
Virtualization type: container
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave osxsave avx f16c rdrand lahf_lm abm 3dnowprefetch fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid avx512f avx512dq rdseed adx smap avx512ifma clflushopt intel_pt avx512cd sha_ni avx512bw avx512vl avx512vbmi umip pku avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg avx512_vpopcntdq rdpid ibrs ibpb stibp ssbd
```

## Change default shell

Use `chsh` to change default shell, EG from `sh` to `bash`. `chsh` asks for a password, and then the path to the new shell, EG `\bin\bash`. Changes take effect across the system after logging out and logging in again.

## Add directory to the `$PATH` environment variable

To add a directory to the `$PATH` environment variable, EG `/home/jakevi/.local/bin`, append the following line to the end of `~/.bashrc`:

```
export PATH="$PATH:/home/jakevi/.local/bin"
```

Then run the command `source ~/.bashrc` to reload the `~/.bashrc` profile in the current `bash` terminal.

[As explained here](https://superuser.com/a/18990/1098000), the reason for using the `export` command rather than just `PATH=...` is that `export` sets an environment variable, which will be available in subprocesses of the current shell process, whereas just setting `PATH=...` in general creates a shell variable, which is not necessarily available to subprocesses of the current shell process.

# Alias `python` to `python3`

Add the following line to the end of `~/.bashrc` ([source](https://askubuntu.com/a/1216095/1078405)):

```
alias python='python3'
```
