---
name: python-runner
description: Execute Python code to perform tasks that are not covered by other tools.
description_cn: 执行 Python 代码以完成其他工具未涵盖的任务。
license: Apache-2.0
metadata:
  author: cowork-team
  version: "1.0"
allowed-tools: run_python_code
---

# Python Runner Skill

This skill allows the agent to execute arbitrary Python code within the workspace.
Use this when you need to calculate data, process text, or perform tasks where no specific tool exists.

## Capabilities
1. **Run Python Code**: Execute a Python script and get the stdout/stderr.

## Usage Guidelines
- **Sandboxed**: Code runs in the user's workspace.
- **Security**: File operations are restricted to the workspace.
- **Dependencies**: Standard library + installed packages (pandas, openpyxl, etc.) are available.
