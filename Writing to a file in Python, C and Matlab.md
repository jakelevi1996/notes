# Writing to a file in Python, C and Matlab

## Writing and reading to/from a text file in Python

### Single integer

Below is a very simple code snippet to write an integer to a text file in Python, then read it out again, and check that the values are consistent:

```python
x = 12345

with open("temp.txt", "w") as f:
    print(x, file=f)

with open("temp.txt", "r") as f:
    y = int(f.read())

print(x, y, x == y)
```

Console output:

```
12345 12345 True
```

### List of integers

Below is an equivalent snipped for writing a list of integers to a text file in Python:

```python
x = [1, 2, 3, 4, 5]

with open("temp.txt", "w") as f:
    print(", ".join(map(str, x)), file=f)

with open("temp.txt", "r") as f:
    y = [int(i) for i in f.read().split(", ")]

print(x, y, x == y)
```

Console output:

```
[1, 2, 3, 4, 5] [1, 2, 3, 4, 5] True
```

## Writing to a file in C

The file `writehello.c` below represents a simple program in C for writing "Hello world" to a file, whose filename is specified as a command-line argument. The program includes error checking for the number of arguments, and the validity of the filename.

### `writehello.c`

```C
/* Write "Hello world" to a text file specified as a command-line argument

* Compile and run using:
gcc writehello.c -o writehello && writehello out.txt
*/

#include <stdio.h>

int main(int argc, char *argv[]) {
    // Checl the number of arguments
    if (argc != 2) {
        fprintf(stderr, "Error: You need to give 1 argument\n");
        return 1;
    }
    // Check the filename
    FILE* fout = fopen(argv[1], "w");
    if (fout == NULL) {
        fprintf(stderr, "Error: couldn't open file\n");
        return 2;
    }
    // Write to the file
    fprintf(fout, "Hello world");
    
    // Close and exit
    fclose(fout);
    return 0;
}
```

## Writing to a file in Matlab

Below is a code snippet for writing to a file in Matlab.

```matlab
% Get name of current file, current directory, and output filename
current_filename = mfilename('fullpath');
[current_dir, ~, ~] = fileparts(current_filename);
debug_filename = fullfile(current_dir, 'debug.txt');

% Open file and check for errors
debug_fid = fopen(debug_filename, 'w');
if debug_fid < 0
    error('Could not open file %s', debug_filename);
end

% Print to file and close
fprintf(debug_fid, 'Hello world, the answer is %i\n', 42);
fclose(debug_fid);
```