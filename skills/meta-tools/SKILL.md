---
name: meta-tools
description: Meta-tools for the Agent to manage its own skills and experience.
description_cn: Agent 自我管理工具，用于记录经验和优化技能。
type: system
created_by: system
allowed-tools: update_experience
---

# Meta Tools

Tools for the Agent to self-evolve and manage the skill system.

## Tools

### update_experience
Records a successful "experience" or "lesson learned" for a specific skill.
This experience will be injected into the system prompt whenever that skill is used in the future.

**When to use:**
- When you encounter an error with a tool (e.g., missing dependency, wrong parameter format) and find a workaround.
- When you discover a specific configuration that works best for the user's environment.
- When you want to persist a "memory" about how to use a specific skill effectively.

**Parameters:**
- `skill_name`: The name of the skill to update (e.g., "yt-dlp-wrapper").
- `experience`: A concise, actionable sentence describing the lesson learned (e.g., "Always use absolute paths for output_dir.").
