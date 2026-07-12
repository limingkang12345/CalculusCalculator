import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = []

# TARGET
target = Executable(
    script="run.py",
    base="gui",
    icon="favicon.ico"
)


def collect_modules(package_dir):
    """收集 package_dir 目录下所有 .py 文件对应的模块名（点分形式）。

    用于显式告知 cx_Freeze 需要打包的模块。ui 使用了 lazy_loader 延迟导入、
    functions 各子模块以字符串形式被动态导入（如 `from functions.solids import ...`），
    cx_Freeze 的静态扫描无法发现这些模块，必须显式列出。
    注意：functions 目录没有 __init__.py（命名空间包），不能用 packages 选项，
    因此使用 includes 逐模块枚举最稳妥。
    """
    base = os.path.dirname(os.path.abspath(__file__))
    abs_dir = os.path.join(base, package_dir)
    modules = []
    if not os.path.isdir(abs_dir):
        return modules
    for root, _, filenames in os.walk(abs_dir):
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            # 跳过 __init__.py（由 packages 处理）以避免重复
            if fn == "__init__.py":
                continue
            rel = os.path.relpath(os.path.join(root, fn), base)
            mod = rel[:-3].replace(os.sep, ".")
            modules.append(mod)
    return modules


ui_modules = collect_modules("ui")
func_modules = collect_modules("functions")
core_modules = collect_modules("core")

# 需要打包的全部模块（显式枚举，确保冻结后均可导入）
includes = (
    ui_modules
    + func_modules
    + core_modules
    + ["lazy_loader", "resources_rc"]
)

# SETUP CX FREEZE
setup(
    name="CalculusCalculator",
    version="1.6.2",
    description="微积分计算器v1.6.2",
    author="LiMingkang",
    options={
        "build_exe": {
            "include_files": files,
            "includes": includes,
            # ui / core 是常规包，functions 为命名空间包；packages 仅对前者有效
            "packages": ["ui", "core", "lazy_loader"],
        }
    },
    executables=[target],
)
