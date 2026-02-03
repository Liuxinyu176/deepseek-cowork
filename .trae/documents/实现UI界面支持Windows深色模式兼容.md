## 目标
为UI界面添加Windows深色模式支持，能够自动检测系统主题并应用相应的界面主题，同时支持用户手动切换。

## 实现方案

### 1. 修改 theme.py
- 添加Windows系统主题检测功能（使用ctypes调用Windows API）
- 修改 `apply_theme` 函数，支持 "auto" 模式自动检测系统主题
- 添加主题切换信号/回调机制，支持运行时切换主题
- 保留手动指定 light/dark 的能力

### 2. 修改 config_manager.py
- 添加 `theme` 配置项（可选值："auto"/"light"/"dark"，默认"auto"）
- 添加 `get_theme()` 和 `set_theme()` 方法

### 3. 修改 main.py
- 在应用启动时调用 `apply_theme()` 应用主题
- 在设置对话框中添加主题选择下拉框（自动/亮色/暗色）
- 监听系统主题变化事件（Windows WM_SETTINGCHANGE消息），实现运行时自动切换

### 4. 添加依赖
- 需要添加 `pywin32` 或 `ctypes` 用于Windows API调用（ctypes为Python内置，无需额外安装）

## 文件修改清单
1. `core/theme.py` - 添加系统主题检测和自动切换逻辑
2. `core/config_manager.py` - 添加主题配置项
3. `main.py` - 应用主题、添加设置选项、监听系统主题变化

## 技术细节
- 使用Windows注册表 `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize` 下的 `AppsUseLightTheme` 值检测系统主题
- 使用 `QApplication.setStyleSheet()` 应用主题样式
- 通过重写 `QMainWindow.nativeEvent()` 监听Windows消息实现实时切换