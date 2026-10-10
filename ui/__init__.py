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
    "shouye", "help",
    "shezhi", "huancun", "blockly", "functions"
]
__getattr__, __dir__, __all__ = lazy_loader.attach(__name__, _submodules)

# Extend __all__ with our own exports
__all__ += ["tabs_list", "tabs_dict"]

# ==================== Tab Registry ====================
# Each entry: (submodule_name, class_name)
_tab_registry = [
    ("shouye",           "Shouye"),
    ("help",             "Help"),
    ("shezhi",           "Shezhi"),
    ("huancun",          "Huancun"),
    ("blockly",          "Blockly"),
    ("functions",       "Functions")
]

# Tab name -> index mapping
tabs_dict = {
    "首页": 0,   "帮助": 1,
    "设置": 2,  "缓存区": 3,  "积木编辑器": 4, "功能集成": 5
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
