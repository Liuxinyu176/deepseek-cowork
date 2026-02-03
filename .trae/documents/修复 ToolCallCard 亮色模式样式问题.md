## 问题分析

用户反馈在亮色模式下，以下区域显示黑色背景（深色模式的颜色）：
1. ToolCallCard 的 text_container
2. 工具详情的 arguments 区域 (td_args_edit)
3. 内容预览标题区域 (r_preview_header)

## 原因

这些区域的样式在初始化时设置，但 `_on_theme_changed` 中没有更新它们的样式。

## 解决方案

1. 将 `r_preview_header` 改为实例变量 `self.r_preview_header`
2. 在 `_on_theme_changed` 中添加对这些区域的样式更新：
   - 更新 preview_header 样式
   - 更新 td_args_edit 样式
   - 确保 ToolCallCard 的 update_theme 正确工作

## 修改内容

1. 修改预览区域初始化代码，使用实例变量
2. 修改工具详情区域初始化代码
3. 在 _on_theme_changed 中添加样式更新逻辑