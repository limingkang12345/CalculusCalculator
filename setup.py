import sys
import os
from cx_Freeze import setup, Executable

# cx_Freeze 把 packages 中的模块放到 <exe>/lib/<包名>/，并自动复制包目录下的
# 全部非 .py 文件（cx_Freeze.freezer.Freezer._copy_package_data），
# 因此 math_input 内的 *.html 与 mathlive/（含字体）无需在此列出。
#
# 下面只列“包目录之外”的资源。目标路径必须与代码中的查找路径一致——
# 冻结后各模块位于 <exe>/lib/，于是 `os.path.join(dirname(__file__), '..', X)`
# 解析到 <exe>/lib/X。

# i18n/*.qm：由 core/settings.py、ui/i18n.py 定位，两级回退
#   冻结后 lib/i18n → <exe>/i18n，故放在可执行文件同级
I18N_FILES = [("i18n", "i18n")]

# 帮助文档：ui/help.py 与 ui/ui_help.py 都按 lib/help*.html 查找
HELP_FILES = [
    ("help.html", "lib/help.html"),
    ("help_en.html", "lib/help_en.html"),
]

# 积木编辑器：ui/blockly.py 按 lib/blockly/index.html 查找
# 其页面又以 ../mathjax/es5/tex-svg.js 引用公式渲染库，故两者同级
BLOCKLY_FILES = [
    ("blockly", "lib/blockly"),
    ("mathjax", "lib/mathjax"),
]

# 应用图标：build 时嵌入 exe；运行时主窗口按 exe 同级目录查找
ICON_FILES = [("favicon.ico", "favicon.ico")]

files = I18N_FILES + HELP_FILES + BLOCKLY_FILES + ICON_FILES

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
    + ["lazy_loader"]
    + collect_modules("math_input")
)

# 版本号与 core/settings.py 的 APP_VERSION 同源，避免两处不一致
APP_VERSION = "2.1.0"

# SETUP CX FREEZE
setup(
    name="CalculusCalculator",
    version=APP_VERSION,
    description="微积分计算器v" + APP_VERSION,
    author="LiMingkang",
    options={
        "build_exe": {
            "include_files": files,
            "includes": includes,
            # ui / core / math_input 是常规包（math_input 的 html 与 mathlive/
            # 作为包内数据自动复制）；functions 为命名空间包，只能用 includes
            "packages": ["ui", "core", "math_input", "lazy_loader"],
        }
    },
    executables=[target],
)