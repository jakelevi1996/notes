# Notes on Python

This is a collection of notes on Python, including useful links, useful snippets, Python implementations of algorithms, and notes on built-in and third-party modules.

TODO: migrate existing Python-related Gists into subsections of this Gist

## Contents

- [Notes on Python](#notes-on-python)
  - [Contents](#contents)
  - [Useful links](#useful-links)
  - [Profiling Python code](#profiling-python-code)
  - [Useful Python snippets](#useful-python-snippets)
    - [Print the running time of a Python script](#print-the-running-time-of-a-python-script)
    - [Get a timestamped filename](#get-a-timestamped-filename)
    - [Get the directory name of the current source file](#get-the-directory-name-of-the-current-source-file)
    - [Create a directory if it doesn't exist](#create-a-directory-if-it-doesnt-exist)
    - [Clean up a filename string](#clean-up-a-filename-string)
    - [Writing to and reading from a text file in Python](#writing-to-and-reading-from-a-text-file-in-python)
    - [Custom context managers using `__enter__` and `__exit__`](#custom-context-managers-using-__enter__-and-__exit__)
    - [Recursively search a directory for all files of a certain type](#recursively-search-a-directory-for-all-files-of-a-certain-type)
    - [Extract a substring from a file](#extract-a-substring-from-a-file)
    - [Start a parallel subprocess in a new console window](#start-a-parallel-subprocess-in-a-new-console-window)
    - [Run a command using `subprocess` and parse its output to STDOUT](#run-a-command-using-subprocess-and-parse-its-output-to-stdout)
    - [Call a function with a timeout using `multiprocessing`](#call-a-function-with-a-timeout-using-multiprocessing)
    - [Set `numpy` print options (including preventing `numpy` from wrapping lines)](#set-numpy-print-options-including-preventing-numpy-from-wrapping-lines)
    - [Rename files programmatically using `os.path.walk` and `os.rename`](#rename-files-programmatically-using-ospathwalk-and-osrename)
  - [Python implementations of algorithms](#python-implementations-of-algorithms)
    - [Find all permutations of a string](#find-all-permutations-of-a-string)
    - [Burrows–Wheeler transform (BWT)](#burrowswheeler-transform-bwt)
  - [Notes on built-in and third-party modules](#notes-on-built-in-and-third-party-modules)
    - [`pip`](#pip)
    - [`argparse`](#argparse)
    - [`pickle`](#pickle)
    - [`socket`](#socket)

## Useful links

- [Python homepage](https://www.python.org/)
- [Download Python](https://www.python.org/downloads/)
- [Documentation](https://docs.python.org/3/)
  - [The Python Tutorial](https://docs.python.org/3/tutorial/index.html)
  - [The Python Standard Library](https://docs.python.org/3/library/index.html) (including all built-in modules)
    - [Built-in Functions](https://docs.python.org/3/library/functions.html)
    - [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
  - [The Python Language Reference](https://docs.python.org/3/reference/index.html)
    - [Data model](https://docs.python.org/3/reference/datamodel.html)
- [Project Euler](https://projecteuler.net/archives) (useful and interesting problems for practising numerical programming, and well-suited to Python)

## Profiling Python code

Profiling a Python script involves 2 stages: collecting profiling information while running the script using the `cProfile` Python module, and then analysing the profiling information using the `pstats` Python module.

Suppose the following script called `maths_test.py` is to be profiled:

```python
import math
import statistics

def f(x):
    return statistics.stdev(g(i) for i in range(x))

def g(x):
    return sum(math.sqrt(i) for i in range(x))

if __name__ == "__main__":
    f(1000)
```

This can be achieved simply using the following two commands:

```
python -m cProfile -o .profile_output.bin ./maths_test.py
python -c "import pstats; p = pstats.Stats('.profile_output.bin'); p.sort_stats('cumtime'); p.print_stats(15)"
```

These commands produce the following output:

```
Tue Sep  6 12:12:24 2022    .profile_output.bin

         1019414 function calls (1019273 primitive calls) in 0.166 seconds

   Ordered by: cumulative time
   List reduced from 240 to 15 due to restriction <15>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      8/1    0.000    0.000    0.166    0.166 {built-in method builtins.exec}
        1    0.000    0.000    0.166    0.166 ./maths_test.py:1(<module>)
        1    0.000    0.000    0.157    0.157 ./maths_test.py:4(f)
        1    0.000    0.000    0.157    0.157 C:\Program Files\Python37\lib\statistics.py:640(stdev)
        1    0.000    0.000    0.157    0.157 C:\Program Files\Python37\lib\statistics.py:545(variance)
     1001    0.000    0.000    0.152    0.000 ./maths_test.py:5(<genexpr>)
     1000    0.001    0.000    0.152    0.000 ./maths_test.py:7(g)
     1003    0.033    0.000    0.152    0.000 {built-in method builtins.sum}
   500500    0.072    0.000    0.118    0.000 ./maths_test.py:8(<genexpr>)
   499501    0.046    0.000    0.046    0.000 {built-in method math.sqrt}
      9/2    0.000    0.000    0.009    0.004 <frozen importlib._bootstrap>:978(_find_and_load)
      9/2    0.000    0.000    0.009    0.004 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/2    0.000    0.000    0.008    0.004 <frozen importlib._bootstrap>:663(_load_unlocked)
      6/1    0.000    0.000    0.008    0.008 <frozen importlib._bootstrap_external>:722(exec_module)
     12/3    0.000    0.000    0.008    0.003 <frozen importlib._bootstrap>:211(_call_with_frames_removed)
```

The arguments to [`print_stats`](https://docs.python.org/3/library/profile.html#pstats.Stats.print_stats) specifiy restrictions on which lines to print, and the order in which to apply those restrictions. An integer argument `n` prints only the first `n` lines. A string argument `s` only prints lines whose filename (including directory name) matches the regular expression `s`.

For example, to only print the first 10 lines of functions in the current directory (which is called `Notes on Python`), we can call the script using its full path (including the name of the parent directory), regenerate the profiling information, and then pass the arguments `'Notes on Python', 10` to the `print_stats` method, as shown below (note that instead of using the full path we could have just matched the pattern `maths_test` in this case, but the former approach is more robust in cases where the script being profiled calls other modules in the current directory, which are also intended to be profiled):

```
python -m cProfile -o .profile_output.bin "C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py"
python -c "import pstats; p = pstats.Stats('.profile_output.bin'); p.sort_stats('cumtime'); p.print_stats('Notes on Python', 10)"
```

This produces the following output (only 5 lines are printed because there are only 5 entries which match the pattern `'Notes on Python'`):

```
Tue Sep  6 12:12:48 2022    .profile_output.bin

         1019414 function calls (1019273 primitive calls) in 0.158 seconds

   Ordered by: cumulative time
   List reduced from 240 to 5 due to restriction <'Notes on Python'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.158    0.158 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:1(<module>)
        1    0.000    0.000    0.149    0.149 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:4(f)
     1001    0.000    0.000    0.144    0.000 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:5(<genexpr>)
     1000    0.001    0.000    0.144    0.000 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:7(g)
   500500    0.067    0.000    0.112    0.000 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:8(<genexpr>)
```

From this we see that the generator expressions are taking up quite a lot of time; replacing `g(i) for i in range(x)` with `map(g, range(x))` and `math.sqrt(i) for i in range(x)` with `map(math.sqrt, range(x))` and re-profiling, the following profiling results are obtained, reducing the overall running time by >50%:

```
Tue Sep  6 12:13:24 2022    .profile_output.bin

         18413 function calls (18272 primitive calls) in 0.050 seconds

   Ordered by: cumulative time
   List reduced from 238 to 3 due to restriction <'Notes on Python'>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.050    0.050 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:1(<module>)
        1    0.000    0.000    0.041    0.041 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:4(f)
     1000    0.001    0.000    0.036    0.000 C:/Users/Jake/Documents/Programming/Gists/Notes on Python/maths_test.py:7(g)
```

To avoid printing directory names in the function listings, call the `strip_dirs` method of the `pstats.Stats` object before calling the `print_stats` method, as shown below (but note that this will prevent matching by directory names in the `print_stats` method):

```
python -c "import pstats; p = pstats.Stats('.profile_output.bin'); p.strip_dirs(); p.sort_stats('cumtime'); p.print_stats(10)"
```

This produces the following output:

```
Tue Sep  6 12:13:24 2022    .profile_output.bin

         18413 function calls (18272 primitive calls) in 0.050 seconds

   Ordered by: cumulative time
   List reduced from 238 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      8/1    0.000    0.000    0.050    0.050 {built-in method builtins.exec}
        1    0.000    0.000    0.050    0.050 maths_test.py:1(<module>)
        1    0.000    0.000    0.041    0.041 maths_test.py:4(f)
        1    0.000    0.000    0.041    0.041 statistics.py:640(stdev)
        1    0.000    0.000    0.041    0.041 statistics.py:545(variance)
     1000    0.001    0.000    0.036    0.000 maths_test.py:7(g)
     1003    0.036    0.000    0.036    0.000 {built-in method builtins.sum}
      9/2    0.000    0.000    0.010    0.005 <frozen importlib._bootstrap>:978(_find_and_load)
      9/2    0.000    0.000    0.009    0.005 <frozen importlib._bootstrap>:948(_find_and_load_unlocked)
      9/2    0.000    0.000    0.009    0.005 <frozen importlib._bootstrap>:663(_load_unlocked)
```

When calling the script being profiled using `cProfile`, it is possible to call the script with command line arguments by appending them to the end of the command as usual, for example:

```
python -m cProfile -o .profile_output.bin ./maths_test.py --arg1 val1 --arg2 val2
```

When calling the script being profiled using `cProfile`, instead of calling the script using its path, it is also possible to call the script using `-m` and module syntax (and including any command line arguments, if desired), for example:

```
python -m cProfile -o .profile_output.bin -m maths_test
```

This can also be used to profile unit tests using `pytest`, for example:

```
python -m cProfile -o .profile_output.bin -m pytest
```

Note that `pytest` can be followed by the `-k` flag to select which tests to run based on their name, [as described here](https://docs.pytest.org/en/7.1.x/example/markers.html#using-k-expr-to-select-tests-based-on-their-name).

Often when profiling, it might be desirable to change the code, re-profile, and compare against the original profiling information. To this end it can be useful to generate unique timestamped filenames on the command line into which `stdout` can be redirected, for example by appending ` > ".profile $(date '+%Y-%m-%d %H-%M-%S').txt"` to the end of the `pstats` command, as shown below:

```
python -c "import pstats; p = pstats.Stats('.profile_output.bin'); p.sort_stats('cumtime'); p.print_stats()" > ".profile $(date '+%Y-%m-%d %H-%M-%S').txt"
```

Note that errors can occur when trying to profile code which uses the `pickle` module. The explanation and a workaround are provided in [this StackOverflow answer](https://stackoverflow.com/a/53890887/8477566). A simple solution is the modify the code being profiled such that it has an option to run without using `pickle`.

## Useful Python snippets

### Print the running time of a Python script

The running time of a Python script can be printed using `time.perf_counter()`, as shown below:

```python
import time

def main():
    """ Main function for the script """
    from time import sleep
    sleep(3)

if __name__ == "__main__":
    t_start = time.perf_counter()

    # Call main function
    main()

    # Print time taken
    t_total = time.perf_counter() - t_start
    mins, secs = divmod(t_total, 60)
    print("\n\nScript ran in %i mins, %.1f secs" % (mins, secs))
```

This can be wrapped up in a reusable function as follows:

```python
import time

def main(t_sleep):
    """ Main function for the script """
    from time import sleep
    sleep(t_sleep)

def time_func(func, *args, **kwargs):
    t_start = time.perf_counter()
    func(*args, **kwargs)
    t_total = time.perf_counter() - t_start

    print("\nFinished %r function in %.1fs" % (func.__name__, t_total))

if __name__ == "__main__":
    time_func(main, 3.0)
```

### Get a timestamped filename

```python
import datetime

s = datetime.datetime.now()

print(s)
# >>> 2022-10-10 19:23:18.975783

output_filename = "%s Output.txt" % s
print(output_filename)
# >>> 2022-10-10 19:23:18.975783 Output.txt
```

### Get the directory name of the current source file

```python
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
```

### Create a directory if it doesn't exist

```python
import os

if not os.path.isdir(dir_name):
    os.makedirs(dir_name)
```

### Clean up a filename string

```python
def clean_filename(filename_str, allowed_non_alnum_chars="-_.,"):
    filename_str_clean = "".join(
        c if (c.isalnum() or c in allowed_non_alnum_chars) else "_"
        for c in str(filename_str)
    )
    return filename_str_clean

print(clean_filename("hello/world:!\\.txt"))
# >>> hello_world___.txt
```

### Writing to and reading from a text file in Python

To write to or read from a file in Python, create a file object using the `open` built-in function, and use the objects `write` and `read` methods (or alternatively, `print(s, file=f)`), for example:

```python
x = 12345

with open(".temp.txt", "w") as f:
    f.write(str(x))

with open(".temp.txt", "r") as f:
    y = int(f.read())

print(x, y, x == y)
```

Console output:

```
12345 12345 True
```

To read/write a list of integers from/to a text file in Python:

```python
x = [1, 2, 3, 4, 5]

with open(".temp.txt", "w") as f:
    f.write(", ".join(str(i) for i in x))

with open(".temp.txt", "r") as f:
    y = [int(s) for s in f.read().split(", ")]

print(x, y, x == y)
```

Console output:

```
[1, 2, 3, 4, 5] [1, 2, 3, 4, 5] True
```

### Custom context managers using `__enter__` and `__exit__`

Inside a class definition, defining the methods `__enter__(self)` and `__exit__(self, exc_type, exc_value, traceback)` allows that class to be used as a context manager. Note that if an exception is raised inside the context manager, the `__exit__` method will be executed before the exception is raised (or not raised, in case `__exit__` returns a true value), as described in the documentation for the `__exit__` method in the [Python data model](https://docs.python.org/3/reference/datamodel.html):

> Exit the runtime context related to this object. The parameters describe the exception that caused the context to be exited. If the context was exited without an exception, all three arguments will be None.

> If an exception is supplied, and the method wishes to suppress the exception (i.e., prevent it from being propagated), it should return a true value. Otherwise, the exception will be processed normally upon exit from this method.

This is useful EG if some clean-up code is supposed to be run after calling the `main` function, regardless of whether or not an exception is raised in `main` - the `main` function can be put inside a context manager, and the clean-up code can be put inside the `__exit__` method.

For example, if some experimental data collected from the `main` function should be saved to disk even if an error is raised in `main`, the context manager can be designed so that it stores a reference to the desired data as an attribute before the `main` function is called, and when the context manager exits, it saves that data to disk (EG using [`pickle.dump`](https://docs.python.org/3/library/pickle.html#pickle.dump)).

Here is a simple example of context managers and exceptions:

```python
class C:
    def __enter__(self):
        print("In enter")
        return self

    def __exit__(self, *args):
        print("In exit")

with C() as c:
    print("Inside context manager, c = %s" % c)
    raise RuntimeError()
    print("This statement is not reached")
```

Output:

```
In enter
Inside context manager, c = <__main__.C object at 0x00000221DED41A88>
In exit
Traceback (most recent call last):
  File "~/.temp.py", line 11, in <module>
    raise RuntimeError()
RuntimeError
```

### Recursively search a directory for all files of a certain type

Using `os.path.walk`:

```python
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

wav_files = [
    os.path.join(dir_name, filename)
    for (dir_name, _, f_list) in os.walk(current_dir)
    for filename in f_list
    if filename.endswith(".wav")
]

print(*wav_files, sep="\n", file=open("filenames.txt", "w"))
```

Using `glob`:

```python
import os
import glob

current_dir = os.path.dirname(os.path.abspath(__file__))

wav_files_glob = [
    os.path.abspath(f) for f in glob.glob("**/*.wav", recursive=True)
]

print(*wav_files_glob, sep="\n", file=open("filenames from glob.txt", "w"))
```

### Extract a substring from a file

In Python, given the filename of a text file, read the text file into a string, and extract the substring which begins after the prefix substring and ends before the suffix substring.

```python
def extract_substr_from_file(filename, prefix=None, suffix=None):
    """ Given the filename of a text file, read the text file into a string,
    and extract the substring which begins after the prefix substring and ends
    before the suffix substring. If prefix is None then the start of the file
    is used as the prefix. If suffix is None then the end of the file is used
    as the suffix. """
    with open(filename) as f:
        s = f.read()

    start_ind = 0 if (prefix is None) else (s.index(prefix) + len(prefix))
    end_ind = len(s) if (suffix is None) else (s.index(suffix, start_ind))

    return s[start_ind:end_ind]
```

### Start a parallel subprocess in a new console window

`create_process.py`

```python
import subprocess
import time

print("Starting new process...")

cmd = ["python", "print_slow.py"]
subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

print("This process runs in parallel...")
time.sleep(1)
print("... while the other process is running in a new console...")
time.sleep(1)
print("... and both processes are running at the same time")
```

`print_slow.py`

```python
from time import sleep

print("Console closing in ", end="\n")
for i in reversed(range(5)):
    print("%i..." % (i + 1))
    sleep(1)
```

### Run a command using `subprocess` and parse its output to STDOUT

```python
""" Run a command in the console, and parse its output to STDOUT """

import subprocess

ls_cmd = ["ls", "/dev/serial/by-id/"]
try:
    console_output = subprocess.check_output(ls_cmd).decode()
except subprocess.CalledProcessError:
    raise RuntimeError("Error running command \"%s\"" % (" ".join(ls_cmd)))


serial_device_list = [s for s in console_output.split("\n") if len(s) > 0]

print("List of serial devices:\n\n%s" % serial_device_list)
```

### Call a function with a timeout using `multiprocessing`

`call_func_with_timeout.py`

```python
from multiprocessing import Process, Queue
from time import sleep

def call_func_with_timeout(
    func,
    timeout,
    args=None,
    kwargs=None,
    timeout_retval=None,
):
    """ Call the given function in a subprocess with the given arguments and
    keyword arguments. If the function takes longer than timeout seconds to
    return, then terminate the subprocess, and return timeout_retval. Otherwise
    return the value returned by the function call """
    # Set default args and kwargs values
    if args is None:
        args = list()

    if kwargs is None:
        kwargs = dict()

    # Initialise the Queue and Process objects
    result_queue = Queue()
    p = Process(target=func_wrapper, args=[func, result_queue, args, kwargs])

    # Start the process, wait for timeout seconds, and check the process
    p.start()
    p.join(timeout)
    if p.is_alive():
        # The function hasn't returned, so terminate the subprocess
        p.terminate()
        p.join()
        p.close()
        ret_val = timeout_retval
    else:
        # The process finished, so close the process and retrieve the results
        p.close()
        ret_val = result_queue.get()

    return ret_val

def func_wrapper(func, result_queue, args, kwargs):
    """ Wrapper for the function passed to call_func_with_timeout, which is
    started in a subprocess by call_func_with_timeout. Call the target
    function, and place the result in a queue, which can be retrieved by
    call_func_with_timeout """
    ret_val = func(*args, **kwargs)
    result_queue.put(ret_val)
```

`test.py`

```python
from time import sleep
from call_func_with_timeout import call_func_with_timeout


def f(x):
    for i in range(x):
        print(i)
        sleep(1)

    return 42

if __name__ == "__main__":
    print(call_func_with_timeout(f, timeout=4, args=[2]), end="\n\n")
    print(call_func_with_timeout(f, timeout=4, args=[6]), end="\n\n")
    print(call_func_with_timeout(f, timeout=4, kwargs={"x": 6}), end="\n\n")
```

Output from `test.py`:

```
0
1
42

0
1
2
3
None

0
1
2
3
None
```

### Set `numpy` print options (including preventing `numpy` from wrapping lines)

```python
import numpy as np

np.set_printoptions(
    precision=3,
    linewidth=10000,
    suppress=True,
    threshold=10000,
)

print(np.random.normal(size=[3, 15]))
# >>> [[-0.351 -0.593  1.616  0.333 -1.238 -0.166 -1.251 -0.084 -0.562  2.429  0.715  0.676  1.393 -0.69  -0.992]
#      [-0.674 -0.276  2.243 -2.216 -0.595 -0.246 -1.241 -0.282 -1.07  -0.183 -0.193  0.028 -0.365 -0.602 -0.893]
#      [-0.105 -0.082  0.305 -0.207  0.369  0.655 -1.292 -0.629 -0.275 -0.492 -1.085  0.064  0.037  0.428  0.126]]
```

### Rename files programmatically using `os.path.walk` and `os.rename`

Below is an example of renaming all files in the current directory (including all subdirectories) not in `.git/` which contain a space, replacing spaces with underscores and converting to lowercase. To simply see what would happen without actually renaming any files (IE perform a dry run), simply comment out the line `os.rename(old_name, new_name)`.

```python
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(CURRENT_DIR):
    if ".git" not in root:
        for filename in files:
            if " " in filename:
                old_name = os.path.join(root, filename)
                new_name = os.path.join(
                    root,
                    filename.replace(" ", "_").lower(),
                )
                print("Renaming %120s to %s" % (old_name, new_name))
                os.rename(old_name, new_name)
```

## Python implementations of algorithms

### Find all permutations of a string

Note that this could be made more efficient by storing each 2-tuple (each of which contains the prefix of a valid permutation, and the remaining choices for that permutation) as a single string.

```python
def find_permutations(s):
    """ Find all permutations of the string s. This can be performed using
    itertools.permutations, but implementing it from scratch is an interesting
    challenge. """
    # Initialise list of 2-tuples, each of which contains the prefix of a valid
    # permutation, and the remaining choices for that permutation
    prefix_choices_tuple_list = [("", s)]
    # On each iteration we increase the length of each prefix by 1, until each
    # prefix is the length of a full permutation
    for _ in range(len(s)):
        # For each tuple of a valid prefix of a perumutation and the remaining
        # choices, replace the tuple with all tuples containing the same prefix
        # extended by one of the remaining choices, and the other remaining
        # choices
        prefix_choices_tuple_list = [
            (prefix + choice, choice_list[:i] + choice_list[i+1:])
            for prefix, choice_list in prefix_choices_tuple_list
            for i, choice in enumerate(choice_list)
        ]
    # Extract and return all of the prefixes, which are now complete
    # permutations (with no remaining choices for each prefix)
    perm_list = [prefix for prefix, _ in prefix_choices_tuple_list]
    return perm_list

print(find_permutations("1234"))
# >>> ['1234', '1243', '1324', '1342', '1423', '1432', '2134', '2143', '2314',
#      '2341', '2413', '2431', '3124', '3142', '3214', '3241', '3412', '3421',
#      '4123', '4132', '4213', '4231', '4312', '4321']
```

### Burrows–Wheeler transform (BWT)

```python
""" This is a simple, non-optimised implementation of the Burrows–Wheeler
transform, described here:
https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform """

def bwt(s_in):
    all_rotations = [s_in[-i:] + s_in[:-i] for i in range(len(s_in))]
    sorted_rotations = sorted(all_rotations)
    list_pos = sorted_rotations.index(s_in)
    s_out = "".join(s[-1] for s in sorted_rotations)

    return s_out, list_pos

def inverse_bwt(s_out, list_pos):
    all_rotations = sorted(s_out)
    for _ in range(len(s_out) - 1):
        all_rotations = sorted(
            s_out[i] + all_rotations[i]
            for i in range(len(s_out))
        )

    return all_rotations[list_pos]

s, i = bwt("^BANANA|")
print(s)
# BNN^AA|A
s = inverse_bwt(s, i)
print(s)
# ^BANANA|
```

## Notes on built-in and third-party modules

### `pip`

Upgrade `pip` with the following command (on Linux use `python3` instead of `python`):

```
python -m pip install -U pip
```

On Ubuntu, if `pip` is not installed, use the following commands to install it:

```
sudo apt-get update
sudo apt-get install python3-pip
```

To install a new package, EG `numpy`, use the following command:

```
python3 -m pip install numpy
```

To upgrade an existing package, EG `numpy`, use the following command:

```
python3 -m pip install -U numpy
```

### `argparse`

`argparse` is a module in Python for adding command line arguments to a Python script. The official Python documentation contains an [`argparse` tutorial](https://docs.python.org/3/howto/argparse.html), and an [`argparse` API reference](https://docs.python.org/3/library/argparse.html). Below is an example of a script which uses `argparse`, and examples of calling it from the command line.

Note that in the example below, the `-` characters before the argument names specify that those arguments are optional (as opposed to positional). The character used to specify optional arguments can be set using the `prefix_chars` argument of the constructor for the `ArgumentParser` class (the default is "`-`").

```python
"""
This is a dummy script, meant to imitate a script for training a CNN. This
script has a command-line interface, which allows epochs, num_hidden_units,
whether to use batch_norm, and whether to save the model to be specified from
the command-line.

Below are some examples of calling this script:

    python ./train.py --epochs 3 --num_hidden_units 15,3,15 --batch_norm

    python ./train.py --num_hidden_units 10,10,10 --epochs 10

For more information on the available arguments, use the following command:

    python ./train.py --help

"""

import argparse

def main(args):
    print(
        "epochs = %s, batch_norm = %s, num_hidden_units = %s, save = %s"
        % (args.epochs, args.batch_norm, args.num_hidden_units, args.save)
    )

if __name__ == "__main__":
    # Define CLI using argparse and parse command-line arguments
    parser = argparse.ArgumentParser(description="Script for training a CNN")

    parser.add_argument(
        "--epochs",
        help="Number epochs to train on training data. Default is 1",
        default=1,
        type=int,
    )
    parser.add_argument(
        "--num_hidden_units",
        help="Comma-separated list of hidden units per layer, EG 4,5,6",
        default="20,20",
        type=str,
    )
    parser.add_argument(
        "--batch_norm",
        help="Apply batch-normalisation to layer outputs",
        action="store_true",
    )
    parser.add_argument(
        "--no_save",
        help="Don't save the model",
        action="store_false",
        dest="save",
    )

    args = parser.parse_args()

    # Convert comma-separated string to list of ints
    args.num_hidden_units = [int(i) for i in args.num_hidden_units.split(",")]

    # Call main function using command-line arguments
    main(args)

```

The script can be called with or without the [`-m` flag](https://docs.python.org/3/using/cmdline.html#cmdoption-m):

```
$ python train.py
epochs = 1, batch_norm = False, num_hidden_units = [20, 20], save = True
$ python -m train
epochs = 1, batch_norm = False, num_hidden_units = [20, 20], save = True
```

A help message can be printed by adding a `-h` or `--help` argument:

```
$ python train.py -h
usage: train.py [-h] [--epochs EPOCHS] [--num_hidden_units NUM_HIDDEN_UNITS]
                [--batch_norm] [--no_save]

Script for training a CNN

optional arguments:
  -h, --help            show this help message and exit
  --epochs EPOCHS       Number epochs to train on training data. Default is 1
  --num_hidden_units NUM_HIDDEN_UNITS
                        Comma-separated list of hidden units per layer, EG
                        4,5,6
  --batch_norm          Apply batch-normalisation to layer outputs
  --no_save             Don't save the model
```

Optional arguments can be specified from the command line in any order, or they can be excluded, in which case the default value will be used:

```
$ python train.py --epochs 10 --num_hidden_units 10,10,10
epochs = 10, batch_norm = False, num_hidden_units = [10, 10, 10], save = True
$ python train.py --num_hidden_units 10,10,10 --epochs 10
epochs = 10, batch_norm = False, num_hidden_units = [10, 10, 10], save = True
$ python train.py --batch_norm --num_hidden_units 10,10,10 --epochs 10
epochs = 10, batch_norm = True, num_hidden_units = [10, 10, 10], save = True
$ python train.py --batch_norm --num_hidden_units 10,10,10 --epochs 10 --no_save
epochs = 10, batch_norm = True, num_hidden_units = [10, 10, 10], save = False
```

Since the `epochs` argument has been specified as having type `int`, an error will be thrown it is provided with a value which can't be converted directly into an `int`:

```
$ python train.py  --epochs ten
usage: train.py [-h] [--epochs EPOCHS] [--num_hidden_units NUM_HIDDEN_UNITS]
                [--batch_norm] [--no_save]
train.py: error: argument --epochs: invalid int value: 'ten'
```

### `pickle`

Use `pickle.dump` and `pickle.load` to save and load Python objects in binary files, as shown below.

```python
import pickle

x = [1, 2, 3, 5]
with open(".temp.pkl", "wb") as f:
    pickle.dump(x, f)

with open(".temp.pkl", "rb") as f:
    y = pickle.load(f)

print(x, y)
```

Output:

```
[1, 2, 3, 5] [1, 2, 3, 5]
```

`pickle.dumps` and `pickle.loads` can also be used to convert a Python object to and from a `bytes` object, which can be useful EG for [sending Python objects over `socket` connections (see below)]((#socket)).

### `socket`

These notes are mostly made from the [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/) on [realpython.com](https://realpython.com/). See also the [Python documentation for the `socket` module](https://docs.python.org/3/library/socket.html).

Below are the `echo-server.py` and `echo-client.py` programs from the [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/) on [realpython.com](https://realpython.com/), demonstrating a simple client-server application which communicates using sockets:

Server program:

```python
# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

Client program:

```python
# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")
```

- Sockets can be used to communicate between different processes on a single PC, or different PCs connected over a network
- Sockets "originated with [ARPANET](https://en.wikipedia.org/wiki/ARPANET) in 1971 and later became an API in the [Berkeley Software Distribution (BSD)](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution) operating system released in 1983 called [Berkeley sockets](https://en.wikipedia.org/wiki/Berkeley_sockets)"
- "All modern operating systems implement a version of the Berkeley socket interface. It became the standard interface for applications running in the Internet" ([source](https://en.wikipedia.org/wiki/Berkeley_sockets))
- "The most common type of socket applications are client-server applications, where one side acts as the server and waits for connections from clients"
- In Python, after importing the `socket` module using `import socket`, a socket can be created using the [`socket.socket`](https://docs.python.org/3/library/socket.html#socket.socket) class, EG `s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
  - The first argument to `socket.socket` is `family`, which represents the "address (and protocol) families", and can be EG `socket.AF_INET` or `socket.AF_INET6`
    - `socket.AF_INET` represents the [Internet Protocol version 4 (IPv4)](https://en.wikipedia.org/wiki/IPv4) **A**ddress **F**amily
    - `socket.AF_INET6` can be used for IPv6
  - The second argument to `socket.socket` is `type`, which represents the "socket types", and can be EG `socket.SOCK_STREAM` or `socket.SOCK_DGRAM`
    - `socket.SOCK_STREAM` specifies that the default protocol used by the socket is the [Transmission Control Protocol (TCP)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol), which is reliable ("packets dropped in the network are detected and retransmitted by the sender") and has in-order data delivery ("data is read by your application in the order it was written by the sender")
    - `socket.SOCK_DGRAM` can be used to specify User Datagram Protocol (UDP) sockets, which aren’t reliable, and can deliver data in a different order from that which was sent
- In a client-server socket application, in order to initialise a 2-way connection between the client and the server:
  - The server's socket object will call the `bind`, `listen`, and `accept` methods
    - The `bind(address)` method "is used to associate the socket with a specific network interface and port number"
      - The format of `address` depends on the address family of the socket
      - When the address family is `socket.AF_INET` (IPv4), `address` should be a 2-tuple containing the host and the port
      - The host "can be a hostname, IP address, or empty string"
        - "If an IP address is used, host should be an IPv4-formatted address string"
          - "The IP address 127.0.0.1 is the standard IPv4 address for the loopback interface", which can be used to connect to other sockets on the same PC, which "bypasses any local network interface hardware" (see the Wikipedia entry for [`localhost`](https://en.wikipedia.org/wiki/Localhost))
          - The 24-bit block 10.0.0.0/8 (16,777,216 addresses), 20-bit block 172.16.0.0/12 (1,048,576 addresses) and 16-bit block 192.168.0.0/16 (65,536 addresses) are reserved for addresses on the private network (see the Wikipedia entry for [Private network](https://en.wikipedia.org/wiki/Private_network))
        - "If you pass an empty string, the server will accept connections on all available IPv4 interfaces"
        - "If you use a hostname in the host portion of IPv4/v6 socket address, the program may show a non-deterministic behavior, as Python uses the first address returned from the DNS resolution... For deterministic behavior use a numeric address in host portion"
      - The port "represents the TCP port number to accept connections on from clients"
        - "It should be an integer from 1 to 65535, as 0 is reserved"
        - "Some systems may require superuser privileges if the port number is less than 1024"
    - The `listen` method "enables a server to accept connections", and makes the server's socket object a "listening" socket
      - The `listen` method has an optional backlog parameter, which "specifies the number of unaccepted connections that the system will allow before refusing new connections... If not specified, a default backlog value is chosen"
      - "If your server receives a lot of connection requests simultaneously, increasing the `backlog` value may help by setting the maximum length of the queue for pending connections"
    - The `accept()` method "blocks execution and waits for an incoming connection"
      - When a client socket connects to the server's socket object, the server's socket object's call to the `accept` method returns a 2-tuple containing:
        - A new socket object representing the connection
        - A tuple holding the address of the client
          - For IPv4 connections, the tuple holding the address of the client will contain `(host, port)`
      - Note that the new socket returned by the `accept` method is the socket that will be used to communicate with the client's socket
        - This is distinct from the listening socket that was previously created by the server (the object from which the `accept` method was called), which is a listening socket that the server can use to accept new connections
  - The client's socket object will call the `connect` method to connect to the server's socket object
    - `connect(address)` accepts an address whose format depends on the address family
    - When the address family is `socket.AF_INET` (IPv4), `address` should be a 2-tuple containing the host and the port
- The socket on the client can communicate with the socket returned by `accept` on the server EG by calling `send` and `recv`, while the original socket created on the server which called `listen` remains a listening socket
- The client and server can be on different machines connected over a local network, in which case the IP address that the server passes to `socket.bind(address)` and the IP address that the client passes to `socket.connect(address)` should both be set to the IP address of the network adapter of the *server* through which the server will communicate (EG an ethernet connection), and of course the port numbers should also match
  - The IP address of the desired network adapter can be found in `bash` using the commands `ip a` or `ifconfig`, or in Powershell using the command `ipconfig`
  - The address in the second element of the tuple returned by the `socket.accept()` method on the server will contain the IP address and port of the network adapter through which the *client* will communicate
- Both the client and the server can send bytes objects using the `send` or `sendall` methods and receive bytes using the `recv` method
- When the client has finished sending and receiving information, it can call the `socket.close()` method
  - Calling `socket.close()` on the client sends an empty bytes object to the server
  - Therefore, when the server receives an empty bytes object from the `recv` method, it may also wish to call the `socket.close()` method
  - Python `socket.socket` objects support context managers, which call the `socket.close()` method when the context manager exits, EG with the expression `with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:`, or after `conn, addr = s.accept()`, with the expression `with conn:`
- NB an entire complex Python object can be sent through a socket, by converting the Python object to a bytes object using `pickle.dumps`, sending that bytes object through the socket using `socket.sendall`/`socket.recv`, and then unpickling the bytes object using `pickle.loads` ([source](https://stackoverflow.com/a/53577447/8477566))
