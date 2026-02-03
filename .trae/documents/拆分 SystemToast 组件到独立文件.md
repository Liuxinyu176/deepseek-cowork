## 拆分计划

将 SystemToast 类从 main.py 拆分到 `ui/components/toast.py`

## 步骤

1. 创建目录结构 `ui/components/`
2. 创建 `ui/components/__init__.py`
3. 创建 `ui/components/toast.py` 包含 SystemToast 类
4. 更新 main.py 导入 SystemToast
5. 删除 main.py 中的 SystemToast 类定义
6. 运行语法检查验证

## 依赖分析

SystemToast 依赖：
- PySide6.QtWidgets: QFrame, QHBoxLayout, QLabel, QWidget
- PySide6.QtCore: Qt
- core.theme: get_theme_colors
- qtawesome as qta

这些依赖都需要在新文件中导入。