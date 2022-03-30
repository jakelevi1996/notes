# Writing to a file in Python and Matlab

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

## Writing to a file in Matlab

### Strings and text

Below is a code snippet for writing strings and text to a file in Matlab.

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

A convenient function for reading a text file is [`fileread`](https://uk.mathworks.com/help/matlab/ref/fileread.html), which accepts a string containing the filename (as opposed to a file ID, so there is no need to call `fopen` and check the error code), and reads the entire text file (possibly containing multiple lines) into a single string, which is returned by the function.

### Printing a struct to a file

A struct can be printed to a file using the [`evalc` function](https://uk.mathworks.com/help/matlab/ref/evalc.html), EG:

```matlab
a = [1 2 3; 4 5 6];
fprintf(fopen('temp.txt', 'w'), '%s\n', evalc('disp(whos(''a''))'));
```

Contents of `temp.txt`:

```
          name: 'a'
          size: [2 3]
         bytes: 48
         class: 'double'
        global: 0
        sparse: 0
       complex: 0
       nesting: [1×1 struct]
    persistent: 0


```
