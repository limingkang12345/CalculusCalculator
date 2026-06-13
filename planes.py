from sympy import (
    Point, Line, Circle, Triangle, Polygon, Segment, Ray,
    pi, sqrt, simplify, radsimp, acos, atan2, atan, sin, cos, tan,
    symbols, Symbol, Eq, latex, N, oo, Abs, Matrix, expand,
)
from sympify import sympify


# ============================================================
# 几何对象创建
# ============================================================

def create_point(x, y, fs):
    """创建点对象
    x(str): 点的x坐标
    y(str): 点的y坐标
    fs(dict): 函数列表
    return: sympy Point 对象
    """
    return Point(sympify(x, fs), sympify(y, fs))


def create_line(pt1, pt2):
    """通过两点创建直线
    pt1(Point): 点1
    pt2(Point): 点2
    return: sympy Line 对象
    """
    return Line(pt1, pt2)


def create_circle(center, radius, fs):
    """通过圆心和半径创建圆
    center(Point): 圆心
    radius(str): 半径
    fs(dict): 函数列表
    return: sympy Circle 对象
    """
    return Circle(center, sympify(radius, fs))


def create_circle_three_points(p1, p2, p3):
    """通过三点创建圆（外接圆）
    p1,p2,p3(Point): 三个点
    return: sympy Circle 对象
    """
    return Circle(p1, p2, p3)


def create_triangle(p1, p2, p3):
    """通过三点创建三角形
    p1,p2,p3(Point): 顶点
    return: sympy Triangle 对象
    """
    return Triangle(p1, p2, p3)


def create_polygon(points):
    """通过顶点列表创建多边形
    points(list of Point): 顶点列表
    return: sympy Polygon 对象
    """
    return Polygon(*points)


# ============================================================
# 点相关运算
# ============================================================

def point_distance(pt1, pt2):
    """计算两点之间的距离
    pt1,pt2(Point): 点
    return: 距离
    """
    return radsimp(pt1.distance(pt2))


def midpoint(pt1, pt2):
    """计算两点中点坐标
    pt1,pt2(Point): 点
    return: (x, y) 元组
    """
    mp = pt1.midpoint(pt2)
    return (radsimp(mp.x), radsimp(mp.y))


def collinear_check(points):
    """判断多点是否共线
    points(list of Point): 点列表
    return: bool
    """
    return Point.is_collinear(*points)


def translate_point(pt, dx, dy, fs):
    """平移点
    pt(Point): 原始点
    dx(str): x方向平移量
    dy(str): y方向平移量
    fs(dict): 函数列表
    return: (x', y') 元组
    """
    vx = sympify(dx, fs)
    vy = sympify(dy, fs)
    new_pt = pt.translate(vx, vy)
    return (radsimp(new_pt.x), radsimp(new_pt.y))


def rotate_point(pt, angle, center, fs):
    """绕定点旋转点
    pt(Point): 原始点
    angle(str): 旋转角度（弧度）
    center(Point): 旋转中心
    fs(dict): 函数列表
    return: (x', y') 元组
    """
    theta = sympify(angle, fs)
    c = center if center else Point(0, 0)
    new_pt = pt.rotate(theta, c)
    return (radsimp(new_pt.x), radsimp(new_pt.y))


def reflect_point(pt, line_pt1, line_pt2):
    """点关于直线的反射
    pt(Point): 原始点
    line_pt1,line_pt2(Point): 直线上的两点
    return: (x', y') 元组
    """
    line = Line(line_pt1, line_pt2)
    new_pt = pt.reflect(line)
    return (radsimp(new_pt.x), radsimp(new_pt.y))


# ============================================================
# 线相关运算
# ============================================================

def line_equation(pt1, pt2):
    """求经过两点的直线方程
    pt1,pt2(Point): 点
    return: 直线方程
    """
    l = Line(pt1, pt2)
    return simplify(l.equation())


def line_slope(pt1, pt2):
    """求直线斜率
    pt1,pt2(Point): 点
    return: 斜率（垂直线返回oo）
    """
    l = Line(pt1, pt2)
    return radsimp(l.slope)


def line_intersection(p1, p2, q1, q2):
    """求两直线的交点
    p1,p2(Point): 第一条直线上的两点
    q1,q2(Point): 第二条直线上的两点
    return: (x, y) 元组或"平行/重合"
    """
    l1 = Line(p1, p2)
    l2 = Line(q1, q2)
    inter = l1.intersection(l2)
    if not inter:
        return "两直线平行"
    if len(inter) > 1:
        return "两直线重合"
    pt = inter[0]
    return (radsimp(pt.x), radsimp(pt.y))


def point_to_line_distance(pt, line_pt1, line_pt2):
    """求点到直线的距离
    pt(Point): 点
    line_pt1,line_pt2(Point): 直线上两点
    return: 距离
    """
    l = Line(line_pt1, line_pt2)
    return radsimp(pt.distance(l))


def angle_between_lines(p1, p2, q1, q2):
    """求两直线的夹角（锐角，弧度）
    p1,p2(Point): 第一条直线上的两点
    q1,q2(Point): 第二条直线上的两点
    return: 夹角（弧度）
    """
    l1 = Line(p1, p2)
    l2 = Line(q1, q2)
    return radsimp(l1.angle_between(l2))


def parallel_check(p1, p2, q1, q2):
    """判断两直线是否平行
    p1,p2(Point): 第一条直线上的两点
    q1,q2(Point): 第二条直线上的两点
    return: bool
    """
    l1 = Line(p1, p2)
    l2 = Line(q1, q2)
    return l1.is_parallel(l2)


def perpendicular_check(p1, p2, q1, q2):
    """判断两直线是否垂直
    p1,p2(Point): 第一条直线上的两点
    q1,q2(Point): 第二条直线上的两点
    return: bool
    """
    l1 = Line(p1, p2)
    l2 = Line(q1, q2)
    return l1.is_perpendicular(l2)


# ============================================================
# 圆相关运算
# ============================================================

def circle_center(center, radius, fs):
    """求圆的圆心
    center(Point): 圆心
    radius(str): 半径
    fs(dict): 函数列表
    return: (x, y) 元组
    """
    c = Circle(center, sympify(radius, fs))
    return (radsimp(c.center.x), radsimp(c.center.y))


def circle_radius(center, radius, fs):
    """求圆的半径
    center(Point): 圆心
    radius(str): 半径
    fs(dict): 函数列表
    return: 半径
    """
    c = Circle(center, sympify(radius, fs))
    return radsimp(c.radius)


def circle_area_func(center, radius, fs):
    """求圆的面积
    center(Point): 圆心
    radius(str): 半径
    fs(dict): 函数列表
    return: 面积
    """
    c = Circle(center, sympify(radius, fs))
    return radsimp(c.area)


def circle_circumference(center, radius, fs):
    """求圆的周长
    center(Point): 圆心
    radius(str): 半径
    fs(dict): 函数列表
    return: 周长
    """
    c = Circle(center, sympify(radius, fs))
    return radsimp(c.circumference)


def circle_intersection(center1, radius1, center2, radius2, fs):
    """求两圆的交点
    center1,center2(Point): 圆心
    radius1,radius2(str): 半径
    fs(dict): 函数列表
    return: 交点列表
    """
    c1 = Circle(center1, sympify(radius1, fs))
    c2 = Circle(center2, sympify(radius2, fs))
    inter = c1.intersection(c2)
    result = []
    for pt in inter:
        result.append((radsimp(pt.x), radsimp(pt.y)))
    if not result:
        return "两圆不相交"
    return result


def circle_tangent_lines(center, radius, point, fs):
    """求圆外一点到圆的切线方程
    center(Point): 圆心
    radius(str): 半径
    point(Point): 圆外点
    fs(dict): 函数列表
    return: 切线方程列表
    """
    c = Circle(center, sympify(radius, fs))
    tangents = c.tangent_lines(point)
    result = []
    for line in tangents:
        eq = line.equation()
        result.append(simplify(eq))
    return result if result else "无切线"


# ============================================================
# 三角形相关运算
# ============================================================

def triangle_area(p1, p2, p3):
    """求三角形面积
    p1,p2,p3(Point): 顶点
    return: 面积
    """
    return radsimp(Triangle(p1, p2, p3).area)


def triangle_perimeter(p1, p2, p3):
    """求三角形周长
    p1,p2,p3(Point): 顶点
    return: 周长
    """
    return radsimp(Triangle(p1, p2, p3).perimeter)


def triangle_circumcenter(p1, p2, p3):
    """求三角形外心（外接圆圆心）
    p1,p2,p3(Point): 顶点
    return: (x, y) 元组
    """
    tri = Triangle(p1, p2, p3)
    c = tri.circumcircle
    return (radsimp(c.center.x), radsimp(c.center.y))


def triangle_circumradius(p1, p2, p3):
    """求三角形外接圆半径
    p1,p2,p3(Point): 顶点
    return: 半径
    """
    tri = Triangle(p1, p2, p3)
    return radsimp(tri.circumcircle.radius)


def triangle_incenter(p1, p2, p3):
    """求三角形内心（内切圆圆心）
    p1,p2,p3(Point): 顶点
    return: (x, y) 元组
    """
    tri = Triangle(p1, p2, p3)
    i = tri.incenter
    return (radsimp(i.x), radsimp(i.y))


def triangle_inradius(p1, p2, p3):
    """求三角形内切圆半径
    p1,p2,p3(Point): 顶点
    return: 半径
    """
    return radsimp(Triangle(p1, p2, p3).inradius)


def triangle_centroid(p1, p2, p3):
    """求三角形重心
    p1,p2,p3(Point): 顶点
    return: (x, y) 元组
    """
    ct = Triangle(p1, p2, p3).centroid
    return (radsimp(ct.x), radsimp(ct.y))


def triangle_orthocenter(p1, p2, p3):
    """求三角形垂心
    p1,p2,p3(Point): 顶点
    return: (x, y) 元组
    """
    o = Triangle(p1, p2, p3).orthocenter
    return (radsimp(o.x), radsimp(o.y))


def triangle_is_right(p1, p2, p3):
    """判断三角形是否为直角三角形
    p1,p2,p3(Point): 顶点
    return: bool
    """
    return Triangle(p1, p2, p3).is_right()


def triangle_is_isosceles(p1, p2, p3):
    """判断三角形是否为等腰三角形
    p1,p2,p3(Point): 顶点
    return: bool
    """
    return Triangle(p1, p2, p3).is_isosceles()


def triangle_is_equilateral(p1, p2, p3):
    """判断三角形是否为等边三角形
    p1,p2,p3(Point): 顶点
    return: bool
    """
    return Triangle(p1, p2, p3).is_equilateral()


# ============================================================
# 多边形相关运算
# ============================================================

def polygon_area_func(points):
    """求多边形面积
    points(list of Point): 顶点列表
    return: 面积
    """
    return radsimp(Polygon(*points).area)


def polygon_perimeter_func(points):
    """求多边形周长
    points(list of Point): 顶点列表
    return: 周长
    """
    poly = Polygon(*points)
    sides = poly.sides
    perimeter = sum(s.length for s in sides)
    return radsimp(perimeter)


# ============================================================
# 综合几何分析
# ============================================================

def triangle_analysis(p1, p2, p3):
    """三角形综合分析，返回各类心坐标和基本属性
    p1,p2,p3(Point): 顶点
    return: dict，包含面积、周长、各种心
    """
    tri = Triangle(p1, p2, p3)
    cc = tri.circumcircle
    result = {
        "面积": radsimp(tri.area),
        "周长": radsimp(tri.perimeter),
        "外心": (radsimp(cc.center.x), radsimp(cc.center.y)),
        "外接圆半径": radsimp(cc.radius),
        "内心": (radsimp(tri.incenter.x), radsimp(tri.incenter.y)),
        "内切圆半径": radsimp(tri.inradius),
        "重心": (radsimp(tri.centroid.x), radsimp(tri.centroid.y)),
        "垂心": (radsimp(tri.orthocenter.x), radsimp(tri.orthocenter.y)),
        "直角三角形": tri.is_right(),
        "等腰三角形": tri.is_isosceles(),
        "等边三角形": tri.is_equilateral(),
    }
    return result


# ============================================================
# 几何构造（通过点线面的位置关系创建新对象）
# ============================================================

def circle_with_diameter(p1, p2):
    """以两点为直径端点构造圆
    p1,p2(Point): 直径的两个端点
    return: Circle 对象
    """
    center = p1.midpoint(p2)
    radius = p1.distance(p2) / 2
    return Circle(center, radius)


def circle_by_center_and_point(center, pt):
    """以圆心和圆上一点构造圆
    center(Point): 圆心
    pt(Point): 圆上一点
    return: Circle 对象
    """
    return Circle(center, center.distance(pt))


def perpendicular_bisector(p1, p2):
    """求线段的中垂线
    p1,p2(Point): 线段端点
    return: Line 对象
    """
    mid = p1.midpoint(p2)
    # 方向向量为 p1->p2 的法向量（旋转90°）
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    # (dx, dy) 的法向量为 (-dy, dx)
    direction = Point(-dy, dx)
    other = Point(mid.x - dy, mid.y + dx)  # 中垂线上另一点
    return Line(mid, other)


def line_parallel_through_point(line, pt):
    """过一点作已知直线的平行线
    line(Line): 已知直线
    pt(Point): 目标点
    return: Line 对象
    """
    d = line.direction
    other = Point(pt.x + d.x, pt.y + d.y)
    return Line(pt, other)


def line_perpendicular_through_point(line, pt):
    """过一点作已知直线的垂线
    line(Line): 已知直线
    pt(Point): 目标点
    return: Line 对象
    """
    d = line.direction
    # 垂直方向向量为 (-dy, dx)
    other = Point(pt.x - d.y, pt.y + d.x)
    return Line(pt, other)


def angle_bisector_line(l1, l2):
    """求两相交直线的角平分线（锐角方向）
    l1,l2(Line): 两条相交直线
    return: Line 对象 或 描述信息
    """
    inter = l1.intersection(l2)
    if not inter:
        return "两直线平行，无角平分线"
    if len(inter) > 1:
        return "两直线重合"
    intersection_pt = inter[0]

    # 取两直线上的方向点（距离交点单位长度）
    d1 = l1.direction
    d2 = l2.direction
    mag1 = sqrt(d1.x**2 + d1.y**2)
    mag2 = sqrt(d2.x**2 + d2.y**2)

    # 单位方向向量
    u1 = Point(d1.x / mag1, d1.y / mag1)
    u2 = Point(d2.x / mag2, d2.y / mag2)

    # 角平分线方向 = u1 + u2（菱形对角线方向）
    bisector_dir = Point(u1.x + u2.x, u1.y + u2.y)
    bisector_mag = sqrt(bisector_dir.x**2 + bisector_dir.y**2)

    if bisector_mag < 1e-12:
        # 反向平分线
        bisector_dir = Point(u1.x - u2.x, u1.y - u2.y)
    else:
        bisector_dir = Point(bisector_dir.x / bisector_mag, bisector_dir.y / bisector_mag)

    other_pt = Point(intersection_pt.x + bisector_dir.x,
                     intersection_pt.y + bisector_dir.y)
    return Line(intersection_pt, other_pt)


def angle_bisector(p1, p2, p3):
    """求角 p1-p2-p3 的角平分线（p2 为顶点）
    p1,p2,p3(Point): 角的三点
    return: Line 对象
    """
    l1 = Line(p2, p1)
    l2 = Line(p2, p3)
    return angle_bisector_line(l1, l2)


def triangle_median(tri, vertex_label):
    """求三角形的中线（顶点到对边中点）
    tri(Triangle): 三角形
    vertex_label(int): 顶点索引（0,1,2）
    return: Segment 对象
    """
    verts = tri.vertices
    v = verts[vertex_label]
    # 对边两端点
    other = [verts[i] for i in range(3) if i != vertex_label]
    mid_opp = other[0].midpoint(other[1])
    return Segment(v, mid_opp)


def triangle_altitude(tri, vertex_label):
    """求三角形的高线（过顶点作对边的垂线）
    tri(Triangle): 三角形
    vertex_label(int): 顶点索引（0,1,2）
    return: Line 对象
    """
    verts = tri.vertices
    v = verts[vertex_label]
    # 对边
    other = [verts[i] for i in range(3) if i != vertex_label]
    opposite_side = Line(other[0], other[1])
    return line_perpendicular_through_point(opposite_side, v)


def triangle_midsegment(tri):
    """求三角形的中位线（连接两边中点的线段）
    tri(Triangle): 三角形
    return: Segment 对象
    """
    verts = tri.vertices
    mid01 = verts[0].midpoint(verts[1])
    mid02 = verts[0].midpoint(verts[2])
    return Segment(mid01, mid02)


def triangle_incircle(tri):
    """求三角形的内切圆
    tri(Triangle): 三角形
    return: Circle 对象
    """
    return Circle(tri.incenter, tri.inradius)


def triangle_excircle(tri, vertex_label):
    """求三角形的旁切圆（与某边及另外两边的延长线相切）
    tri(Triangle): 三角形
    vertex_label(int): 顶点索引（0,1,2），该顶点所对的边为切边
    return: Circle 对象
    """
    from sympy import Point as SymPoint
    verts = tri.vertices
    a, b, c = verts
    # 三边长度
    side_a = b.distance(c)  # a 对边
    side_b = a.distance(c)  # b 对边
    side_c = a.distance(b)  # c 对边

    # 旁心坐标计算公式（与 vertex_label 相对的边）
    if vertex_label == 0:
        # 与顶点A相对的边为a，旁切圆与边a及ba、ca延长线相切
        excenter = SymPoint(
            (-side_a * a.x + side_b * b.x + side_c * c.x) / (-side_a + side_b + side_c),
            (-side_a * a.y + side_b * b.y + side_c * c.y) / (-side_a + side_b + side_c),
        )
        # 半径 = 面积 / (半周长 - a)
        s = (side_a + side_b + side_c) / 2
        exradius = tri.area / (s - side_a)
    elif vertex_label == 1:
        # 与顶点B相对的边为b
        excenter = SymPoint(
            (side_a * a.x - side_b * b.x + side_c * c.x) / (side_a - side_b + side_c),
            (side_a * a.y - side_b * b.y + side_c * c.y) / (side_a - side_b + side_c),
        )
        s = (side_a + side_b + side_c) / 2
        exradius = tri.area / (s - side_b)
    else:
        # 与顶点C相对的边为c
        excenter = SymPoint(
            (side_a * a.x + side_b * b.x - side_c * c.x) / (side_a + side_b - side_c),
            (side_a * a.y + side_b * b.y - side_c * c.y) / (side_a + side_b - side_c),
        )
        s = (side_a + side_b + side_c) / 2
        exradius = tri.area / (s - side_c)

    return Circle(excenter, exradius)


def segment_from_points(p1, p2):
    """通过两点构造线段
    p1,p2(Point): 端点
    return: Segment 对象
    """
    return Segment(p1, p2)


# ============================================================
# 坐标转换与向量运算（平面几何辅助）
# ============================================================

def vector_from_points(pt1, pt2):
    """计算两点间的向量
    pt1(Point): 起点
    pt2(Point): 终点
    return: (dx, dy) 元组
    """
    return (radsimp(pt2.x - pt1.x), radsimp(pt2.y - pt1.y))


def vector_length(dx, dy, fs):
    """计算向量的模
    dx(str): x分量
    dy(str): y分量
    fs(dict): 函数列表
    return: 模长
    """
    vx = sympify(dx, fs)
    vy = sympify(dy, fs)
    return radsimp(sqrt(vx**2 + vy**2))


def vector_dot(v1_dx, v1_dy, v2_dx, v2_dy, fs):
    """计算两向量的点积
    v1_dx,v1_dy(str): 向量1的分量
    v2_dx,v2_dy(str): 向量2的分量
    fs(dict): 函数列表
    return: 点积
    """
    a1 = sympify(v1_dx, fs)
    a2 = sympify(v1_dy, fs)
    b1 = sympify(v2_dx, fs)
    b2 = sympify(v2_dy, fs)
    return radsimp(a1 * b1 + a2 * b2)


def vector_angle(v1_dx, v1_dy, v2_dx, v2_dy, fs):
    """计算两向量的夹角（弧度）
    v1_dx,v1_dy(str): 向量1的分量
    v2_dx,v2_dy(str): 向量2的分量
    fs(dict): 函数列表
    return: 夹角（弧度）
    """
    a1 = sympify(v1_dx, fs)
    a2 = sympify(v1_dy, fs)
    b1 = sympify(v2_dx, fs)
    b2 = sympify(v2_dy, fs)
    dot = a1 * b1 + a2 * b2
    mag1 = sqrt(a1**2 + a2**2)
    mag2 = sqrt(b1**2 + b2**2)
    return radsimp(acos(dot / (mag1 * mag2)))


def area_by_coordinates(x1, y1, x2, y2, x3, y3, fs):
    """通过坐标字符串计算三角形面积（行列式法）
    x1,y1,x2,y2,x3,y3(str): 三个顶点的坐标
    fs(dict): 函数列表
    return: 面积
    """
    p1 = Point(sympify(x1, fs), sympify(y1, fs))
    p2 = Point(sympify(x2, fs), sympify(y2, fs))
    p3 = Point(sympify(x3, fs), sympify(y3, fs))
    return triangle_area(p1, p2, p3)


# ============================================================
# 辅助函数（内部使用）
# ============================================================

def _parse_point(pt_str, fs):
    """将 "x,y" 格式的字符串解析为 sympy Point 对象
    pt_str(str): 点坐标字符串
    fs(dict): 函数列表
    return: sympy Point
    """
    parts = pt_str.split(',')
    if len(parts) != 2:
        raise ValueError(f"点坐标格式错误，应为'x,y'，但收到'{pt_str}'")
    return Point(sympify(parts[0].strip(), fs), sympify(parts[1].strip(), fs))


# ============================================================
# 主调用接口（UI 使用，参数仍为字符串）
# ============================================================

# 平面几何功能列表，用于 UI 选择
planes_operation_list = [
    "两点距离",
    "中点坐标",
    "共线判断",
    "直线方程",
    "直线斜率",
    "直线交点",
    "点到直线距离",
    "两直线夹角",
    "平行判断",
    "垂直判断",
    "圆的面积",
    "圆的周长",
    "两圆交点",
    "圆切线方程",
    "三角形面积",
    "三角形周长",
    "三角形外心",
    "三角形内心",
    "三角形重心",
    "三角形垂心",
    "三角形分析",
    "多边形面积",
    "多边形周长",
    "平移变换",
    "旋转变换",
    "反射变换",
    "两点向量",
    "向量模",
    "向量点积",
    "向量夹角",
]


def get_planes_result(op_index, params, fs):
    """统一调度接口，根据操作类型调用对应函数
    op_index(int): 操作索引，对应 planes_operation_list
    params(list of str): 参数列表
    fs(dict): 函数列表
    return: 计算结果
    """
    try:
        # 内部将字符串参数转为 Point 对象，再调用核心函数
        pt = lambda i: _parse_point(params[i], fs)  # 快捷转换
        pts_list = lambda i: [_parse_point(p.strip(), fs) for p in params[i].split(';') if p.strip()]

        if op_index == 0:     # 两点距离
            return point_distance(pt(0), pt(1))
        elif op_index == 1:   # 中点坐标
            return midpoint(pt(0), pt(1))
        elif op_index == 2:   # 共线判断
            return collinear_check(pts_list(0))
        elif op_index == 3:   # 直线方程
            return line_equation(pt(0), pt(1))
        elif op_index == 4:   # 直线斜率
            return line_slope(pt(0), pt(1))
        elif op_index == 5:   # 直线交点
            return line_intersection(pt(0), pt(1), pt(2), pt(3))
        elif op_index == 6:   # 点到直线距离
            return point_to_line_distance(pt(0), pt(1), pt(2))
        elif op_index == 7:   # 两直线夹角
            return angle_between_lines(pt(0), pt(1), pt(2), pt(3))
        elif op_index == 8:   # 平行判断
            return parallel_check(pt(0), pt(1), pt(2), pt(3))
        elif op_index == 9:   # 垂直判断
            return perpendicular_check(pt(0), pt(1), pt(2), pt(3))
        elif op_index == 10:  # 圆的面积
            return circle_area_func(pt(0), params[1], fs)
        elif op_index == 11:  # 圆的周长
            return circle_circumference(pt(0), params[1], fs)
        elif op_index == 12:  # 两圆交点
            return circle_intersection(pt(0), params[1], pt(2), params[3], fs)
        elif op_index == 13:  # 圆切线方程
            return circle_tangent_lines(pt(0), params[1], pt(2), fs)
        elif op_index == 14:  # 三角形面积
            return triangle_area(pt(0), pt(1), pt(2))
        elif op_index == 15:  # 三角形周长
            return triangle_perimeter(pt(0), pt(1), pt(2))
        elif op_index == 16:  # 三角形外心
            return triangle_circumcenter(pt(0), pt(1), pt(2))
        elif op_index == 17:  # 三角形内心
            return triangle_incenter(pt(0), pt(1), pt(2))
        elif op_index == 18:  # 三角形重心
            return triangle_centroid(pt(0), pt(1), pt(2))
        elif op_index == 19:  # 三角形垂心
            return triangle_orthocenter(pt(0), pt(1), pt(2))
        elif op_index == 20:  # 三角形分析
            return triangle_analysis(pt(0), pt(1), pt(2))
        elif op_index == 21:  # 多边形面积
            return polygon_area_func(pts_list(0))
        elif op_index == 22:  # 多边形周长
            return polygon_perimeter_func(pts_list(0))
        elif op_index == 23:  # 平移变换
            return translate_point(pt(0), params[1], params[2], fs)
        elif op_index == 24:  # 旋转变换
            return rotate_point(pt(0), params[1], pt(2), fs)
        elif op_index == 25:  # 反射变换
            return reflect_point(pt(0), pt(1), pt(2))
        elif op_index == 26:  # 两点向量
            return vector_from_points(pt(0), pt(1))
        elif op_index == 27:  # 向量模
            return vector_length(params[0], params[1], fs)
        elif op_index == 28:  # 向量点积
            return vector_dot(params[0], params[1], params[2], params[3], fs)
        elif op_index == 29:  # 向量夹角
            return vector_angle(params[0], params[1], params[2], params[3], fs)
        else:
            return "未知操作"
    except Exception as e:
        return f"计算错误: {e}"
