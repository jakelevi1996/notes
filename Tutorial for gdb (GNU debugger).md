# Tutorial for `gdb` (GNU debugger)

## Contents

- [Tutorial for `gdb` (GNU debugger)](#tutorial-for-gdb-gnu-debugger)
  - [Contents](#contents)
  - [References](#references)
  - [Compiling and opening a program in `gdb`](#compiling-and-opening-a-program-in-gdb)
  - [Useful commands](#useful-commands)
  - [Examples](#examples)

## References

-   [University of Toronto CS: GDB Tutorial](http://www.cs.toronto.edu/~krueger/csc209h/tut/gdb_tutorial.html)
-   [University of Maryland CS: GDB Tutorial](https://www.cs.umd.edu/~srhuang/teaching/cmsc212/gdb-tutorial-handout.pdf)
-   [Tutorials point: GNU debugger tutorial](https://www.tutorialspoint.com/gnu_debugger/gnu_debugger_tutorial.pdf)
-   [sourceware.org: "Examining Memory"](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html)
-   Stack Overflow questions:
    -   [What are the best ways to automate a GDB debugging session?](https://stackoverflow.com/questions/10748501/what-are-the-best-ways-to-automate-a-gdb-debugging-session)
    -   [Gdb dump memory in specific region, save formatted output into a file](https://stackoverflow.com/questions/16095948/gdb-dump-memory-in-specific-region-save-formatted-output-into-a-file)
    -   [Gdb print to file instead of stdout](https://stackoverflow.com/questions/5941158/gdb-print-to-file-instead-of-stdout)

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

## Useful commands

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
`print x` | | Print the value of the variable `x`. If it is an array, the whole array is printed. The `->`, `*` and `.` operators can be used in case `x` is a struct/pointer/pointer to a struct, or even print the entire contents of the struct that a pointer references
`print/x x` | | Print the value of the variable `x` in hexadecimal
`watch x` | | Place a watchpoint on variable `x`, meaning that the program will pause whenever the value of `x` is modified, and the old and new values of `x` will be printed (if `x` is an array, then the program will pause and print out the old and new values of the whole array whenever any element of `x` is modified)
`list` | | Print the current line, and a few lines above and below
`backtrace` | `bt` | List all the function calls in the stack frame at the current location
`x addr` | | Print value at memory location `addr`
`x/nfu addr` | | Examine memory in the specified format (see [sourceware.org: "Examining Memory"](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html))
`delete` | | Delete all breakpoints that have been set
`delete n` | | Delete breakpoint number `n`
`clear function_name` | | Deletes the breakpoint set in that function
`condition N COND` | | Specify breakpoint number `N` to break only if `COND` is true (this can also be achieved using `break` in a single command using the syntax `break file.c:N if COND`)
`info breakpoints` | | Display information about all declared breakpoints

## Examples

Using `backtrace`/`bt`:

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
