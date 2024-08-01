# Notes on VSCode

## Contents

- [Notes on VSCode](#notes-on-vscode)
  - [Contents](#contents)
  - [Installed extensions](#installed-extensions)
  - [Settings files](#settings-files)

## Installed extensions

Installed extensions can be listed on the command line using the command `code --list-extensions`. Below are the extensions I regularly use:

```
eamodio.gitlens
james-yu.latex-workshop
mechatroner.rainbow-csv
mhutchie.git-graph
ms-python.debugpy
ms-python.python
ms-python.vscode-pylance
ms-toolsai.jupyter-keymap
ms-vscode-remote.remote-ssh
ms-vscode-remote.remote-ssh-edit
ms-vscode.cpptools
ms-vscode.hexeditor
ms-vscode.remote-explorer
oliversturm.fix-json
pkief.material-icon-theme
stkb.rewrap
v4run.transpose
yzhang.markdown-all-in-one
```

To install an extension from the command line, use the `code --install-extension` command, EG `code --install-extension eamodio.gitlens`.

Below are some old extensions I have used in the past:

```
tomoki1207.pdf
yzane.markdown-pdf
donjayamanne.githistory
DavidAnson.vscode-markdownlint
fabiospampinato.vscode-diff
Gimly81.matlab
jack89ita.open-file-from-path
johnstoncode.svn-scm
```

Useful commands using the "Markdown All in One" extension:

-   Markdown: Open Locked Preview to the Side
-   Markdown All in One: Create Table of Contents
-   Markdown All in One: Update Table of Contents

## Settings files

- [`settings.json`](settings.json)
  - For more information about C/C++ default include-paths in VSCode, and how to combine them with local settings, see [Customizing default settings](https://code.visualstudio.com/docs/cpp/customize-default-settings-cpp)
- [`keybindings.json`](keybindings.json)
- [`./.vscode/settings.json`](workspace_settings.json)
  - `./.vscode/settings.json` contains workspace settings, included here in particular for the `pytestArgs`, and also for `"python.analysis.extraPaths"`, which allows paths to imported modules to be specified so that Pylance does not think they are missing
- [`./.vscode/c_cpp_properties.json`](c_cpp_properties.json)
  - C/C++ language settings, including `#define` macros, `#include` paths, and the compiler path
- [`./.vscode/launch.json`](launch.json)
  - Debugging configurations, including for Python and for C
- [`./.vscode/tasks.json`](tasks.json)
  - Task configurations, used as build commands for debugging configurations
