# Notes on Matlab

## Contents

- [Notes on Matlab](#notes-on-matlab)
  - [Contents](#contents)
  - [Get the directory name of a source file](#get-the-directory-name-of-a-source-file)
  - [Create a directory if it doesn't exist](#create-a-directory-if-it-doesnt-exist)
  - [Read from and write to a file](#read-from-and-write-to-a-file)
  - [Print a struct to a file](#print-a-struct-to-a-file)

## Get the directory name of a source file

```matlab
current_filename = mfilename('fullpath');
[current_dir, ~, ~] = fileparts(current_filename);
```

## Create a directory if it doesn't exist

```matlab
dir_name = 'new_folder';

if ~exist(dir_name, 'dir')
    mkdir(dir_name)
end
```

## Read from and write to a file

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

## Print a struct to a file

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
