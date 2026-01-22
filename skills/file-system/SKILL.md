---
name: file-system
description: Provides capabilities to list and read files in the user's workspace.
description_cn: 提供在用户工作区中列出、读取和操作文件的能力。
license: Apache-2.0
metadata:
  author: cowork-team
  version: "1.0"
security_level: high
allowed-tools: ["list_files", "read_file", "rename_file"]
---

# File System Skill

This skill allows the agent to interact with the local file system within the allowed workspace.
It is the **preferred way** to check file existence and list directory contents.

## Capabilities
1. **List Files**: Explore the directory structure to understand what files are available. Use this instead of running OS commands like `ls` or `dir`.
2. **Read Files**: Read the content of text files to understand data formats or code logic.
3. **Rename Files**: Rename or move files within the workspace.

## Usage Guidelines
- **Safety First**: Always check if a file exists using `list_files` before trying to read it.
- **Sandboxed**: You can only access files within the user-selected workspace.
- **Pathing**: Use relative paths (e.g., `data.csv` or `subdir/config.json`). Absolute paths or `..` traversals will be blocked.
