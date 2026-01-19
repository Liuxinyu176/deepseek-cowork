# Agent 通用事件处理逻辑设计 (Technical Design)

## 1. 核心理念：DeepSeek Reasoning Mode (Thinking -> Coding)

我们放弃传统的 **ReAct (Reason + Act)** 循环模式，转而采用 **DeepSeek R1** 风格的 **推理-编码 (Reasoning-Coding)** 模式。

### 1.1 模式对比
*   **旧模式 (ReAct)**:
    *   Think: 我需要看下有哪些文件。
    *   Action: `list_files()`
    *   Observation: `['data.csv']`
    *   Think: 我需要读取它。
    *   Action: `read_file('data.csv')`
    *   ... (多轮交互，速度慢，易出错)
*   **新模式 (DeepSeek CoT)**:
    *   **Input**: 用户指令 + 当前目录结构快照。
    *   **Reasoning (`<think>`)**: 用户想要转换 CSV。我看到目录下有 `data.csv`。我应该使用 pandas 读取它，清洗数据，然后保存为 Excel。需要注意处理编码问题...
    *   **Code Generation**: 一次性生成包含所有步骤的完整 Python 脚本。
    *   **Execution**: 本地环境运行该脚本。
    *   **Result**: 任务完成。

### 1.2 优势
*   **减少延迟**: 只有一轮 LLM 调用。
*   **逻辑连贯**: 复杂的逻辑在 Thinking 阶段被完整规划，代码质量更高。
*   **透明度**: 将 `<think>` 内容展示给用户，增强信任感。

---

## 2. 架构组件 (Architecture Components)

### 2.1 Agent Core (DeepSeek Powered)
*   **Prompt 策略**: 
    *   System Prompt 中不再定义复杂的 Tool Schema。
    *   注入当前 Context（工作区文件列表、环境库版本）。
    *   使用 DeepSeek API 的 `reasoning_content` 特性。
    *   **Tool Calling**: 支持原生工具调用（如 `list_files`），允许模型在生成代码前探索环境。
    *   **技能创建策略**: 明确指示模型仅为可重用的算法或系统操作创建新技能，避免为文本总结等一次性任务创建技能。
*   **Parser**:
    *   直接读取 API 返回的 `reasoning_content` 字段 -> UI 右侧 "运行记录" (Task Monitor)。
    *   支持多轮工具调用循环 (Reasoning -> Tool Call -> Tool Output -> Reasoning -> Final Code)。
    *   提取 `content` 中的 `python` 代码块 -> 安全检查器 -> 执行器。

### 2.2 UI Layer Update
*   **Chat Interface**: 
    *   **中央聊天区**: 保持整洁，仅展示用户的指令和 Agent 的最终回复（Final Answer）。
    *   **Task Monitor (右侧栏)**: 承载详细的运行日志和 DeepSeek 的深度思考过程（可折叠展示）。
*   **Skills Center (功能中心)**:
    *   使用 `QTabWidget` 分页管理技能。
    *   **Tab 1**: 标准功能模块（内置技能）。
    *   **Tab 2**: AI 生成的技能（动态扩展）。
*   **Controls**: 新增暂停 (`Pause`) 和停止 (`Stop`) 按钮，允许用户实时干预执行流程。

### 2.3 Executor (执行器)
*   **职责**: 解析 Agent 的指令，安全地运行工具，并将结果标准化返回。
*   **特性**: 错误处理、超时控制、权限验证。
*   **Interaction Bridge**:
    *   **Input Interception**: 劫持 Python `input()` 函数，将其转换为 UI 层的弹窗请求 (`__REQUEST_INPUT__` 信号)。
    *   **GUI Modal**: 支持 Yes/No 确认框和文本输入框，实现后台代码与前台用户的同步交互。

### 2.4 Skill Manager (技能管理器)
*   **动态加载**: 支持从 `skills/` (内置) 和 `user_skills/` (用户自定义) 双路径加载技能。
*   **多语言支持**: 解析 `SKILL.md` 中的 `description_cn` 字段，优先在 UI 中展示中文描述。
*   **自动分类**: 根据 `created_by` 或 `type` 字段自动识别 "AI Generated" 技能。

---

## 3. 数据流示例 (Data Flow Example)

**用户输入**: "把当前目录下所有的 PNG 图片重命名为 JPG。"

**Round 1:**
*   **Context**: 用户指令
*   **Agent Thought**: 用户想处理文件。我需要先知道当前目录下有哪些文件。
*   **Agent Action**: Call `list_files({ path: "." })`
*   **Executor**: 执行 `ls`，返回 `['a.png', 'b.png', 'doc.txt']`

**Round 2:**
*   **Context**: 历史 + `list_files` 结果
*   **Agent Thought**: 我看到了两个 PNG 文件。我需要编写一个脚本来重命名它们。
*   **Agent Action**: Call `generate_and_run_script({ language: "python", code: "..." })`
*   **Executor**: 运行 Python 脚本，返回 "Success"

**Round 3:**
*   **Context**: 历史 + 脚本执行成功
*   **Agent Thought**: 任务已完成。
*   **Agent Final Answer**: "已成功将 a.png 和 b.png 转换为 JPG 格式。"

---

## 4. 技术架构 (Python Desktop App)

### 4.1 核心选型
采用纯 Python 技术栈开发，利用 Python 丰富的生态系统，简化开发与部署流程。

*   **GUI 框架**: **PySide6 (Qt for Python)**
    *   **理由**: 工业级 UI 框架，支持现代化界面，组件丰富，跨平台表现一致。
*   **打包工具**: **PyInstaller** 或 **Nuitka**
    *   **理由**: 将 Python 解释器、依赖库和脚本打包为独立的 `.exe` (Windows) 或 `.app` (Mac)，用户无需额外安装 Python。

### 4.2 模块划分与主要类

*   **UI Layer (PySide6)**:
    *   **MainWindow**: 负责工作区选择、会话列表、聊天区域、功能中心入口和运行日志展示。
    *   **SettingsDialog**: 负责 DeepSeek API Key、技能开关、安全模式等配置管理。
    *   **SkillsCenterDialog**: 基于 Tab 的技能管理界面。
*   **Workers**:
    *   **LLMWorker (QThread)**: 在后台线程执行 DeepSeek 调用，输出推理过程和最终回答，通过信号驱动 UI 更新。
    *   **CodeWorker (QThread)**: 在后台线程执行生成的 Python 代码，将 stdout/stderr 与输入请求映射为 UI 信号。
*   **Core Logic**:
    *   **Agent / LLMWorker**: 负责构建 Prompt，上下文管理（历史对话与技能定义），解析 reasoning_content 与 content。
    *   **SkillManager**: 扫描并加载 `skills/` 目录下的技能，将其暴露为可被 LLM 调用的工具。
    *   **ConfigManager**: 持久化用户设置，包括 API Key、工作区路径、技能启用状态、安全模式和自定义安全规则。
    *   **Executor / CodeWorker**:
        *   利用打包好的 Python 环境运行生成的代码。
        *   使用 `subprocess` 或受控 `exec`（结合 AST 检查）执行，统一错误处理和超时控制。

---

## 6. 安全机制 (Security & Sandboxing)

为了防止 AI 生成的恶意代码或误操作损害用户系统，必须实施严格的权限控制。

### 6.1 目录权限控制 (Workspace Restriction)
*   **原则**: Agent 只能读取和写入用户显式授权的目录（"Workspace"）。
*   **实现**:
    *   每次文件操作前，检查目标路径是否是 Workspace 的子路径。
    *   如果检测到 `..` 试图跳出目录，立即拦截并报错。
    *   在 System Prompt 中强制要求 Agent 使用相对路径或绝对路径（经校验）。

### 6.2 危险操作拦截 (High-Risk Interception)
*   **定义**: 删除文件、覆盖文件、执行未知命令等被视为高风险操作。
*   **机制**:
    *   Agent 在生成代码前，必须自我评估风险。
    *   如果涉及删除/修改，必须调用 `ask_user_confirmation` 工具。
    *   UI 层会弹出模态对话框，明确展示即将受影响的文件列表，只有用户点击 "Yes" 后才会继续执行。
