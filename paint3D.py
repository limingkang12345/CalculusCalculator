"""立体几何绘图模块
输入：由 sympy Point3D, Line3D, Plane, Segment3D, Ray3D 等对象
      构成的列表，每项为 (对象, 可选样式字典)
输出：matplotlib.figure.Figure 对象（含 3D 坐标轴），可直接嵌入 QWebEngineView
"""

import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D, art3d
from sympy import Point3D, Line3D, Plane, Segment3D, Ray3D, Symbol, N, pi, sqrt


# ============================================================
# 默认样式
# ============================================================

_DEFAULT_STYLE = {
    Point3D:   {'marker': 'o', 'color': '#1f77b4', 'markersize': 6, 'linestyle': 'none'},
    Line3D:    {'color': '#d62728', 'linewidth': 1.5},
    Segment3D: {'color': '#2ca02c', 'linewidth': 2.0},
    Ray3D:     {'color': '#9467bd', 'linewidth': 1.5},
    Plane:     {'color': '#ff7f0e', 'alpha': 0.3, 'linewidth': 0.5},
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


# ============================================================
# 各类对象的绘图函数
# ============================================================

def _plot_point3d(ax, pt, style, label_text=None):
    """绘制三维点"""
    x, y, z = _to_float(pt.x), _to_float(pt.y), _to_float(pt.z)
    # scatter 与 plot 的参数名不同，需做映射
    scatter_kw = {}
    for k, v in style.items():
        if k == 'markersize':
            scatter_kw['s'] = v ** 2  # scatter 的 s 是面积（点半径平方）
        elif k == 'color':
            scatter_kw['c'] = v
        elif k == 'markeredgecolor':
            scatter_kw['edgecolors'] = v
        elif k in ('marker', 'alpha', 'zorder'):
            scatter_kw[k] = v
    ax.scatter([x], [y], [z], **scatter_kw)
    if label_text:
        ax.text(x, y, z, label_text, fontsize=10)


def _get_line3d_extents(line, xlim, ylim, zlim):
    """获取三维直线在视口范围内的两个端点"""
    p0 = line.projection(Point3D(0, 0, 0))
    d = line.direction
    dx, dy, dz = _to_float(d.x), _to_float(d.y), _to_float(d.z)

    # 用参数 t 表示直线上点：P = p0 + t * d
    # 在六个边界面上求 t
    x1, x2 = xlim
    y1, y2 = ylim
    z1, z2 = zlim
    p0x, p0y, p0z = _to_float(p0.x), _to_float(p0.y), _to_float(p0.z)

    t_candidates = []
    eps = 1e-12

    if abs(dx) > eps:
        t_candidates.append((x1 - p0x) / dx)
        t_candidates.append((x2 - p0x) / dx)
    if abs(dy) > eps:
        t_candidates.append((y1 - p0y) / dy)
        t_candidates.append((y2 - p0y) / dy)
    if abs(dz) > eps:
        t_candidates.append((z1 - p0z) / dz)
        t_candidates.append((z2 - p0z) / dz)

    valid_pts = []
    for t in t_candidates:
        px = p0x + t * dx
        py = p0y + t * dy
        pz = p0z + t * dz
        if (x1 - eps <= px <= x2 + eps and
            y1 - eps <= py <= y2 + eps and
            z1 - eps <= pz <= z2 + eps):
            valid_pts.append((float(px), float(py), float(pz)))

    if len(valid_pts) >= 2:
        return valid_pts[:2]
    return valid_pts


def _plot_line3d(ax, line, style, xlim=None, ylim=None, zlim=None, label_text=None):
    """绘制三维直线"""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    if zlim is None:
        zlim = ax.get_zlim()
    pts = _get_line3d_extents(line, xlim, ylim, zlim)
    if len(pts) >= 2:
        xs, ys, zs = zip(*pts[:2])
        style_plot = {k: v for k, v in style.items()
                      if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder')}
        ax.plot(xs, ys, zs, **style_plot, label=label_text)


def _plot_segment3d(ax, seg, style, label_text=None):
    """绘制三维线段"""
    p1, p2 = seg.points
    xs = [_to_float(p1.x), _to_float(p2.x)]
    ys = [_to_float(p1.y), _to_float(p2.y)]
    zs = [_to_float(p1.z), _to_float(p2.z)]
    style_plot = {k: v for k, v in style.items()
                  if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder')}
    ax.plot(xs, ys, zs, **style_plot, label=label_text)


def _plot_ray3d(ax, ray, style, xlim=None, ylim=None, zlim=None, label_text=None):
    """绘制三维射线"""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    if zlim is None:
        zlim = ax.get_zlim()
    src = ray.source
    d = ray.direction
    sx, sy, sz = _to_float(src.x), _to_float(src.y), _to_float(src.z)
    dsx, dsy, dsz = _to_float(d.x), _to_float(d.y), _to_float(d.z)

    # 沿方向延伸到视口外
    rx = sx + 1e6 * dsx
    ry = sy + 1e6 * dsy
    rz = sz + 1e6 * dsz

    temp_line = Line3D(src, Point3D(rx, ry, rz))
    pts = _get_line3d_extents(temp_line, xlim, ylim, zlim)
    all_pts = [(sx, sy, sz)]
    for px, py, pz in pts:
        dx, dy, dz = px - sx, py - sy, pz - sz
        if dx * dsx + dy * dsy + dz * dsz > 0:
            all_pts.append((px, py, pz))
    if len(all_pts) >= 2:
        xs, ys, zs = zip(*all_pts)
        style_plot = {k: v for k, v in style.items()
                      if k in ('color', 'linewidth', 'linestyle', 'alpha', 'zorder')}
        ax.plot(xs, ys, zs, **style_plot, label=label_text)


def _plot_plane(ax, plane, style, xlim=None, ylim=None, zlim=None, label_text=None):
    """绘制平面（在视口范围内的矩形网格面）"""
    if xlim is None:
        xlim = ax.get_xlim()
    if ylim is None:
        ylim = ax.get_ylim()
    if zlim is None:
        zlim = ax.get_zlim()
    x1, x2 = xlim
    y1, y2 = ylim
    z1, z2 = zlim

    # 获取平面方程 Ax + By + Cz + D = 0
    n = plane.normal_vector
    A, B, C = _to_float(n[0]), _to_float(n[1]), _to_float(n[2])
    # 求 D：代入平面上一点
    some_pt = plane.projection(Point3D(0, 0, 0))
    px0, py0, pz0 = _to_float(some_pt.x), _to_float(some_pt.y), _to_float(some_pt.z)
    D = -(A * px0 + B * py0 + C * pz0)

    eps = 1e-12

    # 生成采样点网格，裁剪到视口范围内
    step = 0.5 * max(x2 - x1, y2 - y1, z2 - z1) / 8
    xs = np.arange(x1, x2 + step, step)
    ys = np.arange(y1, y2 + step, step)
    xs_2d, ys_2d = np.meshgrid(xs, ys)

    if abs(C) > eps:
        # 平面非竖直，用 z = -(Ax + By + D) / C
        zs_2d = -(A * xs_2d + B * ys_2d + D) / C
        mask = (zs_2d >= z1) & (zs_2d <= z2)
        if not np.any(mask):
            return
        xs_plot = np.where(mask, xs_2d, np.nan)
        ys_plot = np.where(mask, ys_2d, np.nan)
        zs_plot = np.where(mask, zs_2d, np.nan)
        color = style.get('color', '#ff7f0e')
        alpha = style.get('alpha', 0.3)
        edge_color = style.get('edgecolor', None)
        ax.plot_surface(xs_plot, ys_plot, zs_plot,
                        color=color, alpha=alpha,
                        edgecolor=edge_color, linewidth=0.2,
                        shade=True, antialiased=True, label=label_text)
    elif abs(B) > eps:
        # 用 y 表示
        xs_2d, zs_2d = np.meshgrid(xs, np.arange(z1, z2 + step, step))
        ys_2d = -(A * xs_2d + C * zs_2d + D) / B
        mask = (ys_2d >= y1) & (ys_2d <= y2)
        if not np.any(mask):
            return
        xs_plot = np.where(mask, xs_2d, np.nan)
        ys_plot = np.where(mask, ys_2d, np.nan)
        zs_plot = np.where(mask, zs_2d, np.nan)
        color = style.get('color', '#ff7f0e')
        alpha = style.get('alpha', 0.3)
        ax.plot_surface(xs_plot, ys_plot, zs_plot,
                        color=color, alpha=alpha, linewidth=0.2,
                        shade=True, antialiased=True, label=label_text)
    elif abs(A) > eps:
        # 用 x 表示
        ys_2d, zs_2d = np.meshgrid(ys, np.arange(z1, z2 + step, step))
        xs_2d = -(B * ys_2d + C * zs_2d + D) / A
        mask = (xs_2d >= x1) & (xs_2d <= x2)
        if not np.any(mask):
            return
        xs_plot = np.where(mask, xs_2d, np.nan)
        ys_plot = np.where(mask, ys_2d, np.nan)
        zs_plot = np.where(mask, zs_2d, np.nan)
        color = style.get('color', '#ff7f0e')
        alpha = style.get('alpha', 0.3)
        ax.plot_surface(xs_plot, ys_plot, zs_plot,
                        color=color, alpha=alpha, linewidth=0.2,
                        shade=True, antialiased=True, label=label_text)


# ============================================================
# 主入口
# ============================================================

def draw3d(objects, figsize=(8.0, 6.0), dpi=100,
           show_axis=True, show_grid=True, auto_scale=True,
           xlim=None, ylim=None, zlim=None, margin=0.15,
           elev=25, azim=-60):
    """将 sympy 三维几何对象列表绘制为 3D matplotlib Figure

    Parameters
    ----------
    objects : list of (obj, style_dict_or_None)
        三维几何对象列表。每项为 (sympy几何对象, 样式字典或None)。
        支持类型：Point3D, Line3D, Segment3D, Ray3D, Plane
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
    xlim, ylim, zlim : tuple or None
        手动指定坐标范围
    margin : float, default 0.15
        自动缩放时的边距比例
    elev : float, default 25
        3D 视图仰角
    azim : float, default -60
        3D 视图方位角

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig = Figure(figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, projection='3d')

    # 自动计算坐标范围
    if auto_scale and xlim is None and ylim is None:
        bbox = _compute_bbox3d(objects)
        if bbox:
            xmin, xmax, ymin, ymax, zmin, zmax = bbox
            dx = max((xmax - xmin) * margin, 1.0)
            dy = max((ymax - ymin) * margin, 1.0)
            dz = max((zmax - zmin) * margin, 1.0)
            xlim = (xmin - dx, xmax + dx)
            ylim = (ymin - dy, ymax + dy)
            zlim = (zmin - dz, zmax + dz)

    # 绘制每个对象
    for obj, user_style in objects:
        style = _merge_style(obj, user_style)
        label_text = style.pop('label', None)

        if isinstance(obj, Point3D):
            _plot_point3d(ax, obj, style, label_text)

        elif isinstance(obj, Line3D):
            _plot_line3d(ax, obj, style, xlim, ylim, zlim, label_text)

        elif isinstance(obj, Segment3D):
            _plot_segment3d(ax, obj, style, label_text)

        elif isinstance(obj, Ray3D):
            _plot_ray3d(ax, obj, style, xlim, ylim, zlim, label_text)

        elif isinstance(obj, Plane):
            _plot_plane(ax, obj, style, xlim, ylim, zlim, label_text)

    # 坐标轴与网格
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if zlim:
        ax.set_zlim(*zlim)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if show_grid:
        ax.grid(True, linestyle='--', alpha=0.6)
    if not show_axis:
        ax.set_axis_off()

    ax.view_init(elev=elev, azim=azim)
    fig.tight_layout()
    return fig


# ============================================================
# 自动边界计算
# ============================================================

def _compute_bbox3d(objects):
    """计算所有三维对象的包围盒 (xmin, xmax, ymin, ymax, zmin, zmax)"""
    all_x, all_y, all_z = [], [], []

    for obj, _ in objects:
        pts = _collect_points3d(obj)
        for p in pts:
            all_x.append(_to_float(p.x))
            all_y.append(_to_float(p.y))
            all_z.append(_to_float(p.z))

    if not all_x:
        return None

    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)
    zmin, zmax = min(all_z), max(all_z)

    if abs(xmax - xmin) < 1e-12:
        xmin -= 1
        xmax += 1
    if abs(ymax - ymin) < 1e-12:
        ymin -= 1
        ymax += 1
    if abs(zmax - zmin) < 1e-12:
        zmin -= 1
        zmax += 1

    return xmin, xmax, ymin, ymax, zmin, zmax


def _collect_points3d(obj):
    """从三维几何对象中提取所有特征点"""
    if isinstance(obj, Point3D):
        return [obj]
    elif isinstance(obj, (Line3D, Segment3D)):
        return list(obj.points)
    elif isinstance(obj, Ray3D):
        return [obj.source]
    elif isinstance(obj, Plane):
        # 平面上取原点投影作为代表点
        return [obj.projection(Point3D(0, 0, 0))]
    return []
