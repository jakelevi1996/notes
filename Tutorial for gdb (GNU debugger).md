# Tutorial for `gdb` (GNU debugger)

## Contents

- [Tutorial for `gdb` (GNU debugger)](#tutorial-for-gdb-gnu-debugger)
  - [Contents](#contents)
  - [References](#references)
  - [Compiling and opening a program in `gdb`](#compiling-and-opening-a-program-in-gdb)
  - [Useful `gdb` commands](#useful-gdb-commands)
  - [Examples](#examples)
    - [Using `backtrace`/`bt`](#using-backtracebt)
    - [Using `dump` (and loading a binary file from Python)](#using-dump-and-loading-a-binary-file-from-python)
    - [Scripting `gdb` from the command line](#scripting-gdb-from-the-command-line)
    - [Open `gdb` with a core file](#open-gdb-with-a-core-file)
    - [Attach `gdb` to a running process](#attach-gdb-to-a-running-process)

## References

-   [University of Toronto CS: GDB Tutorial](http://www.cs.toronto.edu/~krueger/csc209h/tut/gdb_tutorial.html)
-   [University of Maryland CS: GDB Tutorial](https://www.cs.umd.edu/~srhuang/teaching/cmsc212/gdb-tutorial-handout.pdf)
-   [Tutorials point: GNU debugger tutorial](https://www.tutorialspoint.com/gnu_debugger/gnu_debugger_tutorial.pdf)
-   [sourceware.org](https://sourceware.org/):
    -   [Examining Memory](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html)
    -   [Copy Between Memory and a File](https://sourceware.org/gdb/current/onlinedocs/gdb/Dump_002fRestore-Files.html)
-   Stack Overflow questions:
    -   [What are the best ways to automate a GDB debugging session?](https://stackoverflow.com/questions/10748501/what-are-the-best-ways-to-automate-a-gdb-debugging-session)
    -   [Gdb dump memory in specific region, save formatted output into a file](https://stackoverflow.com/questions/16095948/gdb-dump-memory-in-specific-region-save-formatted-output-into-a-file)
    -   [Gdb print to file instead of stdout](https://stackoverflow.com/questions/5941158/gdb-print-to-file-instead-of-stdout)
    -   [Printing all global variables/local variables](https://stackoverflow.com/questions/6261392/printing-all-global-variables-local-variables)

## Compiling and opening a program in `gdb`

Consider the following C program, `temp.c`:

```c
#include <stdio.h>

void f(int x) {
    printf("Inside function f(x), x = %i\n", x);
}

void g(int x) {
    printf("Inside function g(x), x = %i\n", x);
}

int main() {
    int x[20];
    for (int i = 0; i < 20; i++) {
        x[i] = i + 100;
    }
    for (int i = 0; i < 20; i++) {
        printf("x[%i] = %i\n", i, x[i]);
    }
    f(3);
    g(4);
    f(5);
    g(6);
}

```

To compile this program with debugging symbols (which is necessary for debugging with `gdb`), compile this program using the `-g` flag as follows:

```
$ gcc ./temp.c -o ./temp -g
```

To open the program in `gdb`:

```
$ gdb temp
GNU gdb (Ubuntu 9.1-0ubuntu1) 9.1
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from temp...
(gdb)
```

The `gdb` prompt is now open.

## Useful `gdb` commands

Full command | Abbreviation | Description
--- | --- | ---
`help` | | Get help on a particular command, EG `help run`
`file FILE` | | Use `FILE` as program to be debugged.
`break temp.c:28` | `b temp.c:28` | Set a breakpoint in the file `temp.c` at line 28
`break f` | `b f` | Set a breakpoint at the start of the `f` function
`run` | `r` | Start the program and run until the end of the program/the program crashes/the next breakpoint/the next watchpoint (if the program is already running, this command will tell the program to start from the beginning)
`continue` | `c` | Continue running until the end of the program/the program crashes/the next breakpoint/the next watchpoint
`next` | `n` | Execute the current command, and move to the next command in the program (if the current command is a function call, then execute the whole function and return from it)
`step` | `s` | Step through the current command, but if this command is a function call, then go to the first line of that function
`finish` | | Run until the current function is finished
`until` | `u` | This is like `n`, except that if we are in a loop, `u` will continue execution until the loop is exited
| | | [No command] Repeat the previous command (useful if repeating the same command repeatedly, EG stepping through a loop)
`list` | | Print the current line, and a few lines above and below
`backtrace` | `bt` | List all the function calls in the stack frame at the current location
`print x` | | Print the value of the variable `x`. If it is an array, the whole array is printed. The `->`, `*` and `.` operators can be used in case `x` is a struct/pointer/pointer to a struct, or even print the entire contents of the struct
`print/x x` | | Print the value of the variable `x` in hexadecimal
`x addr` | | Print value at memory location `addr`
`x/nfu addr` | | Examine memory in the specified format (see [sourceware.org: "Examining Memory"](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html))
`watch x` | | Place a watchpoint on variable `x`, meaning that the program will pause whenever the value of `x` is modified, and the old and new values of `x` will be printed (if `x` is an array, then the program will pause and print out the old and new values of the whole array whenever any element of `x` is modified)
`condition N COND` | | Specify breakpoint number `N` to break only if `COND` is true (this can also be achieved using `break` in a single command using the syntax `break file.c:N if COND`)
`info breakpoints` | | Display information about all declared breakpoints
`info variables` | | List all global and static variable names
`info locals` | | List local variables of current stack frame (names and values), including static variables in that function.
`info args` | | List arguments of the current stack frame (names and values)
`delete` | | Delete all breakpoints that have been set
`delete n` | | Delete breakpoint number `n`
`clear function_name` | | Deletes the breakpoint set in that function
`dump memory filename start_addr end_addr` | | Copy binary data starting at `start_addr` and ending at `end_addr` (not including `end_addr`) into a binary file called `filename`. `start_addr` and `end_addr` can refer to variables and use array and pointer operators, EG `dump memory x.bin x &x[20]`. See section [Using `dump` (and loading a binary file from Python)](#using-dump-and-loading-a-binary-file-from-python) below for an example of how to load this memory in Python
`dump value filename expr` | | Copy binary data starting from `expr` into a binary file called `filename`. If `expr` is the name of an array, then the whole array is copied, EG `dump value x.bin x` is the same as `dump memory x.bin x &x[20]` if x is an array of length 20
`restore filename binary bias start end` | | Restore the contents of binary file `filename` into memory
`set max-value-size unlimited` | | Remove the limit on the maximum value size. This can be useful when trying to use the `dump` command on a value which is too big, in which case an error message will be displayed which says `value requires 115202 bytes, which is more than max-value-size` (or similar)
`set logging on` | | Enable logging
`set logging file filename` | | Tell `gdb` to store logging outputs in a file called `filename` (without calling this command, the default filename for logging outputs is `gdb.txt`)
`quit` | | Exit `gdb`

## Examples

### Using `backtrace`/`bt`

```
(gdb) file temp
Reading symbols from temp...
(gdb) b f
Breakpoint 1 at 0x1169: file .temp.c, line 14.
(gdb) r
Starting program: /home/airport/fac_receiver/temp 

Breakpoint 1, f (x=0) at .temp.c:14
14      void f(int x) {
(gdb) bt
#0  f (x=0) at .temp.c:14
#1  0x00005555555551de in main () at .temp.c:23
(gdb) 
```

### Using `dump` (and loading a binary file from Python)

Load `temp`, fill array `x`, and save it to a binary file:

```
(gdb) file temp
Reading symbols from temp...
(gdb) b f
Breakpoint 1 at 0x1169: file .temp.c, line 14.
(gdb) r
Starting program: /home/airport/fac_receiver/temp 

Breakpoint 1, f (x=0) at .temp.c:14
14      void f(int x) {
(gdb) bt
#0  f (x=0) at .temp.c:14
#1  0x00005555555551de in main () at .temp.c:23
(gdb) finish
Run till exit from #0  f (x=0) at .temp.c:14
Inside function f(x), x = 2
main () at .temp.c:25
25          for (int i = 0; i < 20; i++) {
(gdb) c
Continuing.
x[0] = 100
x[1] = 101
...
x[19] = 119

Breakpoint 1, f (x=2) at .temp.c:14
14      void f(int x) {
(gdb) finish
Run till exit from #0  f (x=2) at .temp.c:14
Inside function f(x), x = 3
main () at .temp.c:32
32          g(4);
(gdb) bt
#0  main () at .temp.c:32
(gdb) dump memory x.bin x &x[20]
```

This creates the file `x.bin`, which can be restored as a list of integers within Python using the `struct` module as follows:

```python
import struct

with open("x.bin", "rb") as f:
    b = f.read()

print(len(b))
# >>> 80

x = struct.unpack("20i", b)

print(x)
# >>> (100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119)
```

### Scripting `gdb` from the command line

To automatically run a series of commands in `gdb` without having to enter them manually one by one, start of by saving the commands in a text file, separated by new lines, called `gdb_script.cmd`:

```
file temp
break f
run
backtrace
finish
continue
finish
backtrace
dump memory x.bin x &x[20]
quit
```

To compile `temp.c`, open it in `gdb`, and run the commands in `gdb_script.cmd`, use the following commands in a bash terminal:

```
$ gcc temp.c -o temp -g
$ gdb temp --command=gdb_script.cmd
```

Batch mode can be used to disable pagination and exit once the command files have finished processing with zero/nonzero status depending on if an error occurs in executing the GDB commands (meaning `quit` does not have to be included at the end of `gdb_script.cmd`) using the `-batch` command line argument:

```
$ gdb temp --command=gdb_script.cmd -batch`
```

To run in batch mode and also prevent all output from `gdb` to `stdout`, use the `-batch-silent` command line argument:

```
$ gdb temp --command=gdb_script.cmd -batch-silent`
```

See [sourceware.org](https://sourceware.org/) for more information on [invoking GDB](https://sourceware.org/gdb/current/onlinedocs/gdb/Invoking-GDB.html#Invoking-GDB), [file options](https://sourceware.org/gdb/current/onlinedocs/gdb/File-Options.html#File-Options), and [mode options](https://sourceware.org/gdb/current/onlinedocs/gdb/Mode-Options.html#Mode-Options).

`gdb` command files can include comments (which are not executed) by starting a line with `#`.

### Open `gdb` with a core file

The most usual way to start `gdb` is with one argument, specifying an executable program:

```
gdb program
```

You can also start with both an executable program and a core file specified:

```
gdb program core
```

### Attach `gdb` to a running process

You can specify a process ID as a second argument to `gdb` or use option `-p`, if you want to debug a running process. The following examples would attach `gdb` to process `1234`:

```
gdb program 1234
gdb -p 1234
```

With option `-p` you can omit the program filename.

Taking advantage of the second command-line argument requires a fairly complete operating system; when you use `gdb` as a remote debugger attached to a bare board, there may not be any notion of "process", and there is often no way to get a core dump. `gdb` will warn you if it is unable to attach or to read core dumps.
