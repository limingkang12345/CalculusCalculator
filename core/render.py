import matplotlib
matplotlib.use('Agg')  # 非交互式后端，避免首次渲染时与 PySide6 冲突导致闪退

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import QByteArray, Qt
from io import BytesIO
import matplotlib.pyplot as plt
from sympy import latex

# 缓存每个 QGraphicsView 的渲染参数及必需对象，用于主题切换后刷新
# value: (func_name, latex_str, QSvgRenderer)
# QSvgRenderer 必须缓存以保持其存活 —— QGraphicsSvgItem 仅持有非拥有指针
_svg_cache = {}

# 支持中文显示的字体列表（按优先级），普通文本（非数学模式）使用这些字体，
# 避免中文在 SVG 中渲染为方块（tofu）
_CJK_FONT_LIST = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi',
                  'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']

# 匹配 CJK 统一表意文字、CJK 标点与全角字符
import re
_CJK_RE = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')


def _split_cjk(s):
    """将字符串按 CJK / 非 CJK 切分为片段。

    返回片段列表，每段为 (text, is_cjk)。
    """
    segs = []
    i, n = 0, len(s)
    while i < n:
        cjk = bool(_CJK_RE.match(s[i]))
        j = i
        while j < n and bool(_CJK_RE.match(s[j])) == cjk:
            j += 1
        segs.append((s[i:j], cjk))
        i = j
    return segs


def _to_render_text(n, l):
    """构造 matplotlib 文本字符串。

    - 含中文的片段以普通文本渲染（使用 CJK 字体）
    - 其余片段置于 $...$ 数学模式（使用 mathtext 字体）
    这样中文可正常显示，而 LaTeX 表达式仍按数学公式排版。
    """
    raw = (n or '') + (l or '')
    if not raw:
        return ''
    if not _CJK_RE.search(raw):
        return f'${raw}$'
    parts = []
    for text, cjk in _split_cjk(raw):
        if cjk:
            parts.append(text)          # 中文：普通文本
        else:
            if text.strip():
                parts.append(f'${text}$')  # 非中文：数学模式
            else:
                parts.append(text)      # 仅空白，原样保留
    return ''.join(parts)


def setGraphicsView(n, l, g):
    """渲染 LaTeX 表达式到指定的 QGraphicsView。

    参数:
        n: 函数名/前缀
        l: LaTeX 表达式字符串
        g: 目标 QGraphicsView
    """
    # 确定当前主题颜色
    text_color = "black"
    bg_color = "white"
    p = g.parentWidget()
    while p is not None:
        if hasattr(p, 'theme'):
            if p.theme == "dark":
                text_color = "white"
                bg_color = "black"
            break
        p = p.parentWidget()

    # 用 Matplotlib 渲染 LaTeX → SVG
    # 将 rcParams 变更限定在本函数内（rc_context），避免 font.size 等全局设置
    # 泄漏到绘图模块（huitu_*），导致坐标轴字号被放大
    # 中文片段以普通文本渲染（CJK 字体），其余以数学模式渲染
    render_text = _to_render_text(n, l)
    rc = {
        'text.usetex': False,
        'mathtext.fontset': 'cm',
        'font.family': 'sans-serif',
        'font.sans-serif': _CJK_FONT_LIST,
        'axes.unicode_minus': False,
        'text.color': text_color,
    }
    with plt.rc_context(rc):
        fig, ax = plt.subplots()
        txt = ax.text(0.5, 0.5, render_text,
                      ha='center', va='center', color=text_color,
                      fontsize=48)
        ax.axis('off')
        fig.canvas.draw()

        bbox = txt.get_window_extent(renderer=fig.canvas.get_renderer())
        fig.set_size_inches(bbox.width / fig.dpi, bbox.height / fig.dpi)

    buf = BytesIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0.05,
                transparent=True, facecolor=bg_color, edgecolor='none')
    buf.seek(0)
    svg_data = buf.getvalue().decode('utf-8')
    plt.close(fig)

    # 清理旧场景，避免泄漏
    old_scene = g.scene()
    if old_scene is not None:
        old_scene.clear()

    scene = QGraphicsScene()
    renderer = QSvgRenderer()
    renderer.load(QByteArray(svg_data.encode('utf-8')))

    svg_item = QGraphicsSvgItem()
    svg_item.setSharedRenderer(renderer)
    if renderer.isValid():
        svg_item.setElementId('')
    scene.addItem(svg_item)

    g.setRenderHint(QPainter.Antialiasing)
    g.setDragMode(QGraphicsView.ScrollHandDrag)
    g.setScene(scene)

    if renderer.isValid():
        # 以 SVG 自然尺寸显示，超出视口时自动显示滑动条
        g.resetTransform()
        scene.setSceneRect(renderer.viewBoxF())

    # 缓存渲染参数，同时保持 renderer 存活
    # （QGraphicsSvgItem::setSharedRenderer 不获取所有权，renderer 必须由外部持有）
    _svg_cache[g] = (n, l, renderer)


def refreshGraphicsView():
    """主题切换后刷新所有已缓存的图形视图内容"""
    for w, (n, l, _) in list(_svg_cache.items()):
        try:
            setGraphicsView(n, l, w)
        except Exception:
            pass


def setGraphicsViewTheme(main_class, parent_class):
    """设置 GraphicsView 的主题背景色"""
    for view in main_class.findChildren(QGraphicsView):
        if view.scene() is not None:
            view.scene().setBackgroundBrush(
                QColor(32, 33, 36) if parent_class.theme == "dark"
                else QColor(255, 255, 255))
