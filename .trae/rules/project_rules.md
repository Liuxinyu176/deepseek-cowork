一、命名规范（遵循PEP8）
模块/包：全小写+下划线，如main_app.py、ui_components；类名：大驼峰，UI类加Window/Widget后缀，如LoginWindow；函数/变量：小写+下划线，如init_ui()、user_config_path；常量：全大写+下划线，如APP_NAME、DEFAULT_WINDOW_SIZE；资源：小写+下划线，如app_icon.ico、app_config.ini。
二、目录结构
project_name/（小写+下划线）：main.py（入口）、core/（核心业务）、ui/（界面代码）、utils/（工具类）、resources/（图标/配置）、build/（打包临时目录）、dist/（EXE输出）、requirements.txt（依赖清单）。资源集中管理，禁止散落。
三、编码核心要求
编码UTF-8，首行声明# -*- coding: utf-8 -*-；缩进4空格，单行≤120字符；导入按标准库→第三方→内部模块排序，禁止from xxx import *；函数单一职责，代码量≤50行；注释仅说明复杂逻辑，避免冗余。
四、资源与打包规范
资源路径用工具函数适配源码/EXE场景，禁止硬编码；打包用PyInstaller，统一脚本build_exe.py，参数含-F（单文件）、-w（无控制台）、-i（图标），--add-data加入资源。EXE命名如data_tool_v1.0.0.exe，发布包含EXE、说明文档。
五、异常与日志
禁止bare except，捕获指定异常并给出友好提示；用logging模块，输出日志到文件+控制台，禁止print调试；日志路径适配打包场景，不输出敏感信息。
六、配置管理
用ini/json/yaml存配置，禁止硬编码；创建ConfigManager统一读写配置，校验合法性，非法配置用默认值并提示。
所有的组件都受主题样式表影响，主题切换时需要更新所有组件的样式。
七、版本控制
.gitignore忽略打包目录、虚拟环境、缓存文件；提交信息格式[类型]描述，如[feat]新增登录功能、[fix]修复路径问题。
