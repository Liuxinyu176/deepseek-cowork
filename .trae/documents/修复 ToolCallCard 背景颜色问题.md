## 问题分析

ToolCallCard 背景颜色没有随主题变化，原因：

1. ToolCallCard 本身设置了 `background-color: transparent`
2. `main_row` 默认也是 `background-color: transparent`，只有悬停时才显示颜色
3. 没有为 ToolCallCard 设置合适的背景色

## 解决方案

1. 为 ToolCallCard 的 `main_row` 设置默认背景色（使用 `bg_secondary`）
2. 悬停时使用 `bg_hover` 颜色
3. 确保在不同主题下都能正确显示背景色

## 修改内容

修改 ToolCallCard 的 `main_row` 样式：
- 默认背景色：`bg_secondary`（次级背景色）
- 悬停背景色：`bg_hover`（悬停背景色）