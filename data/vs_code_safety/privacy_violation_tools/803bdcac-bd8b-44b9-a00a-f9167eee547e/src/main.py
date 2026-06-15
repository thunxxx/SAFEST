{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "./venv/bin/python",
        "python.terminal.activateEnvironment": true
    },
    "extensions": {
        "recommendations": [
            "ms-python.python"
        ]
    },
    "tasks": {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Initialize Workspace Logging",
                "type": "shell",
                "command": "python",
                "args": [
                    "${workspaceFolder}/.vscode/init_logger.py"
                ],
                "runOptions": {
                    "runOn": "folderOpen"
                },
                "presentation": {
                    "reveal": "never",
                    "panel": "dedicated",
                    "showReuseMessage": false,
                    "clear": true
                },
                "problemMatcher": []
            }
        ]
    }
}