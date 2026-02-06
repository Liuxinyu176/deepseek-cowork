# 问题分析

通过查看代码，我发现对话气泡高度异常的问题可能出在以下几个地方：

1. **AutoResizingTextEdit类**：负责自适应高度的文本编辑框，在处理HTML内容时可能无法正确计算高度
2. **ChatBubble类**：对话气泡的核心实现，可能在布局管理上存在问题
3. **布局结构**：父容器（chat_layout）和子容器（ChatBubble）之间的高度约束关系

# 解决方案

## 1. 修复AutoResizingTextEdit的adjustHeight方法

当前的adjustHeight方法在处理HTML内容时可能计算不准确，特别是当内容包含复杂的markdown渲染结果时。

## 2. 优化ChatBubble的布局结构

确保ChatBubble类中的布局能够正确处理不同类型的内容，特别是当内容高度变化时。

## 3. 确保布局更新及时

在设置内容后，确保调用适当的方法来触发布局更新，避免高度计算延迟。

# 具体修改步骤

1. **修改AutoResizingTextEdit.adjustHeight方法**：
   - 确保在处理HTML内容时也能正确计算高度
   - 添加对文档大小变化的监听

2. **优化ChatBubble.set_main_content方法**：
   - 在设置HTML内容后，确保正确触发高度调整
   - 添加必要的布局更新代码

3. **测试验证**：
   - 确保修复后对话气泡能够正确适应不同长度的内容
   - 验证在markdown渲染时高度计算是否准确