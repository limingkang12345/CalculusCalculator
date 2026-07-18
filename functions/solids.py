from sympy import (
    pi, sqrt, simplify, radsimp, acos, asin, atan2, sin, cos, tan,
    symbols, Symbol, Eq, latex, N, oo, Abs, Matrix, expand,
)
from sympy.geometry import Point3D, Line3D, Plane, Ray3D, Segment3D
from core.sympify import sympify


# ============================================================
# 3D 几何对象创建
# ============================================================

def create_point3d(x, y, z, fs):
    """创建三维点对象
    x,y,z(str): 点的坐标
    fs(dict): 函数列表
    return: Point3D 对象
    """
    return Point3D(sympify(x, fs), sympify(y, fs), sympify(z, fs))


def create_line3d(pt1, pt2):
    """通过两点创建三维直线
    pt1,pt2(Point3D): 点
    return: Line3D 对象
    """
    return Line3D(pt1, pt2)


def create_plane_three_points(p1, p2, p3):
    """通过三点创建平面
    p1,p2,p3(Point3D): 点
    return: Plane 对象
    """
    return Plane(p1, p2, p3)


def create_plane_point_normal(pt, nx, ny, nz, fs):
    """通过一点和法向量创建平面
    pt(Point3D): 平面上一点
    nx,ny,nz(str): 法向量分量
    fs(dict): 函数列表
    return: Plane 对象
    """
    normal = (sympify(nx, fs), sympify(ny, fs), sympify(nz, fs))
    # Plane(A, normal=(a,b,c)) 通过点和法向量构造
    return Plane(pt, normal_vector=normal)


# ============================================================
# 三维点运算
# ============================================================

def point3d_distance(pt1, pt2):
    """计算两点间的三维距离
    pt1,pt2(Point3D): 点
    return: 距离
    """
    return radsimp(pt1.distance(pt2))


def point3d_midpoint(pt1, pt2):
    """计算三维中点坐标
    pt1,pt2(Point3D): 点
    return: (x, y, z) 元组
    """
    mp = pt1.midpoint(pt2)
    return (radsimp(mp.x), radsimp(mp.y), radsimp(mp.z))


def point3d_to_plane_distance(pt, plane):
    """计算点到平面的距离
    pt(Point3D): 点
    plane(Plane): 平面
    return: 距离
    """
    return radsimp(plane.distance(pt))


def point3d_to_line_distance(pt, line):
    """计算点到三维直线的距离
    pt(Point3D): 点
    line(Line3D): 直线
    return: 距离
    """
    return radsimp(pt.distance(line))


def point3d_projection_on_plane(pt, plane):
    """计算点在平面上的投影
    pt(Point3D): 点
    plane(Plane): 平面
    return: (x, y, z) 元组
    """
    proj = plane.projection(pt)
    return (radsimp(proj.x), radsimp(proj.y), radsimp(proj.z))


def point3d_projection_on_line(pt, line):
    """计算点在三维直线上的投影
    pt(Point3D): 点
    line(Line3D): 直线
    return: (x, y, z) 元组
    """
    proj = line.projection(pt)
    return (radsimp(proj.x), radsimp(proj.y), radsimp(proj.z))


def are_coplanar(points):
    """判断多点是否共面
    points(list of Point3D): 点列表（至少4个点有判断意义）
    return: bool
    """
    return Point3D.are_coplanar(*points)


# ============================================================
# 三维直线运算
# ============================================================

def line3d_direction(line):
    """获取三维直线的方向向量
    line(Line3D): 直线
    return: (dx, dy, dz) 元组
    """
    d = line.direction
    return (radsimp(d.x), radsimp(d.y), radsimp(d.z))


def line3d_intersection(l1, l2):
    """求两三维直线的交点
    l1,l2(Line3D): 直线
    return: (x, y, z) 元组 或 描述信息
    """
    inter = l1.intersection(l2)
    if not inter:
        return "两直线不相交"
    if len(inter) > 1:
        return "两直线重合"
    pt = inter[0]
    if isinstance(pt, Line3D):
        return "两直线重合"
    return (radsimp(pt.x), radsimp(pt.y), radsimp(pt.z))


def line3d_angle(l1, l2):
    """求两三维直线的夹角（锐角，弧度）
    l1,l2(Line3D): 直线
    return: 夹角（弧度）
    """
    return radsimp(l1.angle_between(l2))


def line3d_parallel_check(l1, l2):
    """判断两三维直线是否平行
    l1,l2(Line3D): 直线
    return: bool
    """
    return l1.is_parallel(l2)


def line3d_perpendicular_check(l1, l2):
    """判断两三维直线是否垂直
    l1,l2(Line3D): 直线
    return: bool
    """
    return l1.is_perpendicular(l2)


def line3d_projection_on_plane(line, plane):
    """求三维直线在平面上的投影
    line(Line3D): 直线
    plane(Plane): 平面
    return: (方向向量, 直线上一点) 或 "投影为一点(点坐标)" 或描述信息
    """
    proj = plane.projection_line(line)
    if proj is None:
        return "直线垂直于平面，无投影直线"
    # projection_line 可能返回 Point3D（直线垂直于平面时投影为一点）
    if isinstance(proj, Point3D):
        return f"投影为一点 ({radsimp(proj.x)}, {radsimp(proj.y)}, {radsimp(proj.z)})"
    d = proj.direction
    p = proj.projection(Point3D(0, 0, 0))  # 求直线上一点
    return (
        (radsimp(d.x), radsimp(d.y), radsimp(d.z)),
        (radsimp(p.x), radsimp(p.y), radsimp(p.z)),
    )


# ============================================================
# 平面运算
# ============================================================

def plane_equation_from_points(p1, p2, p3):
    """通过三点求平面方程
    p1,p2,p3(Point3D): 三点
    return: 平面方程
    """
    pl = Plane(p1, p2, p3)
    return simplify(pl.equation())


def plane_normal_vector(plane):
    """计算平面的法向量
    plane(Plane): 平面
    return: (nx, ny, nz) 元组
    """
    n = plane.normal_vector
    return (radsimp(n[0]), radsimp(n[1]), radsimp(n[2]))


def plane_angle_between(pl1, pl2):
    """求两平面的夹角（锐角，弧度）
    pl1,pl2(Plane): 平面
    return: 夹角（弧度）
    """
    return radsimp(pl1.angle_between(pl2))


def plane_parallel_check(pl1, pl2):
    """判断两平面是否平行
    pl1,pl2(Plane): 平面
    return: bool
    """
    return pl1.is_parallel(pl2)


def plane_perpendicular_check(pl1, pl2):
    """判断两平面是否垂直
    pl1,pl2(Plane): 平面
    return: bool
    """
    return pl1.is_perpendicular(pl2)


def plane_intersection(pl1, pl2):
    """求两平面的交线
    pl1,pl2(Plane): 平面
    return: (方向向量, 直线上一点) 或描述信息
    """
    inter = pl1.intersection(pl2)
    if not inter:
        return "两平面平行"
    line = inter[0]
    if not isinstance(line, Line3D):
        return "两平面重合"
    d = line.direction
    # 求直线上一点（原点在直线上的投影）
    origin = Point3D(0, 0, 0)
    pt_on_line = line.projection(origin)
    return (
        (radsimp(d.x), radsimp(d.y), radsimp(d.z)),
        (radsimp(pt_on_line.x), radsimp(pt_on_line.y), radsimp(pt_on_line.z)),
    )


def plane_line_intersection(plane, line):
    """求平面与直线的交点
    plane(Plane): 平面
    line(Line3D): 直线
    return: (x, y, z) 元组 或 描述信息
    """
    inter = plane.intersection(line)
    if not inter:
        return "直线与平面平行"
    if len(inter) > 1:
        return "直线在平面上"
    pt = inter[0]
    return (radsimp(pt.x), radsimp(pt.y), radsimp(pt.z))


def plane_projection_of_line(plane, line):
    """求直线在平面上的投影
    plane(Plane): 平面
    line(Line3D): 直线
    return: (方向向量, 直线上一点) 或描述信息
    """
    return line3d_projection_on_plane(line, plane)


def plane_contains_point(plane, pt):
    """判断平面是否包含某点
    plane(Plane): 平面
    pt(Point3D): 点
    return: bool
    """
    return plane.distance(pt).simplify() == 0


def plane_contains_line(plane, line):
    """判断平面是否包含某直线
    plane(Plane): 平面
    line(Line3D): 直线
    return: bool
    """
    inter = plane.intersection(line)
    return len(inter) > 1 or (len(inter) == 1 and isinstance(inter[0], Line3D))


# ============================================================
# 四面体运算
# ============================================================

def tetrahedron_volume(p1, p2, p3, p4):
    """计算四面体体积
    p1,p2,p3,p4(Point3D): 四个顶点
    return: 体积
    """
    a = Matrix(p2) - Matrix(p1)
    b = Matrix(p3) - Matrix(p1)
    c = Matrix(p4) - Matrix(p1)
    vol = abs(a.dot(b.cross(c))) / 6
    return radsimp(vol)


# ============================================================
# 三维向量运算
# ============================================================

def vector3d_from_points(pt1, pt2):
    """计算两点间的三维向量
    pt1(Point3D): 起点
    pt2(Point3D): 终点
    return: (dx, dy, dz) 元组
    """
    diff = Matrix(pt2) - Matrix(pt1)
    return (radsimp(diff[0]), radsimp(diff[1]), radsimp(diff[2]))


def vector3d_length(dx, dy, dz, fs):
    """计算三维向量的模
    dx,dy,dz(str): 向量分量
    fs(dict): 函数列表
    return: 模长
    """
    vx = sympify(dx, fs)
    vy = sympify(dy, fs)
    vz = sympify(dz, fs)
    return radsimp(sqrt(vx**2 + vy**2 + vz**2))


def vector3d_dot(v1_dx, v1_dy, v1_dz, v2_dx, v2_dy, v2_dz, fs):
    """计算两三维向量的点积
    v1_dx,v1_dy,v1_dz(str): 向量1的分量
    v2_dx,v2_dy,v2_dz(str): 向量2的分量
    fs(dict): 函数列表
    return: 点积
    """
    a = Matrix([sympify(v1_dx, fs), sympify(v1_dy, fs), sympify(v1_dz, fs)])
    b = Matrix([sympify(v2_dx, fs), sympify(v2_dy, fs), sympify(v2_dz, fs)])
    return radsimp(a.dot(b))


def vector3d_cross(v1_dx, v1_dy, v1_dz, v2_dx, v2_dy, v2_dz, fs):
    """计算两三维向量的叉积
    v1_dx,v1_dy,v1_dz(str): 向量1的分量
    v2_dx,v2_dy,v2_dz(str): 向量2的分量
    fs(dict): 函数列表
    return: (x, y, z) 元组
    """
    a = Matrix([sympify(v1_dx, fs), sympify(v1_dy, fs), sympify(v1_dz, fs)])
    b = Matrix([sympify(v2_dx, fs), sympify(v2_dy, fs), sympify(v2_dz, fs)])
    c = a.cross(b)
    return (radsimp(c[0]), radsimp(c[1]), radsimp(c[2]))


def vector3d_angle(v1_dx, v1_dy, v1_dz, v2_dx, v2_dy, v2_dz, fs):
    """计算两三维向量的夹角（弧度）
    v1_dx,v1_dy,v1_dz(str): 向量1的分量
    v2_dx,v2_dy,v2_dz(str): 向量2的分量
    fs(dict): 函数列表
    return: 夹角（弧度）
    """
    a = Matrix([sympify(v1_dx, fs), sympify(v1_dy, fs), sympify(v1_dz, fs)])
    b = Matrix([sympify(v2_dx, fs), sympify(v2_dy, fs), sympify(v2_dz, fs)])
    dot = a.dot(b)
    mag1 = sqrt(a.dot(a))
    mag2 = sqrt(b.dot(b))
    return radsimp(acos(dot / (mag1 * mag2)))


# ============================================================
# 平面与直线综合关系
# ============================================================

def line_plane_angle(line, plane):
    """求直线与平面的夹角（弧度）
    line(Line3D): 直线
    plane(Plane): 平面
    return: 夹角（弧度）
    """
    # 直线方向向量与平面法向量的夹角，直线与平面的夹角 = pi/2 - 该夹角
    line_dir = line.direction
    line_vec = Matrix([line_dir.x, line_dir.y, line_dir.z])
    n = plane.normal_vector
    normal_vec = Matrix(n)
    dot = line_vec.dot(normal_vec)
    mag1 = sqrt(line_vec.dot(line_vec))
    mag2 = sqrt(normal_vec.dot(normal_vec))
    angle_with_normal = acos(abs(dot) / (mag1 * mag2))
    return radsimp(pi / 2 - angle_with_normal)


# ============================================================
# 几何构造（通过点线面的位置关系创建新对象）
# ============================================================

def plane_parallel_through_point(plane, pt):
    """过一点作已知平面的平行平面
    plane(Plane): 已知平面
    pt(Point3D): 目标点
    return: Plane 对象
    """
    # 平行平面法向量相同，过目标点
    n = plane.normal_vector
    return Plane(pt, normal_vector=n)


def plane_perpendicular_to_line_through_point(line, pt):
    """过一点作已知直线的垂直平面
    line(Line3D): 已知直线
    pt(Point3D): 目标点
    return: Plane 对象
    """
    # 直线的方向向量即为平面的法向量
    d = line.direction
    return Plane(pt, normal_vector=(d.x, d.y, d.z))


def line_parallel_through_point_3d(line, pt):
    """过一点作已知直线的平行线
    line(Line3D): 已知直线
    pt(Point3D): 目标点
    return: Line3D 对象
    """
    d = line.direction
    other = Point3D(pt.x + d.x, pt.y + d.y, pt.z + d.z)
    return Line3D(pt, other)


def line_perpendicular_to_plane_through_point(plane, pt):
    """过一点作已知平面的垂线
    plane(Plane): 已知平面
    pt(Point3D): 目标点
    return: Line3D 对象
    """
    n = plane.normal_vector
    other = Point3D(pt.x + n[0], pt.y + n[1], pt.z + n[2])
    return Line3D(pt, other)


def plane_through_line_and_point(line, pt):
    """过一直线和线外一点作平面
    line(Line3D): 已知直线
    pt(Point3D): 直线外一点
    return: Plane 对象
    """
    p_on_line = line.projection(Point3D(0, 0, 0))
    # 取直线上另一点
    d = line.direction
    p_on_line2 = Point3D(p_on_line.x + d.x, p_on_line.y + d.y, p_on_line.z + d.z)
    return Plane(p_on_line, p_on_line2, pt)


def plane_through_two_lines(l1, l2):
    """过两条直线作平面（两直线须相交或平行）
    l1,l2(Line3D): 两条直线
    return: Plane 对象 或 描述信息
    """
    inter = l1.intersection(l2)
    p1_on_l1 = l1.projection(Point3D(0, 0, 0))
    d1 = l1.direction
    p2_on_l1 = Point3D(p1_on_l1.x + d1.x, p1_on_l1.y + d1.y, p1_on_l1.z + d1.z)

    if inter:
        # 相交：交点和两条直线上的各一个非交点
        pt = inter[0]
        if not isinstance(pt, Point3D):
            return "两直线重合"
        # 取 l2 上不同于交点的点
        d2 = l2.direction
        pt_on_l2 = Point3D(pt.x + d2.x, pt.y + d2.y, pt.z + d2.z)
        return Plane(pt, p2_on_l1, pt_on_l2)
    else:
        # 平行或异面
        if l1.is_parallel(l2):
            # 平行：一条直线上取两点，另一条直线上取一点
            d2 = l2.direction
            p_on_l2 = l2.projection(Point3D(0, 0, 0))
            return Plane(p1_on_l1, p2_on_l1, p_on_l2)
        else:
            return "两直线异面，无法确定唯一平面"


def perpendicular_foot_to_plane(pt, plane):
    """求点到平面的垂足
    pt(Point3D): 点
    plane(Plane): 平面
    return: Point3D 对象
    """
    return plane.projection(pt)


def perpendicular_foot_to_line_3d(pt, line):
    """求点到直线的垂足
    pt(Point3D): 点
    line(Line3D): 直线
    return: Point3D 对象
    """
    return line.projection(pt)


def segment3d_from_points(p1, p2):
    """通过两点构造三维线段
    p1,p2(Point3D): 端点
    return: Segment3D 对象
    """
    return Segment3D(p1, p2)


# ============================================================
# 斜二测画法（将三维坐标投影到二维绘图平面）
# 规则：x轴（水平）、z轴（竖直）长度不变
#       y轴（深度）与x轴成45°角，长度减半
# ============================================================

def oblique_project(pt):
    """斜二测画法：三维点 → 二维投影坐标
    pt(Point3D): 三维点
    return: (X, Y) 绘图平面上的二维坐标
            X 为水平方向，Y 为竖直方向
    变换公式:
        X = x + (y/2)·cos(45°)
        Y = z + (y/2)·sin(45°)
    """
    x, y, z = pt.x, pt.y, pt.z
    half_y = y / 2
    cos45 = sqrt(2) / 2
    X = x + half_y * cos45
    Y = z + half_y * cos45
    return (radsimp(X), radsimp(Y))


def oblique_project_points(points):
    """斜二测画法：批量转换多个三维点
    points(list of Point3D): 三维点列表
    return: list of (X, Y) 二维坐标
    """
    return [oblique_project(pt) for pt in points]


def oblique_restore_point(X, Y, z, fs):
    """斜二测画法逆变换：已知投影坐标和z坐标，求原始(x, y)
    X,Y(str): 投影平面上的二维坐标
    z(str): 原始z坐标
    fs(dict): 函数列表
    return: (x, y) 原始水平坐标
    逆变换公式:
        y = (Y - z) / sin(45°) * 2 = (Y - z) * 2√2
        x = X - (y/2) · cos(45°)
    其中 z 必须已知才能唯一确定 y
    """
    X_val = sympify(X, fs)
    Y_val = sympify(Y, fs)
    z_val = sympify(z, fs)
    cos45 = sqrt(2) / 2
    # y = (Y - z) / sin(45°) * 2
    y_val = (Y_val - z_val) / cos45 * 2
    # x = X - (y/2) · cos(45°)
    x_val = X_val - (y_val / 2) * cos45
    return (radsimp(x_val), radsimp(y_val))


def oblique_area_ratio():
    """斜二测画法的面积缩放比（水平面 xOy 上的图形）
    规则: 水平面（xOy平面）上的图形投影后，
          面积变为原来的 √2/4
    return: (缩放因子, 说明)
    """
    factor = sqrt(2) / 4
    return (factor, "水平面(xOy)上的图形投影后面积为原来的 √2/4")


def oblique_restore_area(projected_area, fs):
    """已知斜二测投影面积，反求原始水平面面积
    projected_area(str): 投影面积
    fs(dict): 函数列表
    return: 原始面积
    公式: S_original = S_projected / (√2/4) = S_projected · 2√2
    """
    S_proj = sympify(projected_area, fs)
    S_orig = S_proj / (sqrt(2) / 4)
    return radsimp(S_orig)


def oblique_project_area(original_area, fs):
    """已知原始水平面面积，求斜二测投影面积
    original_area(str): 原始面积
    fs(dict): 函数列表
    return: 投影面积
    公式: S_projected = S_original · (√2/4)
    """
    S_orig = sympify(original_area, fs)
    S_proj = S_orig * sqrt(2) / 4
    return radsimp(S_proj)


def oblique_isometric_factor():
    """斜二测画法中等腰直角三角形的长度恢复因子
    用于已知投影长反求原长（y方向）
    公式: L_original = L_projected * 2√2
    return: 恢复因子
    """
    return radsimp(2 * sqrt(2))


def oblique_project_length_y(original_length, fs):
    """计算斜二测画法下y方向投影长度
    original_length(str): y方向原始长度
    fs(dict): 函数列表
    return: 投影长度
    公式: L_projected = L_original / 2 · √2/2 · 2 ... 
    简化: y方向长度在投影中变为 L_original / 2
          再投影到水平和竖直方向各贡献 L_original · √2/4
    """
    L = sympify(original_length, fs)
    # y方向长度投影到水平/竖直各为 L * √2/4
    proj_h = L * sqrt(2) / 4
    return radsimp(proj_h)


# ============================================================
# 辅助函数（内部使用）
# ============================================================

def _parse_point3d(pt_str, fs):
    """将 "x,y,z" 格式的字符串解析为 Point3D 对象
    pt_str(str): 点坐标字符串
    fs(dict): 函数列表
    return: Point3D
    """
    parts = pt_str.split(',')
    if len(parts) != 3:
        raise ValueError(f"点坐标格式错误，应为'x,y,z'，但收到'{pt_str}'")
    return Point3D(
        sympify(parts[0].strip(), fs),
        sympify(parts[1].strip(), fs),
        sympify(parts[2].strip(), fs),
    )


def _build_line_from_strs(p1_str, p2_str, fs):
    """从两个点字符串构建 Line3D"""
    return Line3D(_parse_point3d(p1_str, fs), _parse_point3d(p2_str, fs))


def _build_plane_from_strs(p1_str, p2_str, p3_str, fs):
    """从三个点字符串构建 Plane"""
    return Plane(
        _parse_point3d(p1_str, fs),
        _parse_point3d(p2_str, fs),
        _parse_point3d(p3_str, fs),
    )


# ============================================================
# 主调用接口（UI 使用，参数仍为字符串）
# ============================================================

# 立体几何功能列表，用于 UI 选择
solids_operation_list = [
    "两点距离",
    "中点坐标",
    "点到平面距离",
    "点到直线距离",
    "点在平面投影",
    "点在直线投影",
    "共面判断",
    "直线方向向量",
    "两直线交点",
    "两直线夹角",
    "平行判断(线)",
    "垂直判断(线)",
    "三点求平面方程",
    "平面的法向量",
    "两平面夹角",
    "平行判断(面)",
    "垂直判断(面)",
    "两平面交线",
    "平面与直线交点",
    "直线在平面投影",
    "平面包含点",
    "平面包含直线",
    "四面体体积",
    "两点三维向量",
    "向量模(3D)",
    "向量点积(3D)",
    "向量叉积(3D)",
    "向量夹角(3D)",
    "直线与平面夹角",
    "斜二测投影(单点)",
    "斜二测投影(多点)",
    "斜二测逆变换",
    "面积缩放比",
    "投影面积求原面积",
    "原面积求投影面积",
    "y方向长度恢复因子",
    "y方向投影长度",
]


def get_solids_result(op_index, params, fs):
    """统一调度接口，根据操作类型调用对应函数
    op_index(int): 操作索引，对应 solids_operation_list
    params(list of str): 参数列表
    fs(dict): 函数列表
    return: 计算结果
    """
    try:
        # 快捷转换
        pt = lambda i: _parse_point3d(params[i], fs)
        pts_list = lambda i: [_parse_point3d(p.strip(), fs) for p in params[i].split(';') if p.strip()]
        line = lambda i, j: _build_line_from_strs(params[i], params[j], fs)
        plane3 = lambda i, j, k: _build_plane_from_strs(params[i], params[j], params[k], fs)

        if op_index == 0:   # 两点距离
            return point3d_distance(pt(0), pt(1))
        elif op_index == 1:   # 中点坐标
            return point3d_midpoint(pt(0), pt(1))
        elif op_index == 2:   # 点到平面距离
            return point3d_to_plane_distance(pt(0), plane3(1, 2, 3))
        elif op_index == 3:   # 点到直线距离
            return point3d_to_line_distance(pt(0), line(1, 2))
        elif op_index == 4:   # 点在平面投影
            return point3d_projection_on_plane(pt(0), plane3(1, 2, 3))
        elif op_index == 5:   # 点在直线投影
            return point3d_projection_on_line(pt(0), line(1, 2))
        elif op_index == 6:   # 共面判断
            return are_coplanar(pts_list(0))
        elif op_index == 7:   # 直线方向向量
            return line3d_direction(line(0, 1))
        elif op_index == 8:   # 两直线交点
            return line3d_intersection(line(0, 1), line(2, 3))
        elif op_index == 9:   # 两直线夹角
            return line3d_angle(line(0, 1), line(2, 3))
        elif op_index == 10:  # 平行判断(线)
            return line3d_parallel_check(line(0, 1), line(2, 3))
        elif op_index == 11:  # 垂直判断(线)
            return line3d_perpendicular_check(line(0, 1), line(2, 3))
        elif op_index == 12:  # 三点求平面方程
            return plane_equation_from_points(pt(0), pt(1), pt(2))
        elif op_index == 13:  # 平面的法向量
            return plane_normal_vector(plane3(0, 1, 2))
        elif op_index == 14:  # 两平面夹角
            return plane_angle_between(plane3(0, 1, 2), plane3(3, 4, 5))
        elif op_index == 15:  # 平行判断(面)
            return plane_parallel_check(plane3(0, 1, 2), plane3(3, 4, 5))
        elif op_index == 16:  # 垂直判断(面)
            return plane_perpendicular_check(plane3(0, 1, 2), plane3(3, 4, 5))
        elif op_index == 17:  # 两平面交线
            return plane_intersection(plane3(0, 1, 2), plane3(3, 4, 5))
        elif op_index == 18:  # 平面与直线交点
            return plane_line_intersection(plane3(0, 1, 2), line(3, 4))
        elif op_index == 19:  # 直线在平面投影
            return plane_projection_of_line(plane3(0, 1, 2), line(3, 4))
        elif op_index == 20:  # 平面包含点
            return plane_contains_point(plane3(0, 1, 2), pt(3))
        elif op_index == 21:  # 平面包含直线
            return plane_contains_line(plane3(0, 1, 2), line(3, 4))
        elif op_index == 22:  # 四面体体积
            return tetrahedron_volume(pt(0), pt(1), pt(2), pt(3))
        elif op_index == 23:  # 两点三维向量
            return vector3d_from_points(pt(0), pt(1))
        elif op_index == 24:  # 向量模(3D)
            return vector3d_length(params[0], params[1], params[2], fs)
        elif op_index == 25:  # 向量点积(3D)
            return vector3d_dot(params[0], params[1], params[2],
                                params[3], params[4], params[5], fs)
        elif op_index == 26:  # 向量叉积(3D)
            return vector3d_cross(params[0], params[1], params[2],
                                  params[3], params[4], params[5], fs)
        elif op_index == 27:  # 向量夹角(3D)
            return vector3d_angle(params[0], params[1], params[2],
                                  params[3], params[4], params[5], fs)
        elif op_index == 28:  # 直线与平面夹角
            return line_plane_angle(line(0, 1), plane3(2, 3, 4))
        elif op_index == 29:  # 斜二测投影(单点)
            return oblique_project(pt(0))
        elif op_index == 30:  # 斜二测投影(多点)
            return oblique_project_points(pts_list(0))
        elif op_index == 31:  # 斜二测逆变换
            return oblique_restore_point(params[0], params[1], params[2], fs)
        elif op_index == 32:  # 面积缩放比
            return oblique_area_ratio()
        elif op_index == 33:  # 投影面积求原面积
            return oblique_restore_area(params[0], fs)
        elif op_index == 34:  # 原面积求投影面积
            return oblique_project_area(params[0], fs)
        elif op_index == 35:  # y方向长度恢复因子
            return oblique_isometric_factor()
        elif op_index == 36:  # y方向投影长度
            return oblique_project_length_y(params[0], fs)
        else:
            return "未知操作"
    except Exception as e:
        return f"计算错误: {e}"
