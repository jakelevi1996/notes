# Tutorial for `gdb` (GNU debugger)

## Contents

- [Tutorial for `gdb` (GNU debugger)](#tutorial-for-gdb-gnu-debugger)
  - [Contents](#contents)
  - [References](#references)
  - [Compiling and opening a program in `gdb`](#compiling-and-opening-a-program-in-gdb)
  - [Useful `gdb` commands](#useful-gdb-commands)
  - [Examples](#examples)
    - [Scripting `gdb` from the command line](#scripting-gdb-from-the-command-line)
    - [Using `backtrace`/`bt`](#using-backtracebt)
    - [Using `dump` (and loading a binary file from Python)](#using-dump-and-loading-a-binary-file-from-python)
    - [Open `gdb` with a core file](#open-gdb-with-a-core-file)
    - [Attach `gdb` to a running process](#attach-gdb-to-a-running-process)
    - [Printing `struct` types](#printing-struct-types)
    - [Performing a list of commands when a breakpoint is reached using `commands`](#performing-a-list-of-commands-when-a-breakpoint-is-reached-using-commands)
    - [Extract data from a program during a loop](#extract-data-from-a-program-during-a-loop)
    - [Export data from `gdb` in YAML format](#export-data-from-gdb-in-yaml-format)

## References

-   [University of Toronto CS: GDB Tutorial](http://www.cs.toronto.edu/~krueger/csc209h/tut/gdb_tutorial.html)
-   [University of Maryland CS: GDB Tutorial](https://www.cs.umd.edu/~srhuang/teaching/cmsc212/gdb-tutorial-handout.pdf)
-   [Tutorials point: GNU debugger tutorial](https://www.tutorialspoint.com/gnu_debugger/gnu_debugger_tutorial.pdf)
-   [sourceware.org](https://sourceware.org/):
    -   [Examining Memory](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html)
    -   [Copy Between Memory and a File](https://sourceware.org/gdb/current/onlinedocs/gdb/Dump_002fRestore-Files.html)
    -   [Breakpoint Command Lists](https://sourceware.org/gdb/current/onlinedocs/gdb/Break-Commands.html)
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
`finish` | | Run until the current function is finished and has returned
`until` | `u` | This is like `n`, except that if we are in a loop, `u` will continue execution until the loop is exited
| | | [No command] Repeat the previous command (useful if repeating the same command repeatedly, EG stepping through a loop)
`list` | | Print the current line, and a few lines above and below
`backtrace` | `bt` | List all the function calls in the stack frame at the current location
`frame N` | `f N` | Examine stack frame `N`, which gives access to the local variables in that stack frame. Frame zero is the innermost (currently executing) frame, frame one is the frame that called the innermost one, and so on. The highest level frame is usually the one for the `main` function. The frame numbers correspond to the numbers printed by the `backtrace` function.
`up N` | | Move `N` frames up the stack. `N` defaults to 1.
`down N` | | Move `N` frames down the stack. `N` defaults to 1.
`print x` | `p x` | Print the value of the variable `x`. If it is an array, the whole array is printed. The `->`, `*` and `.` operators can be used in case `x` is a struct/pointer/pointer to a struct, or even print the entire contents of the struct (see section [Printing `struct` types](#printing-struct-types) below for an example of printing out struct types)
`print/x x` | `p/x x` | Print the value of the variable `x` in hexadecimal
`print x[0]@4` | `p x[0]@4` | Print the first 4 values in the array pointed to by `x`. This is equivalent to the `gdb` command `print *x@4`. For more information, see [10.4 Artificial Arrays on sourceware.org](https://sourceware.org/gdb/current/onlinedocs/gdb/Arrays.html)
`printf` | | Print formatted text to the console window. The first argument should be a format string (using the same syntax as the format string in the [C `printf` function](https://www.cplusplus.com/reference/cstdio/printf/)), and subsequent arguments should be expressions, which can include [convenience variables](https://sourceware.org/gdb/onlinedocs/gdb/Convenience-Vars.html). The arguments to this function should be separated by commas, EG `printf "$x + 10 = %i\n", $x + 10` (assuming `$x` is an integer)
`eval` | | Send a command to `gdb`, using `printf` syntax to format the command. This is useful if the command depends on convenience variables, EG `eval "dump memory %s &multiples[0] &multiples[10]", $filename`. It can also be used to set convenience variables that depend on other convenience variables, EG `eval "set $filename = \"data/data_%i.bin\"", $i`
`set` | | Set a [convenience variable](https://sourceware.org/gdb/onlinedocs/gdb/Convenience-Vars.html). The name of the convenience variable should always start with `$`, including when it is set and every time it is used, EG `set $x = 5`, `printf "$x + 10 = %i\n", $x + 10`
`set var` | | Set the value of a variable in the program being debugged, EG `set var width=47`. Equivalent to `print width=47`, except that the return value is not printed ([source](https://sourceware.org/gdb/current/onlinedocs/gdb/Assignment.html))
`define` | | Create a user-defined command, which is essentially a user-defined function containing `gdb` commands. A user-defined command can contain any number (or even a variable number) of arguments. See [User-defined Commands](https://sourceware.org/gdb/current/onlinedocs/gdb/Define.html) for more information and examples
`ptype x` | | Print a detailed description of the type `x` (EG a `typdef struct`), or the type of a variable `x`, or the type of an expression `x`. Contrary to `whatis`, `ptype` always unrolls any typedefs in its argument declaration, whether the argument is a variable, expression, or a data type
`ptype /o x` | | If `x` is a struct, then print the sizes and offsets (in bytes) of each element in the struct
`whatis x` | | Print the data type of `x`, which can be either an expression or a name of a data type. With no argument, print the data type of `$`, the last value in the value history. If `x` is a variable or an expression, `whatis` prints its literal type as it is used in the source code. If `x` is a type name that was defined using `typedef`, whatis unrolls only one level of that `typedef`.
`x addr` | | Print value at memory location `addr`
`x/nfu addr` | | Examine memory in the specified format (see [sourceware.org: "Examining Memory"](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html))
`watch x` | | Place a watchpoint on variable `x`, meaning that the program will pause whenever the value of `x` is modified, and the old and new values of `x` will be printed (if `x` is an array, then the program will pause and print out the old and new values of the whole array whenever any element of `x` is modified)
`condition N COND` | | Specify breakpoint number `N` to break only if `COND` is true (this can also be achieved using `break` in a single command using the syntax `break file.c:N if COND`)
`commands N` | | Specify a list of commands to run when breakpoint `N` is reached. If `N` is omitted, then `commands` refers to the last breakpoint, watchpoint, or catchpoint set (not to the breakpoint most recently encountered). The commands themselves appear on the following lines. Type a line containing just `end` to terminate the commands. You can use breakpoint commands to start your program up again, EG by using the `continue` command, or `step`, or any other command that resumes execution. See [Breakpoint Command Lists](https://sourceware.org/gdb/current/onlinedocs/gdb/Break-Commands.html) for more.
`info breakpoints` | `info b` | Display information about all declared breakpoints
`info variables` | | List all global and static variable names
`info locals` | | List local variables of current stack frame (names and values), including static variables in that function.
`info args` | | List arguments of the current stack frame (names and values)
`info symbol addr` | | Print the name of a symbol which is stored at the address `addr`. If no symbol is stored exactly at `addr`, GDB prints the nearest symbol and an offset from it
`delete breakpoints` | `delete` | Delete all breakpoints that have been set
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
$ gdb temp --command=gdb_script.cmd -batch
```

To run in batch mode and also prevent all output from `gdb` to `stdout`, use the `-batch-silent` command line argument:

```
$ gdb temp --command=gdb_script.cmd -batch-silent
```

See [sourceware.org](https://sourceware.org/) for more information on [invoking GDB](https://sourceware.org/gdb/current/onlinedocs/gdb/Invoking-GDB.html#Invoking-GDB), [file options](https://sourceware.org/gdb/current/onlinedocs/gdb/File-Options.html#File-Options), and [mode options](https://sourceware.org/gdb/current/onlinedocs/gdb/Mode-Options.html#Mode-Options).

`gdb` command files can include comments (which are not executed) by starting a line with `#`.

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

### Printing `struct` types

`struct` type variables can be nicely printed by `gdb`. Consider the following C program:

```c
#include <stdio.h>

typedef struct {
    int x;
    int y;
    char* name;
    float price;
} C;

C init_c(int x, int y, char* name, float price) {
    C c = {
        .x = x,
        .y = y,
        .name = name,
        .price = price
    };
    return c;
}

int main() {
    C c = init_c(3, 4, "c struct", 3.99);
    C d = init_c(5, 6, "d struct", 4.99);
    C e = init_c(7, 8, "e struct", 5.99);
    printf("3 structs have been created\n");
}
```

The following `gdb` script can be used to run to the final `printf` statement, and then nicely print out the fields of the `struct` variables:

```
break main
break init_c
run
continue
continue
continue
finish
print c
print d
print e
```

The following commands can be used to compile the program, open it in the debugger, and execute the debugging script, producing the following output:

```
$ gcc .temp.c -o temp -g
$ gdb temp --command=gdb_script.cmd -batch
Breakpoint 1 at 0x11c3: file .temp.c, line 37.
Breakpoint 2 at 0x1169: file .temp.c, line 27.

Breakpoint 1, main () at .temp.c:37
37      int main() {

Breakpoint 2, init_c (x=0, y=0, name=0x0, price=0) at .temp.c:27
27      C init_c(int x, int y, char* name, float price) {

Breakpoint 2, init_c (x=3, y=4, name=0x555555556004 "c struct", price=3.99000001) at .temp.c:27
27      C init_c(int x, int y, char* name, float price) {

Breakpoint 2, init_c (x=5, y=6, name=0x55555555600d "d struct", price=4.98999977) at .temp.c:27
27      C init_c(int x, int y, char* name, float price) {
main () at .temp.c:48
48          printf("3 structs have been created\n");
Value returned is $1 = {x = 7, y = 8, name = 0x555555556016 "e struct", price = 5.98999977}
$2 = {x = 3, y = 4, name = 0x555555556004 "c struct", price = 3.99000001}
$3 = {x = 5, y = 6, name = 0x55555555600d "d struct", price = 4.98999977}
$4 = {x = 7, y = 8, name = 0x555555556016 "e struct", price = 5.98999977}
```

It is also possible to use `ptype` to print the generic fields of a `struct` type:

```
(gdb) ptype C
type = struct {
    int x;
    int y;
    char *name;
    float price;
}
```

Using the `/o` option for `ptype` will also print the sizes and offsets in bytes for each field in the struct:

```
(gdb) ptype /o C
type = struct {
/*    0      |     4 */    int x;
/*    4      |     4 */    int y;
/*    8      |     8 */    char *name;
/*   16      |     4 */    float price;
/* XXX  4-byte padding  */

                           /* total size (bytes):   24 */
                         }
```

### Performing a list of commands when a breakpoint is reached using `commands`

A list of commands can be run automatically when a breakpoint is reached using the `gdb` command `commands`. Consider the following C program, `temp.c`:

```c
#include "stdio.h"

void f(int x) {
    printf("The value of x is %i\n", x);
}

void main() {
    int x, y, i;

    for (i = 0; i < 10; i++) {
        x = i * i;
        y = x + 3;
        f(x);
    }
}
```

Say for example it is desirable to print the value of `y` each time `f` is called using `gdb`, without stopping at each breakpoint and manually continuing. This can be achieved using the following `gdb` commands, saved in a file called `gdb_commands.txt`:

```
break f

commands
up
printf "y = %i\n", y
continue
end

run
```

The following terminal commands can be used to compile `temp.c` with debugging symbols, and run the `gdb` commands in `gdb_commands.txt`:

```
$ gcc -g .temp.c -o temp
$ gdb ./temp --command=gdb_commands.txt -batch
```

It is possible to avoid printing some of the statements that are printed by `gdb` when the breakpoint is reached and when changing stack frames. As described in [Breakpoint Command Lists](https://sourceware.org/gdb/current/onlinedocs/gdb/Break-Commands.html) on [sourceware.org](https://sourceware.org/), if the first command you specify in a command list is `silent`, the usual message about stopping at a breakpoint is not printed. This may be desirable for breakpoints for which the intention is to print a specific message and then continue. Also, `up-silently` can be used instead of `up` to move up one stack frame without printing information about the stack frame. With these modifications, the new `gdb_commands.txt` looks like this:

```
break f

commands
silent
up-silent
printf "y = %i\n", y
continue
end

run
```

Note that, if there were any other `gdb` commands in `gdb_commands.txt` after `continue` and before `end`, then they would not be executed. More generally, as desribed in [Breakpoint Command Lists](https://sourceware.org/gdb/current/onlinedocs/gdb/Break-Commands.html) on [sourceware.org](https://sourceware.org/):

> Any other commands in the command list, after a command that resumes execution, are ignored. This is because any time you resume execution (even with a simple next or step), you may encounter another breakpoint - which could have its own command list, leading to ambiguities about which list to execute.

### Extract data from a program during a loop

Consider the following C program, `temp.c`:

```C
#include <stdint.h>
#include <stdio.h>

#define N_MULTIPLES (10)

int16_t multiples[N_MULTIPLES];

void f(int x) {
    for (int i = 0; i < N_MULTIPLES; i++) {
        multiples[i] = (int16_t) x * (i + 1);
    }
}

int main() {
    printf("Times tables up to 100:");
    for (int i = 1; i <= 100; i++) {
        printf("\n%3i: ", i);
        f(i);
        for (int j = 0; j < N_MULTIPLES; j++) {
            printf("%3i, ", multiples[j]);
        }

    }

    return 0;
}
```

Say it is desirable to run this until the `f` function has been called 20 or so times, then extract the `multiples` buffer the next 10 times that `f` is called into separate binary data files, and then quit. This can be achieved with the following `gdb` script, `gdb.txt`:

```
break f
run
continue 20

set $i = 0

while $i < 10
    eval "set $filename = \"data/data_%i.bin\"", $i
    printf "filename = %s\n", $filename
    finish
    eval "dump memory %s &multiples[0] &multiples[10]", $filename
    set $i = $i + 1
    continue
end
```

Use the following commands to compile and run the program and debugger script (note that the `mkdir data` command is used because if the `data` directory doesn't exist when the `eval "dump memory %s &multiples[0] &multiples[10]", $filename` command is used, then `gdb` will crash and exit, because it does not automatically create directories that don't exist when calling the `dump` command):

```
gcc temp.c -o temp.exe -g
mkdir data
gdb temp.exe --command=gdb.txt -batch
```

Below is an example Python script to read and print the contents of each of these files:

```python
import os
import struct

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

for i in range(10):
    data_path = os.path.join(CURRENT_DIR, "data", "data_%i.bin" % i)
    with open(data_path, "rb") as f:
        b = f.read()

    sizeof_int16_t = 2
    num_elements = len(b) / sizeof_int16_t
    struct_fmt_str = "%ih" % num_elements
    x = struct.unpack(struct_fmt_str, b)
    print("i = %i, x = %s" % (i, x))
```

### Export data from `gdb` in YAML format

If a lot of structured data is to be exported from a C program, then exporting the data from `gdb` in YAML format can make it easier to process the data within a Python script. Below is an example of a `gdb` script that exports data in a YAML format (with the exception of the `@@@` strings, which are explained afterwards):

```
break func_1
commands
silent
up-silently
printf "@@@- \n"
continue
end

break func_2
commands
silent
up-silently
printf "  - a: %d\n", a
printf "    b: %d\n", b
up-silently
printf "    c: %d@@@\n", c
continue
end

run
```

To install yaml for Python, use the following command-line commands (replace `python` with `python3` on Linux):

```
python -m pip install -U pip
python -m pip install pyyaml
```

A useful trick for figuring out the correct YAML format is to define some example data in the desired Python formats (EG lists and dictionaries), convert the data to YAML format, and then print it out, and replicate that format in the `gdb` script. Below is an example of 2 different Python formats (run the commands to see the YAML formt):

```python
import yaml

results = {
    "Group 0": {"subgroup 0": {"a": 1, "b": 2}, "subgroup 1": {"a": 3, "b": 4}},
    "Group 1": {"subgroup 0": {"a": 5, "b": 6}, "subgroup 1": {"a": 7, "b": 8}},
}
print(yaml.dump(results))

results = [
    [{"a": 1, "b": 2}, {"a": 3, "b": 4}],
    [{"a": 5, "b": 6}, {"a": 7, "b": 8}],
]
print(yaml.dump(results))
print(results)
print(yaml.safe_load(yaml.dump(results)))
print(yaml.safe_load(yaml.dump(results)) == results)
```

A marker such as `@@@` can be used to separate the generic `gdb` output to `stdout` from the desired YAML output, and the marker can be processed and removed from the output in Python using the following function (`s` is the `gdb` output as a string, `marker` is the marker as a string, EG `"@@@"`):

```python
def trim_str_marker(s, marker):
    substr_start_ind = s.index(marker)
    substr_end_ind = s.rindex(marker)
    substr = s[substr_start_ind:substr_end_ind]
    substr_clean = substr.replace(marker, "")
    return substr_clean
```

Additionally, the following function and commands can be used to call the `gdb` script and parse the output into the desired format in Python:

```python
import subprocess
import yaml

def call_cmd(arg_list, print_cmd=True, print_stdout=True):
    if print_cmd:
        print("> %s" % " ".join(arg_list))

    completed_process = subprocess.run(
        arg_list,
        check=True,
        stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
    )
    cmd_stdout = completed_process.stdout.decode()

    if print_stdout:
        print(cmd_stdout)

    return cmd_stdout

gdb_cmd_list = [
    "gdb",
    exe_path,
    "--command",
    gdb_script_path,
    "-batch",
]
gdb_output = call_cmd(gdb_cmd_list, print_stdout=False)
gdb_output_clean = trim_str_marker(gdb_output, "@@@")
test_info_list = yaml.safe_load(gdb_output_clean)
```
