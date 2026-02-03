## 问题分析

从用户反馈，父容器（text_container）的背景还是白色。可能的原因：

1. `text_container` 是 QWidget，样式表可能需要针对 QWidget 选择器
2. 或者 `text_container` 的样式表被其他样式覆盖了
3. 也可能是 `main_row` 的背景色没有正确显示

## 解决方案

1. 修改 `text_container` 的样式表，使用 QWidget 选择器
2. 确保样式表正确应用
3. 或者移除 `text_container` 的背景色设置，让它继承 `main_row` 的背景色

## 修改内容

将 `text_container` 的样式表从 `background-color` 改为继承父容器背景，或者使用正确的选择器。