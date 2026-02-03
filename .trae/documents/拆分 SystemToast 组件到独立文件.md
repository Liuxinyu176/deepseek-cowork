## 问题分析

代码逻辑有问题：
1. 第 987 行先设置了 `bubble_layout.setContentsMargins(16, 12, 16, 12)`
2. 第 1001 行 `bubble_layout.addWidget(content_label)`
3. 第 1003-1007 行又重新设置内边距

但问题是 `addWidget` 在调整内边距之前执行了，而且内边距调整逻辑在 `addWidget` 之后，这可能导致布局计算不正确。

## 解决方案

重新组织代码：
1. 先根据文本长度确定内边距
2. 设置内边距
3. 然后添加 widget

## 修改内容

调整代码顺序，确保内边距在添加 widget 之前正确设置。