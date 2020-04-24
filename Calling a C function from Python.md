# Calling a C function from Python

The [`ctypes` module](https://docs.python.org/3/library/ctypes.html) in Python can be used to call a function which has been written and compiled using C. This Gist demonstrates a simple example of a C-function which takes an argument of type `in_struct` and returns a value of type `out_struct` (both of these types are defined in the source code), which is compiled into a DLL and called from a Python script.

There are a few quirks to bear in mind when using `ctypes`:

- From the section ["Return types"](https://docs.python.org/3/library/ctypes.html#return-types) of the `ctypes` documentation: "By default functions are assumed to return the C int type. Other return types can be specified by setting the `restype` attribute of the function object"
- If using 64-bit Python, then only 64-bit DLLs can be loaded using `ctypes` (and similarly for 32-bit Python and 32-bit DLLs); one way to compile 64-bit DLLs in Windows is to use the `x86_64-w64-mingw32-gcc` C compiler, which can be installed via [Cygwin](https://cygwin.com/install.html)
- Functions in C++ executables can also be called from Python, but they must be wrapped in an `extern "C"` block, as described in [this Stack Overflow answer](https://stackoverflow.com/a/145649/8477566); the reason for using `extern "C"` is to do with the name-mangling that C++ performs during compilation in order to allow function overloading, as described in [this Stack Overflow answer](https://stackoverflow.com/a/1041880/8477566)

Below is the C source code, and the Python script which calls the resulting binary DLL.

## `lib.c`

```c
/* Compile on 64-bit Windows using:
x86_64-w64-mingw32-gcc -fpic -shared -O3 lib.c -o lib64.dll
*/

typedef struct {
    int a;
    int b;
} in_struct;

typedef struct {
    int add;
    int subtract;
    int multiply;
    int max;
} out_struct;

out_struct calc_answer(in_struct i_s) {
    out_struct o_s;
    o_s.add = i_s.a + i_s.b;
    o_s.subtract = i_s.a - i_s.b;
    o_s.multiply = i_s.a * i_s.b;
    o_s.max = i_s.a > i_s.b ? i_s.a : i_s.b;
    return o_s;
}
```

## `main.py`

Before running this script, make sure `lib.c` is present in the same directory, and `lib64.dll` has been compiled using the command `x86_64-w64-mingw32-gcc -fpic -shared -O3 lib.c -o lib64.dll`.

```python
import os
import ctypes as ct

# Define structure that will be passed to the DLL function
class InStruct(ct.Structure):
    _fields_ = [("a", ct.c_int), ("b", ct.c_int)]

# Define structure that will be returned from the DLL function
class OutStruct(ct.Structure):
    _fields_ = [("add", ct.c_int), ("subtract", ct.c_int),
        ("multiply", ct.c_int), ("max", ct.c_int)]

# Load the DLL
lib = ct.cdll.LoadLibrary("lib64.dll")

# Get the function from the DLL and set the return type
calc_answer = lib.calc_answer
calc_answer.restype = OutStruct

def print_lib_func_values(a, b):
    i_s = InStruct(a, b)
    o_s = calc_answer(i_s)

    print("a = {}, b = {}".format(a, b))
    print("\tadd = {}, subtract = {}, multiply = {}, max = {}".format(
        o_s.add, o_s.subtract, o_s.multiply, o_s.max))

if __name__ == "__main__":
    # Test some random inputs
    print_lib_func_values(3, 4)
    print_lib_func_values(8, 5)
```

Output:

```
a = 3, b = 4
        add = 7, subtract = -1, multiply = 12, max = 4
a = 8, b = 5
        add = 13, subtract = 3, multiply = 40, max = 8
```