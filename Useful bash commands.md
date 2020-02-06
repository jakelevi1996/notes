# Useful `bash` commands

This is just a random collection of commands which are useful in Bash. This Gist is expected to grow over time (until I have mastered the whole of Bash).

## Viewing the system path

To view the system path (directories in which executables can be run from any other directory without need to specify the path to the executable):

```bash
echo $PATH
```

This will print every directory on the system path, separated by a colon. To print each directory on a new line, use a [shell parameter expansion](https://stackoverflow.com/questions/13210880/replace-one-substring-for-another-string-in-shell-script/13210909):

```bash
echo -e "${PATH//:/'\n'}"
```

## Changing access mode

Use `chmod` ("change mode") to change the access of a file or folder. The 3-digit octal number which follows `chmod` and precedes the file/folder which is being modified decides whether reading, writing, and execution is available to the user (the owner that created the file/folder), the group (the users from group that owner is member) and other (all other users) ([source](https://superuser.com/questions/295591/what-is-the-meaning-of-chmod-666)).


```bash
```