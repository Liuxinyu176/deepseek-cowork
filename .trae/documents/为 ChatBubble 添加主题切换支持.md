## 问题分析

`think_toggle_btn` 在 ChatBubble 初始化时设置了样式表，使用了当时的主题颜色。当主题切换时，没有方法可以更新这个按钮的样式。

## 解决方案

1. 为 ChatBubble 添加 `update_theme` 方法
2. 在 `_on_theme_changed` 中遍历所有会话的 ChatBubble 并调用 `update_theme`

## 修改内容

1. 在 ChatBubble 类中添加 `update_theme` 方法，更新 `think_toggle_btn` 和 `think_container` 的样式
2. 在 `_on_theme_changed` 中更新所有 ChatBubble 的主题