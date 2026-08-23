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
import os
os.environ['MPLBACKEND'] = 'Agg'   # 强制使用 Agg 后端，避免动态加载其他后端

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
    bg_color = "#F8F9FA"
    p = g.parentWidget()
    while p is not None:
        if hasattr(p, 'theme'):
            if p.theme == "dark":
                text_color = "white"
                bg_color = "#202124"
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
        'font.family': 'Microsoft YaHei',
        'axes.unicode_minus': False,
        'text.color': text_color,
        'svg.fonttype': 'path',
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


def clearGraphicsView(g):
    """清空指定的 QGraphicsView 并移除其渲染缓存。

    QGraphicsView 没有 setHtml 方法，清空渲染结果应新建一个空场景，
    避免调用 setHtml 抛出 AttributeError。
    """
    old_scene = g.scene()
    if old_scene is not None:
        old_scene.clear()
    g.setScene(QGraphicsScene())
    _svg_cache.pop(g, None)


def applyPlotTheme(fig, ax, theme='light'):
    """将 matplotlib Figure/Axes 适配为浅色 / 深色主题配色。

    参数:
        fig: matplotlib.figure.Figure
        ax: matplotlib Axes（2D 或 3D）
        theme: 'light' 或 'dark'
    返回:
        (bg, fg, grid_color, axis_color)，供调用方继续设置网格、坐标轴线等。
    """
    dark = theme == 'dark'
    if dark:
        bg, fg, grid_c, axis_c = '#202124', '#e8eaed', '#5f6368', '#9aa0a6'
    else:
        bg, fg, grid_c, axis_c = 'white', 'black', '#cccccc', 'black'

    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.tick_params(colors=fg)
    try:
        for spine in ax.spines.values():
            spine.set_color(axis_c)
    except Exception:
        # 3D 轴没有 spines，改为设置三个坐标轴面板的颜色
        for aname in ('xaxis', 'yaxis', 'zaxis'):
            axi = getattr(ax, aname, None)
            if axi is not None:
                try:
                    axi.pane.set_facecolor(bg)
                    axi.pane.set_edgecolor(axis_c)
                except Exception:
                    pass
    return bg, fg, grid_c, axis_c


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


def _wheel_zoom_handler(canvas):
    """构造 2D 滚轮缩放事件处理函数（围绕鼠标所在位置缩放）。

    3D 轴跳过：mpl 的 Axes3D 已自带旋转/缩放/平移交互。
    """
    from mpl_toolkits.mplot3d import Axes3D

    def on_scroll(event):
        if event.inaxes is None or event.button not in ("up", "down"):
            return
        ax = event.inaxes
        if isinstance(ax, Axes3D):
            return
        xdata, ydata = event.xdata, event.ydata
        if xdata is None or ydata is None:
            return
        scale = 1.3 if event.button == "up" else 1 / 1.3
        xlim, ylim = ax.get_xlim(), ax.get_ylim()
        ax.set_xlim(xdata - (xdata - xlim[0]) * scale,
                    xdata + (xlim[1] - xdata) * scale)
        ax.set_ylim(ydata - (ydata - ylim[0]) * scale,
                    ydata + (ylim[1] - ydata) * scale)
        canvas.draw_idle()

    return on_scroll


def attach_plot_toolbar(layout, canvas, parent, wheel_zoom=False):
    """为嵌入的 matplotlib 画布添加原生导航工具栏，并可选启用滚轮缩放。

    工具栏提供与原生 matplotlib 窗口一致的交互：
    Home（复位）、后退/前进、平移、缩放框、子图配置、保存图片。

    参数:
        layout: 目标 QVBoxLayout（工具栏插入到画布上方）
        canvas: FigureCanvasQTAgg 实例
        parent: 工具栏的父控件（通常为所在页面）
        wheel_zoom: 是否启用 2D 滚轮缩放（围绕鼠标位置）
    返回:
        NavigationToolbar2QT 实例（调用方需持有引用并在重建时清理）
    """
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
    toolbar = NavigationToolbar2QT(canvas, parent)
    layout.addWidget(toolbar)
    if wheel_zoom:
        canvas.mpl_connect("scroll_event", _wheel_zoom_handler(canvas))
    return toolbar
