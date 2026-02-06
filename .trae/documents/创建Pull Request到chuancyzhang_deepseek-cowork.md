# 创建PR计划

## 步骤

1. **添加远程仓库**
   - 添加fork的仓库作为远程仓库：`git remote add fork https://github.com/Liuxinyu176/deepseek-cowork.git`
   - 添加原始仓库作为upstream：`git remote add upstream https://github.com/chuancyzhang/deepseek-cowork.git`

2. **创建新分支**
   - 创建并切换到新分支：`git checkout -b fix/chat-bubble-height`

3. **提交更改**
   - 添加更改：`git add main.py`
   - 提交：`git commit -m "fix: 修复对话气泡高度异常问题"`

4. **推送到fork仓库**
   - 推送分支：`git push fork fix/chat-bubble-height`

5. **创建Pull Request**
   - 使用GitHub API创建PR到原始仓库

## 修复内容摘要

本次修复解决了两个对话气泡高度异常的问题：

1. **AI气泡高度异常**：`AutoResizingTextEdit.adjustHeight()` 方法添加最大高度限制，并在 `set_main_content` 中使用延迟调整高度

2. **用户气泡高度异常**：移除 `avatar_container` 中的 `addStretch()`，避免容器被撑高