# Notes on C/C++

These are some notes/useful snippets in C and C++. Unless otherwise specifed, it is assumed that the file in question is saved as `.temp.c`, and compiled and run with the command `gcc ./.temp.c -o ./.temp && ./.temp`

## Contents

- [Notes on C/C++](#notes-on-cc)
  - [Contents](#contents)
  - [Read and print command line arguments](#read-and-print-command-line-arguments)
  - [Write to a file](#write-to-a-file)
  - [Convert an int or float to a C-string in C++](#convert-an-int-or-float-to-a-c-string-in-c)

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

`std::to_string` can be used to convert an `int` or a `float` to a `string`, and the `string.c_str` method can be used to convert a `string` to `char*` (IE a C-string):

```C++
/* Compile and run:
g++ ./.temp.cpp -o ./.temp && ./.temp
*/
#include "stdio.h"
#include <string>

int main() {
    float a  = 3.7;
    int b = 4;
    printf(
        "a = %s, b = %s\n",
        std::to_string(a).c_str(),
        std::to_string(b).c_str()
    );

    return 0;
}
```

```
$ g++ ./.temp.cpp -o ./.temp && ./.temp
a = 3.700000, b = 4
```
