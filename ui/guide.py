"""初始化引导（新手引导教学）对话框。

通过分步向导带领新用户了解软件各功能区，内容与帮助文档（help.html）对应。
文案采用双语内嵌字典，按当前界面语言（core.settings.current_language）取用，
避免与 .ts/.qm 长文本匹配出错；首次启动或用户点击“关于 → 引导”时显示。

第 1 步为“语言与主题”设置：用户可在向导最前面选择语言与主题色，
选择后立即应用（回调 MainWindow.change_language / dark / light）。
语言选项无论当前语言为何，均固定以“中文 (Chinese)” / “English (中文)” 形式显示。
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextBrowser, QFrame, QSizePolicy, QRadioButton, QWidget, QButtonGroup,
    QProgressBar, QLineEdit,
)
from PySide6.QtCore import Qt

from sympy import sympify, SympifyError

from core.settings import current_language, current_theme, save_initialized


# 引导内容步骤（不含第 1 步“语言与主题”设置页）：每步含标题与正文（双语）。
# 正文为 HTML 片段，对应帮助文档各章节。
_GUIDE_STEPS = [
    {
        "title": {
            "zh": "欢迎使用 CalculusCalculator",
            "en": "Welcome to CalculusCalculator",
        },
        "html": {
            "zh": (
                "<p>这是一款面向微积分与代数运算的可视化计算工具。本向导将带你快速了解"
                "各功能区与常用操作。</p>"
                "<h3>界面概览</h3>"
                "<ul>"
                "<li><b>菜单栏</b>：文件、功能、积木、关于等入口。</li>"
                "<li><b>标签页</b>：求导、积分、定义、绘图、平面/立体几何、积木化等。</li>"
                "<li><b>主题与语言</b>：可在“功能 → 设置”中切换浅色/深色与中英文。</li>"
                "</ul>"
                "<p>点击“下一步”继续，或“跳过引导”直接进入主界面。</p>"
            ),
            "en": (
                "<p>This is a visual calculator for calculus and algebra. This guide "
                "walks you through the main areas and common operations.</p>"
                "<h3>UI Overview</h3>"
                "<ul>"
                "<li><b>Menu bar</b>: File, Functions, Blockly, About, etc.</li>"
                "<li><b>Tabs</b>: Derivative, Integral, Define, Plot, Plane/Solid "
                "Geometry, Blockly, and more.</li>"
                "<li><b>Theme &amp; Language</b>: switch light/dark and languages in "
                "Functions → Settings.</li>"
                "</ul>"
                "<p>Click “Next” to continue, or “Skip” to enter the main window.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "表达式输入（SymPy / LaTeX）",
            "en": "Expression Input (SymPy / LaTeX)",
        },
        "html": {
            "zh": (
                "<div style=\"margin:0 0 12px 0; padding:12px 14px; border:2px solid #8c52dc; "
                "border-radius:8px; background:#f3eeff;\">"
                "<b>✍ 可视化公式输入（推荐）</b><br>"
                "点击任意输入框右侧的 <b>“可视化输入”按钮</b>，即可在主窗口<b>底部</b>呼出"
                "内嵌的 <b>公式编辑器面板</b>（类似虚拟键盘）：<br>"
                "① 在面板上方的编辑器里用可视化方式拼出公式（分数、根号、上下标、矩阵等都能点选）；<br>"
                "② 面板会<b>实时预览</b> LaTeX；<br>"
                "③ 点击面板右下角 <b>“插入公式”</b>，结果自动写回输入框并关闭面板。<br>"
                "无需记忆 LaTeX，即可输入任意复杂的数学式。</div>"
                "<p>所有文本框支持标准 Python / SymPy 语法：</p>"
                "<ul>"
                "<li>加减乘除：<code>+</code> <code>-</code> <code>*</code> <code>/</code></li>"
                "<li>乘方：<code>x**2</code>；根号：<code>sqrt(x)</code>；对数：<code>log(x)</code></li>"
                "<li>常数：<code>pi</code>、<code>e</code>、<code>oo</code>（无穷）；虚数：<code>I</code></li>"
                "</ul>"
                "<p>还支持<b>直接输入 LaTeX</b>：在表达式前加半角美元符 <code>$</code>，"
                "例如 <code>$\\frac{x}{2}</code>、<code>$x^{2}</code>、<code>$\\sin{x}</code>。</p>"
            ),
            "en": (
                "<div style=\"margin:0 0 12px 0; padding:12px 14px; border:2px solid #8c52dc; "
                "border-radius:8px; background:#f3eeff;\">"
                "<b>✍ Visual Formula Input (recommended)</b><br>"
                "Click the <b>“Visual Input”</b> button on the right of any input box to pop up an "
                "embedded <b>formula editor panel</b> at the <b>bottom</b> of the main window "
                "(like a virtual keyboard):<br>"
                "① Compose your formula visually in the editor above (fractions, roots, sub/superscripts, "
                "matrices, etc. are one click away);<br>"
                "② The panel gives a <b>live LaTeX preview</b>;<br>"
                "③ Click <b>“Insert Formula”</b> at the bottom-right; the result is written back to the "
                "input box and the panel closes.<br>"
                "No need to memorize LaTeX to enter complex math.</div>"
                "<p>All text boxes accept standard Python / SymPy syntax:</p>"
                "<ul>"
                "<li>Add/sub/mul/div: <code>+</code> <code>-</code> <code>*</code> <code>/</code></li>"
                "<li>Power: <code>x**2</code>; sqrt: <code>sqrt(x)</code>; log: <code>log(x)</code></li>"
                "<li>Constants: <code>pi</code>, <code>e</code>, <code>oo</code> (infinity); "
                "imaginary: <code>I</code></li>"
                "</ul>"
                "<p>You can also input <b>LaTeX directly</b>: prefix the expression with a "
                "half-width dollar sign <code>$</code>, e.g. <code>$\\frac{x}{2}</code>, "
                "<code>$x^{2}</code>, <code>$\\sin{x}</code>.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "计算选项卡与计算引擎",
            "en": "Calculation Tab & Engines",
        },
        "html": {
            "zh": (
                "<p>“计算”页面提供四种计算引擎：</p>"
                "<ul>"
                "<li><b>Python 内置引擎</b>：快速数值计算，普通文本显示。</li>"
                "<li><b>Mpmath 高精度引擎</b>：可自定义精度。</li>"
                "<li><b>SymPy 符号引擎</b>：符号运算，结果同时显示 LaTeX 与文本。</li>"
                "<li><b>LaTeX 代码生成引擎</b>：由 Python 表达式生成 LaTeX 代码。</li>"
                "</ul>"
            ),
            "en": (
                "<p>The “Calculation” tab offers four engines:</p>"
                "<ul>"
                "<li><b>Python built-in</b>: fast numeric evaluation, plain text.</li>"
                "<li><b>Mpmath high-precision</b>: configurable decimal precision.</li>"
                "<li><b>SymPy symbolic</b>: symbolic math, results shown as both LaTeX and text.</li>"
                "<li><b>LaTeX generator</b>: produces LaTeX code from a Python expression.</li>"
                "</ul>"
            ),
        },
    },
    {
        "title": {
            "zh": "定义函数",
            "en": "Define Functions",
        },
        "html": {
            "zh": (
                "<p>在“定义”页面可定义自定义函数（存入 <code>fs</code> 字典）。</p>"
                "<p>定义后，在多数输入框中可直接使用该函数：</p>"
                "<ul>"
                "<li>作为符号：已定义 <code>g(x)=x**2</code>，输入 <code>g+1/g</code>。</li>"
                "<li>函数调用：输入 <code>f(3)</code> 自动计算，支持嵌套如 <code>f(g(2))</code>。</li>"
                "</ul>"
                "<p>定义域、单调性、奇偶性等分析也基于所定义的函数。</p>"
            ),
            "en": (
                "<p>Define your own functions on the “Define” page (stored in the <code>fs</code> dict).</p>"
                "<p>Once defined, use the function in most input boxes:</p>"
                "<ul>"
                "<li>As a symbol: with <code>g(x)=x**2</code>, enter <code>g+1/g</code>.</li>"
                "<li>By call: <code>f(3)</code> evaluates automatically; nesting like "
                "<code>f(g(2))</code> is supported.</li>"
                "</ul>"
                "<p>Domain, monotonicity and parity analysis all rely on defined functions.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "微积分与微分方程",
            "en": "Calculus & Differential Equations",
        },
        "html": {
            "zh": (
                "<p>在对应标签页可完成：</p>"
                "<ul>"
                "<li><b>求导</b>：对函数或表达式求导。</li>"
                "<li><b>积分</b>：不定/定积分，分母含根号时自动有理化。</li>"
                "<li><b>微分方程</b>：使用 <code>f(x).diff(x)</code> 表示导数，"
                "待求函数固定为 <code>f(x)</code>。</li>"
                "</ul>"
                "<p>示例：左式 <code>f(x).diff(x)</code>，右式 <code>f(x)+1</code> 求解 "
                "<code>f'(x)=f(x)+1</code>。</p>"
            ),
            "en": (
                "<p>Use the corresponding tabs to:</p>"
                "<ul>"
                "<li><b>Differentiate</b>: derivative of a function or expression.</li>"
                "<li><b>Integrate</b>: indefinite/definite; radicals in denominators are "
                "rationalized automatically.</li>"
                "<li><b>Differential equations</b>: use <code>f(x).diff(x)</code> for the "
                "derivative; the unknown is fixed as <code>f(x)</code>.</li>"
                "</ul>"
                "<p>Example: LHS <code>f(x).diff(x)</code>, RHS <code>f(x)+1</code> solves "
                "<code>f'(x)=f(x)+1</code>.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "方程 / 不等式 / 解三角形",
            "en": "Equations / Inequalities / Triangles",
        },
        "html": {
            "zh": (
                "<ul>"
                "<li><b>方程（组）</b>：支持符号与数值求解，主元范围可用集合限定。</li>"
                "<li><b>不等式（组）</b>：解集以集合或区间形式返回。</li>"
                "<li><b>解三角形</b>：填入 3 个有效条件（角 A/B/C 或边 a/b/c），"
                "支持 ASA、AAS、SAS、SSA、SSS 等情形，多解会分别标注。</li>"
                "</ul>"
            ),
            "en": (
                "<ul>"
                "<li><b>Equation(s)</b>: symbolic/numeric solving; the principal range "
                "can be constrained with sets.</li>"
                "<li><b>Inequality(s)</b>: solution sets returned as sets or intervals.</li>"
                "<li><b>Solve triangles</b>: enter 3 valid conditions (angle A/B/C or side "
                "a/b/c); supports ASA, AAS, SAS, SSA, SSS; multiple solutions are labeled.</li>"
                "</ul>"
            ),
        },
    },
    {
        "title": {
            "zh": "绘图功能",
            "en": "Plotting",
        },
        "html": {
            "zh": (
                "<ul>"
                "<li><b>绘制函数</b>：输入表达式或选择已定义函数，设置定义域后点击绘制；"
                "自动处理间断点。</li>"
                "<li><b>平面绘图</b>：可视化平面几何对象（点、线、圆、三角形、多边形）。</li>"
                "<li><b>立体绘图</b>：3D 可视化立体几何对象，可旋转视角。</li>"
                "</ul>"
                "<p>图像由 Matplotlib 渲染，坐标轴清晰标注。</p>"
            ),
            "en": (
                "<ul>"
                "<li><b>Plot function</b>: enter an expression or pick a defined function, "
                "set the domain, then plot; discontinuities are handled automatically.</li>"
                "<li><b>Plane plot</b>: visualize plane-geometry objects (points, lines, "
                "circles, triangles, polygons).</li>"
                "<li><b>Solid plot</b>: 3D visualization of solid-geometry objects with a "
                "rotatable view.</li>"
                "</ul>"
                "<p>Plots are rendered by Matplotlib with clearly labeled axes.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "平面 / 立体几何",
            "en": "Plane / Solid Geometry",
        },
        "html": {
            "zh": (
                "<p>在“平面几何 / 立体几何”页面定义对象，再在对应“计算”页面进行运算：</p>"
                "<ul>"
                "<li><b>平面</b>：点、直线、圆、三角形、多边形（共 19 种构造方法），"
                "支持距离、交点、面积、周长、质心等 32 种运算。</li>"
                "<li><b>立体</b>：三维点、直线、平面、线段，支持 22 种空间运算与四面体体积等。</li>"
                "</ul>"
                "<p>对象以名称引用，参数用英文半角逗号分隔。</p>"
            ),
            "en": (
                "<p>Define objects on the “Plane / Solid Geometry” pages, then compute on the "
                "matching “Calculation” pages:</p>"
                "<ul>"
                "<li><b>Plane</b>: points, lines, circles, triangles, polygons (19 constructors); "
                "32 operations such as distance, intersection, area, perimeter, centroid.</li>"
                "<li><b>Solid</b>: 3D points, lines, planes, segments; 22 spatial operations "
                "including tetrahedron volume.</li>"
                "</ul>"
                "<p>Reference objects by name; parameters separated by half-width commas.</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "向量",
            "en": "Vectors",
        },
        "html": {
            "zh": (
                "<p>在“定义向量”页面定义二维向量（名称、x/y 坐标），支持 SymPy 表达式。</p>"
                "<ul>"
                "<li><b>属性</b>：表达式、模、方向角、单位向量。</li>"
                "<li><b>运算</b>：选择两个向量，执行加法、减法、点积、夹角。</li>"
                "</ul>"
            ),
            "en": (
                "<p>On the “Define Vector” page, define 2D vectors (name, x/y) with SymPy "
                "expressions allowed.</p>"
                "<ul>"
                "<li><b>Properties</b>: expression, magnitude, direction angle, unit vector.</li>"
                "<li><b>Operations</b>: pick two vectors to add, subtract, dot-product, or "
                "find the angle.</li>"
                "</ul>"
            ),
        },
    },
    {
        "title": {
            "zh": "积木化功能（Blockly）",
            "en": "Blockly (Visual Blocks)",
        },
        "html": {
            "zh": (
                "<p>“积木化”页面提供可视化编辑器，拖拽拼接积木即可搭建计算流程，无需写代码：</p>"
                "<ul>"
                "<li>积木内直接输入 SymPy 表达式或以 <code>$</code> 输入 LaTeX。</li>"
                "<li>点击运行，按顺序执行并实时显示中间结果。</li>"
                "<li>输出公式以 LaTeX 自动渲染。</li>"
                "<li>支持定义函数、求导/积分、解方程/不等式/三角形。</li>"
                "<li>工程可存档/读档，受“设置 → 存档设置”控制。</li>"
                "</ul>"
            ),
            "en": (
                "<p>The “Blockly” page offers a visual editor: drag and snap blocks to build "
                "computation flows without coding:</p>"
                "<ul>"
                "<li>Enter SymPy expressions in blocks, or LaTeX with <code>$</code>.</li>"
                "<li>Click Run to execute in order with live intermediate results.</li>"
                "<li>Outputs are rendered as LaTeX automatically.</li>"
                "<li>Define functions, differentiate/integrate, solve equations/inequalities/triangles.</li>"
                "<li>Projects can be saved/loaded, governed by Settings → Save Options.</li>"
                "</ul>"
            ),
        },
    },
    {
        "title": {
            "zh": "效率工具：缓存 / 公式输入 / 设置",
            "en": "Productivity: Cache / Formula Input / Settings",
        },
        "html": {
            "zh": (
                "<ul>"
                "<li><b>缓存区</b>：双击列表项复制表达式；输入框右侧按钮可存/取缓存。</li>"
                "<li><b>可视化公式输入</b>：点击输入框右侧键盘图标，图形化插入数学符号（基于 MathLive）。</li>"
                "<li><b>设置</b>：配置语言、主题，以及“存档设置”精细控制保存哪些数据。</li>"
                "<li><b>存档/读档</b>：通过“文件 → 保存/打开”保存工作现场（含主题与语言）。</li>"
                "</ul>"
                "<p>设置以 JSON 保存在 Qt 标准配置目录下（含 <code>language</code>、<code>theme</code> 等）。</p>"
            ),
            "en": (
                "<ul>"
                "<li><b>Cache</b>: double-click a list item to copy; input-box buttons store/fetch cache.</li>"
                "<li><b>Visual formula input</b>: click the keyboard icon to insert math symbols "
                "graphically (MathLive-based).</li>"
                "<li><b>Settings</b>: configure language, theme, and fine-grained Save Options.</li>"
                "<li><b>Save/Load</b>: use File → Save/Open to persist the workspace (theme &amp; language included).</li>"
                "</ul>"
                "<p>Settings are stored as JSON in the Qt config directory (with <code>language</code>, "
                "<code>theme</code>, …).</p>"
            ),
        },
    },
    {
        "title": {
            "zh": "帮助与完成",
            "en": "Help & Finish",
        },
        "html": {
            "zh": (
                "<p>你已完成初始化引导！</p>"
                "<ul>"
                "<li>随时可点击<b>“关于 → 引导”</b>再次查看本向导。</li>"
                "<li>点击<b>“关于 → 帮助”</b>（或菜单“关于 → 帮助”）查看完整帮助文档。</li>"
                "<li>遇到疑问可参考 Python / SymPy / Mpmath 官方文档。</li>"
                "</ul>"
                "<p>感谢使用 CalculusCalculator，祝你计算愉快！</p>"
            ),
            "en": (
                "<p>You have finished the onboarding guide!</p>"
                "<ul>"
                "<li>Reopen this guide anytime via <b>About → Guide</b>.</li>"
                "<li>Open the full help via <b>About → Help</b> (or the About menu).</li>"
                "<li>For questions, refer to the Python / SymPy / Mpmath official docs.</li>"
                "</ul>"
                "<p>Thanks for using CalculusCalculator. Happy calculating!</p>"
            ),
        },
    },
]

# ---------------------------------------------------------------------------
# 各内容步骤的“动手试试”互动练习（按内容步骤索引 0..n-1 对应 _GUIDE_STEPS）。
# 仅用于让用户在引导中亲自动手验证某个操作，不属于多选题。
# ---------------------------------------------------------------------------
_GUIDE_EXERCISES = {
    1: {
        "zh": "动手试试：在下方输入一个 SymPy 表达式（例如 x**2+2*x+1），输入后按回车检查是否合法。",
        "en": "Try it: type a SymPy expression below (e.g. x**2+2*x+1), then press Enter to check it.",
    },
}

# 第 1 步“语言与主题”设置页标题（双语）。
_SETTINGS_STEP_TITLE = {
    "zh": "语言与主题",
    "en": "Language & Theme",
}

# 设置页内固定双语标签：语言选项无论当前语言始终以“中文 (Chinese)”形式显示。
# 这些标签固定双语，切换语言时无需重新翻译。
_SETUP_LABELS = {
    "lang": "语言 (Language)",
    "theme": "主题 (Theme)",
    "light": "浅色 (Light)",
    "dark": "深色 (Dark)",
}


def _guide_text(d):
    """按当前语言从双语字典取文本，回退到中文。"""
    lang = (current_language() or "").lower()
    return d.get("en" if lang.startswith("en") else "zh", d["zh"])


class GuideDialog(QDialog):
    """分步引导教学对话框，首步为语言/主题选择（即时应用）。"""

    def __init__(self, parent=None, open_help_callback=None,
                 apply_language_callback=None, apply_theme_callback=None):
        super(GuideDialog, self).__init__(parent)
        self._steps = _GUIDE_STEPS
        self._idx = 0
        self._open_help = open_help_callback
        self._apply_lang = apply_language_callback
        self._apply_theme_cb = apply_theme_callback
        self.setWindowTitle(_guide_text({
            "zh": "初始化引导",
            "en": "Getting Started",
        }))
        self.setMinimumSize(640, 560)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._build_ui()
        self._apply_theme()
        self._show_step(0)

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        # 标题
        self._title = QLabel("")
        self._title.setObjectName("guideTitle")
        f = self._title.font()
        f.setPointSize(16)
        f.setBold(True)
        self._title.setFont(f)
        root.addWidget(self._title)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        root.addWidget(line)

        # 设置页（第 1 步：语言与主题选择）
        self._setup_page = QWidget()
        self._setup_page.setObjectName("guideSetup")
        self._build_setup_page(self._setup_page)
        root.addWidget(self._setup_page, 1)

        # 正文
        self._body = QTextBrowser()
        self._body.setOpenExternalLinks(False)
        self._body.setReadOnly(True)
        self._body.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root.addWidget(self._body, 1)

        # “动手试试”互动练习区
        self._build_exercise_ui(root)

        # 底部：进度 + 按钮
        bottom = QHBoxLayout()
        bottom.setSpacing(8)

        self._progress = QProgressBar()
        self._progress.setObjectName("guideProgress")
        self._progress.setTextVisible(True)
        self._progress.setFixedWidth(220)
        bottom.addWidget(self._progress)

        bottom.addStretch(1)

        self._btn_skip = QPushButton(_guide_text({
            "zh": "跳过引导", "en": "Skip",
        }))
        self._btn_back = QPushButton(_guide_text({
            "zh": "上一步", "en": "Back",
        }))
        self._btn_next = QPushButton(_guide_text({
            "zh": "下一步", "en": "Next",
        }))
        self._btn_finish = QPushButton(_guide_text({
            "zh": "完成", "en": "Finish",
        }))

        self._btn_skip.clicked.connect(self._on_skip)
        self._btn_back.clicked.connect(self._on_back)
        self._btn_next.clicked.connect(self._on_next)
        self._btn_finish.clicked.connect(self._on_finish)

        bottom.addWidget(self._btn_skip)
        bottom.addWidget(self._btn_back)
        bottom.addWidget(self._btn_next)
        bottom.addWidget(self._btn_finish)
        root.addLayout(bottom)

    def _build_setup_page(self, page):
        """构建“语言与主题”设置页。语言选项始终以“中文 (Chinese)”形式显示。"""
        layout = QVBoxLayout(page)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(12)

        lang_hint = QLabel(_SETUP_LABELS["lang"])
        lang_hint.setObjectName("guideSubTitle")
        layout.addWidget(lang_hint)

        # 语言选项：无论当前语言，均固定以“中文 (English)”形式显示
        self._lang_group = QButtonGroup(self)
        self._lang_group.setExclusive(True)
        self._lang_zh = QRadioButton("中文 (Chinese)")
        self._lang_en = QRadioButton("英文 (English)")
        self._lang_group.addButton(self._lang_zh)
        self._lang_group.addButton(self._lang_en)
        layout.addWidget(self._lang_zh)
        layout.addWidget(self._lang_en)

        theme_hint = QLabel(_SETUP_LABELS["theme"])
        theme_hint.setObjectName("guideSubTitle")
        layout.addWidget(theme_hint)

        # 主题选项单独成组，与语言组互不干扰（否则四个单选会互斥只能选一个）
        self._theme_group = QButtonGroup(self)
        self._theme_group.setExclusive(True)
        self._theme_light = QRadioButton(_SETUP_LABELS["light"])
        self._theme_dark = QRadioButton(_SETUP_LABELS["dark"])
        self._theme_group.addButton(self._theme_light)
        self._theme_group.addButton(self._theme_dark)
        layout.addWidget(self._theme_light)
        layout.addWidget(self._theme_dark)

        layout.addStretch(1)

        # 初始勾选（连接信号前设置，避免触发回调）
        self._lang_zh.setChecked(current_language() != "en_US")
        self._lang_en.setChecked(current_language() == "en_US")
        self._theme_light.setChecked(current_theme() != "dark")
        self._theme_dark.setChecked(current_theme() == "dark")

        self._lang_zh.toggled.connect(lambda c: self._on_lang_pick("zh_CN", c))
        self._lang_en.toggled.connect(lambda c: self._on_lang_pick("en_US", c))
        self._theme_light.toggled.connect(lambda c: self._on_theme_pick("light", c))
        self._theme_dark.toggled.connect(lambda c: self._on_theme_pick("dark", c))

    # ---------------------------------------------------------- exercise UI
    def _build_exercise_ui(self, root):
        """构建“动手试试”互动练习区（不再包含多选题）。"""
        self._exercise_box = QWidget()
        self._exercise_box.setObjectName("guideExercise")
        box = QVBoxLayout(self._exercise_box)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(6)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        box.addWidget(sep)

        self._exercise_hint = QLabel("")
        self._exercise_hint.setObjectName("guideExerciseHint")
        self._exercise_hint.setWordWrap(True)
        box.addWidget(self._exercise_hint)

        self._exercise_input = QLineEdit()
        self._exercise_input.setObjectName("guideExerciseInput")
        self._exercise_input.setPlaceholderText("x**2+2*x+1")
        self._exercise_input.returnPressed.connect(self._on_exercise_check)
        box.addWidget(self._exercise_input)

        ex_btns = QHBoxLayout()
        ex_btns.setSpacing(6)
        self._btn_ex_check = QPushButton("")
        self._btn_ex_check.clicked.connect(self._on_exercise_check)
        ex_btns.addWidget(self._btn_ex_check)
        ex_btns.addStretch(1)
        box.addLayout(ex_btns)

        self._exercise_feedback = QLabel("")
        self._exercise_feedback.setObjectName("guideExerciseFeedback")
        self._exercise_feedback.setWordWrap(True)
        box.addWidget(self._exercise_feedback)

        root.addWidget(self._exercise_box)

    # ---------------------------------------------------------- lang/theme
    def _on_lang_pick(self, lang, checked):
        """语言选择即时应用：仅当选中（checked=True）且与当前不同才处理。"""
        if not checked:
            return
        if lang == (current_language() or "zh_CN"):
            return
        if callable(self._apply_lang):
            self._apply_lang(lang)
        # 重新渲染当前步骤：标题/正文/进度/按钮均按新语言刷新
        self._show_step(self._idx)

    def _on_theme_pick(self, theme, checked):
        """主题选择即时应用。"""
        if not checked:
            return
        if theme == current_theme():
            return
        if callable(self._apply_theme_cb):
            self._apply_theme_cb(theme)
        self._apply_theme()

    # -------------------------------------------------------------- theme
    def _apply_theme(self):
        dark = current_theme() == "dark"
        if dark:
            self._body.setStyleSheet(
                "QTextBrowser { background-color: #202020; color: #e6e6e6; border: none; }")
            self._title.setStyleSheet("color: #e6e6e6;")
            self._progress.setStyleSheet(
                "QProgressBar { color: #e6e6e6; background-color: #2c2c2c; "
                "border: 1px solid #444; border-radius: 4px; text-align: center; }"
                "QProgressBar::chunk { background-color: #8c52dc; border-radius: 3px; }")
            self._exercise_hint.setStyleSheet("color: #e6e6e6; font-weight: bold;")
        else:
            self._body.setStyleSheet(
                "QTextBrowser { background-color: #ffffff; color: #1a1a1a; border: none; }")
            self._title.setStyleSheet("color: #1a1a1a;")
            self._progress.setStyleSheet(
                "QProgressBar { color: #1a1a1a; background-color: #e8e8e8; "
                "border: 1px solid #c8c8c8; border-radius: 4px; text-align: center; }"
                "QProgressBar::chunk { background-color: #0078d4; border-radius: 3px; }")
            self._exercise_hint.setStyleSheet("color: #1a1a1a; font-weight: bold;")

    def _style_html(self, body_html):
        dark = current_theme() == "dark"
        accent = "#8c52dc" if dark else "#0078d4"
        code_bg = "#3a3a3a" if dark else "#f0f0f0"
        code_fg = "#e6e6e6" if dark else "#1a1a1a"
        return (
            "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>"
            "body { font-family: 'Microsoft YaHei', 'SimSun', sans-serif; "
            "font-size: 14px; line-height: 1.8; margin: 4px 8px; }"
            "h3 { font-size: 15px; margin: 14px 0 6px; "
            "border-left: 4px solid %s; padding-left: 8px; }"
            "p { margin: 6px 0; }"
            "ul, ol { margin: 6px 0; padding-left: 26px; }"
            "li { margin-bottom: 4px; }"
            "code { background-color: %s; color: %s; padding: 1px 6px; "
            "border-radius: 3px; font-family: Consolas, 'Courier New', monospace; "
            "font-size: 13px; }"
            "</style></head><body>%s</body></html>"
        ) % (accent, code_bg, code_fg, body_html)

    # -------------------------------------------------------------- steps
    def _show_step(self, idx):
        self._idx = idx
        total = len(self._steps) + 1  # 含第 1 步设置页
        self.setWindowTitle(_guide_text({
            "zh": "初始化引导",
            "en": "Getting Started",
        }))

        if idx == 0:
            self._setup_page.show()
            self._body.hide()
            self._title.setText(_guide_text(_SETTINGS_STEP_TITLE))
            self._exercise_box.hide()
        else:
            self._setup_page.hide()
            self._body.show()
            step = self._steps[idx - 1]
            self._title.setText(_guide_text(step["title"]))
            self._body.setHtml(self._style_html(_guide_text(step["html"])))
            self._body.verticalScrollBar().setValue(0)
            self._render_exercise(idx - 1)

        # 进度条（%v = 当前值，%m = 最大值）
        self._progress.setRange(0, total)
        self._progress.setValue(idx + 1)
        self._progress.setFormat(_guide_text({
            "zh": "第 %v / %m 步",
            "en": "Step %v / %m",
        }))

        # 按钮文案随语言刷新（切换语言后即时更新）
        self._btn_skip.setText(_guide_text({"zh": "跳过引导", "en": "Skip"}))
        self._btn_back.setText(_guide_text({"zh": "上一步", "en": "Back"}))
        self._btn_next.setText(_guide_text({"zh": "下一步", "en": "Next"}))
        self._btn_finish.setText(_guide_text({"zh": "完成", "en": "Finish"}))

        self._btn_back.setEnabled(idx > 0)
        last = idx == total - 1
        self._btn_next.setVisible(not last)
        self._btn_finish.setVisible(last)
        self._btn_next.setEnabled(True)

    # --------------------------------------------------------- exercise
    def _render_exercise(self, content_idx):
        """渲染当前内容步骤的“动手试试”练习，或隐藏练习区。"""
        ex = _GUIDE_EXERCISES.get(content_idx)
        if not ex:
            self._exercise_box.hide()
            return
        self._exercise_box.show()
        self._exercise_hint.setText(_guide_text(ex))
        self._exercise_input.clear()
        self._exercise_feedback.setText("")
        self._btn_ex_check.setText(_guide_text({"zh": "检查", "en": "Check"}))

    def _on_exercise_check(self):
        """检查“动手试试”中输入的 SymPy 表达式是否合法。"""
        text = self._exercise_input.text().strip()
        if not text:
            self._exercise_feedback.setText(_guide_text({
                "zh": "请先输入一个表达式。",
                "en": "Please type an expression first.",
            }))
            self._set_exercise_feedback("err")
            return
        try:
            sympify(text)
            self._exercise_feedback.setText(_guide_text({
                "zh": "✓ 表达式合法！",
                "en": "✓ Valid expression!",
            }))
            self._set_exercise_feedback("ok")
        except SympifyError:
            self._exercise_feedback.setText(_guide_text({
                "zh": "✗ 表达式无法解析，请检查语法（例如用 x**2 而非 x^2）。",
                "en": "✗ Could not parse. Check the syntax (e.g. x**2, not x^2).",
            }))
            self._set_exercise_feedback("err")

    def _set_exercise_feedback(self, kind):
        dark = current_theme() == "dark"
        if kind == "ok":
            self._exercise_feedback.setStyleSheet(
                "QLabel { color: %s; font-weight: bold; }"
                % ("#a0dda0" if dark else "#0a7d33"))
        elif kind == "err":
            self._exercise_feedback.setStyleSheet(
                "QLabel { color: %s; font-weight: bold; }"
                % ("#ff9d9d" if dark else "#c00000"))

    def _on_back(self):
        if self._idx > 0:
            self._show_step(self._idx - 1)

    def _on_next(self):
        if self._idx < len(self._steps):  # 最大索引 = len(steps)（设置页+内容页）
            self._show_step(self._idx + 1)

    def _finish(self):
        save_initialized(True)
        self.accept()

    def _on_finish(self):
        self._finish()

    def _on_skip(self):
        self._finish()

    def keyPressEvent(self, event):
        """方向键快速切换：← 上一步，→ 下一步（仅当对应按钮可用）。"""
        if event.key() == Qt.Key_Right and self._btn_next.isEnabled():
            self._on_next()
            event.accept()
            return
        if event.key() == Qt.Key_Left and self._btn_back.isEnabled():
            self._on_back()
            event.accept()
            return
        super(GuideDialog, self).keyPressEvent(event)

    def open_help(self):
        """由外部按钮触发打开帮助页（供菜单“关于 → 引导”复用）。"""
        if callable(self._open_help):
            self._open_help()
