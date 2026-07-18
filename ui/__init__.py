"""UI package initialization with lazy tab class loading.

Uses lazy_loader to defer importing of UI submodules until they are
actually needed (i.e., when a tab of that type is created).
"""

import sys
import lazy_loader

# ==================== Lazy submodule registration ====================
# lazy_loader.attach returns __getattr__, __dir__, __all__ which must be
# assigned at module level to enable deferred imports via ui.<submodule>.
_submodules = [
    "shouye", "dingyi", "qiudao", "jifen", "bianxing",
    "fangcheng", "fangchengzu", "budengshi", "budengshizu",
    "jisuan", "help", "dingyixiangliang", "huitu_hanshu",
    "jiesanjiaoxing", "dingyi_pj", "huitu_pj", "dingyi_lj",
    "huitu_lj", "pjjisuan", "ljjisuan", "shezhi", "huancun"
]
__getattr__, __dir__, __all__ = lazy_loader.attach(__name__, _submodules)

# Extend __all__ with our own exports
__all__ += ["tabs_list", "tabs_dict"]

# ==================== Tab Registry ====================
# Each entry: (submodule_name, class_name)
_tab_registry = [
    ("shouye",           "Shouye"),
    ("dingyi",           "Dingyi"),
    ("qiudao",           "Qiudao"),
    ("jifen",            "Jifen"),
    ("bianxing",         "Bianxing"),
    ("fangcheng",        "Fangcheng"),
    ("fangchengzu",      "Fangchengzu"),
    ("budengshi",        "Budengshi"),
    ("budengshizu",      "Budengshizu"),
    ("jisuan",           "Jisuan"),
    ("help",             "Help"),
    ("dingyixiangliang", "Dingyixiangliang"),
    ("huitu_hanshu",     "Huitu_hanshu"),
    ("jiesanjiaoxing",   "Jiesanjiaoxing"),
    ("dingyi_pj",        "Dingyi_pj"),
    ("huitu_pj",         "Huitu_pj"),
    ("dingyi_lj",        "Dingyi_lj"),
    ("huitu_lj",         "Huitu_lj"),
    ("pjjisuan",         "Pjjisuan"),
    ("ljjisuan",         "Ljjisuan"),
    ("shezhi",           "Shezhi"),
    ("huancun",          "Huancun")
]

# Tab name -> index mapping
tabs_dict = {
    "首页": 0,   "定义": 1,    "求导": 2,      "积分": 3,
    "变形": 4,   "方程": 5,    "方程组": 6,    "不等式": 7,
    "不等式组": 8, "计算": 9,   "帮助": 10,    "定义向量": 11,
    "绘制函数": 12, "解三角形": 13, "平面几何": 14, "平面绘图": 15,
    "立体几何": 16, "立体绘图": 17, "平面计算": 18, "立体计算": 19,
    "设置": 20, "缓存区": 21
}

# Cache to avoid repeated getattr after first import
_tab_class_cache: dict = {}


def _get_tab_class(index):
    """Lazy-load and return the tab class for the given index.

    Accesses the submodule via the ui package namespace, which triggers
    lazy_loader's deferred import on first access. Result is cached.
    """
    if index not in _tab_class_cache:
        submodule_name, class_name = _tab_registry[index]
        # Access through the package to trigger lazy_loader's __getattr__
        _self = sys.modules[__name__]
        module = getattr(_self, submodule_name)
        _tab_class_cache[index] = getattr(module, class_name)
    return _tab_class_cache[index]


class _LazyTabList:
    """List-like proxy that lazily loads tab classes on access.

    Compatible with existing code that uses:
        tabs_list[index](parent, fs)    — deferred class instantiation
        len(tabs_list)                  — length queries
    """
    def __getitem__(self, index):
        return _get_tab_class(index)

    def __len__(self):
        return len(_tab_registry)


tabs_list = _LazyTabList()
