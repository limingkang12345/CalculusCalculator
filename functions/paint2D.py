"""平面几何绘图模块
输入：由 sympy Point, Line, Circle, Triangle, Polygon, Segment, Ray 等对象
      构成的列表，每项为 (对象, 可选样式字典)
输出：matplotlib.figure.Figure 对象，可直接嵌入 QWebEngineView
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle as MplCircle, Arc as MplArc
from sympy import (
    Point, Line, Circle, Triangle, Polygon, Segment, Ray,
    Symbol, pi, sqrt, N,
)


# ============================================================
# 默认样式
# ============================================================

_DEFAULT_STYLE = {
    Point:     {'marker': 'o', 'color': '#1f77b4', 'markersize': 6, 'linestyle': 'none'},
    Line:      {'color': '#d62728', 'linewidth': 1.5},
    Segment:   {'color': '#2ca02c', 'linewidth': 2.0},
    Ray:       {'color': '#9467bd', 'linewidth': 1.5},
    Circle:    {'edgecolor': '#ff7f0e', 'facecolor': 'none', 'linewidth': 1.5},
    Triangle:  {'color': '#1f77b4', 'linewidth': 1.5, 'marker': 'o', 'markersize': 4},
    Polygon:   {'color': '#1f77b4', 'linewidth': 1.5, 'marker': 'o', 'markersize': 4},
}


def _merge_style(obj, user_style=None):
    """合并默认样式与用户自定义样式（通过 isinstance 查找，兼容子类）"""
    base = {}
    for cls, sty in _DEFAULT_STYLE.items():
        if isinstance(obj, cls):
            base.update(sty)
    if user_style:
        base.update(user_style)
    return base


def _to_float(val):
    """安全转换为 float"""
    try:
        return float(N(val))
    except Exception:
        return float(val)


def _line_x_at_y(line, y_val):
    """求直线上给定 y 对应的 x（用于垂直/水平线）"""
    eq = line.equation()
    # eq 是 Ax + By + C = 0 的形式
    from sympy import solve, Eq
    x_sym = Symbol('x')
    sol = solve(eq.subs(Symbol('y'), y_val), x_sym)
    return float(N(sol[0])) if sol else None


def _line_y_at_x(line, x_val):
    """求直线上给定 x 对应的 y"""
    eq = line.equation()
    from sympy import solve
    y_sym = Symbol('y')
    sol = solve(eq.subs(Symbol('x'), x_val), y_sym)
    return float(N(sol[0])) if sol else None


def _get_line_extents(line, xlim, ylim):
    """获取无限直线在视口范围内的两个端点"""
    x1, x2 = xlim
    y1, y2 = ylim
    eq = line.equation()
    # 从方程中提取实际的 Symbol 对象（避免 Symbol('x') 与 abc.x 不匹配）
    free_syms = list(eq.free_symbols)
    x_sym = next((s for s in free_syms if s.name == 'x'), Symbol('x'))
    y_sym = next((s for s in free_syms if s.name == 'y'), Symbol('y'))

    A = float(eq.coeff(x_sym, 1))
    B = float(eq.coeff(y_sym, 1))
    C = float(eq.subs({x_sym: 0, y_sym: 0}))
    
    # 垂直直线 B=0
    if abs(B) < 1e-12:
        x_val = -C / A if abs(A) > 1e-12 else 0
        return [(x_val, y1), (x_val, y2)]
    
    # 水平直线 A=0
    if abs(A) < 1e-12:
        y_val = -C / B if abs(B) > 1e-12 else 0
        return [(x1, y_val), (x2, y_val)]
    
    # 一般直线：计算与视口四边的交点
    pts = []
    # 与左边界 x=x1 的交点
    y_at_x1 = -(A * x1 + C) / B
    if y1 <= y_at_x1 <= y2:
        pts.append((x1, float(N(y_at_x1))))
    # 与右边界 x=x2 的交点
    y_at_x2 = -(A * x2 + C) / B
    if y1 <= y_at_x2 <= y2:
        pts.append((x2, float(N(y_at_x2))))
    # 与上边界 y=y2 的交点
    x_at_y2 = -(B * y2 + C) / A
    if x1 <= x_at_y2 <= x2:
        pts.append((float(N(x_at_y2)), y2))
    # 与下边界 y=y1 的交点
    x_at_y1 = -(B * y1 + C) / A
    if x1 <= x_at_y1 <= x2:
        pts.append((float(N(x_at_y1)), y1))
    
    if len(pts) >= 2:
        return pts[:2]
    return pts


# ============================================================
# 各类对象的绘图函数
# ============================================================

def _plot_point(ax, pt, style, label_text=None):
    """绘制点"""
    x, y = _to_float(pt.x), _to_float(pt.y)
    style = {k: v for k, v in style.items() if k in ('marker', 'color', 'markersize', 'markeredgecolor',
                                                      'markerfacecolor', 'linestyle', 'alpha', 'zorder')}
    ax.plot(x, y, **style)
    if label_text:
        ax.annotate(label_text, (x, y), xytext=(5, 5),
                    textcoords='offset points', fontsize=10)


def _plot_line(ax, line, style, xlim=None, ylim=None, label_text=None):
    """绘制无限直线"""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    pts = _get_line_extents(line, xlim, ylim)
    if len(pts) >= 2:
        xs, ys = zip(*pts[:2])
        style_plot = {k: v for k, v in style.items()
                      if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder', 'marker')}
        ax.plot(xs, ys, **style_plot, label=label_text)


def _plot_segment(ax, seg, style, label_text=None):
    """绘制线段"""
    p1, p2 = seg.points
    xs = [_to_float(p1.x), _to_float(p2.x)]
    ys = [_to_float(p1.y), _to_float(p2.y)]
    style_plot = {k: v for k, v in style.items()
                  if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder', 'marker')}
    ax.plot(xs, ys, **style_plot, label=label_text)


def _plot_ray(ax, ray, style, xlim=None, ylim=None, label_text=None):
    """绘制射线"""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    src = ray.source
    d = ray.direction
    sx, sy = _to_float(src.x), _to_float(src.y)
    
    # 沿方向延伸到视口外
    t_far = 1e6
    rx, ry = sx + t_far * _to_float(d.x), sy + t_far * _to_float(d.y)
    
    # 用线段方式画射线（起点到远处点）
    temp_line = Line(src, Point(sx + 1000 * _to_float(d.x), sy + 1000 * _to_float(d.y)))
    pts = _get_line_extents(temp_line, xlim, ylim)
    all_pts = [(sx, sy)]
    for px, py in pts:
        dx, dy = px - sx, py - sy
        if dx * _to_float(d.x) + dy * _to_float(d.y) > 0:
            all_pts.append((px, py))
    if len(all_pts) >= 2:
        xs, ys = zip(*all_pts)
        style_plot = {k: v for k, v in style.items()
                      if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder', 'marker')}
        ax.plot(xs, ys, **style_plot, label=label_text)


def _plot_circle(ax, circle, style, label_text=None):
    """绘制圆"""
    cx, cy = _to_float(circle.center.x), _to_float(circle.center.y)
    r = _to_float(circle.radius)
    patch_style = {k: v for k, v in style.items()
                   if k in ('edgecolor', 'facecolor', 'linewidth', 'linestyle', 'alpha', 'zorder')}
    patch = MplCircle((cx, cy), r, **patch_style)
    ax.add_patch(patch)
    if label_text:
        ax.annotate(label_text, (cx + r * 0.7, cy + r * 0.7),
                    fontsize=10)


def _plot_triangle(ax, tri, style, label_text=None):
    """绘制三角形（边+顶点标记+填充）"""
    verts = tri.vertices
    xs = [_to_float(v.x) for v in verts] + [_to_float(verts[0].x)]
    ys = [_to_float(v.y) for v in verts] + [_to_float(verts[0].y)]
    
    fill = style.pop('fill', None)
    style_plot = {k: v for k, v in style.items()
                  if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder', 'marker', 'markersize')}
    ax.plot(xs, ys, **style_plot, label=label_text)
    
    if fill:
        from matplotlib.patches import Polygon as MplPolygon
        verts_2d = [(_to_float(v.x), _to_float(v.y)) for v in verts]
        poly = MplPolygon(verts_2d, closed=True, **({} if fill is True else fill))
        ax.add_patch(poly)


def _plot_polygon(ax, poly, style, label_text=None):
    """绘制多边形"""
    verts = poly.vertices
    xs = [_to_float(v.x) for v in verts] + [_to_float(verts[0].x)]
    ys = [_to_float(v.y) for v in verts] + [_to_float(verts[0].y)]
    
    fill = style.pop('fill', None)
    style_plot = {k: v for k, v in style.items()
                  if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder', 'marker', 'markersize')}
    ax.plot(xs, ys, **style_plot, label=label_text)
    
    if fill:
        from matplotlib.patches import Polygon as MplPolygon
        verts_2d = [(_to_float(v.x), _to_float(v.y)) for v in verts]
        mpl_poly = MplPolygon(verts_2d, closed=True, **({} if fill is True else fill))
        ax.add_patch(mpl_poly)


# ============================================================
# 主入口
# ============================================================

def draw2d(objects, figsize=(8.0, 6.0), dpi=100,
           show_axis=True, show_grid=True, auto_scale=True,
           xlim=None, ylim=None, margin=0.15):
    """将 sympy 平面几何对象列表绘制为 matplotlib Figure

    Parameters
    ----------
    objects : list of (obj, style_dict_or_None)
        平面几何对象列表。每项为 (sympy几何对象, 样式字典或None)。
        样式字典覆盖默认样式，常用键：
          color, linewidth, linestyle, marker, markersize,
          edgecolor, facecolor, fill, alpha, label
    figsize : tuple, default (8.0, 6.0)
        Figure 尺寸（英寸）
    dpi : int, default 100
        分辨率
    show_axis : bool, default True
        是否显示坐标轴
    show_grid : bool, default True
        是否显示网格
    auto_scale : bool, default True
        是否根据对象自动计算坐标范围
    xlim, ylim : tuple or None
        手动指定坐标范围，若为 None 则自动计算
    margin : float, default 0.15
        自动缩放时的边距比例

    Returns
    -------
    matplotlib.figure.Figure
    """
    # 配置中文字体（避免 label 中汉字显示为方框）
    import matplotlib as _mpl
    _fonts = ['Microsoft YaHei', 'SimHei', 'SimSun', 'KaiTi', 'DejaVu Sans']
    _mpl.rcParams['font.sans-serif'] = _fonts
    _mpl.rcParams['axes.unicode_minus'] = False

    fig = Figure(figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111)

    # 自动计算坐标范围
    if auto_scale and xlim is None and ylim is None:
        bbox = _compute_bbox(objects)
        if bbox:
            xmin, xmax, ymin, ymax = bbox
            dx = max((xmax - xmin) * margin, 1.0)
            dy = max((ymax - ymin) * margin, 1.0)
            xlim = (xmin - dx, xmax + dx)
            ylim = (ymin - dy, ymax + dy)

    # 绘制每个对象
    for obj, user_style in objects:
        style = _merge_style(obj, user_style)
        label_text = style.pop('label', None)

        if isinstance(obj, Point):
            _plot_point(ax, obj, style, label_text)

        elif isinstance(obj, Line):
            _plot_line(ax, obj, style, xlim, ylim, label_text)

        elif isinstance(obj, Segment):
            _plot_segment(ax, obj, style, label_text)

        elif isinstance(obj, Ray):
            _plot_ray(ax, obj, style, xlim, ylim, label_text)

        elif isinstance(obj, Circle):
            _plot_circle(ax, obj, style, label_text)

        elif isinstance(obj, Triangle):
            _plot_triangle(ax, obj, style, label_text)

        elif isinstance(obj, Polygon):
            _plot_polygon(ax, obj, style, label_text)

    # 坐标轴与网格
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5)
    if show_grid:
        ax.grid(True, linestyle='--', alpha=0.6)
    if not show_axis:
        ax.set_axis_off()
    ax.set_aspect('equal')

    fig.tight_layout()
    return fig


# ============================================================
# 自动边界计算
# ============================================================

def _compute_bbox(objects):
    """计算所有对象的包围盒 (xmin, xmax, ymin, ymax)"""
    all_x, all_y = [], []

    for obj, _ in objects:
        pts = _collect_points(obj)
        for p in pts:
            all_x.append(_to_float(p.x))
            all_y.append(_to_float(p.y))

    if not all_x:
        return None

    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)

    # 退化情况：所有点重合
    if abs(xmax - xmin) < 1e-12:
        xmin -= 1
        xmax += 1
    if abs(ymax - ymin) < 1e-12:
        ymin -= 1
        ymax += 1

    return xmin, xmax, ymin, ymax


def _collect_points(obj):
    """从几何对象中提取所有特征点"""
    if isinstance(obj, Point):
        return [obj]
    elif isinstance(obj, (Line, Segment)):
        return list(obj.points)
    elif isinstance(obj, Ray):
        return [obj.source]
    elif isinstance(obj, Circle):
        return [obj.center]
    elif isinstance(obj, (Triangle, Polygon)):
        return list(obj.vertices)
    return []
