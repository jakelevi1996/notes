# Notes on VSCode

## Contents

- [Notes on VSCode](#notes-on-vscode)
  - [Contents](#contents)
  - [Useful links](#useful-links)
  - [Installed extensions](#installed-extensions)
  - [Settings files](#settings-files)
  - [Snippets](#snippets)
  - [Synchronise settings](#synchronise-settings)

## Useful links

- [VS Code docs - Terminal Basics](https://code.visualstudio.com/docs/terminal/basics)
- [VS Code docs - Terminal Advanced (including `workbench.action.terminal.sendSequence`)](https://code.visualstudio.com/docs/terminal/advanced)
- [VS Code docs - Key Bindings for Visual Studio Code (including `runCommands`)](https://code.visualstudio.com/docs/getstarted/keybindings)
- [VS Code docs - Variables Reference (including `${relativeFile}`)](https://code.visualstudio.com/docs/editor/variables-reference)
- [Virtual-Key Codes (including `0x0D`)](https://learn.microsoft.com/en-gb/windows/win32/inputdev/virtual-key-codes)

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
ms-vscode.live-server
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

## Snippets

- To configure snippets (for a particular language):
  - Open command palette (`ctrl+shift+p`)
  - Select "Snippets: Configure Snippets"
  - Select language (EG `python`)
  - A `json` file in `~/.config/Code/User/snippets/` will be created (if it doesn't already exist) and opened
- Useful links:
  - [Snippets in Visual Studio Code](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
  - [Stack Overflow: "Visual Studio Code snippet invalid control character"](https://stackoverflow.com/q/46345154)
- Snippet files:
  - [`python.json`](snippets/python.json)
- Notes:
  - There seems to be a quirk when typing `import m` (`...`)
  - Only matching snippets are provided as a suggestion, but not other valid modules that could be imported (EG `math`)
  - Solutions:
    - (1) After typing `import m`, press `esc`/`backspace`, then continue typing
    - (2) When typing `import`, press `enter`/`tab` to autocomplete "`import`", then continue typing

## Synchronise settings

```
cp ~/.config/Code/User/snippets/python.json   topics/vscode/snippets/python.json
cp ~/.config/Code/User/snippets/markdown.json topics/vscode/snippets/markdown.json
cp ~/.config/Code/User/keybindings.json       topics/vscode/keybindings.json
cp ~/.config/Code/User/settings.json          topics/vscode/settings.json
```
