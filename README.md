# Notes

My notes on... everything! (WIP)

In particular:

- [Bash](./topics/bash/Notes%20on%20bash.md)
- [C/C++](./topics/c_cpp/Notes%20on%20C%20and%20C%2B%2B.md)
- [Calling C code in Python](./topics/c_python/Calling%20a%20C%20function%20from%20Python.md)
- [Cuda](./topics/cuda/Notes%20on%20CUDA.md)
- [`gdb` (GNU debugger)](./topics/gdb/Notes%20on%20gdb%20(GNU%20debugger).md)
- [GitLab CI](./topics/gitlab_ci/Notes%20on%20Gitlab%20CI.md)
- [LaTeX](./topics/latex/.Notes%20on%20Latex.md)
- [MATLAB](./topics/matlab/Notes%20on%20Matlab.md)
- [Python](./topics/python/Notes%20on%20Python.md)
- [PyTorch](./topics/pytorch/topics/pytorch/.Notes%20on%20PyTorch.md)
- [VS Code](./topics/vscode/Notes%20on%20VSCode.md)
- ...

Note: many of the topics here started out as separate Gist repositories, and were later cloned into this repository using the `git subtree add` command. As explained in [this Stack Overflow answer](https://stackoverflow.com/a/47571452/8477566), it is possible to clone an entire `git` repository into a subdirectory of the current repository (including all git history from the repository which is about to be cloned) using the following command (replace `$SUBDIR_NAME` and `$GIT_URL` as appropriate):

```
git subtree add -P $SUBDIR_NAME $GIT_URL HEAD
```
