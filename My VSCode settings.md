# My VSCode settings

## `settings.json`

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


}
```

## `keybindings.json`

Note that the `"ctrl+oem_8"` (`ctrl + \``, ctrl + backtick) shortcuts are specifically for my laptop, which has a non-standard keyboard layout, with the backslash moved to the right hand side of the keyboard, preventing me from toggling comments with my left hand.

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
        "key": "alt+delete",
        "command": "editor.action.deleteLines",
        "when": "textInputFocus && !editorReadonly"
    },
    {
        "key": "alt+t",
        "command": "workbench.action.terminal.focus"
    },
    {
        "key": "alt+t",
        "command": "workbench.action.focusActiveEditorGroup",
        "when": "terminalFocus"
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
        "command": "workbench.action.terminal.runSelectedText"
    },
    {
        "key": "ctrl+oem_5",
        "command": "editor.action.commentLine",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+shift+oem_5",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+shift+oem_2",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+alt+oem_5",
        "command": "workbench.action.splitEditor"
    },
    {
        "key": "ctrl+oem_8",
        "command": "editor.action.commentLine",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+shift+oem_8",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },
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
                "${workspaceFolder}/**"
                "C:/Program Files/MATLAB/R2019b/extern/include"
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