# My VSCode settings

## `settings.json`

For more information about C/C++ default include-paths in VSCode, and how to combine them with local settings, see [Customizing default settings](https://code.visualstudio.com/docs/cpp/customize-default-settings-cpp).

```
{
    "window.zoomLevel": 0,
    "workbench.panel.defaultLocation": "right",
    "workbench.list.horizontalScrolling": true,

    "explorer.confirmDelete": false,
    "git.enableSmartCommit": true,
    "debug.console.historySuggestions": false,
    "editor.rulers": [80, 160],
    "explorer.confirmDragAndDrop": false,
    "workbench.colorTheme": "Visual Studio Dark",
    "python.linting.pylintArgs": [
        "--disable", "E1130", // Thinking numpy array doesn't support unary operator
        "--disable", "E0401", // Can't find modules that exist
        "--disable", "E1137", // 'a.flat' does not support item assignment
        "--disable", "C", // ignore conventions
        "--disable", "W", // ignore warnings
        "--disable", "R", // ignore refactor suggestions
    ],
    "workbench.iconTheme": "material-icon-theme",
    "material-icon-theme.files.associations": {
        "*.m": "Matlab",
        "*.lnk": "Url",
        "*.readme": "Readme",
    },
    "C_Cpp.default.includePath": [
        "C:/Python37/include",
        "C:/Program Files/MATLAB/R2020a/extern/include"
    ],
    "matlab.mlintpath": "C:/Program Files/MATLAB/R2020a/bin/win64/mlint.exe"
}
```

## `keybindings.json`

```json
// Place your key bindings in this file to overwrite the defaults
[
    {
        "key": "alt+r",
        "command": "python.execInTerminal",
        "when": "editorTextFocus"
    },
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
        "key": "alt+s",
        "command": "extension.transpose",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "alt+d",
        "command": "editor.action.deleteLines",
        "when": "textInputFocus && !editorReadonly"
    },
    {
        "key": "alt+t",
        "command": "workbench.action.terminal.toggleTerminal",
    },
    {
        "key": "alt+m",
        "command": "workbench.action.toggleMaximizedPanel",
    },
    {
        "key": "shift+alt+r",
        "command": "revealFileInOS",
    },
    {
        "key": "ctrl+f5",
        "command": "workbench.action.reloadWindow",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+d",
        "command": "compareSelected"
    },
    {
        "key": "ctrl+enter",
        "command": "workbench.action.terminal.runSelectedText",
        "when": "editorTextFocus"
    }
]
```

## `./.vscode/settings.json`

These are the workspace settings, included here in particular for the `pytestArgs`:

```
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
    "python.testing.pytestEnabled": true
}
```

## Installed extensions

Output of executing in terminal `code --list-extensions`:

```
yzane.markdown-pdf
donjayamanne.githistory
DavidAnson.vscode-markdownlint
fabiospampinato.vscode-diff  
Gimly81.matlab
jack89ita.open-file-from-path
johnstoncode.svn-scm
ms-python.python
ms-vscode.cpptools
oliversturm.fix-json
PKief.material-icon-theme
stkb.rewrap
v4run.transpose
```

## `c_cpp_properties.json`

```json
{
    "configurations": [
        {
            "name": "Win32",
            "compilerPath": "C:\\cygwin64\bin\\gcc.exe",
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