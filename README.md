# Notes

My notes on... everything! (WIP)

In particular:

- [Bash](topics/bash/README.md)
- [C/C++](topics/c_cpp/README.md)
- [Calling C code in Python](topics/c_python/README.md)
- [Cuda](topics/cuda/README.md)
- [`gdb` (GNU debugger)](topics/gdb/README.md)
- [GitLab CI](topics/gitlab_ci/README.md)
- [LaTeX](topics/latex/README.md)
- [MATLAB](topics/matlab/README.md)
- [Python](topics/python/README.md)
- [PyTorch](topics/pytorch/README.md)
- [Quotes](topics/quotes/README.md)
- [VS Code](topics/vscode/README.md)
- ...

Note: many of the topics here started out as separate Gist repositories, and were later cloned into this repository using the `git subtree add` command. As explained in [this Stack Overflow answer](https://stackoverflow.com/a/47571452/8477566), it is possible to clone an entire `git` repository into a subdirectory of the current repository (including all git history from the repository which is about to be cloned) using the following command (replace `$SUBDIR_NAME` and `$GIT_URL` as appropriate, NB `$GIT_URL` can include credentials as part of the URL, as described [here](topics/bash/README.md#use-git-push-with-an-authentication-token)):

```
git subtree add -P $SUBDIR_NAME $GIT_URL HEAD
```
