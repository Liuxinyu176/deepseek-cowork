## 问题分析

1. **工作区宽度固定**：之前设置了 `setMaximumWidth(400)` 限制最大宽度，导致无法自由调节

2. **新建对话UI优化需求**：需要查看 EmptyStateWidget 的具体实现并优化

## 解决方案

1. **移除工作区最大宽度限制**：
   - 移除 `setMaximumWidth(400)`
   - 保留最小宽度限制，但允许自由扩展

2. **优化新建对话UI**：
   - 检查 EmptyStateWidget 的布局和样式
   - 优化卡片显示和布局

## 修改内容

1. 移除 `right_sidebar.setMaximumWidth(400)`
2. 优化 EmptyStateWidget 的UI