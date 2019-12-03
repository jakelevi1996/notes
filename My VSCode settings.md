# My VSCode settings

## `settings.json`

```json
{
    "window.zoomLevel": 0,
    "explorer.confirmDelete": false,
    "git.enableSmartCommit": true,
    "editor.rulers": [
        80
    ],
    "explorer.confirmDragAndDrop": false,
    "workbench.colorTheme": "Visual Studio Dark",
    "python.pythonPath": "C:\\Users\\Jake\\Anaconda3\\python.exe",
    "telemetry.enableTelemetry": false,
    "telemetry.enableCrashReporter": false
}
```

## `keybindings.json`

```json
// Place your key bindings in this file to overwrite the defaults
[
    {
        "key": "f5",
        "command": "python.execInTerminal"
    },
    {
        "key": "ctrl+enter",
        "command": "workbench.action.terminal.runSelectedText"
    },
    {
        "key": "ctrl+d",
        "command": "diff.file"
    }
]
```

## Installed extensions

Output of executing in terminal `code --list-extensions`:

```
DavidAnson.vscode-markdownlint
donjayamanne.githistory
fabiospampinato.vscode-diff
Gimly81.matlab
ms-python.python
ms-vscode.cpptools
stkb.rewrap
yzane.markdown-pdf
```