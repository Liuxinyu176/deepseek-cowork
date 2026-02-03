## 问题分析

`text_container` 设置为 `background: transparent` 后，无法正确继承父容器背景色，导致子容器背景色不能随主题变化。

## 解决方案

为 `text_container` 显式设置与父容器相同的背景色 `bg_secondary`，确保它能随主题正确变化。

## 修改内容

将 `text_container` 的样式表设置回使用 `bg_secondary` 颜色。