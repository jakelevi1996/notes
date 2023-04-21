# Notes

My notes on... everything! (WIP)

In particular:

- [Bash](./topics/bash/)
- [C/C++](./topics/c_cpp/)
- [Calling C code in Python](./topics/c_python/)
- [Cuda](./topics/cuda/)
- [`gdb` (GNU debugger)](./topics/gdb/)
- [GitLab CI](./topics/gitlab_ci/)
- [LaTeX](./topics/latex/)
- [MATLAB](./topics/matlab/)
- [Python](./topics/python/)
- [PyTorch](./topics/pytorch/)
- [VS Code](./topics/vscode/)
- ...

Note: many of the topics here started out as separate Gist repositories, and were later cloned into this repository using the `git subtree add` command. As explained in [this Stack Overflow answer](https://stackoverflow.com/a/47571452/8477566), it is possible to clone an entire `git` repository into a subdirectory of the current repository (including all git history from the repository which is about to be cloned) using the following command (replace `$SUBDIR_NAME` and `$GIT_URL` as appropriate):

```
git subtree add -P $SUBDIR_NAME $GIT_URL HEAD
```
