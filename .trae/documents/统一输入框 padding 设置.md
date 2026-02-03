## 问题分析

发现了两个不同的 padding 设置：
1. `get_tech_stylesheet` 中：`padding: 10px 16px`
2. `get_main_input_style` 中：`padding: 12px 16px`

padding 不同会导致输入框的实际高度不同，即使用户设置了固定高度，padding 也会影响内容的显示区域。

## 解决方案

统一所有 QTextEdit#MainInput 的 padding 为 12px 16px。

## 修改内容

修改 `get_tech_stylesheet` 中的 padding 为 12px 16px。