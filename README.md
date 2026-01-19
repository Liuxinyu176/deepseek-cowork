# Smart File Assistant (DeepSeek Edition)

[中文文档](README_CN.md) | [English](README.md)

Smart File Assistant is a powerful desktop application that leverages **DeepSeek's advanced reasoning models (R1/V3)** to automate complex file operations through natural language.

Unlike traditional chatbots, this assistant uses a **Chain-of-Thought (CoT)** approach to plan, generate, and safely execute Python code to fulfill your requests—whether it's batch renaming files, analyzing data, or restructuring project directories.

![App Screenshot](placeholder-screenshot.png)

## 🚀 Key Features

*   **🧠 DeepSeek Reasoning Core**: Utilizes the "Reasoning-Coding" pattern. The agent thinks through the problem (`<think>`) before taking action, ensuring higher accuracy for complex tasks.
    *   **Real-time Thinking**: The "Reasoning" process is displayed in real-time in the right-side "Task Monitor" panel, keeping the main chat area clean with only final answers.
*   **🔌 Modular Skills Center**: 
    *   **Visual Management**: Built-in "Skills Center" panel to visually manage installed skills.
    *   **Categorized Display**: Automatically separates "Standard Skills" and "AI Generated Skills" for better organization using tabs.
    *   **Dynamic Extension**: The agent can solidify reusable algorithmic logic into new skills, evolving over time.
*   **🛡️ Secure Execution**:
    *   **Workspace Sandbox**: Operations are strictly confined to the user-selected directory.
    *   **AST Analysis**: Static code analysis prevents unauthorized path access (e.g., `../`, absolute paths) before execution.
    *   **Security Policy**: The agent is explicitly instructed to only create new skills for algorithmic/system operations, avoiding misuse.
*   **🤖 Multi-Agent Dispatch**: Capable of spawning sub-agents (`agent-manager`) to handle parallel tasks independently.
*   **💾 Auto-Save History**: Chat sessions are automatically saved and restored, allowing seamless continuation of tasks.
*   **⏯️ Real-time Control**: Supports pausing/resuming tasks at any time, and forcibly stopping execution if stuck in a loop.
*   **🖥️ Modern UI**: Built with **PySide6** (Qt for Python), offering a responsive and native desktop experience.

## 📦 Installation

### Option 1: Run from Executable (Windows)
1.  Download and unzip `dist/SmartFileAssistant.zip`.
2.  Run `SmartFileAssistant/SmartFileAssistant.exe`.
3.  No Python installation required.

### Option 2: Run from Source
**Prerequisites**: Python 3.10+

1.  Clone the repository:
    ```bash
    git clone https://github.com/chuancyzhang/smart-file-assistant.git
    cd smart-file-assistant
    ```

2.  Install dependencies:
    ```bash
    pip install PySide6 requests openai colorama
    ```

3.  Run the application:
    ```bash
    python main.py
    ```

## 📖 Usage Guide

1.  **Configuration**:
    *   Launch the app and click the **⚙️ Settings** button.
    *   Enter your **DeepSeek API Key** (and optional Base URL).
    *   Check and manage enabled skills in the "Skills Center".

2.  **Select Workspace**:
    *   Click "Select Workspace" to choose the folder you want the agent to work on. **The agent has NO access to files outside this folder.**

3.  **Start Chatting**:
    *   Enter a command, e.g.:
        *   *"Rename all .txt files in this folder to .md"*
        *   *"Read data.csv and tell me the average value of the 'Price' column"*
        *   *"Create a new folder named 'backup' and move all images there"*
    *   Watch the **Thinking** process in the right panel to understand how the agent plans the task.

4.  **Control Tasks**:
    *   Use the **⏸️ Pause** and **⏹️ Stop** buttons at the bottom to control the AI execution flow in real-time.

## 🏗️ Architecture

The project follows a modular design:

*   **`core/`**:
    *   `agent.py`: Manages LLM interaction, System Prompt policies (including skill creation restrictions), and conversation history.
    *   `skill_manager.py`: Handles dynamic tool loading, metadata parsing (supports multi-language descriptions), and categorization.
    *   `config_manager.py`: Persists user settings.
*   **`skills/`**:
    *   Plugins that extend functionality. Each skill (e.g., `file-system`) has its own `impl.py` and `SKILL.md` definition (supporting `description_cn`).
*   **`main.py`**: The PySide6 GUI entry point, including the main window, Skills Center dialog (Tabbed view), chat bubble components, etc.

## 🛠️ Developing New Skills

To add a new skill:
1.  Create a folder in `skills/` (e.g., `skills/git-helper`).
2.  Add `SKILL.md` to define the skill's purpose and prompts (adding `description_cn` is recommended).
3.  Add `impl.py` with Python functions. The `SkillManager` will automatically detect and register these functions as tools for the LLM.

## 📄 License

[MIT License](LICENSE)
