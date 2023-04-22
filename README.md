# Notes

My notes on... everything! (WIP)

In particular:

- [Bash](./topics/bash/notes_on_bash.md)
- [C/C++](./topics/c_cpp/notes_on_c_and_cpp.md)
- [Calling C code in Python](./topics/c_python/calling_a_c_function_from_python.md)
- [Cuda](./topics/cuda/notes_on_cuda.md)
- [`gdb` (GNU debugger)](./topics/gdb/notes_on_gdb_(gnu_debugger).md)
- [GitLab CI](./topics/gitlab_ci/notes_on_gitlab_ci.md)
- [LaTeX](./topics/latex/.notes_on_latex.md)
- [MATLAB](./topics/matlab/notes_on_matlab.md)
- [Python](./topics/python/notes_on_python.md)
- [PyTorch](./topics/pytorch/.notes_on_pytorch.md)
- [VS Code](./topics/vscode/notes_on_vscode.md)
- ...

Note: many of the topics here started out as separate Gist repositories, and were later cloned into this repository using the `git subtree add` command. As explained in [this Stack Overflow answer](https://stackoverflow.com/a/47571452/8477566), it is possible to clone an entire `git` repository into a subdirectory of the current repository (including all git history from the repository which is about to be cloned) using the following command (replace `$SUBDIR_NAME` and `$GIT_URL` as appropriate):

```
git subtree add -P $SUBDIR_NAME $GIT_URL HEAD
```
