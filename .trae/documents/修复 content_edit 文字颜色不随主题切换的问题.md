## 问题分析

`self.content_edit.setStyleSheet("background: transparent; border: none; padding: 0;")` 没有设置文字颜色，所以文字颜色不会随主题切换。

## 解决方案

1. 在初始化时添加文字颜色到样式表
2. 在 `update_theme` 方法中更新 `content_edit` 的样式

## 修改内容

1. 修改初始化时的样式表，添加 `color: {c['text_primary']};`
2. 在 `update_theme` 方法中添加对 `content_edit` 的样式更新