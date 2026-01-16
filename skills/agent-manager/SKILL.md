---
name: agent-manager
description: Manage and spawn sub-agents to perform tasks in parallel.
license: Apache-2.0
metadata:
  author: cowork-team
  version: "1.0"
allowed-tools: dispatch_agents
---

# Agent Manager Skill

This skill allows the main agent to act as a manager and spawn multiple sub-agents to handle tasks simultaneously.

## Capabilities
1. **Dispatch Agents**: Spawn multiple sub-agents to execute a list of tasks in parallel.

## Usage Guidelines
- Use `dispatch_agents` when you have multiple independent tasks (e.g., "Research topic A", "Write code for module B", "Test module C").
- Each sub-agent runs in its own thread with its own context but shares the workspace.
- The manager waits for all sub-agents to complete and receives their aggregated results.
