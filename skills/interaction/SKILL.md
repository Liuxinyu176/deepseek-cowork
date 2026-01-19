---
name: interaction
description: Provides interaction capabilities with the user.
description_cn: 提供与用户进行交互（提问、确认）的能力。
license: Apache-2.0
allowed-tools: ask_user_confirmation
---

# Interaction Skill

This skill provides interaction capabilities with the user.

## Tools

### ask_user_confirmation
Ask the user for confirmation (Yes/No) or input about a specific action or question.
If the user provides text input, it will be returned as "User replied: ...".

- **message** (string, required): The message to display to the user.
