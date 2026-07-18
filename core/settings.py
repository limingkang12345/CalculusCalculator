"""多语言翻译辅助模块。

集中管理 QTranslator 的安装/卸载、.qm 文件定位，以及语言选择的持久化。
- 开发环境：.qm 位于项目根目录下的 i18n/。
- 冻结后（cx_Freeze）：.qm 由 include_files 复制到可执行文件同级的 i18n/。
"""

import os
import sys
import json

from PySide6.QtCore import QTranslator, QCoreApplication

# 当前已安装的翻译器（单例）；None 表示使用源语言（zh_CN）
_translator = None
_current = "zh_CN"
# 当前主题：'light' / 'dark'，默认浅色
_theme = "light"


def _qm_dir():
    """定位 .qm 所在目录，兼容开发环境与冻结后环境。"""
    # 开发环境：core/settings.py 的上级目录（项目根）下应有 i18n/
    here = os.path.dirname(os.path.abspath(__file__))      # .../ui
    pkg_root = os.path.dirname(here)                        # 项目根
    cand = os.path.join(pkg_root, "i18n")
    if os.path.isdir(cand):
        return cand
    # 冻结环境：可执行文件同级目录
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    cand2 = os.path.join(exe_dir, "i18n")
    if os.path.isdir(cand2):
        return cand2
    return cand


# 设置文件路径缓存：_settings_path() 的结果只计算一次。
# 必须在 run.py 设置好 QCoreApplication 的组织/应用名之后再触发首次计算，
# 否则无 QApplication 与有 QApplication 时 QStandardPaths 会解析出不同路径，
# 导致“保存”与“读取”指向不同文件（主题/语言无法持久化，历史 bug）。
_SETTINGS_PATH_CACHE = None


def _settings_path():
    """语言/主题设置的持久化文件路径，优先使用 Qt 标准配置目录。结果会被缓存。"""
    global _SETTINGS_PATH_CACHE
    if _SETTINGS_PATH_CACHE is not None:
        return _SETTINGS_PATH_CACHE
    path = None
    try:
        from PySide6.QtCore import QStandardPaths
        d = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
        if d:
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, "settings.json")
    except Exception:
        pass
    if not path:
        try:
            path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "settings.json")
        except Exception:
            path = os.path.join(os.getcwd(), "settings.json")
    _SETTINGS_PATH_CACHE = path
    return path


def _read_settings():
    """读取设置字典；文件不存在或损坏时返回 {}。"""
    p = _settings_path()
    try:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _write_settings(data):
    """把设置字典写入新路径（确保目录存在）。"""
    p = _settings_path()
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
    except Exception:
        pass
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def current_language():
    """返回当前语言代码（如 'zh_CN' / 'en_US'）。"""
    return _current


def apply_language(lang):
    """安装或卸载翻译器。

    lang 为 None / '' / 'zh_CN' 时卸载翻译器（使用源语言）；
    其它值（如 'en_US'）时加载对应 .qm 并安装。
    """
    global _translator, _current
    _current = lang or "zh_CN"

    app = QCoreApplication.instance()
    if app is None:
        return

    # 先移除并释放旧翻译器，否则界面不会回退/切换
    if _translator is not None:
        app.removeTranslator(_translator)
        _translator.deleteLater()
        _translator = None

    if _current in ("zh_CN", "zh", ""):
        return

    qm = os.path.join(_qm_dir(), _current + ".qm")
    if not os.path.exists(qm):
        return

    tr = QTranslator()
    if tr.load(qm):
        app.installTranslator(tr)
        _translator = tr


def load_saved_language():
    """从持久化文件读取上次选择的语言，默认 'zh_CN'。"""
    return _read_settings().get("language", "zh_CN")


def save_language(lang):
    """将语言选择写入持久化文件（合并历史设置，避免覆盖主题等其它项）。"""
    global _current
    _current = lang or "zh_CN"
    data = _read_settings()
    data["language"] = _current
    _write_settings(data)


def current_theme():
    """返回当前主题（'light' / 'dark'）。"""
    return _theme


def load_saved_theme():
    """从持久化文件读取上次选择的主题，默认 'light'。"""
    return _read_settings().get("theme", "light")


def save_theme(theme):
    """将主题选择写入持久化文件（合并历史设置，避免覆盖语言等其它项）。"""
    global _theme
    _theme = theme or "light"
    data = _read_settings()
    data["theme"] = _theme
    _write_settings(data)


# 模块加载时按已保存的设置同步当前主题，使 current_theme() 反映持久化值
_theme = load_saved_theme()
