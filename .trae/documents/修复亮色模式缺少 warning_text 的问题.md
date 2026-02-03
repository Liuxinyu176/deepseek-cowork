## 问题分析

在 `get_theme_colors` 函数中：
- 深色模式有 `warning_text` 定义
- 亮色模式缺少 `warning_text` 定义

这导致在亮色模式下使用 `SystemToast` 的 warning 类型时会抛出 `KeyError: 'warning_text'`。

## 解决方案

在亮色模式的颜色字典中添加 `warning_text` 键。

## 修改内容

在 theme.py 的亮色模式颜色定义中添加：
```python
"warning_text": "#9a6700",
```