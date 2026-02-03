# -*- coding: utf-8 -*-
"""
配置管理模块，统一管理应用配置。
"""

import json
import os
import sys
import shutil
from .env_utils import get_app_data_dir, get_base_dir


class ConfigManager:
    """配置管理器，负责配置的加载、保存和管理。"""
    
    def __init__(self):
        self.config_file = "config.json"
        
        # Use centralized data directory logic
        self.data_dir = get_app_data_dir()
        self.config_path = os.path.join(self.data_dir, self.config_file)
        
        # Migration: Check if config exists in old location (base_dir)
        base_dir = get_base_dir()
        old_config_path = os.path.join(base_dir, self.config_file)
        
        # If old config exists and new config doesn't, migrate it.
        # Check inequality to avoid copy error if paths are same (e.g. portable mode setup)
        if os.path.abspath(old_config_path) != os.path.abspath(self.config_path):
            if os.path.exists(old_config_path) and not os.path.exists(self.config_path):
                print(f"[Config] Migrating config from {old_config_path} to {self.config_path}")
                try:
                    shutil.copy2(old_config_path, self.config_path)
                except Exception as e:
                    print(f"[Config] Migration failed: {e}")

        self.config = {
            "api_key": "",
            "base_url": "https://api.deepseek.com",
            "model_name": "deepseek-reasoner",
            "llm_provider": "openai",
            "disabled_skills": [],
            "god_mode": False,
            "default_workspace": "",
            "theme": "auto",  # 主题设置，可选值 "auto"/"light"/"dark"
            "font_size": "medium"  # 字体大小设置，可选值 "small"/"medium"/"large"
        }
        self.load_config()

    def get_god_mode(self):
        """获取God Mode状态。"""
        return self.config.get("god_mode", False)

    def set_god_mode(self, enabled: bool):
        """设置God Mode状态。"""
        self.config["god_mode"] = enabled
        self.save_config()

    def get_chat_history_dir(self):
        """获取聊天记录存储目录。"""
        default_dir = os.path.join(self.data_dir, 'chat_history')
        return self.config.get("chat_history_dir", default_dir)

    def set_chat_history_dir(self, path):
        """设置聊天记录存储目录。"""
        self.config["chat_history_dir"] = path
        self.save_config()

    def get_theme(self):
        """
        获取主题设置。
        
        Returns:
            str: "auto", "light", 或 "dark"
        """
        theme = self.config.get("theme", "auto")
        if theme not in ("auto", "light", "dark"):
            return "auto"
        return theme

    def set_theme(self, theme):
        """
        设置主题。
        
        Args:
            theme: "auto", "light", 或 "dark"
        """
        if theme in ("auto", "light", "dark"):
            self.config["theme"] = theme
            self.save_config()

    def get_font_size(self):
        """
        获取字体大小设置。
        
        Returns:
            str: "small", "medium", 或 "large"
        """
        font_size = self.config.get("font_size", "medium")
        if font_size not in ("small", "medium", "large"):
            return "medium"
        return font_size

    def set_font_size(self, font_size):
        """
        设置字体大小。
        
        Args:
            font_size: "small", "medium", 或 "large"
        """
        if font_size in ("small", "medium", "large"):
            self.config["font_size"] = font_size
            self.save_config()

    def load_config(self):
        """从文件加载配置。"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        """保存配置到文件。"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        """获取配置项。"""
        return self.config.get(key, default)

    def set(self, key, value):
        """设置配置项。"""
        self.config[key] = value
        self.save_config()

    def is_skill_enabled(self, skill_name):
        """检查技能是否启用。"""
        return skill_name not in self.config.get("disabled_skills", [])

    def set_skill_enabled(self, skill_name, enabled):
        """设置技能启用状态。"""
        disabled = set(self.config.get("disabled_skills", []))
        if enabled:
            if skill_name in disabled:
                disabled.remove(skill_name)
        else:
            disabled.add(skill_name)
        self.config["disabled_skills"] = list(disabled)
        self.save_config()
