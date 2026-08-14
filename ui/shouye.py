import webbrowser

from ui.ui_shouye import Ui_shouye
from PySide6.QtCore import QFile, QIODevice, QObject, Slot
from PySide6.QtWidgets import QWidget
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineScript
from core.settings import current_theme, current_language

# 首页背景渐变（对角线，左上→右下），与 qlineargradient(x1:0,y1:0,x2:1,y2:1) 一致。
# 浅色模式：蓝→白；深色模式：深紫→黑。
_HOME_GRADIENT = {
    'light': 'linear-gradient(to bottom right, rgba(0, 120, 240, 1), rgba(255, 255, 255, 1))',
    'dark': 'linear-gradient(to bottom right, rgba(140, 82, 220, 1), rgba(0, 0, 0, 1))',
}

# 各主题下的样式参数（卡片背景/边框/图标/强调色等）
_HOME_STYLE = {
    'light': {
        'text': '#000000',
        'badge_bg': 'rgba(0, 90, 160, 0.08)',
        'card_bg': 'rgba(255, 255, 255, 0.62)',
        'border': 'rgba(0, 90, 160, 0.28)',
        'icon_bg': 'rgba(0, 120, 240, 0.12)',
        'icon_color': '#005a9e',
        'tag_bg': 'rgba(0, 120, 240, 0.10)',
        'accent': '#0078d4',
    },
    'dark': {
        'text': '#d9c9f2',
        'badge_bg': 'rgba(217, 201, 242, 0.14)',
        'card_bg': 'rgba(16, 12, 32, 0.45)',
        'border': 'rgba(217, 201, 242, 0.35)',
        'icon_bg': 'rgba(217, 201, 242, 0.16)',
        'icon_color': '#e6d9f8',
        'tag_bg': 'rgba(217, 201, 242, 0.16)',
        'accent': '#b48df0',
    },
}

# 功能卡片：(标签页索引, 图标符号, 标题, 描述, 分类)
# 索引与 ui/__init__.py 的 tabs_dict 对应，点击后通过主窗口 create_tab(index) 打开
_CARDS = {
    'zh_CN': [
        (2,  'ƒ′', '求导',   '导数、隐函数与高阶导数',       '微积分'),
        (3,  '∫',  '积分',   '定积分与不定积分',             '微积分'),
        (4,  '≡',  '代数变形', '化简、展开、换元代入',         '代数'),
        (5,  'x²', '方程',   '方程与不等式求解',             '代数'),
        (6,  '{',  '方程组', '线性与非线性方程组',           '代数'),
        (7,  '<',  '不等式', '不等式及其组求解',             '代数'),
        (1,  'f(x)', '定义函数', '自定义函数表达式',         '代数'),
        (12, '∿',  '函数绘图', '函数图像与性质分析',         '可视化'),
        (13, '∠',  '解三角形', '正弦、余弦与三角形求解',     '几何'),
        (14, '△',  '平面几何', '点、线、圆与平面图形',       '几何'),
        (16, '◆',  '立体几何', '三维点线面与空间向量',       '几何'),
        (22, '▣',  '积木模式', '积木式可视化编程',           '可视化'),
    ],
    'en_US': [
        (2,  'ƒ′', 'Derivative',     'Derivatives & implicit functions',  'Calculus'),
        (3,  '∫',  'Integral',       'Definite & indefinite integrals',    'Calculus'),
        (4,  '≡',  'Simplify',       'Simplify, expand & substitute',      'Algebra'),
        (5,  'x²', 'Equation',       'Equations & inequalities',           'Algebra'),
        (6,  '{',  'System',         'Linear & nonlinear systems',         'Algebra'),
        (7,  '<',  'Inequality',     'Inequalities & their systems',       'Algebra'),
        (1,  'f(x)', 'Define',       'Define your own functions',          'Algebra'),
        (12, '∿',  'Plot',           'Function graphs & analysis',         'Visual'),
        (13, '∠',  'Triangle',       'Sine, cosine & triangle solving',    'Geometry'),
        (14, '△',  'Plane Geometry', 'Points, lines, circles & shapes',    'Geometry'),
        (16, '◆',  'Solid Geometry', '3D points, lines, planes & vectors', 'Geometry'),
        (22, '▣',  'Blockly',        'Visual block programming',           'Visual'),
    ],
}

# 页面文案（含顶部导航链接、特性亮点、底部信息）
_TEXTS = {
    'zh_CN': {
        'badge': '微积分计算器 · v2.0.0',
        'subtitle': '求导 · 积分 · 方程 · 几何 · 绘图 —— 一站式科学计算工具',
        'intro': '开源的微积分与几何计算工具：求导、积分、方程、不等式、函数绘图与几何计算一应俱全，'
                 '并支持 LaTeX 可视化输入、积木式编程与双语界面。',
        'features': [
            ('可视化输入', 'LaTeX 公式编辑器 · 表达式缓存区'),
            ('全模块覆盖', '微积分 · 代数 · 几何 · 绘图'),
            ('双语界面',   '中文 / English 一键切换'),
            ('明暗主题',   '浅色 / 深色自由切换'),
        ],
        'ext_links': [('Github', 'https://github.com/limingkang12345/CalculusCalculator'),
                      ('网页版', 'https://limingkang.pythonanywhere.com')],
        'top_links': [('帮助', 10), ('设置', 20), ('缓存区', 21)],
        'footer': 'Author: Li Mingkang · Contributor: CuberAHZ · v2.0.0',
    },
    'en_US': {
        'badge': 'Calculus Calculator · v2.0.0',
        'subtitle': 'Derivative · Integral · Equation · Geometry · Plot — one-stop scientific tool',
        'intro': 'An open-source calculus & geometry toolkit — derivatives, integrals, equations, '
                 'inequalities, plotting and geometry, with LaTeX visual input, block programming '
                 'and a bilingual UI.',
        'features': [
            ('Visual input',   'LaTeX editor · expression cache'),
            ('All modules',    'Calculus · Algebra · Geometry · Plot'),
            ('Bilingual UI',   '中文 / English one-click switch'),
            ('Light & dark',   'Switchable color themes'),
        ],
        'ext_links': [('GitHub', 'https://github.com/limingkang12345/CalculusCalculator'),
                      ('Web', 'https://limingkang.pythonanywhere.com')],
        'top_links': [('Help', 10), ('Settings', 20), ('Cache', 21)],
        'footer': 'Author: Li Mingkang · Contributor: CuberAHZ · v2.0.0',
    },
}

# 首页 HTML 模板；占位符在渲染时替换（__TEXT__ 等避免与 CSS 花括号冲突）
# 布局：顶部导航条 + 中部（Hero + 功能卡片 + 特性亮点）+ 底部信息，用 flex 撑满整屏。
_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>首页</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; }
        body {
            background: __GRADIENT__;
            background-attachment: fixed;
            font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
            color: __TEXT__;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            overflow: hidden;
        }
        /* 顶部导航条：左外部链接，右功能快捷链接 */
        .topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 30px;
            flex: none;
        }
        .topbar nav a {
            color: inherit;
            text-decoration: none;
            font-size: 11pt;
            opacity: .85;
            border-bottom: 1px dashed currentColor;
            padding-bottom: 1px;
        }
        .topbar nav a:hover { opacity: 1; }
        .topbar nav.left a { margin-right: 20px; }
        .topbar nav.right a { margin-left: 20px; }
        /* 中部内容区：垂直铺满 */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 6px 30px;
            overflow-y: auto;
        }
        .hero { text-align: center; margin-bottom: 20px; }
        .badge {
            display: inline-block; padding: 5px 18px; border-radius: 999px;
            font-size: 12.5px; letter-spacing: 2px; margin-bottom: 12px;
            background: __BADGE_BG__; border: 1px solid __BORDER__;
        }
        .title {
            font-family: 'Times New Roman', 'SimSun', serif;
            font-size: 58pt; font-weight: 800; letter-spacing: 1px; line-height: 1.15;
        }
        .subtitle { font-size: 13.5pt; margin-top: 8px; opacity: .88; }
        .intro {
            max-width: 780px;
            margin: 12px auto 0;
            font-size: 11pt;
            line-height: 1.7;
            opacity: .78;
        }
        /* 功能卡片 */
        .grid {
            width: 100%;
            max-width: 1180px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(232px, 1fr));
            gap: 12px;
        }
        .card {
            display: flex; align-items: center; gap: 13px; padding: 14px 16px;
            background: __CARD_BG__; border: 1px solid __BORDER__; border-radius: 14px;
            text-decoration: none; color: inherit;
            transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 26px rgba(0, 0, 0, .18);
            border-color: __ACCENT__;
        }
        .icon {
            flex: none; width: 50px; height: 50px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Times New Roman', serif; font-size: 21pt;
            background: __ICON_BG__; color: __ICON_COLOR__;
        }
        .c-title { font-size: 13.5pt; font-weight: 700; }
        .c-desc { font-size: 10pt; opacity: .75; margin-top: 3px; }
        .c-tag {
            display: inline-block; margin-top: 5px; padding: 1px 8px; border-radius: 999px;
            font-size: 8.5pt; background: __TAG_BG__;
        }
        /* 特性亮点 */
        .features {
            width: 100%;
            max-width: 1180px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-top: 18px;
        }
        .feat {
            background: __CARD_BG__; border: 1px solid __BORDER__; border-radius: 12px;
            padding: 12px 16px; text-align: center;
        }
        .feat .f-t { font-size: 11.5pt; font-weight: 700; }
        .feat .f-d { font-size: 9.5pt; opacity: .72; margin-top: 3px; }
        /* 底部信息 */
        footer {
            flex: none;
            padding: 10px 30px 14px;
            font-size: 10.5pt;
            opacity: .85;
            text-align: center;
        }
    </style>
</head>
<body>
    <header class="topbar">
        <nav class="left">__EXT_LINKS__</nav>
        <nav class="right">__TOP_LINKS__</nav>
    </header>
    <main>
        <div class="hero">
            <div class="badge">__BADGE__</div>
            <h1 class="title">CalculusCalculator</h1>
            <div class="subtitle">__SUBTITLE__</div>
            <div class="intro">__INTRO__</div>
        </div>
        <div class="grid">
__CARDS__
        </div>
        <div class="features">
__FEATURES__
        </div>
    </main>
    <footer>__FOOTER__</footer>
</body>
</html>"""


class _HomePage(QWebEnginePage):
    """首页专用页面：外部链接交给系统浏览器，避免首页被导航走。

    功能卡片/快捷链接的跳转通过 QWebChannel 桥（_HomeBridge）完成，
    tab:// 分支仅作为 JS 桥不可用时的兜底。
    """

    def __init__(self, on_open_tab, parent=None):
        super().__init__(parent)
        self._on_open_tab = on_open_tab

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        if is_main_frame and url.scheme() == "tab":
            try:
                idx = int(url.host())
            except (TypeError, ValueError):
                idx = -1
            if idx >= 0 and self._on_open_tab is not None:
                self._on_open_tab(idx)
            return False
        if is_main_frame and url.scheme() in ("http", "https"):
            # Github / 网页版等外部链接：交给系统浏览器，避免首页被导航走
            webbrowser.open(url.toString())
            return False
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)


class _HomeBridge(QObject):
    """QWebChannel 桥：供首页 JS 调用，直接触发主窗口 create_tab。"""

    def __init__(self, on_open_tab, parent=None):
        super().__init__(parent)
        self._on_open_tab = on_open_tab

    @Slot(int)
    def open_tab(self, index):
        if self._on_open_tab is not None:
            self._on_open_tab(index)


class Shouye(QWidget, Ui_shouye):
    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)
        self._main = parent
        self._lang = current_language()
        # 用自定义页面拦截外部链接；通过 QWebChannel 桥让 JS 直接创建标签页
        page = _HomePage(self._open_tab, self)
        self.webEngineView.setPage(page)
        self._bridge = _HomeBridge(self._open_tab, self)
        self._channel = QWebChannel(page)
        self._channel.registerObject("home", self._bridge)
        page.setWebChannel(self._channel)
        page.scripts().insert(self._make_bridge_script())
        self._apply_home_theme(current_theme())

    @staticmethod
    def _make_bridge_script():
        """构造注入脚本：加载 qwebchannel.js 并把 home 桥暴露为 window.homeBridge。"""
        script = QWebEngineScript()
        script.setName("home_qwebchannel")
        # Qt 6.8 起不再区分注入框架（默认注入顶层框架），子框架一并注入
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        qjs = ""
        f = QFile(":/qtwebchannel/qwebchannel.js")
        if f.open(QIODevice.ReadOnly):
            qjs = bytes(f.readAll()).decode("utf-8", "ignore")
        script.setSourceCode(qjs + "\nnew QWebChannel(qt.webChannelTransport, function (channel) {\n"
                                   "    window.homeBridge = channel.objects.home;\n"
                                   "});")
        return script

    def _open_tab(self, index):
        """首页卡片被点击时，在主窗口打开对应功能标签页。"""
        try:
            self._main.create_tab(index)
        except Exception:
            pass

    def _apply_home_theme(self, theme):
        """按主题与当前语言渲染首页 HTML。"""
        grad = _HOME_GRADIENT.get(theme, _HOME_GRADIENT['light'])
        st = _HOME_STYLE.get(theme, _HOME_STYLE['light'])
        tx = _TEXTS.get(self._lang, _TEXTS['zh_CN'])
        cards = _CARDS.get(self._lang, _CARDS['zh_CN'])

        cards_html = '\n'.join(
            '            <a class="card" href="#" '
            'onclick="if (window.homeBridge) {{ homeBridge.open_tab({}); }} return false;" '
            'title="{}">\n'
            '                <div class="icon">{}</div>\n'
            '                <div class="c-body">\n'
            '                    <div class="c-title">{}</div>\n'
            '                    <div class="c-desc">{}</div>\n'
            '                    <span class="c-tag">{}</span>\n'
            '                </div>\n'
            '            </a>'.format(idx, desc, sym, title, desc, tag)
            for (idx, sym, title, desc, tag) in cards
        )
        features_html = '\n'.join(
            '            <div class="feat">\n'
            '                <div class="f-t">{}</div>\n'
            '                <div class="f-d">{}</div>\n'
            '            </div>'.format(ft, fd)
            for ft, fd in tx['features']
        )
        top_links_html = ''.join(
            '<a href="#" onclick="if (window.homeBridge) {{ homeBridge.open_tab({}); }} return false;">{}</a>'.format(i, t)
            for t, i in tx['top_links']
        )
        ext_links_html = ''.join(
            '<a href="{}">{}</a>'.format(url, t) for t, url in tx['ext_links']
        )

        html = _HTML_TEMPLATE
        for key, value in {
            '__GRADIENT__': grad,
            '__TEXT__': st['text'],
            '__BADGE_BG__': st['badge_bg'],
            '__CARD_BG__': st['card_bg'],
            '__BORDER__': st['border'],
            '__ICON_BG__': st['icon_bg'],
            '__ICON_COLOR__': st['icon_color'],
            '__TAG_BG__': st['tag_bg'],
            '__ACCENT__': st['accent'],
            '__BADGE__': tx['badge'],
            '__SUBTITLE__': tx['subtitle'],
            '__INTRO__': tx['intro'],
            '__FOOTER__': tx['footer'],
            '__TOP_LINKS__': top_links_html,
            '__EXT_LINKS__': ext_links_html,
            '__CARDS__': cards_html,
            '__FEATURES__': features_html,
        }.items():
            html = html.replace(key, value)
        self.webEngineView.setHtml(html)

    def set_theme(self, theme):
        """主题切换时由主窗体调用，刷新首页背景与配色。"""
        self._apply_home_theme(theme)

    def set_language(self, lang):
        """语言切换时由主窗体调用，重新渲染首页文案。"""
        self._lang = lang or 'zh_CN'
        self._apply_home_theme(current_theme())
