## 问题分析

ToolCallCard 在初始化时获取主题颜色并设置样式，但切换主题后：
1. 已创建的 ToolCallCard 不会自动更新样式
2. `_on_theme_changed` 方法没有更新 ToolCallCard 的逻辑
3. ToolCallCard 没有提供更新样式的方法

## 解决方案

1. 为 ToolCallCard 添加 `update_theme()` 方法，用于更新样式
2. 在 `_on_theme_changed` 方法中遍历所有 session 的 tool_cards 并调用 update_theme()
3. 更新 main_row、text_container、icon_label、labels 等的样式

## 修改内容

1. 在 ToolCallCard 类中添加 update_theme() 方法
2. 在 _on_theme_changed 中添加 ToolCallCard 样式更新逻辑