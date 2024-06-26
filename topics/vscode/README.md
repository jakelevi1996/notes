# Notes on VSCode

## Contents

- [Notes on VSCode](#notes-on-vscode)
  - [Contents](#contents)
  - [Installed extensions](#installed-extensions)
  - [`settings.json`](#settingsjson)
  - [`keybindings.json`](#keybindingsjson)
  - [`./.vscode/settings.json` (workspace settings, including `pytestArgs` and `python.analysis.extraPaths`)](#vscodesettingsjson-workspace-settings-including-pytestargs-and-pythonanalysisextrapaths)
  - [`./.vscode/c_cpp_properties.json` (C/C++ language settings, including `#define` macros, `#include` paths, and the compiler path)](#vscodec_cpp_propertiesjson-cc-language-settings-including-define-macros-include-paths-and-the-compiler-path)
  - [`./.vscode/launch.json` (debugging configurations, including for Python and for C)](#vscodelaunchjson-debugging-configurations-including-for-python-and-for-c)
  - [`./.vscode/tasks.json` (task configurations, used as build commands for debugging configurations)](#vscodetasksjson-task-configurations-used-as-build-commands-for-debugging-configurations)

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

## `settings.json`

For more information about C/C++ default include-paths in VSCode, and how to combine them with local settings, see [Customizing default settings](https://code.visualstudio.com/docs/cpp/customize-default-settings-cpp)

```jsonc
{
    "python.defaultInterpreterPath": "python",
    "explorer.confirmDelete": false,
    "git.enableSmartCommit": true,
    "debug.console.historySuggestions": false,
    "editor.rulers": [79, 160],
    "explorer.confirmDragAndDrop": false,
    "[python]": {
        "editor.showUnused": false, // Disable greying out code which Pylance mistakenly thinks is unreachable
    },
    "python.linting.pylintArgs": [
        "--disable", "E1130", // Thinking numpy array doesn't support unary operator
        "--disable", "E0401", // Can't find modules that exist
        "--disable", "E1137", // 'a.flat' does not support item assignment
        "--disable", "C", // ignore conventions
        "--disable", "W", // ignore warnings
        "--disable", "R" // ignore refactor suggestions
    ],
    "material-icon-theme.files.associations": {
        "*.m": "Matlab",
        "*.mexw64": "Matlab",
        "*.lnk": "Url",
        "*.readme": "Readme"
    },
    "C_Cpp.default.includePath": [
        "${workspaceFolder}",
        "C:/Python37/include",
        "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.0/include/",
        "C:/Program Files/MATLAB/R2020a/extern/include"
    ],
    "matlab.mlintpath": "C:/Program Files/MATLAB/R2020a/bin/win64/mlint.exe",
    "[matlab]": {
        "editor.rulers": [75]
    },
    // "diffEditor.ignoreTrimWhitespace": false,
    "diffEditor.ignoreTrimWhitespace": true,
    "gitlens.hovers.currentLine.over": "line",
    "gitlens.currentLine.enabled": false,
    "gitlens.codeLens.enabled": false,
    "files.exclude": {
        ".git": true
    },
    "search.useGlobalIgnoreFiles": false,
    "search.useIgnoreFiles": false,
    // "editor.multiCursorModifier": "ctrlCmd", // <- this can be useful on Linux
    "files.trimTrailingWhitespace": true,
    "debug.onTaskErrors": "abort",
    "explorer.copyRelativePathSeparator": "/",
    "files.associations": {
        "*.vhd": "sql"
    },
    "workbench.colorTheme": "Default Dark+",
    "workbench.editor.wrapTabs": true,
    "workbench.editorAssociations": {
        "*.ipynb": "jupyter-notebook",
        "*.bin": "hexEditor.hexedit"
    },
    "workbench.iconTheme": "material-icon-theme",
    "workbench.list.horizontalScrolling": true,
    "workbench.panel.defaultLocation": "bottom",
    // "workbench.colorCustomizations": {
    //     "editorOverviewRuler.errorForeground": "#0000",
    //     "editorOverviewRuler.warningForeground": "#0000",
    // },
    // "workbench.colorCustomizations": {
    //     "editorError.foreground":   "#00000000",
    //     "editorWarning.foreground": "#00000000",
    //     "editorInfo.foreground":    "#00000000"
    // }
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "icon": "terminal-powershell"
        },
        "Command Prompt": {
            "path": [
                "${env:windir}\\Sysnative\\cmd.exe",
                "${env:windir}\\System32\\cmd.exe"
            ],
            "args": [],
            "icon": "terminal-cmd"
        },
        "Git Bash": {
            "source": "Git Bash"
        },
        "Ubuntu-18.04 (WSL)": {
            "path": "C:\\WINDOWS\\System32\\wsl.exe",
            "args": [
                "-d",
                "Ubuntu-18.04"
            ]
        },
        "Ubuntu (WSL)": {
            "path": "C:\\WINDOWS\\System32\\wsl.exe",
            "args": [
                "-d",
                "Ubuntu"
            ]
        }
    },
    // "terminal.integrated.defaultProfile.windows": "Ubuntu (WSL)",
    // "terminal.integrated.defaultProfile.windows": "Ubuntu-18.04 (WSL)",
    "terminal.integrated.scrollback": 1200,
	"terminal.integrated.wordSeparators": " []{}',\"`─",
    "[plaintext]": {
        "editor.language.colorizedBracketPairs": [
            ["{", "}"],
            ["[", "]"],
            ["(", ")"]
        ],
    },
    "[markdown]": {
        "editor.language.colorizedBracketPairs": [
            ["{", "}"],
            ["[", "]"],
            ["(", ")"]
        ],
    },
    "files.autoSave": "off",
}
```

## `keybindings.json`

```jsonc
// Place your key bindings in this file to overwrite the defaults
[
    {
        "key": "alt+c",
        "command": "editor.action.commentLine",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+c",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+alt+c",
        "command": "copyRelativeFilePath",
    },
    {
        "key": "ctrl+shift+alt+c",
        "command": "copyFilePath",
    },
    {
        "key": "alt+r",
        "command": "python.execInTerminal",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+r",
        "command": "workbench.action.terminal.runSelectedText",
        "when": "editorTextFocus"
    },
    {
        "key": "shift+alt+r",
        "command": "revealFileInOS",
    },
    {
        "key": "ctrl+alt+r",
        "command": "workbench.files.action.showActiveFileInExplorer",
    },
    {
        "key": "alt+s",
        "command": "extension.transpose",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+s",
        "command": "editor.action.insertCursorAtEndOfEachLineSelected",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+d",
        "command": "compareSelected"
    },
    {
        "key": "alt+d",
        "command": "editor.action.deleteLines",
        "when": "textInputFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+d",
        "command": "workbench.debug.action.toggleRepl",
    },
    {
        "key": "ctrl+alt+d",
        "command": "workbench.action.duplicateWorkspaceInNewWindow",
    },
    {
        "key": "alt+t",
        "command": "workbench.action.terminal.toggleTerminal",
    },
    {
        "key": "shift+alt+t",
        "command": "openInTerminal",
    },
    {
        "key": "alt+m",
        "command": "workbench.action.toggleMaximizedPanel",
    },
    {
        "key": "alt+k",
        "command": "workbench.action.terminal.kill"
    },
    {
        "key": "alt+a",
        "command": "git.stageSelectedRanges",
    },
    {
        "key": "alt+u",
        "command": "git.unstageSelectedRanges",
    },
    {
        "key": "alt+v",
        "command": "git.revertSelectedRanges",
    },
    {
        "key": "alt+g",
        "command": "git.openChange"
    },
    {
        "key": "ctrl+g",
        "command": "runCommands",
        "args": {
            "commands": [
                "workbench.scm.focus",
                "list.focusFirst",
                "list.select",
            ],
        },
    },
    {
        "key": "ctrl+alt+g",
        "command": "git-graph.view"
    },
    {
        "key": "alt+n",
        "command": "workbench.action.editor.nextChange",
        "when": "editorTextFocus"
    },
    {
        "key": "alt+n",
        "command": "workbench.action.compareEditor.nextChange",
        "when": "textCompareEditorVisible"
    },
    {
        "key": "alt+b",
        "command": "workbench.action.editor.previousChange",
        "when": "editorTextFocus"
    },
    {
        "key": "alt+b",
        "command": "workbench.action.compareEditor.previousChange",
        "when": "textCompareEditorVisible"
    },
    {
        "key": "ctrl+b",
        "command": "editor.action.selectToBracket",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+n",
        "command": "explorer.newFile"
    },
    {
        "key": "ctrl+alt+v",
        "command": "markdown.showPreviewToSide",
        "when": "!notebookEditorFocused && editorLangId == 'markdown'"
    },
    {
        "key": "alt+f",
        "command": "workbench.action.openRecent"
    },
    {
        "key": "ctrl+f5",
        "command": "workbench.action.reloadWindow",
        "when": "editorTextFocus"
    },
    {
        "key": "shift+alt+down",
        "command": "editor.action.copyLinesDownAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+up",
        "command": "editor.action.copyLinesUpAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "alt+left",
        "command": "workbench.action.navigateBack"
    },
    {
        "key": "alt+right",
        "command": "workbench.action.navigateForward"
    },
]

```

## `./.vscode/settings.json` (workspace settings, including `pytestArgs` and `python.analysis.extraPaths`)

These are the workspace settings, included here in particular for the `pytestArgs`, and also for `"python.analysis.extraPaths"`, which allows paths to imported modules to be specified so that Pylance does not think they are missing

```jsonc
{
    "python.pythonPath": "env\\Scripts\\python.exe",
    "python.testing.pytestArgs": [
        ".",
        "-o", "junit_family=xunit1",
        "--durations=5",
        // "-s"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
    "python.analysis.extraPaths": ["Scripts"]
}
```

## `./.vscode/c_cpp_properties.json` (C/C++ language settings, including `#define` macros, `#include` paths, and the compiler path)

```jsonc
{
    "configurations": [
        {
            "name": "Win32",
            "compilerPath": "C:\\cygwin64\\bin\\gcc.exe",
            "includePath": [
                "${workspaceFolder}/**",
                "C:/Program Files/MATLAB/R2019b/extern/include",
                "C:/Program Files/MATLAB/R2020a/extern/include",
                "C:/Program Files/MATLAB/R2020a/sys/lcc64/lcc64/include64"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE",
                "_GNU_SOURCE"
            ],
            "intelliSenseMode": "msvc-x64"
        }
    ],
    "version": 4
}
```

## `./.vscode/launch.json` (debugging configurations, including for Python and for C)

```jsonc
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
        },
        {
            "name": "Python, including stepping into external libraries",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false,
        },
        {
            "name": "Specific Python script with args",
            "type": "python",
            "request": "launch",
            "program": "path/to/Python/script.py",
            "console": "integratedTerminal",
            "args": ["--arg_1_name", "arg_2_name", "-etc"]
        },
        {
            // Remember to pass the -g flag to gcc when compiling
            "name": "Debug C executable",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/path/to/executable",
            "stopAtEntry": true,
            "cwd": "${workspaceFolder}",
            "preLaunchTask": "custom_build_task"
        }
    ]
}
```

## `./.vscode/tasks.json` (task configurations, used as build commands for debugging configurations)

```jsonc
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "custom_build_task",
            "type": "shell",
            "command": "gcc /path/to/source/file -o /path/to/executable -g"
        }
    ]
}
```
