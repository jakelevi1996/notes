# Notes on C/C++

These are some notes/useful snippets in C and C++. Unless otherwise specifed, it is assumed that the file in question is saved as `.temp.c`, and compiled and run with the command `gcc ./.temp.c -o ./.temp && ./.temp`

## Contents

- [Notes on C/C++](#notes-on-cc)
  - [Contents](#contents)
  - [Read and print command line arguments](#read-and-print-command-line-arguments)
  - [Write to a file](#write-to-a-file)
  - [Convert an int or float to a C-string in C++](#convert-an-int-or-float-to-a-c-string-in-c)
  - [C error function](#c-error-function)

## Read and print command line arguments

```C
/* Compile and run:
gcc ./.temp.c -o ./.temp && ./.temp && ./.temp 1 2 3 4 && ./.temp Hello, world!
*/
#include <stdio.h>

int main(int argc, char** argv) {
    printf("Number of command line arguments = %i\n", argc);
    printf("Values of command line arguments = [");
    for (int i = 0; i < argc; i++) {
        printf("\"%s\", ", argv[i]);
    }
    printf("]\n\n");
}
```

```
$ gcc ./.temp.c -o ./.temp && ./.temp && ./.temp 1 2 3 4 && ./.temp Hello, world!
Number of command line arguments = 1
Values of command line arguments = ["./.temp", ]

Number of command line arguments = 5
Values of command line arguments = ["./.temp", "1", "2", "3", "4", ]

Number of command line arguments = 3
Values of command line arguments = ["./.temp", "Hello,", "world!", ]
```

## Write to a file

```C
/* Compile and run:
gcc ./.temp.c -o ./.temp && ./.temp
*/
#include <stdio.h>

int main() {
    /* Open the file and check that it's valid */
    char* filename = ".temp_out.txt";
    FILE* fout = fopen(filename, "w");
    if (fout == NULL) {
        fprintf(stderr, "Error: couldn't open file\n");
        return 2;
    }

    /* Write to the file */
    fprintf(fout, "Hello world");

    /* Close and exit */
    fclose(fout);
    return 0;
}

```

## Convert an int or float to a C-string in C++

`std::to_string` can be used to convert an `int` or a `float` to a `string`, and the `string.c_str` method can be used to convert a `string` to `char*` (IE a C-string). This can be useful, EG if printing the value of a numeric type within a template function:

```C++
/* Compile and run:
g++ ./.temp.cpp -o ./.temp && ./.temp
*/
#include "stdio.h"
#include <string>

template <typename T>
void f(const char* name, T x) {
    printf("\"%s\" = %s\n", name, std::to_string(x).c_str());
}

int main() {
    float a  = 3.7;
    int b = 4;
    f("a", a);
    f("b", b);

    return 0;
}
```

```
$ g++ ./.temp.cpp -o ./.temp && ./.temp
"a" = 3.700000
"b" = 4
```

## C error function

When a C library function fails, it usually sets a variable called `errno` (which can be accessed by including the header file `<errno.h>`) to a value which corresponds to the way in which failure occured. A string which describes the failure can be printed by passing `errno` to the `strerror` function (found in the `<string.h>` header file). Often, when such a failure occurs, it is desirable to exit the program using a call to `exit` (found in `<stdlib.h>`). Finally, rather than repeating these lines of code everywhere in a C program where an error can occur, it is sensible to define an `error` function, which performs all of these instructions; an example of a program which includes such a function is shown below:

```C
/* Compile and run:
gcc ./.temp.c -o ./.temp && ./.temp
*/

#include <stdio.h>      /* FILE, fopen, printf */
#include <string.h>     /* strerror */
#include <stdlib.h>     /* exit, EXIT_FAILURE */
#include <errno.h>      /* errno */

void error(char* error_msg) {
    fprintf(stderr, "ERROR: %s: %s\n", error_msg, strerror(errno));
    exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
    FILE* bad_file = fopen("This file doesn't exist.txt", "r");
    if (bad_file == NULL) {
        error("Could not open file");
    }
    else {
        printf("File opened successfully\n");
    }

    return 0;
}
```

```
$ gcc ./.temp.c -o ./.temp && ./.temp
ERROR: Could not open file: No such file or directory
```
