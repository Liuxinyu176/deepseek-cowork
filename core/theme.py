# -*- coding: utf-8 -*-
"""
主题管理模块，支持亮色/暗色模式切换，自动检测Windows系统主题。
"""

import qdarktheme
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QObject, Signal
import platform


# 字体大小配置
FONT_SIZES = {
    "small": {
        "base": 12,
        "title": 16,
        "subtitle": 11,
        "label": 10,
        "button": 11,
        "input": 12,
        "code": 10,
    },
    "medium": {
        "base": 14,
        "title": 18,
        "subtitle": 13,
        "label": 11,
        "button": 12,
        "input": 14,
        "code": 11,
    },
    "large": {
        "base": 16,
        "title": 20,
        "subtitle": 14,
        "label": 12,
        "button": 13,
        "input": 15,
        "code": 12,
    }
}

# 内边距配置（根据字体大小调整）
PADDING_CONFIG = {
    "small": {
        "button": "4px 8px",
        "input": "6px 10px",
        "card": "12px",
        "container": "8px",
    },
    "medium": {
        "button": "6px 12px",
        "input": "8px 12px",
        "card": "16px",
        "container": "12px",
    },
    "large": {
        "button": "8px 16px",
        "input": "10px 14px",
        "card": "20px",
        "container": "16px",
    }
}


def get_font_size(size_key="medium"):
    """获取字体大小配置。"""
    return FONT_SIZES.get(size_key, FONT_SIZES["medium"])


def get_padding(size_key="medium"):
    """获取内边距配置。"""
    return PADDING_CONFIG.get(size_key, PADDING_CONFIG["medium"])


class DesignTokens:
    """设计令牌，定义应用的颜色和样式常量。"""
    
    # Core Colors
    primary = "#2563eb"  # Blue 600
    primary_hover = "#1d4ed8"  # Blue 700
    
    # Gradient for User Bubble
    primary_gradient_start = "#4d6bfe" 
    primary_gradient_end = "#3d5ce5"
    
    # Text
    text_primary = "#111827"  # Gray 900
    text_secondary = "#6b7280"  # Gray 500
    text_tertiary = "#9ca3af"  # Gray 400
    
    # Borders & Backgrounds
    border = "#e5e7eb"  # Gray 200
    bg_main = "#ffffff"
    bg_secondary = "#f6f8fa"  # GitHub Sidebar Gray
    
    # Shadows
    shadow_sidebar = "2px 0 8px rgba(0,0,0,0.04)"
    shadow_card = "0 1px 3px rgba(0,0,0,0.1)"

    # Semantic Colors (Success, Error, Warning, Info)
    # Functional Accents
    accent_ai = "#4d6bfe"      # AI 相关的强调色（思考气泡、AI头像）
    accent_user = "#4b5563"    # 用户标识色
    accent_success = "#10b981"  # 成功/完成
    accent_tool = "#f59e0b"    # 工具调用高亮

    # Success
    success_bg = "#f0fdf4"
    success_text = "#166534"
    success_border = "#bbf7d0"
    success_icon = "#166534"
    success_accent = "#10b981"  # Emerald 500
    
    # Error
    error_bg = "#fef2f2"
    error_text = "#991b1b"
    error_border = "#fecaca"
    error_icon = "#991b1b"
    
    # Warning
    warning_bg = "#fffbeb"
    warning_text = "#92400e"
    warning_border = "#fde68a"
    warning_icon = "#92400e"
    
    # Info
    info_bg = "#eff6ff"
    info_text = "#1e40af"
    info_border = "#bfdbfe"
    info_icon = "#1e40af"


class ThemeManager(QObject):
    """主题管理器，负责检测和应用主题。"""
    
    theme_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._current_theme = "light"
        self._app = None
    
    def get_windows_system_theme(self):
        """
        检测Windows系统主题。
        
        Returns:
            str: "light" 或 "dark"
        """
        if platform.system() != "Windows":
            return "light"
        
        try:
            import ctypes
            from ctypes import wintypes
            
            # 打开注册表项
            advapi32 = ctypes.windll.advapi32
            
            hKey = wintypes.HKEY()
            result = advapi32.RegOpenKeyExW(
                wintypes.HKEY(0x80000001),  # HKEY_CURRENT_USER
                "Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                0,
                0x20019,  # KEY_READ
                ctypes.byref(hKey)
            )
            
            if result != 0:
                return "light"
            
            # 读取 AppsUseLightTheme 值
            value_type = wintypes.DWORD()
            value_data = wintypes.DWORD()
            value_size = wintypes.DWORD(ctypes.sizeof(value_data))
            
            result = advapi32.RegQueryValueExW(
                hKey,
                "AppsUseLightTheme",
                None,
                ctypes.byref(value_type),
                ctypes.byref(value_data),
                ctypes.byref(value_size)
            )
            
            advapi32.RegCloseKey(hKey)
            
            if result == 0:
                # 0 = 暗色模式, 1 = 亮色模式
                return "light" if value_data.value == 1 else "dark"
            
        except Exception:
            pass
        
        return "light"
    
    def resolve_theme(self, theme):
        """
        解析主题设置。
        
        Args:
            theme: "auto", "light", 或 "dark"
            
        Returns:
            str: 实际应用的主题 "light" 或 "dark"
        """
        if theme == "auto":
            return self.get_windows_system_theme()
        return theme if theme in ("light", "dark") else "light"
    
    def get_current_theme(self):
        """获取当前应用的主题。"""
        return self._current_theme
    
    def set_app(self, app):
        """设置QApplication实例。"""
        self._app = app


# 全局主题管理器实例
theme_manager = ThemeManager()


def get_tech_stylesheet(theme="dark"):
    """
    获取技术风格的样式表。
    
    Args:
        theme: "light" 或 "dark"
        
    Returns:
        str: CSS样式表字符串
    """
    is_dark = theme == "dark"
    
    # Tech Palette
    # Dark: GitHub Dark Dimmed / VS Code Dark inspired
    # Light: Clean White / Google Material inspired
    
    if is_dark:
        c_bg_main = "#0d1117"      # Main window background
        c_bg_sidebar = "#010409"   # Sidebar background
        c_bg_card = "#161b22"      # Card/Container background
        c_bg_input = "#0d1117"     # Input field background
        
        c_text_primary = "#e6edf3"
        c_text_secondary = "#8b949e"
        c_text_tertiary = "#484f58"
        
        c_accent = "#2f81f7"       # Tech Blue
        c_accent_hover = "#58a6ff"
        
        c_border = "#30363d"       # Subtle border
        c_border_active = "#8b949e"
        
        c_success = "#238636"
        c_error = "#da3633"
        
        c_selection = "#1f6feb"  # Selection background
    else:
        c_bg_main = "#ffffff"
        c_bg_sidebar = "#f6f8fa"
        c_bg_card = "#ffffff"
        c_bg_input = "#f6f8fa"
        
        c_text_primary = "#24292f"
        c_text_secondary = "#57606a"
        c_text_tertiary = "#8c959f"
        
        c_accent = "#0969da"
        c_accent_hover = "#2188ff"
        
        c_border = "#d0d7de"
        c_border_active = "#0969da"
        
        c_success = "#1a7f37"
        c_error = "#cf222e"
        
        c_selection = "#b3d7ff"

    css = f"""
    /* Global Font & Reset */
    QWidget {{
        font-family: 'Segoe UI', 'Microsoft YaHei', 'Roboto', sans-serif;
        font-size: 14px;
        color: {c_text_primary};
        selection-background-color: {c_selection};
        selection-color: {c_text_primary};
    }}
    
    /* Main Layout Areas */
    QMainWindow, QWidget#MainContainer {{
        background-color: {c_bg_main};
    }}
    
    QWidget#Sidebar, QWidget#RightSidebar {{
        background-color: {c_bg_sidebar};
        border-right: 1px solid {c_border};
    }}
    QWidget#RightSidebar {{
        border-right: none;
        border-left: 1px solid {c_border};
    }}

    /* Card Containers */
    QFrame#ContentCard, QFrame#SkillCard {{
        background-color: {c_bg_card};
        border: 1px solid {c_border};
        border-radius: 8px;
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {c_bg_card};
        border: 1px solid {c_border};
        border-radius: 6px;
        padding: 6px 12px;
        color: {c_text_primary};
        text-align: center;
    }}
    QPushButton:hover {{
        border-color: {c_text_secondary};
        background-color: {c_bg_sidebar};
    }}
    QPushButton:pressed {{
        background-color: {c_border};
    }}
    
    /* Primary Action Button (Solid Accent) */
    QPushButton#PrimaryBtn {{
        background-color: {c_accent};
        color: #ffffff;
        border: 1px solid {c_accent};
        font-weight: bold;
    }}
    QPushButton#PrimaryBtn:hover {{
        background-color: {c_accent_hover};
        border-color: {c_accent_hover};
    }}
    
    /* Ghost/Text Button */
    QPushButton#GhostBtn {{
        background-color: transparent;
        border: none;
        color: {c_text_secondary};
    }}
    QPushButton#GhostBtn:hover {{
        color: {c_accent};
        background-color: {c_bg_sidebar};
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {c_bg_input};
        border: 1px solid {c_border};
        border-radius: 6px;
        padding: 8px;
        color: {c_text_primary};
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {c_accent};
        background-color: {c_bg_card};
    }}
    
    /* Search Box / Chips */
    QTextEdit#MainInput {{
        font-size: 15px;
        border: 1px solid {c_accent};
        border-radius: 20px; /* Pill shape */
        padding: 10px 16px;
        background-color: {c_bg_card};
    }}
    QTextEdit#MainInput:focus {{
        border: 1px solid {c_accent};
    }}

    /* Lists & Trees */
    QTreeView, QListView {{
        background-color: {c_bg_sidebar};
        border: none;
        outline: none;
    }}
    QTreeView::item {{
        padding: 4px;
        border-radius: 4px;
        margin: 1px 4px;
    }}
    QTreeView::item:hover {{
        background-color: {c_bg_card};
        border: 1px solid {c_border};
    }}
    QTreeView::item:selected {{
        background-color: {c_accent}22; /* Transparent accent */
        color: {c_text_primary};
        border: 1px solid {c_accent};
    }}
    
    /* Tab Widget */
    QTabWidget::pane {{
        border: none;
        background: {c_bg_main};
    }}
    QTabBar::tab {{
        background: transparent;
        padding: 8px 16px;
        margin-bottom: 2px;
        color: {c_text_secondary};
        font-weight: 500;
        border-bottom: 2px solid transparent;
    }}
    QTabBar::tab:hover {{
        color: {c_text_primary};
        background-color: {c_bg_sidebar};
        border-radius: 4px;
    }}
    QTabBar::tab:selected {{
        color: {c_accent};
        border-bottom: 2px solid {c_accent};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        border: none;
        background: transparent;
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {c_text_tertiary}44;
        min-height: 30px;
        border-radius: 5px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {c_text_tertiary}88;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    /* Specific Labels */
    QLabel[roleTitle="true"] {{
        font-size: 20px;
        font-weight: 600;
        color: {c_text_primary};
    }}
    QLabel[roleSubtitle="true"] {{
        font-size: 13px;
        color: {c_text_secondary};
    }}
    
    /* Menus */
    QMenu {{
        background-color: {c_bg_card};
        border: 1px solid {c_border};
        padding: 4px;
        border-radius: 6px;
    }}
    QMenu::item {{
        padding: 6px 24px 6px 12px;
        border-radius: 4px;
    }}
    QMenu::item:selected {{
        background-color: {c_accent};
        color: #ffffff;
    }}
    QMenu::separator {{
        height: 1px;
        background: {c_border};
        margin: 4px 0;
    }}
    
    /* Tooltips */
    QToolTip {{
        background-color: {c_bg_card};
        color: {c_text_primary};
        border: 1px solid {c_border};
        padding: 4px;
        border-radius: 4px;
    }}
    """
    return css


def apply_theme(app, theme="auto"):
    """
    应用主题到应用程序。
    
    Args:
        app: QApplication实例
        theme: "auto"（自动检测）, "light"（亮色）, 或 "dark"（暗色）
    """
    theme_manager.set_app(app)
    
    # 解析主题（处理auto情况）
    resolved_theme = theme_manager.resolve_theme(theme)
    theme_manager._current_theme = resolved_theme
    
    # 1. 加载 qdarktheme 基础样式
    base_sheet = qdarktheme.load_stylesheet(resolved_theme)
    
    # 2. 添加自定义技术样式覆盖
    tech_sheet = get_tech_stylesheet(resolved_theme)
    
    # 3. 合并并应用样式表
    app.setStyleSheet(base_sheet + "\n" + tech_sheet)
    
    # 4. 发出主题变更信号
    theme_manager.theme_changed.emit(resolved_theme)


def get_current_theme():
    """获取当前应用的主题。"""
    return theme_manager.get_current_theme()


def get_system_theme():
    """获取Windows系统当前主题设置。"""
    return theme_manager.get_windows_system_theme()


def get_theme_colors(theme=None):
    """
    获取指定主题的颜色配置。
    
    Args:
        theme: "light" 或 "dark"，为None时返回当前主题颜色
        
    Returns:
        dict: 包含各种颜色值的字典
    """
    if theme is None:
        theme = get_current_theme()
    
    is_dark = theme == "dark"
    
    if is_dark:
        return {
            # 背景色
            "bg_main": "#0d1117",
            "bg_sidebar": "#010409",
            "bg_card": "#161b22",
            "bg_input": "#0d1117",
            "bg_hover": "#1c2128",
            "bg_selected": "#1f6feb22",
            "bg_secondary": "#161b22",
            "bg_tertiary": "#0d1117",
            
            # 文字色
            "text_primary": "#e6edf3",
            "text_secondary": "#8b949e",
            "text_tertiary": "#484f58",
            "text_disabled": "#6e7681",
            
            # 边框色
            "border": "#30363d",
            "border_active": "#8b949e",
            "border_hover": "#58a6ff",
            
            # 强调色
            "accent": "#2f81f7",
            "accent_hover": "#58a6ff",
            "accent_light": "#388bfd",
            
            # 功能色
            "success": "#238636",
            "success_bg": "#23863633",
            "success_text": "#3fb950",
            "error": "#da3633",
            "error_bg": "#da363333",
            "error_text": "#f85149",
            "warning": "#d29922",
            "warning_bg": "#d2992233",
            "info": "#58a6ff",
            
            # 选择色
            "selection_bg": "#1f6feb",
            "selection_text": "#ffffff",
            
            # 历史会话
            "history_selected_bg": "#1f6feb33",
            "history_selected_text": "#58a6ff",
            "history_hover_bg": "#21262d",
            
            # 按钮
            "btn_primary_bg": "#238636",
            "btn_primary_hover": "#2ea043",
            "btn_secondary_bg": "#21262d",
            "btn_secondary_hover": "#30363d",
            
            # 阴影
            "shadow": "rgba(0,0,0,0.4)",
        }
    else:
        return {
            # 背景色
            "bg_main": "#ffffff",
            "bg_sidebar": "#f6f8fa",
            "bg_card": "#ffffff",
            "bg_input": "#f6f8fa",
            "bg_hover": "#f3f4f6",
            "bg_selected": "#eff6ff",
            "bg_secondary": "#f6f8fa",
            "bg_tertiary": "#f9fafb",
            
            # 文字色
            "text_primary": "#24292f",
            "text_secondary": "#57606a",
            "text_tertiary": "#8c959f",
            "text_disabled": "#9ca3af",
            
            # 边框色
            "border": "#d0d7de",
            "border_active": "#0969da",
            "border_hover": "#2188ff",
            
            # 强调色
            "accent": "#0969da",
            "accent_hover": "#2188ff",
            "accent_light": "#54aeff",
            
            # 功能色
            "success": "#1a7f37",
            "success_bg": "#dafbe1",
            "success_text": "#1a7f37",
            "error": "#cf222e",
            "error_bg": "#ffebe9",
            "error_text": "#cf222e",
            "warning": "#9a6700",
            "warning_bg": "#fff8c5",
            "warning_text": "#9a6700",
            "info": "#0969da",
            
            # 选择色
            "selection_bg": "#b3d7ff",
            "selection_text": "#24292f",
            
            # 历史会话
            "history_selected_bg": "#eff6ff",
            "history_selected_text": "#1d4ed8",
            "history_hover_bg": "#f3f4f6",
            
            # 按钮
            "btn_primary_bg": "#4d6bfe",
            "btn_primary_hover": "#3d5ce5",
            "btn_secondary_bg": "#f6f8fa",
            "btn_secondary_hover": "#e5e7eb",
            
            # 阴影
            "shadow": "rgba(0,0,0,0.1)",
        }


def get_sidebar_style(theme=None):
    """获取侧边栏样式。"""
    c = get_theme_colors(theme)
    return f"""
        background-color: {c['bg_sidebar']};
        border-right: 1px solid {c['border']};
    """


def get_right_sidebar_style(theme=None):
    """获取右侧边栏样式。"""
    c = get_theme_colors(theme)
    return f"""
        background-color: {c['bg_main']};
        border-left: 1px solid {c['border']};
    """


def get_history_button_style(selected=False, theme=None):
    """获取历史会话按钮样式。"""
    c = get_theme_colors(theme)
    if selected:
        return f"""
            QPushButton {{
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 8px;
                background-color: {c['history_selected_bg']};
                color: {c['history_selected_text']};
                font-weight: 600;
            }}
        """
    else:
        return f"""
            QPushButton {{
                text-align: left;
                padding: 10px;
                border: none;
                border-radius: 8px;
                background-color: transparent;
                color: {c['text_secondary']};
            }}
            QPushButton:hover {{
                background-color: {c['history_hover_bg']};
                color: {c['text_primary']};
            }}
        """


def get_workspace_selector_style(theme=None):
    """获取工作区选择器样式。"""
    c = get_theme_colors(theme)
    return f"""
        QFrame {{
            background-color: {c['bg_secondary']};
            border-radius: 8px;
            border: 1px solid {c['border']};
        }}
    """


def get_file_tree_style(theme=None):
    """获取文件树样式。"""
    c = get_theme_colors(theme)
    return f"""
        QTreeView {{
            border: none;
            background-color: {c['bg_main']};
        }}
        QTreeView::item {{
            padding: 4px;
            color: {c['text_primary']};
        }}
        QTreeView::item:selected {{
            background-color: {c['bg_selected']};
            color: {c['accent']};
        }}
        QTreeView::item:hover {{
            background-color: {c['bg_hover']};
        }}
    """


def get_preview_header_style(theme=None):
    """获取预览区域头部样式。"""
    c = get_theme_colors(theme)
    return f"""
        font-weight: 600;
        color: {c['text_secondary']};
        padding: 8px 12px;
        border-top: 1px solid {c['border']};
        border-bottom: 1px solid {c['border']};
        background: {c['bg_secondary']};
    """


def get_skill_card_style(theme=None):
    """获取技能卡片样式。"""
    c = get_theme_colors(theme)
    return f"""
        background-color: {c['bg_secondary']};
        border-radius: 5px;
        margin-bottom: 5px;
        border: 1px solid {c['border']};
    """


def get_sidebar_button_style(theme=None):
    """获取侧边栏按钮样式。"""
    c = get_theme_colors(theme)
    return f"""
        QPushButton {{
            text-align: left;
            padding: 8px;
            border: none;
            color: {c['text_secondary']};
            background: transparent;
            border-radius: 6px;
        }}
        QPushButton:hover {{
            background-color: {c['bg_hover']};
            color: {c['text_primary']};
        }}
    """


def get_new_chat_button_style(theme=None):
    """获取新建对话按钮样式。"""
    c = get_theme_colors(theme)
    return f"""
        QPushButton {{
            background-color: {c['btn_primary_bg']};
            color: white;
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: bold;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {c['btn_primary_hover']};
        }}
    """


def get_right_tabs_style(theme=None):
    """获取右侧标签页样式。"""
    c = get_theme_colors(theme)
    return f"""
        QTabWidget::pane {{
            border: none;
            background-color: {c['bg_main']};
        }}
        QTabBar::tab {{
            background: transparent;
            padding: 8px 12px;
            margin-right: 2px;
            border-bottom: 2px solid transparent;
            color: {c['text_secondary']};
            font-weight: 500;
        }}
        QTabBar::tab:selected {{
            color: {c['accent']};
            border-bottom: 2px solid {c['accent']};
        }}
        QTabBar::tab:hover {{
            background: {c['bg_hover']};
        }}
    """


def get_tool_details_style(theme=None):
    """获取工具详情区域样式。"""
    c = get_theme_colors(theme)
    text_edit_style = f"""
        QTextEdit, QPlainTextEdit {{
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 8px;
            background-color: {c['bg_input']};
            color: {c['text_primary']};
            font-family: 'Consolas', monospace;
            font-size: 11px;
        }}
    """
    return {
        "header": f"font-size: 14px; font-weight: bold; color: {c['text_primary']};",
        "info": f"color: {c['text_secondary']}; font-size: 12px;",
        "label": f"font-size: 12px; font-weight: 600; color: {c['text_primary']}; margin-top: 8px;",
        "input": text_edit_style,
        "result": text_edit_style
    }


def get_active_skills_label_style(theme=None):
    """获取活跃技能标签样式。"""
    c = get_theme_colors(theme)
    return f"color: {c['text_tertiary']}; font-size: 11px; margin-left: 12px;"


def get_confirmation_dialog_style(theme=None):
    """获取确认对话框样式。"""
    c = get_theme_colors(theme)
    return f"font-size: 14px; line-height: 1.4; color: {c['text_primary']};"


def get_menu_stylesheet(theme=None):
    """获取菜单样式表。"""
    c = get_theme_colors(theme)
    return f"""
        QMenu {{
            background-color: {c['bg_card']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 4px;
        }}
        QMenu::item {{
            padding: 6px 24px 6px 12px;
            border-radius: 4px;
            color: {c['text_primary']};
        }}
        QMenu::item:selected {{
            background-color: {c['accent']};
            color: #ffffff;
        }}
        QMenu::separator {{
            height: 1px;
            background: {c['border']};
            margin: 4px 0;
        }}
    """


def get_empty_state_style(theme=None):
    """获取空状态（快捷方式）区域样式。"""
    c = get_theme_colors(theme)
    return {
        "icon_color": c['border'],
        "title": f"font-size: 20px; font-weight: 600; color: {c['text_primary']};",
        "card": f"""
            QPushButton {{
                background-color: {c['bg_card']};
                border: 1px solid {c['border']};
                border-radius: 16px;
                padding: 24px;
                text-align: left;
            }}
            QPushButton:hover {{
                border: 1px solid {c['accent']};
                background-color: {c['bg_hover']};
            }}
        """,
        "card_title": f"font-size: 18px; font-weight: 600; color: {c['text_primary']}; background: transparent; border: none;",
        "card_desc": f"font-size: 14px; color: {c['text_secondary']}; background: transparent; border: none;"
    }


def get_main_input_style(theme=None):
    """获取主输入框样式。"""
    c = get_theme_colors(theme)
    return f"""
        QTextEdit#MainInput {{
            padding: 12px 16px;
            border-radius: 20px;
            border: 1px solid {c['accent']};
            background: {c['bg_card']};
            font-size: 14px;
            color: {c['text_primary']};
        }}
        QTextEdit#MainInput:focus {{
            border: 1px solid {c['accent']};
            background: {c['bg_card']};
            border-radius: 20px;
        }}
    """


def get_main_window_stylesheet(theme=None):
    """获取主窗口样式表。"""
    c = get_theme_colors(theme)
    return f"""
        QMainWindow {{
            background-color: {c['bg_main']};
        }}
        QLabel[roleTitle="true"] {{
            font-size: 18px;
            font-weight: 600;
            color: {c['text_primary']};
        }}
        QLabel[roleSubtitle="true"] {{
            font-size: 13px;
            color: {c['text_secondary']};
        }}
        {get_main_input_style(theme)}
        QScrollArea {{
            border: none;
            background: transparent;
        }}
        QTabWidget::pane {{
            border: none;
            background: {c['bg_main']};
        }}
        QTabBar::tab {{
            background: transparent;
            padding: 8px 16px;
            margin-right: 4px;
            border-radius: 6px;
            color: {c['text_secondary']};
        }}
        QTabBar::tab:selected {{
            background: {c['bg_selected']};
            color: {c['accent']};
            font-weight: bold;
        }}
        QTabBar::tab:hover {{
            background: {c['bg_hover']};
            color: {c['text_primary']};
        }}
        /* Global Scrollbar Beautification */
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 6px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {c['border']};
            min-height: 20px;
            border-radius: 3px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {c['text_tertiary']};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: transparent;
            height: 6px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {c['border']};
            min-width: 20px;
            border-radius: 3px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {c['text_tertiary']};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
        }}
    """


def get_dialog_stylesheet(theme=None):
    """获取对话框样式表。"""
    c = get_theme_colors(theme)
    return f"""
        QDialog {{
            background-color: {c['bg_main']};
        }}
        QLabel {{
            color: {c['text_primary']};
        }}
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {c['bg_input']};
            border: 1px solid {c['accent']};
            border-radius: 6px;
            padding: 8px;
            color: {c['text_primary']};
        }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {c['accent']};
        }}
        QPushButton {{
            background-color: {c['bg_card']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 6px 12px;
            color: {c['text_primary']};
        }}
        QPushButton:hover {{
            border-color: {c['accent']};
            background-color: {c['bg_hover']};
        }}
        QComboBox {{
            background-color: {c['bg_input']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            padding: 6px;
            color: {c['text_primary']};
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {c['bg_card']};
            color: {c['text_primary']};
            selection-background-color: {c['accent']};
        }}
        QCheckBox {{
            color: {c['text_primary']};
        }}
        QGroupBox {{
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            margin-top: 8px;
            padding-top: 8px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
    """


def get_system_toast_style(type="info", theme=None):
    """获取系统通知样式。"""
    c = get_theme_colors(theme)
    if type == "error":
        return {
            "bg": c['error_bg'],
            "text": c['error_text'],
            "border": c['error_bg']
        }
    elif type == "success":
        return {
            "bg": c['success_bg'],
            "text": c['success_text'],
            "border": c['success_bg']
        }
    elif type == "warning":
        return {
            "bg": c['warning_bg'],
            "text": c['warning_text'],
            "border": c['warning_bg']
        }
    else:
        return {
            "bg": c['info_bg'],
            "text": c['info_text'],
            "border": c['info_bg']
        }
