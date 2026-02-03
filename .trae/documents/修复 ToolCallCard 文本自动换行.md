## 问题分析

从截图可以看到两个问题：
1. 显示 arguments 的区域背景是纯白色，没有跟随主题
2. 长文本没有自动换行，导致布局错乱

## 原因

1. `args_preview` QLabel 没有设置背景色，可能继承了默认白色背景
2. `args_preview` 没有设置 `setWordWrap(True)`

## 解决方案

1. 为 `args_preview` 设置透明背景或继承父容器背景
2. 启用自动换行
3. 设置文本可选择，方便复制

## 修改内容

修改 ToolCallCard 中的 args_preview 标签：
- 添加 `setWordWrap(True)`
- 设置背景透明
- 添加 `setTextInteractionFlags`