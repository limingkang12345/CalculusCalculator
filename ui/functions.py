"""功能集成页：定义区、计算区与绘图区。

定义区与计算区共用同一套输入表引擎：每种类型由 _Spec 描述，_Spec.rows 依当前
取值给出行定义 (标题, 默认值, 角色)，_InputTable 据此生成控件、缓存取值并处理联动。
平面 / 立体几何只是"带两个下拉框、参数行随创建方式变化"的一种规格。

绘图区与「平面绘图」「立体几何绘图」标签页一致，直接取用 parent.pjs / parent.ljs
中已定义的几何对象绘制为 matplotlib 图表。

行角色决定控件类型与保存时取值的解析方式：
    VALUE     数值 / 表达式，原样传给构造函数（由其内部 sympify）
    SELECT    下拉框，选项固定，取值为选项原文（与语言无关）
    QUANTITY  数字框，其后的变长行按该数量展开
    POINT / LINE / SEGMENT / TRIANGLE / PLANE
              已定义的几何对象，控件为「已定义对象名称」下拉框，
              保存时按名称查对象
    INTEGER   整数

几何创建方式的规格表（PLANE_GEOMETRY / SOLID_GEOMETRY）每项为
(创建方式名称, 参数行, 结果类别, 构造函数名)，参数顺序与
functions/planes.py、functions/solids.py 中构造函数的形参顺序一致。
"""

from PySide6.QtWidgets import (QWidget, QMessageBox, QHeaderView, QTableWidgetItem,
                               QTreeWidgetItem, QListWidgetItem, QLineEdit, QComboBox,
                               QSpinBox, QVBoxLayout, QSplitter, QApplication)
from PySide6.QtCore import QCoreApplication, QEvent, QObject, QTimer, Qt
from PySide6.QtGui import QAction, QIcon, QWheelEvent
tr = QCoreApplication.translate
from ui.ui_functions import Ui_functions
from ui.huancun import open_cache
from core.render import setGraphicsView, setGraphicsViewTheme
from core.sympify import sympify
from math_input.math_input import open_formula_dialog
from sympy import latex, Eq, Rel, Symbol


CALC_FUNCTION_NAMES = [
    "计算", "求导", "积分", "解方程", "解不等式", "解方程组", "解不等式组",
    "平面计算", "立体计算", "变形", "解三角形"
]

DEF_TYPE_NAMES = [
    "函数", "集合", "向量", "平面几何", "立体几何"
]

CALC_GEO_INDEX = {7: "plane", 8: "solid"}
CALC_TRANSFORM_INDEX = 9
CALC_TRIANGLE_INDEX = 10

# 解三角形的条件类型（下标与「解三角形」标签页一致）
TRIANGLE_PARTS = ["未选择", "角A", "角B", "角C", "边a", "边b", "边c"]
TRIANGLE_KEYS = ["", "A", "B", "C", "a", "b", "c"]

# 定义区 / 计算区 / 绘图区的初始宽度权重
AREA_WEIGHTS = (0.32, 0.31, 0.37)

# 绘图区模式（.ui 中只有前两项，函数模式运行时补齐；追加在末尾以兼容旧存档）
DRAW_MODE_NAMES = ["平面几何模式", "立体几何模式", "函数模式"]
DRAW_FUNC_INDEX = 2

# 与「计算」标签页一致：计算引擎与变形方法

CALC_ENGINE_NAMES = [
    "Python内置引擎", "Mpmath高精度引擎", "Sympy符号引擎", "Latex代码生成引擎"
]

TRANSFORM_NAMES = [
    "通用化简(simplify)", "展开(expand)", "因式分解(factor)", "主元(collect)",
    "通分(cancel)", "分离(apart)", "三角变换(trigsimp)", "三角展开(expand_trig)",
    "指数合并(powsimp)", "指数展开(expand_power_exp)", "对数展开(expand_log)",
    "对数合并(logcombine)", "换元",
]

# 需要额外参数的下标：主元(collect)、换元
TRANSFORM_PIVOT = 3
TRANSFORM_SUBST = 12

VALUE = "value"
SELECT = "select"
QUANTITY = "quantity"
POINT = "point"
LINE = "line"
SEGMENT = "segment"
TRIANGLE = "triangle"
CIRCLE = "circle"
PLANE = "plane"
INTEGER = "integer"

ROLE_CATEGORY = {
    POINT: "点",
    LINE: "直线",
    SEGMENT: "线段",
    TRIANGLE: "三角形",
    CIRCLE: "圆",
    PLANE: "平面",
}

NAME_PREFIX = {
    "点": "p",
    "直线": "l",
    "线段": "s",
    "三角形": "t",
    "圆": "c",
    "多边形": "poly",
    "平面": "pl",
}


# ==================== 几何定义规格 ====================

PLANE_GEOMETRY = {
    "点": [
        ("按坐标创建", [("x坐标", "0", VALUE), ("y坐标", "0", VALUE)], "点", "create_point"),
    ],
    "直线": [
        ("两点创建", [("点1名称", "", POINT), ("点2名称", "", POINT)], "直线", "create_line"),
        ("线段的垂直平分线", [("线段名称", "", SEGMENT)], "直线", "perpendicular_bisector"),
        ("过点作平行线", [("直线名称", "", LINE), ("点名称", "", POINT)], "直线", "line_parallel_through_point"),
        ("过点作垂线", [("直线名称", "", LINE), ("点名称", "", POINT)], "直线", "line_perpendicular_through_point"),
        ("两直线的角平分线", [("直线1名称", "", LINE), ("直线2名称", "", LINE)], "直线", "angle_bisector_line"),
        ("角的平分线", [("点1名称", "", POINT), ("顶点名称", "", POINT), ("点3名称", "", POINT)], "直线", "angle_bisector"),
        ("三角形的高线", [("三角形名称", "", TRIANGLE), ("顶点索引", "0", INTEGER)], "直线", "triangle_altitude"),
    ],
    "线段": [
        ("两点创建", [("点1名称", "", POINT), ("点2名称", "", POINT)], "线段", "segment_from_points"),
        ("三角形的中线", [("三角形名称", "", TRIANGLE), ("顶点索引", "0", INTEGER)], "线段", "triangle_median"),
        ("三角形的中位线", [("三角形名称", "", TRIANGLE)], "线段", "triangle_midsegment"),
    ],
    "三角形": [
        ("三点创建", [("点1名称", "", POINT), ("点2名称", "", POINT), ("点3名称", "", POINT)], "三角形", "create_triangle"),
    ],
    "多边形": [
        ("顶点依次创建", [("顶点数", 3, QUANTITY), ("顶点{}名称", "", POINT)], "多边形", "create_polygon"),
    ],
    "圆": [
        ("圆心与半径", [("圆心名称", "", POINT), ("半径", "1", VALUE)], "圆", "create_circle"),
        ("三点定圆", [("点1名称", "", POINT), ("点2名称", "", POINT), ("点3名称", "", POINT)], "圆", "create_circle_three_points"),
        ("以两点为直径", [("点1名称", "", POINT), ("点2名称", "", POINT)], "圆", "circle_with_diameter"),
        ("圆心与圆上一点", [("圆心名称", "", POINT), ("圆上点名称", "", POINT)], "圆", "circle_by_center_and_point"),
        ("三角形的内切圆", [("三角形名称", "", TRIANGLE)], "圆", "triangle_incircle"),
        ("三角形的旁切圆", [("三角形名称", "", TRIANGLE), ("顶点索引", "0", INTEGER)], "圆", "triangle_excircle"),
    ],
}

SOLID_GEOMETRY = {
    "点": [
        ("按坐标创建", [("x坐标", "0", VALUE), ("y坐标", "0", VALUE), ("z坐标", "0", VALUE)], "点", "create_point3d"),
        ("点到平面的垂足", [("点名称", "", POINT), ("平面名称", "", PLANE)], "点", "perpendicular_foot_to_plane"),
        ("点到直线的垂足", [("点名称", "", POINT), ("直线名称", "", LINE)], "点", "perpendicular_foot_to_line_3d"),
    ],
    "直线": [
        ("两点创建", [("点1名称", "", POINT), ("点2名称", "", POINT)], "直线", "create_line3d"),
        ("过点作平行线", [("直线名称", "", LINE), ("点名称", "", POINT)], "直线", "line_parallel_through_point_3d"),
        ("过点作已知直线的垂线", [("点名称", "", POINT), ("直线名称", "", LINE)], "直线", "perpendicular_line_from_point"),
        ("过点作平面的垂线", [("平面名称", "", PLANE), ("点名称", "", POINT)], "直线", "line_perpendicular_to_plane_through_point"),
    ],
    "平面": [
        ("三点创建", [("点1名称", "", POINT), ("点2名称", "", POINT), ("点3名称", "", POINT)], "平面", "create_plane_three_points"),
        ("一点与法向量", [("点名称", "", POINT), ("法向量x", "1", VALUE), ("法向量y", "1", VALUE), ("法向量z", "1", VALUE)], "平面", "create_plane_point_normal"),
        ("过直线与点", [("直线名称", "", LINE), ("点名称", "", POINT)], "平面", "plane_through_line_and_point"),
        ("过两条直线", [("直线1名称", "", LINE), ("直线2名称", "", LINE)], "平面", "plane_through_two_lines"),
        ("过点作平行平面", [("平面名称", "", PLANE), ("点名称", "", POINT)], "平面", "plane_parallel_through_point"),
        ("过点作垂直于直线的平面", [("直线名称", "", LINE), ("点名称", "", POINT)], "平面", "plane_perpendicular_to_line_through_point"),
    ],
    "线段": [
        ("两点创建", [("点1名称", "", POINT), ("点2名称", "", POINT)], "线段", "segment3d_from_points"),
    ],
}

GEOMETRY = {"plane": PLANE_GEOMETRY, "solid": SOLID_GEOMETRY}

_NEEDS_FS = {"create_point", "create_circle", "create_point3d", "create_plane_point_normal"}


# ==================== 几何计算规格 ====================
# 与「平面计算」「立体计算」标签页一致：每个运算为 (运算名称, 计算键, 参数行)

PLANE_OPS = {
    "点": [
        ("两点距离", "point_distance", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("中点坐标", "midpoint", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("共线判断", "collinear_check", [("点数", 3, QUANTITY), ("点{}名称", "", POINT)]),
        ("平移点", "translate_point", [("点名称", "", POINT), ("x位移", "0", VALUE), ("y位移", "0", VALUE)]),
        ("绕定点旋转", "rotate_point", [("点名称", "", POINT), ("旋转角", "0", VALUE), ("旋转中心名称", "", POINT)]),
        ("点关于直线反射", "reflect_point", [("点名称", "", POINT), ("直线名称", "", LINE)]),
    ],
    "直线": [
        ("直线方程", "line_equation", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("直线斜率", "line_slope", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("两直线交点", "line_intersection", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("点到直线距离", "point_to_line_distance", [("点名称", "", POINT), ("直线名称", "", LINE)]),
        ("两直线夹角", "angle_between_lines", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("平行判断", "parallel_check", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("垂直判断", "perpendicular_check", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
    ],
    "圆": [
        ("圆心坐标", "circle_center", [("圆名称", "", CIRCLE)]),
        ("半径", "circle_radius", [("圆名称", "", CIRCLE)]),
        ("面积", "circle_area", [("圆名称", "", CIRCLE)]),
        ("周长", "circle_circumference", [("圆名称", "", CIRCLE)]),
        ("两圆交点", "circle_intersection", [("圆1名称", "", CIRCLE), ("圆2名称", "", CIRCLE)]),
        ("切线方程", "circle_tangent_lines", [("点名称", "", POINT), ("圆名称", "", CIRCLE)]),
    ],
    "三角形": [
        ("面积", "triangle_area", [("三角形名称", "", TRIANGLE)]),
        ("周长", "triangle_perimeter", [("三角形名称", "", TRIANGLE)]),
        ("外心", "triangle_circumcenter", [("三角形名称", "", TRIANGLE)]),
        ("外接圆半径", "triangle_circumradius", [("三角形名称", "", TRIANGLE)]),
        ("内心", "triangle_incenter", [("三角形名称", "", TRIANGLE)]),
        ("内切圆半径", "triangle_inradius", [("三角形名称", "", TRIANGLE)]),
        ("重心", "triangle_centroid", [("三角形名称", "", TRIANGLE)]),
        ("垂心", "triangle_orthocenter", [("三角形名称", "", TRIANGLE)]),
        ("直角三角形判断", "triangle_is_right", [("三角形名称", "", TRIANGLE)]),
        ("等腰三角形判断", "triangle_is_isosceles", [("三角形名称", "", TRIANGLE)]),
        ("等边三角形判断", "triangle_is_equilateral", [("三角形名称", "", TRIANGLE)]),
    ],
    "多边形": [
        ("面积", "polygon_area_func", [("顶点数", 3, QUANTITY), ("顶点{}名称", "", POINT)]),
        ("周长", "polygon_perimeter_func", [("顶点数", 3, QUANTITY), ("顶点{}名称", "", POINT)]),
    ],
}

SOLID_OPS = {
    "点": [
        ("两点距离", "point3d_distance", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("中点坐标", "point3d_midpoint", [("点1名称", "", POINT), ("点2名称", "", POINT)]),
        ("点到平面距离", "point3d_to_plane_distance", [("点名称", "", POINT), ("平面名称", "", PLANE)]),
        ("点到直线距离", "point3d_to_line_distance", [("点名称", "", POINT), ("直线名称", "", LINE)]),
        ("点在平面上的投影", "point3d_projection_on_plane", [("点名称", "", POINT), ("平面名称", "", PLANE)]),
        ("点在直线上的投影", "point3d_projection_on_line", [("点名称", "", POINT), ("直线名称", "", LINE)]),
        ("共面判断", "are_coplanar", [("点数", 4, QUANTITY), ("点{}名称", "", POINT)]),
        ("四面体体积", "tetrahedron_volume",
         [("点1名称", "", POINT), ("点2名称", "", POINT), ("点3名称", "", POINT), ("点4名称", "", POINT)]),
    ],
    "直线": [
        ("方向向量", "line3d_direction", [("直线名称", "", LINE)]),
        ("两直线交点", "line3d_intersection", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("两直线夹角", "line3d_angle", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("平行判断", "line3d_parallel_check", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("垂直判断", "line3d_perpendicular_check", [("直线1名称", "", LINE), ("直线2名称", "", LINE)]),
        ("在平面上的投影", "line3d_projection_on_plane", [("直线名称", "", LINE), ("平面名称", "", PLANE)]),
        ("与平面的夹角", "line_plane_angle", [("直线名称", "", LINE), ("平面名称", "", PLANE)]),
    ],
    "平面": [
        ("三点求平面方程", "plane_equation_from_points",
         [("点1名称", "", POINT), ("点2名称", "", POINT), ("点3名称", "", POINT)]),
        ("法向量", "plane_normal_vector", [("平面名称", "", PLANE)]),
        ("两平面夹角", "plane_angle_between", [("平面1名称", "", PLANE), ("平面2名称", "", PLANE)]),
        ("两平面交线", "plane_intersection", [("平面1名称", "", PLANE), ("平面2名称", "", PLANE)]),
        ("平行判断", "plane_parallel_check", [("平面1名称", "", PLANE), ("平面2名称", "", PLANE)]),
        ("垂直判断", "plane_perpendicular_check", [("平面1名称", "", PLANE), ("平面2名称", "", PLANE)]),
        ("与直线的交点", "plane_line_intersection", [("平面名称", "", PLANE), ("直线名称", "", LINE)]),
    ],
}

OPS = {"plane": PLANE_OPS, "solid": SOLID_OPS}

# 参数中的直线需要展开为两端点的运算
_LINE_PAIR_OPS = {"line_intersection", "angle_between_lines", "parallel_check", "perpendicular_check"}
_LINE_POINT_OPS = {"point_to_line_distance", "reflect_point"}

# 以三角形三个顶点为实参的运算
_TRIANGLE_OPS = {
    "triangle_area", "triangle_perimeter", "triangle_circumcenter", "triangle_circumradius",
    "triangle_incenter", "triangle_inradius", "triangle_centroid", "triangle_orthocenter",
    "triangle_is_right", "triangle_is_isosceles", "triangle_is_equilateral",
}

# 需要额外传入函数列表（fs）的运算
_FS_OPS = {"translate_point", "rotate_point"}


# ==================== 控件与取值辅助 ====================

class _CellClickFilter(QObject):
    """单元格控件的鼠标按下监听：把用户点击转换为一次回调。"""

    def __init__(self, widget, slot):
        super().__init__(widget)
        self._slot = slot
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            obj.setFocus(Qt.MouseFocusReason)
            self._slot()
        return False


class _CellWheelFilter(QObject):
    """把单元格控件上的滚轮事件转交给所在表格。

    下拉框 / 数字框自身响应滚轮会改变取值，且会让单元格显示为聚焦状态；
    改为转发给表格视口，滚轮用于滚动表格，控件内容保持不变。
    """

    def __init__(self, widget, table):
        super().__init__(widget)
        self._viewport = table.viewport()
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() != QEvent.Type.Wheel:
            return False
        forwarded = QWheelEvent(event.position(), event.globalPosition(),
                                event.pixelDelta(), event.angleDelta(),
                                event.buttons(), event.modifiers(),
                                event.phase(), event.inverted())
        QApplication.sendEvent(self._viewport, forwarded)
        return True


def field_text(field):
    """取行定义的初始文本：下拉框取首项，其余取默认值。"""

    _title, default, role = field
    return default[0] if role == SELECT else str(default)


def attr_default(attr):
    """兼容旧二元组属性定义的默认值取值。"""

    value = attr[1]
    return value[0] if isinstance(value, list) else value


def int_value(text, default = 1):
    """把文本解析为整数，无法解析时取 default。"""

    try:
        return int(str(text).strip())
    except Exception:
        return int(default)


def source_text(source):
    """读取控件内容：下拉框返回其数据项（原文，与语言无关）。"""

    if isinstance(source, QComboBox):
        data = source.currentData()
        return source.currentText() if data is None else str(data)
    if isinstance(source, QSpinBox):
        return str(source.value())
    if isinstance(source, QLineEdit):
        return source.text()
    if isinstance(source, QTableWidgetItem):
        return source.text()
    return ""


def get_cell_text(table, row, col = 0):
    """读取单元格文本：自定义控件优先，无控件时退回普通表格项。"""

    widget = table.cellWidget(row, col)
    return source_text(widget if widget is not None else table.item(row, col))


def set_widget_text(widget, text):
    """写入控件取值：下拉框按数据项匹配，缺失时补入选项，空值则不选中。"""

    if isinstance(widget, QComboBox):
        index = widget.findData(text)
        if index < 0 and text == "":
            widget.setCurrentIndex(-1)
            return
        if index < 0:
            widget.addItem(text, text)
            index = widget.count() - 1
        widget.setCurrentIndex(index)
    elif isinstance(widget, QSpinBox):
        widget.setValue(int_value(text, widget.minimum()))
    elif isinstance(widget, QLineEdit):
        widget.setText(text)


def connect_cell_clicked(widget, slot):
    """在用户点击单元格控件时回调 slot。"""

    widget.click_filter = _CellClickFilter(widget, slot)


def connect_cell_wheel(widget, table):
    """把单元格控件上的滚轮事件转交给表格，避免滚轮改变控件取值。"""

    widget.wheel_filter = _CellWheelFilter(widget, table)


def connect_cell_changed(widget, slot):
    """在单元格控件内容变化时回调 slot。"""

    if isinstance(widget, QComboBox):
        widget.currentIndexChanged.connect(slot)
    elif isinstance(widget, QSpinBox):
        widget.valueChanged.connect(slot)
    elif isinstance(widget, QLineEdit):
        widget.textChanged.connect(slot)


def clear_table(table):
    """清空表格中的普通项与单元格控件。"""

    for row in range(table.rowCount()):
        table.removeCellWidget(row, 0)
    table.clearContents()


# ==================== 输入表规格 ====================

class _Spec:
    """输入表的一种类型。

    rows(values): 依当前取值生成行定义 [(标题, 默认值, 角色)]
    selects: 作为缓存分组键的行号（下拉框所在行）
    dim: 平面 / 立体几何的维度，非几何类型为 None
    store: 对象取值存放的字典
    name_default(seed): 名称行的默认值，None 表示取行定义中的固定默认值
    """

    def __init__(self, title, rows, store = None, selects = (), dim = None,
                 name_default = None):
        self.title = title
        self.rows = rows if callable(rows) else (lambda values: rows)
        self.store = store if store is not None else {}
        self.selects = tuple(selects)
        self.dim = dim
        self.name_default = name_default


def group_rows(fixed, member, count_row = 0):
    """生成"固定行 + 成员行按数量重复"的行定义函数（方程组 / 不等式组）。"""

    def rows(values):
        default = field_text(fixed[count_row])
        count = int_value(values[count_row], default) if values else int_value(default)
        result = list(fixed)
        for i in range(max(1, count)):
            result += [(tr("functions", field[0]).format(i + 1), field[1], field[2]) for field in member]
        return result

    return rows


def geometry_rows(dim, values):
    """平面 / 立体几何的行：名称、对象类型、创建方式，其后为该创建方式的参数。

    名称行的默认值由 _Spec.name_default 依所选对象类型生成，故此处留空。
    """

    table = GEOMETRY[dim]
    types = list(table)
    obj_type = values[1] if values and values[1] in table else types[0]
    methods = table[obj_type]
    titles = [method[0] for method in methods]
    method_title = values[2] if values and values[2] in titles else titles[0]
    params = next(method[1] for method in methods if method[0] == method_title)

    rows = [
        ("名称", "", VALUE),
        ("几何对象类型", types, SELECT),
        ("创建方式", titles, SELECT),
    ]
    return rows + expand_rows(params, values, len(rows))


def expand_rows(params, values, offset):
    """展开某个创建方式 / 运算的参数行：含 {} 的变长行按数量行的取值重复。"""

    count = 3
    for i, field in enumerate(params):
        row = offset + i
        if field[2] == QUANTITY and values and len(values) > row:
            count = max(3, int_value(values[row], field[1]))

    rows = []
    for field in params:
        if "{}" in field[0]:
            rows += [(tr("functions", field[0]).format(i + 1), field[1], field[2]) for i in range(count)]
        else:
            rows.append(field)
    return rows


def geometry_op_rows(dim, values):
    """平面 / 立体几何计算的行：对象类型、计算方式，其后为该运算的参数。"""

    table = OPS[dim]
    types = list(table)
    obj_type = values[0] if values and values[0] in table else types[0]
    operations = table[obj_type]
    titles = [operation[0] for operation in operations]
    op_title = values[1] if values and values[1] in titles else titles[0]
    params = next(operation[2] for operation in operations if operation[0] == op_title)

    rows = [
        ("几何对象类型", types, SELECT),
        ("计算方式", titles, SELECT),
    ]
    return rows + expand_rows(params, values, len(rows))


def triangle_rows():
    """解三角形的输入行：三组「条件类型 + 条件值」。"""

    rows = []
    for i in (1, 2, 3):
        rows.append((tr("functions", "条件{}类型").format(i), TRIANGLE_PARTS, SELECT))
        rows.append((tr("functions", "条件{}值").format(i), "", VALUE))
    return rows


def calc_rows(values):
    """代数式计算的行：计算引擎、表达式，Mpmath 引擎另有精度。"""

    engine = values[0] if values and values[0] in CALC_ENGINE_NAMES else CALC_ENGINE_NAMES[0]
    rows = [
        ("计算引擎", CALC_ENGINE_NAMES, SELECT),
        ("表达式", "", VALUE),
    ]
    if engine == CALC_ENGINE_NAMES[1]:
        rows.append(("精度", "16", VALUE))
    return rows


def transform_rows(values):
    """代数式变形的行：变形方法、表达式，主元 / 换元按方法追加。"""

    method = values[0] if values and values[0] in TRANSFORM_NAMES else TRANSFORM_NAMES[0]
    rows = [
        ("变形方法", TRANSFORM_NAMES, SELECT),
        ("表达式", "", VALUE),
    ]
    if method == TRANSFORM_NAMES[TRANSFORM_PIVOT]:
        rows.append(("主元符号", "x", VALUE))
    elif method == TRANSFORM_NAMES[TRANSFORM_SUBST]:
        rows += [("主元符号", "x", VALUE), ("换元符号", "t", VALUE), ("换元表达式", "x+1", VALUE)]
    return rows


# ==================== 输入表引擎 ====================

class _InputTable:
    """输入表格控制器：定义区与计算区共用。

    按规格生成行控件、缓存各选择组合下的取值，并在下拉框 / 数量行变化时重建表格。
    """

    def __init__(self, page, table, specs, on_preview = None, on_return = None):
        self.page = page
        self.table = table
        self.specs = specs
        self.on_preview = on_preview
        self.on_return = on_return
        self.index = 0
        self.cache = {}
        self.keys = {}
        self.key = ()

    def spec(self):
        return self.specs[self.index]

    def rows(self, values = None):
        """当前类型的行定义；values 为 None 时按默认组合生成。"""

        if values is None:
            values = self.values()
        return self.spec().rows(values)

    def values(self):
        """当前选择组合下的取值缓存，缺失时按该组合的默认值初始化。"""

        store = self.cache.setdefault(self.index, {})
        if self.key not in store:
            rows = self.spec().rows(self.seed_values(self.key))
            values = [field_text(field) for field in rows]
            # 下拉框行取当前所选组合（field_text 只给出首项）
            for pos, row in enumerate(self.spec().selects):
                if row < len(values):
                    values[row] = self.key[pos]
            if self.spec().name_default is not None:
                values[0] = self.spec().name_default(values)
            store[self.key] = values
        return store[self.key]

    def initial_key(self):
        """该类型的默认选择组合。"""

        rows = self.spec().rows(None)
        return tuple(field_text(rows[row]) for row in self.spec().selects)

    def seed_values(self, key):
        """按给定的选择组合生成一份取值模板（仅用于推导后续下拉框的选项）。"""

        values = [field_text(field) for field in self.spec().rows(None)]
        for pos, row in enumerate(self.spec().selects):
            if row < len(values):
                values[row] = key[pos]
        return values

    def current_key(self, changed_row):
        """由下拉框控件推导选择组合。

        改动行之前的下拉框沿用原值，改动行读控件取值，其后的下拉框则按新组合
        重新取首项（改动后其选项列表尚未重建，控件里仍是被替换掉的旧选项）。
        """

        spec = self.spec()
        key = list(self.key)
        for pos, row in enumerate(spec.selects):
            if row < changed_row:
                continue
            if row > changed_row:
                probe = spec.rows(self.seed_values(tuple(key)))
                key[pos] = field_text(probe[row])
                continue
            widget = self.table.cellWidget(row, 0)
            if isinstance(widget, QComboBox):
                key[pos] = source_text(widget)
        return tuple(key)

    def read(self):
        """把表格当前取值写回缓存（下拉框行的取值由组合键决定，不在此缓存）。"""

        values = self.values()
        selects = self.spec().selects
        for i in range(min(self.table.rowCount(), len(values))):
            if i not in selects:
                values[i] = get_cell_text(self.table, i)

    def fill(self, index = None, reset = False, keep_rows = 0, blank_name = False):
        """重建表格：重设行数与行标题，逐行生成控件并回填缓存取值。"""

        if index is not None:
            self.keys[self.index] = self.key
            self.index = index
            self.key = self.keys.get(index) or self.initial_key()
        if reset:
            clear_table(self.table)

        spec = self.spec()
        values = self.values()
        rows = spec.rows(values)
        # 默认名称已被占用时留空，避免保存时静默覆盖已有对象
        if blank_name and values[0] in self.page.occupied_names(spec):
            values[0] = ""

        self.table.setRowCount(len(rows))
        self.table.setVerticalHeaderLabels([tr("functions", row[0]) for row in rows])

        for i, field in enumerate(rows):
            if i < keep_rows and self.table.cellWidget(i, 0) is not None:
                continue
            widget = self.page.make_cell_widget(field, spec)
            widget.setFixedHeight(self.table.rowHeight(i))
            set_widget_text(widget, values[i] if i < len(values) else field_text(field))
            self.table.setCellWidget(i, 0, widget)
            if self.on_preview is not None:
                connect_cell_clicked(widget, lambda w=widget: self.on_preview(w))
            if self.on_return is not None and isinstance(widget, QLineEdit):
                widget.returnPressed.connect(self.on_return)
            connect_cell_wheel(widget, self.table)
            connect_cell_changed(widget, lambda *_args, w=widget: self.on_changed(w))

    def reset(self):
        """丢弃当前选择组合下的取值缓存（选择组合本身保留）。"""

        self.cache.setdefault(self.index, {}).pop(self.key, None)

    def on_changed(self, widget):
        """单元格内容变化：下拉框切换组合，数量行改变行数，其余触发预览。"""

        spec = self.spec()
        rows = spec.rows(self.values())
        row = self.row_of(widget)
        if row < 0 or row >= len(rows):
            return

        if row in spec.selects:
            self.read()
            self.key = self.current_key(row)
            self.fill()
        elif rows[row][2] == QUANTITY:
            self.values()[row] = get_cell_text(self.table, row)
            self.resize(row)
            self.fill(keep_rows = row + 1)
        elif self.on_preview is not None:
            self.on_preview(widget)

    def resize(self, row):
        """按数量行的新取值调整其后的行缓存，保留已填内容。"""

        values = self.values()
        start = row + 1
        values[start:] = [get_cell_text(self.table, start + i)
                          for i in range(len(values) - start)]
        rows = self.spec().rows(values)
        values[start:] = values[start:][:len(rows) - start]
        while len(values) < len(rows):
            values.append(field_text(rows[len(values)]))

    def row_of(self, widget):
        """控件所在的行号，未找到时返回 -1。"""

        for row in range(self.table.rowCount()):
            if self.table.cellWidget(row, 0) is widget:
                return row
        return -1


# ==================== 几何对象构造 ====================

def need(value, label):
    """取值缺失时抛出带名称的错误。"""

    if value is None:
        raise ValueError(tr("functions", "未找到") + label)
    return value


def plane_module():
    from functions import planes
    return planes


def solid_module():
    from functions import solids
    return solids


def resolve_args(params, values, lookup):
    """把行的取值按角色解析为实参。

    数量行只用于展开行数，不作为实参；含 {} 的参数行从当前位置一直取到末尾。
    """

    args = []
    index = 0
    for field in params:
        role = field[2]
        if role == QUANTITY:
            index += 1
            continue
        if "{}" in field[0]:
            for value in values[index:]:
                args.append(resolve_one(role, value, lookup))
            index = len(values)
            continue
        args.append(resolve_one(role, values[index], lookup))
        index += 1
    return args


def resolve_one(role, value, lookup):
    """解析单个取值：表达式原样返回，整数转 int，对象按名称查找。"""

    if role == VALUE:
        return value
    if role == INTEGER:
        return int(value)
    label = tr("functions", ROLE_CATEGORY[role]) + " '" + str(value) + "'"
    return need(lookup(role, value), label)


def build_geometry(dim, obj_type, method_title, values, fs, lookup):
    """按创建方式构造几何对象，返回 (类别, 对象)。"""

    params, category, func_name = geometry_method(dim, obj_type, method_title)

    if func_name == "perpendicular_bisector":
        seg = need(lookup(SEGMENT, values[0]), tr("functions", "线段") + " '" + values[0] + "'")
        return category, plane_module().perpendicular_bisector(seg.points[0], seg.points[1])

    if func_name == "perpendicular_line_from_point":
        pt = need(lookup(POINT, values[0]), tr("functions", "点") + " '" + values[0] + "'")
        line = need(lookup(LINE, values[1]), tr("functions", "直线") + " '" + values[1] + "'")
        solids = solid_module()
        return category, solids.create_line3d(pt, solids.perpendicular_foot_to_line_3d(pt, line))

    if func_name == "create_polygon":
        return category, plane_module().create_polygon(resolve_args(params, values, lookup))

    args = resolve_args(params, values, lookup)
    module = plane_module() if dim == "plane" else solid_module()
    func = getattr(module, func_name)
    if func_name in _NEEDS_FS:
        return category, func(*args, fs)
    return category, func(*args)


def geometry_method(dim, obj_type, method_title):
    """查表取出某创建方式的参数表、结果类别与构造函数名。"""

    methods = GEOMETRY[dim].get(obj_type)
    if not methods:
        raise ValueError(tr("functions", "未知几何对象类型：") + str(obj_type))
    for method in methods:
        if method[0] == method_title:
            return method[1], method[2], method[3]
    raise ValueError(tr("functions", "未知创建方式：") + str(method_title))


def describe(obj):
    """几何对象的可读描述：点给坐标、线段给端点，其余给方程。"""

    if hasattr(obj, "equation"):
        try:
            return str(obj.equation())
        except Exception:
            pass
    if hasattr(obj, "x") and hasattr(obj, "y"):
        if hasattr(obj, "z"):
            return "({}, {}, {})".format(obj.x, obj.y, obj.z)
        return "({}, {})".format(obj.x, obj.y)
    points = getattr(obj, "points", None)
    if points is not None and len(points) == 2:
        return describe(points[0]) + " " + describe(points[1])
    return str(obj)


# ==================== 几何计算 ====================

def line_points(line):
    """取直线的两个端点（求距离、夹角一类运算需要点而不是直线）。"""

    return line.points[0], line.points[1]


def plane_op(key, args, fs):
    """执行平面几何运算：args 已按行角色解析为几何对象或表达式字符串。"""

    from functions import planes
    from sympy import radsimp, simplify

    if key == "circle_center":
        circle = args[0]
        return (radsimp(circle.center.x), radsimp(circle.center.y))
    if key == "circle_radius":
        return radsimp(args[0].radius)
    if key == "circle_area":
        return radsimp(args[0].area)
    if key == "circle_circumference":
        return radsimp(args[0].circumference)
    if key == "circle_intersection":
        points = args[0].intersection(args[1])
        return [(radsimp(pt.x), radsimp(pt.y)) for pt in points] or tr("functions", "两圆不相交")
    if key == "circle_tangent_lines":
        lines = args[1].tangent_lines(args[0])
        return [simplify(line.equation()) for line in lines] or tr("functions", "无切线")
    if key in _TRIANGLE_OPS:
        return getattr(planes, key)(*args[0].vertices)
    if key in ("collinear_check", "polygon_area_func", "polygon_perimeter_func"):
        return getattr(planes, key)(args)
    if key in _LINE_PAIR_OPS:
        return getattr(planes, key)(*line_points(args[0]), *line_points(args[1]))
    if key in _LINE_POINT_OPS:
        return getattr(planes, key)(args[0], *line_points(args[1]))
    if key in _FS_OPS:
        return getattr(planes, key)(*args, fs)
    return getattr(planes, key)(*args)


def solid_op(key, args, fs):
    """执行立体几何运算：args 已按行角色解析为几何对象或表达式字符串。"""

    from functions import solids

    if key == "are_coplanar":
        return solids.are_coplanar(args)
    return getattr(solids, key)(*args)


def compute_geometry(dim, obj_type, op_title, args, fs):
    """按维度分派到平面 / 立体几何的运算。"""

    operations = OPS[dim].get(obj_type)
    if not operations:
        raise ValueError(tr("functions", "未知几何对象类型：") + str(obj_type))
    for operation in operations:
        if operation[0] == op_title:
            return (plane_op if dim == "plane" else solid_op)(operation[1], args, fs)
    raise ValueError(tr("functions", "未知计算方式：") + str(op_title))


def op_params(dim, obj_type, op_title):
    """取某运算的参数行定义。"""

    for operation in OPS[dim].get(obj_type, []):
        if operation[0] == op_title:
            return operation[2]
    raise ValueError(tr("functions", "未知计算方式：") + str(op_title))


# ==================== 功能集成页 ====================

class Functions(QWidget, Ui_functions):
    """功能集成页：定义区与计算区共用一套输入表引擎。"""

    def __init__(self, parent, fs):
        super(Functions, self).__init__(parent)
        self.setupUi(self)

        # 1. 初始化对象字典
        self.fs = parent.fs
        self.vs = parent.vs
        self.ss = parent.ss
        self.geo_plane_dict = {}
        self.geo_solid_dict = {}
        self.parent = parent
        if not hasattr(parent, "pjs"):
            parent.pjs = {}
        if not hasattr(parent, "ljs"):
            parent.ljs = {}

        # 2. 初始化预览定时器
        self.def_preview_text = ""
        self.def_preview_timer = QTimer(self)
        self.def_preview_timer.setSingleShot(True)
        self.def_preview_timer.setInterval(250)
        self.def_preview_timer.timeout.connect(self.update_def_preview)

        # 3. 初始化定义区输入表
        self.specify_row_height(self.def_input)
        self.def_table = _InputTable(self, self.def_input, self.make_def_specs(),
                                     self.schedule_def_preview, self.click_def_save)
        self.def_table.fill(0)
        self.populate_def_combo()

        # 4. 初始化计算区输入表
        self.specify_row_height(self.calc_input)
        self.calc_table = _InputTable(self, self.calc_input, self.make_calc_specs(),
                                      on_return = self.click_calc_calc)
        self.calc_table.fill(0)
        self.populate_calc_combo()

        # 5. 初始化绘图区
        self.draw_canvas = None
        self.draw_toolbar = None
        self.object_snapshot = ()
        self.calc_value = None
        self.draw_layout = QVBoxLayout(self.draw_output)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)
        # 画布占据主要空间，对象列表保持较小的可滚动区域
        self.verticalLayout.setStretchFactor(self.draw_objs, 1)
        self.verticalLayout.setStretchFactor(self.draw_output, 3)
        # 树状列表第一列容纳对象名与属性名，初始给宽一些避免显示不全
        self.def_objs.setColumnWidth(0, 220)
        setGraphicsViewTheme(self, parent)
        self.populate_draw_combo()
        self.update_draw_objs()

        # 6. 指定槽函数
        self.def_type.currentIndexChanged.connect(self.update_def_input)
        self.def_save.clicked.connect(self.click_def_save)
        self.def_clear.clicked.connect(self.clear_def_input)
        self.def_edit.clicked.connect(self.click_def_edit)
        self.def_del.clicked.connect(self.click_def_del)
        self.def_objs.itemClicked.connect(self.preview_def_item)
        self.def_preview_mode.currentIndexChanged.connect(lambda *_: self.update_def_preview())
        self.calc_function.currentIndexChanged.connect(self.update_calc_input)
        self.calc_clear.clicked.connect(self.clear_calc_input)
        self.calc_calc.clicked.connect(self.click_calc_calc)
        self.draw_mode.currentIndexChanged.connect(self.update_draw_objs)
        self.draw_draw.clicked.connect(self.draw_objects)

        # 7. 三个区域之间可拖拽调整宽度
        self.area_splitter = self.enable_area_splitter()
        self.area_splitter_ready = False

    def enable_area_splitter(self):
        """把定义区、计算区、绘图区放进水平分割器，便于拖拽调整各区宽度。

        .ui 中三个区域是顶层网格布局的三个列，搬进分割器后初始宽度仍按原来的
        比例（定义区略宽、绘图区次之）；把手取6 像素便于拖拽，子控件不可折叠，
        避免某个区域被拖到看不见。样式沿用当前主题调色板，明暗主题都协调。
        """

        layout = self.layout()
        boxes = (self.def_groupbox, self.calc_groupbox, self.draw)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setObjectName("area_splitter")
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(6)
        for box, weight in zip(boxes, AREA_WEIGHTS):
            layout.removeWidget(box)
            splitter.addWidget(box)
            # 伸缩因子与初始权重一致，窗口缩放时三区比例得以保持
            splitter.setStretchFactor(splitter.count() - 1, weight * 100)
        splitter.setSizes([1] * len(boxes))
        layout.addWidget(splitter, 0, 0, 1, max(layout.columnCount(), 1))
        return splitter

    def reset_area_sizes(self):
        """按权重重新分配三个区域的宽度（首次显示时布局已就绪，setSizes 才会生效）。"""

        splitter = self.area_splitter
        boxes = (self.def_groupbox, self.calc_groupbox, self.draw)
        avail = splitter.width() - (len(boxes) - 1) * splitter.handleWidth()
        if avail <= 0:
            return
        sizes = [max(int(avail * weight), box.minimumSizeHint().width())
                 for weight, box in zip(AREA_WEIGHTS, boxes)]
        splitter.setSizes(sizes)

    def specify_row_height(self, table):
        """设定输入表的行高与悬停样式。

        行高固定为控件的自然高度：随表格可用高度伸缩时单元格控件会被拉伸或压缩
        （下拉框尤其明显）。同时取消行悬停高亮，鼠标扫过表格时不会出现单元格被
        选中的观感。
        """

        probes = (QComboBox(self), QLineEdit(self), QSpinBox(self))
        height = max(probe.sizeHint().height() for probe in probes)
        for probe in probes:
            probe.deleteLater()

        header = table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        header.setDefaultSectionSize(height + 2)

        table.setStyleSheet("QTableWidget::item:hover { background: transparent; }")

    def geometry_snapshot(self):
        """已定义对象的快照（函数名 + 几何对象的名称与类别），用于判断列表是否需要刷新。"""

        return (tuple(sorted(self.parent.fs)),
                tuple(sorted((name, value[0])
                            for name, value in self.parent.pjs.items())),
                tuple(sorted((name, value[0])
                             for name, value in self.parent.ljs.items())))

    def showEvent(self, event):
        """切换至本页时同步对象列表与参数下拉框（仅在对象集合变化时重建）。"""

        super().showEvent(event)
        # 首次显示时按权重定尺寸：此时布局已完成，setSizes 才会生效
        if not self.area_splitter_ready:
            self.area_splitter_ready = True
            self.reset_area_sizes()
        if self.geometry_snapshot() != self.object_snapshot:
            self.refresh_objects()

    def refresh_def_objects(self):
        """几何对象集合变化后重建定义表，使参数下拉框的选项同步。"""

        self.def_table.read()
        self.def_table.fill(reset = True)

    def refresh_calc_objects(self):
        """几何对象集合变化后重建计算表，使参数下拉框的选项同步。"""

        self.calc_table.read()
        self.calc_table.fill(reset = True)

    def refresh_objects(self):
        """几何对象集合变化后同步绘图列表与两区的对象下拉框。"""

        self.update_draw_objs()
        self.refresh_def_objects()
        self.refresh_calc_objects()

    def make_def_specs(self):
        """定义区的全部类型：函数 / 集合 / 向量为固定行，平面 / 立体几何随创建方式变化。"""

        return [
            _Spec("函数", [
                ("名称", "f", VALUE),
                ("表达式", "", VALUE),
                ("定义域", "Reals", VALUE),
                ("自变量", "x", VALUE),
            ], store = self.fs),
            _Spec("集合", [
                ("名称", "set", VALUE),
                ("表达式", "", VALUE),
            ], store = self.ss),
            _Spec("向量", [
                ("名称", "vec", VALUE),
                ("x", "", VALUE),
                ("y", "", VALUE),
            ], store = self.vs),
            _Spec("平面几何", lambda values: geometry_rows("plane", values),
                  store = self.geo_plane_dict, selects = (1, 2), dim = "plane",
                  name_default = lambda values: self.free_name("plane", values)),
            _Spec("立体几何", lambda values: geometry_rows("solid", values),
                  store = self.geo_solid_dict, selects = (1, 2), dim = "solid",
                  name_default = lambda values: self.free_name("solid", values)),
        ]

    def free_name(self, dim, values):
        """所选对象类型下一个可用的默认名称：前缀 + 序号（序号从 1 开始）。"""

        table = GEOMETRY[dim]
        obj_type = values[1] if len(values) > 1 and values[1] in table else next(iter(table))
        base = NAME_PREFIX.get(obj_type)
        if base is None:
            return ""

        store = self.parent.pjs if dim == "plane" else self.parent.ljs
        used = {name for name, value in store.items() if value[0] == obj_type}
        number = 1
        while base + str(number) in used:
            number += 1
        return base + str(number)

    def make_calc_specs(self):
        """计算区的全部类型：几何计算随「对象类型 + 计算方式」变化，
        方程组 / 不等式组的成员行按数量重复。"""

        equation = [("方程{}左式", "", VALUE), ("方程{}右式", "0", VALUE)]
        inequality = [("不等式{}左式", "", VALUE), ("不等式{}不等号", ["!=", ">", ">=", "<", "<="], SELECT),
                      ("不等式{}右式", "0", VALUE)]
        return [
            _Spec("计算", lambda values: calc_rows(values), selects = (0,)),
            _Spec("求导", [("表达式", "", VALUE), ("求导变量", "x", VALUE), ("求导次数", "1", VALUE)]),
            _Spec("积分", [("表达式", "", VALUE), ("积分变量", "x", VALUE)]),
            _Spec("解方程", [("左式", "", VALUE), ("右式", "0", VALUE),
                          ("求解变量", "x", VALUE), ("求解定义域", "Reals", VALUE)]),
            _Spec("解不等式", [("左式", "", VALUE), ("不等号", ["!=", ">", ">=", "<", "<="], SELECT),
                            ("右式", "0", VALUE), ("求解变量", "x", VALUE),
                            ("求解定义域", "Reals", VALUE)]),
            _Spec("解方程组", group_rows([("方程数量", 2, QUANTITY), ("求解变量", "x,y", VALUE)], equation)),
            _Spec("解不等式组", group_rows([("不等式数量", 2, QUANTITY), ("求解变量", "x", VALUE)], inequality)),
            _Spec("平面计算", lambda values: geometry_op_rows("plane", values),
                  selects = (0, 1), dim = "plane"),
            _Spec("立体计算", lambda values: geometry_op_rows("solid", values),
                  selects = (0, 1), dim = "solid"),
            _Spec("变形", lambda values: transform_rows(values), selects = (0,)),
            _Spec("解三角形", triangle_rows()),
        ]

    def populate_def_combo(self):
        """补齐定义类型下拉框与树状列表的类型节点（.ui 中只有前三项）。"""

        while self.def_type.count() < len(DEF_TYPE_NAMES):
            self.def_type.addItem("")
        for i, name in enumerate(DEF_TYPE_NAMES):
            self.def_type.setItemText(i, tr("functions", name))

        while self.def_objs.topLevelItemCount() < len(DEF_TYPE_NAMES):
            QTreeWidgetItem(self.def_objs)
        sorting = self.def_objs.isSortingEnabled()
        self.def_objs.setSortingEnabled(False)
        for i, name in enumerate(DEF_TYPE_NAMES):
            self.def_objs.topLevelItem(i).setText(0, tr("functions", name))
        self.def_objs.setSortingEnabled(sorting)

    def populate_calc_combo(self):
        """补齐计算功能下拉框（.ui 中只有前五项）。"""

        while self.calc_function.count() < len(CALC_FUNCTION_NAMES):
            self.calc_function.addItem("")
        for i, name in enumerate(CALC_FUNCTION_NAMES):
            self.calc_function.setItemText(i, tr("functions", name))

    def retranslateUi(self, widget):
        """语言切换时重刷各下拉框并重建表格（行标题随语言变化）。"""

        super().retranslateUi(widget)
        if not hasattr(self, "def_table"):
            return
        self.populate_def_combo()
        self.populate_calc_combo()
        self.populate_draw_combo()
        self.def_table.read()
        self.def_table.fill(reset = True)
        self.calc_table.read()
        self.calc_table.fill(reset = True)
        self.update_def_objs()

    def object_names(self, spec, role):
        """当前维度下某类别已定义几何对象的名称列表。"""

        if spec is None or spec.dim is None:
            return []
        store = self.parent.pjs if spec.dim == "plane" else self.parent.ljs
        return [name for name, value in store.items()
                if value[0] == ROLE_CATEGORY[role]]

    def occupied_names(self, spec):
        """该类型下已被占用的名称集合（几何类型取 pjs / ljs，其余取自身字典）。"""

        if spec.dim is None:
            return spec.store
        return self.parent.pjs if spec.dim == "plane" else self.parent.ljs

    def make_cell_widget(self, field, spec = None):
        """按行的角色生成单元格控件。

        SELECT：固定选项下拉框；几何对象角色（点 / 直线 / 线段 / 三角形 / 平面）：
        以已定义对象名称作为选项的下拉框；QUANTITY：数字框；其余：输入框。
        """

        title, default, role = field
        if role == SELECT:
            combo = QComboBox(self)
            for option in default:
                combo.addItem(tr("functions", option), option)
            return combo

        if role in ROLE_CATEGORY:
            combo = QComboBox(self)
            for name in self.object_names(spec, role):
                combo.addItem(name, name)
            return combo

        if role == QUANTITY:
            spin = QSpinBox(self)
            spin.setRange(1, 20)
            return spin

        lineedit = QLineEdit(str(default), self)

        def action(index):
            def run(*_args):
                if index == 0:
                    open_formula_dialog(lineedit)
                elif index == 1:
                    open_cache(lineedit)
                else:
                    self.parent._on_insert_cache(lineedit)
            return run

        lineedit.input_action = QAction(QIcon.fromTheme("input-keyboard"), tr("MainWindow", "可视化输入"), lineedit)
        lineedit.input_action.triggered.connect(action(0))
        lineedit.addAction(lineedit.input_action, QLineEdit.TrailingPosition)
        lineedit.cache_action = QAction(QIcon.fromTheme("document-open"), tr("MainWindow", "打开缓存区"), lineedit)
        lineedit.cache_action.triggered.connect(action(1))
        lineedit.addAction(lineedit.cache_action, QLineEdit.TrailingPosition)
        lineedit.insert_action = QAction(QIcon.fromTheme("list-add"), tr("MainWindow", "存入缓存区"), lineedit)
        lineedit.insert_action.triggered.connect(action(2))
        lineedit.addAction(lineedit.insert_action, QLineEdit.TrailingPosition)
        lineedit.actions_wired = True
        return lineedit

    def update_def_input(self, idx, is_temp = True):
        """切换定义区类型并重建输入表。"""

        # 1. 缓存当前类型的输入
        if is_temp:
            self.def_table.read()

        # 2. 切换类型并重建表格
        self.def_table.fill(idx, reset = True, blank_name = is_temp)

    def clear_def_input(self):
        """清空定义区输入表。"""

        # 1. 丢弃当前类型的缓存
        self.def_table.reset()

        # 2. 重建表格并写入默认值（默认名称被占用时留空）
        clear_table(self.def_input)
        self.def_table.fill(blank_name = True)

    # ========== 定义区保存 / 编辑 / 删除 ==========

    def def_values(self):
        """当前定义区表格的完整取值。"""

        return [get_cell_text(self.def_input, i) for i in range(self.def_input.rowCount())]

    def geo_lookup(self, dim):
        """几何对象查找：按角色与名称取出已创建的对象。"""

        store = self.parent.pjs if dim == "plane" else self.parent.ljs

        def lookup(role, name):
            name = name.strip()
            if name in store and store[name][0] == ROLE_CATEGORY[role]:
                return store[name][1]
            return None

        return lookup

    def click_def_save(self):
        """保存定义：几何类型按创建方式构造对象，其余直接存入对象字典。"""

        # 1. 提取输入的数据
        values = self.def_values()

        # 2. 检查数据是否完整
        if not all(values):
            QMessageBox.critical(self, "Error", tr("functions", "有参数未输入"), QMessageBox.StandardButton.Ok)
            return

        # 3. 几何类型：构造对象并存入 pjs / ljs，与独立标签页共用
        spec = self.def_table.spec()
        name = values[0].strip()
        if spec.dim is not None:
            try:
                category, obj = build_geometry(spec.dim, values[1], values[2], values[3:],
                                               self.fs, self.geo_lookup(spec.dim))
            except Exception as e:
                QMessageBox.warning(self, "Error", tr("functions", "创建几何对象失败：\n") + str(e))
                return
            if isinstance(obj, str):
                QMessageBox.warning(self, "Error", tr("functions", "创建几何对象失败：\n") + obj)
                return
            store = self.parent.pjs if spec.dim == "plane" else self.parent.ljs
            store[name] = (category, obj)

        # 4. 保存取值
        spec.store[name] = values

        # 5. 更新树状列表、同步各处对象下拉框并清空输入
        self.update_def_objs()
        self.update_draw_objs()
        self.refresh_calc_objects()
        self.clear_def_input()

    def click_def_edit(self):
        """编辑定义：把树中所选对象的取值载入输入表。"""

        # 1. 获取当前对象并检测是否为None
        current = self.def_objs.currentItem()
        if current is None:
            QMessageBox.warning(self, "Warning", tr("functions", "请先选择要编辑的对象"))
            return

        # 2. 判断选中项的层级，获取对象节点
        parent = current.parent()
        if parent is None:
            QMessageBox.warning(self, "Warning", tr("functions", "不能编辑类型节点，请选择具体的对象"))
            return
        obj = current if parent.parent() is None else parent

        item_type = self.def_type.findText(obj.parent().text(0))
        if item_type < 0:
            return

        # 3. 切换类型下拉框，并把该对象的取值写入缓存
        self.def_table.read()
        self.def_type.setCurrentIndex(item_type)
        spec = self.def_table.spec()
        values = spec.store.get(obj.text(0))
        if not values:
            return
        rows = spec.rows(values)
        self.def_table.key = tuple(values[row] for row in spec.selects)
        self.def_table.cache.setdefault(item_type, {})[self.def_table.key] = [
            values[i] if i < len(values) else field_text(rows[i]) for i in range(len(rows))
        ]

        # 4. 更新表格
        self.def_table.fill(blank_name = False)

    def click_def_del(self):
        """删除定义：同时移除几何类型在 pjs / ljs 中的对象。"""

        # 1. 获取当前对象并检测是否为None
        current = self.def_objs.currentItem()
        if current is None:
            QMessageBox.warning(self, "Warning", tr("functions", "请先选择要删除的对象"))
            return

        # 2. 判断选中项的层级，获取对象名称
        parent = current.parent()
        if parent is None:
            QMessageBox.warning(self, "Warning", tr("functions", "不能删除类型节点，请选择具体的对象"))
            return
        obj = current if parent.parent() is None else parent
        obj_name = obj.text(0)

        # 3. 从所有对象字典中删除
        deleted = False
        for spec in self.def_table.specs:
            if obj_name in spec.store:
                del spec.store[obj_name]
                deleted = True
        for dim in GEOMETRY:
            store = self.parent.pjs if dim == "plane" else self.parent.ljs
            if obj_name in store:
                del store[obj_name]
                deleted = True

        # 4. 反馈结果
        if deleted:
            QMessageBox.information(self, "Success", tr("functions", "删除成功"))
            self.update_def_objs()
            self.refresh_objects()
        else:
            QMessageBox.warning(self, "Failed", tr("functions", "删除失败，请检查您选中的是否为对象"))

    def update_def_objs(self):
        """更新树状列表（三层结构：类型 → 对象 → 属性）。"""

        def update_item(item, titles, values):
            while item.childCount() > len(values):
                item.removeChild(item.child(item.childCount() - 1))
            while item.childCount() < len(values):
                QTreeWidgetItem(item)
            for i, (title, value) in enumerate(zip(titles, values)):
                child = item.child(i)
                child.setText(0, title)
                child.setText(1, str(value))

        for index, spec in enumerate(self.def_table.specs):
            top_item = self.def_objs.topLevelItem(index)
            names = list(spec.store)
            for i in range(top_item.childCount() - 1, -1, -1):
                if top_item.child(i).text(0) not in names:
                    top_item.removeChild(top_item.child(i))
            existing = {top_item.child(i).text(0): top_item.child(i)
                        for i in range(top_item.childCount())}
            for name, values in spec.store.items():
                item = existing.get(name)
                if item is None:
                    item = QTreeWidgetItem([name, ""])
                    top_item.addChild(item)
                titles = [tr("functions", row[0]) for row in spec.rows(values)]
                update_item(item, titles, values)

    def preview_def_item(self, item, _column = 0):
        """点击树中的属性行时把该属性值渲染到预览框（类型层与对象层不处理）。"""

        # 1. 只处理第三层（对象 → 属性）
        if item is None or item.parent() is None or item.parent().parent() is None:
            return
        text = item.text(1).strip()
        if not text:
            return

        # 2. 渲染属性值：能解析为表达式则渲染 LaTeX，否则按原文显示
        expr = sympify(text, self.fs)
        setGraphicsView("", expr if isinstance(expr, str) else latex(expr), self.def_preview)
        self.def_output.setText(text)

    # ========== 定义区预览 ==========

    def preview_def_cell(self, source):
        """点击单元格时立即预览其内容。"""

        self.def_preview_text = source_text(source)
        self.def_preview_timer.stop()
        self.update_def_preview()

    def schedule_def_preview(self, source):
        """输入过程中触发预览：记下待预览文本并重置节流定时器。"""

        self.def_preview_text = source_text(source)
        self.def_preview_timer.start()

    def geo_preview_text(self, spec):
        """几何类型的预览文本：参数不全时为 ""，构造失败时为错误信息。"""

        values = self.def_values()
        if not values[0].strip() or not all(values[3:]):
            return ""
        try:
            _category, obj = build_geometry(spec.dim, values[1], values[2], values[3:],
                                            self.fs, self.geo_lookup(spec.dim))
        except Exception as e:
            return str(e)
        return obj if isinstance(obj, str) else describe(obj)

    def update_def_preview(self):
        """预览当前输入：几何类型预览所构造的对象，其余预览最后一次输入的表达式。"""

        # 1. 取出待预览文本
        spec = self.def_table.spec()
        if spec.dim is not None:
            text = self.geo_preview_text(spec)
            if text is None:
                return
            if text == "":
                setGraphicsView("", tr("functions", "请先填写全部参数"), self.def_preview)
                self.def_output.setText("")
                return
        else:
            text = self.def_preview_text
            if text == "":
                return

        # 2. 渲染预览
        try:
            expr = sympify(text, self.fs if self.def_preview_mode.currentIndex() == 1 else {})
        except Exception:
            setGraphicsView("", tr("functions", "不是合法的表达式"), self.def_preview)
            self.def_output.setText("")
            return
        if isinstance(expr, str):
            setGraphicsView("", expr, self.def_preview)
            self.def_output.setText(text)
            return
        setGraphicsView("", latex(expr), self.def_preview)
        self.def_output.setText(str(expr))

    # ========== 绘图区 ==========

    def draw_store(self):
        """当前绘图模式对应的对象字典与绘制函数。"""

        if self.draw_mode.currentIndex() == 0:
            from functions.paint2D import draw2d
            return self.parent.pjs, draw2d
        from functions.paint3D import draw3d
        return self.parent.ljs, draw3d

    def draw_list_entries(self):
        """当前绘图模式下列表中的条目：(名称, 类别或 None)。"""

        if self.draw_mode.currentIndex() == DRAW_FUNC_INDEX:
            return [(name, None) for name in self.parent.fs]
        return [(name, value[0]) for name, value in self.draw_store()[0].items()]

    def update_draw_objs(self):
        """按当前绘图模式刷新可绘制对象列表（默认全部勾选）。"""

        self.draw_objs.clear()
        for name, category in self.draw_list_entries():
            text = name if category is None else "[{}] {}".format(category, name)
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.draw_objs.addItem(item)
        self.object_snapshot = self.geometry_snapshot()

    def populate_draw_combo(self):
        """补齐绘图模式下拉框（.ui 中只有平面 / 立体两项）。"""

        while self.draw_mode.count() < len(DRAW_MODE_NAMES):
            self.draw_mode.addItem("")
        for i, name in enumerate(DRAW_MODE_NAMES):
            self.draw_mode.setItemText(i, tr("functions", name))

    def clear_draw(self):
        """销毁上次绘制的画布与导航工具栏。"""

        for widget in (self.draw_canvas, self.draw_toolbar):
            if widget is not None:
                self.draw_layout.removeWidget(widget)
                widget.deleteLater()
        self.draw_canvas = None
        self.draw_toolbar = None

    def draw_objects(self):
        """绘制列表中勾选的对象：几何模式画几何对象，函数模式画函数图像。"""

        # 1. 销毁上次的图表
        self.clear_draw()

        # 2. 函数模式单独处理
        if self.draw_mode.currentIndex() == DRAW_FUNC_INDEX:
            self.draw_function_graphs()
            return

        # 3. 收集勾选的对象
        store, painter = self.draw_store()
        objects = []
        for i in range(self.draw_objs.count()):
            item = self.draw_objs.item(i)
            if item.checkState() != Qt.CheckState.Checked:
                continue
            name = item.data(Qt.ItemDataRole.UserRole)
            if name in store:
                objects.append((store[name][1], {'label': name}))
        if not objects:
            return

        # 4. 绘制为 matplotlib 图表并嵌入绘图区
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from core.render import attach_plot_toolbar
        try:
            fig = painter(objects, figsize=(6.0, 5.1), dpi=100,
                          theme=getattr(self.parent, 'theme', 'light'))
            self.draw_canvas = FigureCanvas(fig)
            self.draw_toolbar = attach_plot_toolbar(self.draw_layout, self.draw_canvas,
                                                    self,
                                                    wheel_zoom=self.draw_mode.currentIndex() == 0)
            self.draw_layout.addWidget(self.draw_canvas)
        except Exception as e:
            self.clear_draw()
            QMessageBox.warning(self, "Error", tr("functions", "绘制时出错：\n") + str(e))

    def draw_function_graphs(self):
        """绘制列表中勾选的自定义函数图像。"""

        # 1. 解析勾选的函数表达式（可引用其他自定义函数）
        entries = []
        for i in range(self.draw_objs.count()):
            item = self.draw_objs.item(i)
            if item.checkState() != Qt.CheckState.Checked:
                continue
            name = item.data(Qt.ItemDataRole.UserRole)
            if name not in self.parent.fs:
                continue
            try:
                expr = sympify(self.parent.fs[name][1], self.parent.fs, is_simplify = True)
            except Exception as e:
                QMessageBox.warning(self, "Error",
                                    tr("functions", "绘制时出错：\n") + str(e))
                return
            entries.append((name, expr, self.parent.fs[name][3]))
        if not entries:
            return

        # 2. 绘制为 matplotlib 图表并嵌入绘图区
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from core.render import attach_plot_toolbar
        from functions.paint2D import draw_functions
        try:
            fig = draw_functions(entries, figsize=(6.0, 5.1), dpi=100,
                                 theme=getattr(self.parent, 'theme', 'light'))
            self.draw_canvas = FigureCanvas(fig)
            self.draw_toolbar = attach_plot_toolbar(self.draw_layout, self.draw_canvas,
                                                    self, wheel_zoom=True)
            self.draw_layout.addWidget(self.draw_canvas)
        except Exception as e:
            self.clear_draw()
            QMessageBox.warning(self, "Error", tr("functions", "绘制时出错：\n") + str(e))

    def set_theme(self, theme):
        """主题切换后按新配色重绘上次的图表（无绘图时为空操作）。"""

        if self.draw_canvas is not None:
            try:
                self.draw_objects()
            except Exception:
                pass

    # ========== 计算区 ==========

    def update_calc_input(self, idx, is_temp = True):
        """切换计算区类型并重建输入表。"""

        # 1. 缓存当前类型的输入
        if is_temp:
            self.calc_table.read()

        # 2. 切换类型并重建表格
        self.calc_table.fill(idx, reset = True)

    def clear_calc_input(self):
        """清空计算区输入表。"""

        # 1. 丢弃当前类型的缓存
        self.calc_table.reset()

        # 2. 重建表格并写入默认值
        clear_table(self.calc_input)
        self.calc_table.fill()

    def click_calc_calc(self):
        """按计算类型执行运算并渲染结果。"""

        # 1. 提取输入的数据
        inputs = [get_cell_text(self.calc_input, i) for i in range(self.calc_input.rowCount())]

        # 2. 检查数据是否完整
        if not all(inputs):
            QMessageBox.critical(self, "Error", tr("functions", "有参数未输入"), QMessageBox.StandardButton.Ok)
            return

        try:
            # 3. 根据计算类型执行运算
            as_latex, output = False, None
            if self.calc_table.index in CALC_GEO_INDEX:
                result = self.compute_geometry_result(inputs)
            elif self.calc_table.index == CALC_TRIANGLE_INDEX:
                result, output = self.solve_triangle(inputs)
                as_latex = True
            elif self.calc_table.index == CALC_TRANSFORM_INDEX:
                result = self.transform_algebra(inputs)
            elif self.calc_table.index == 0:
                result, as_latex, output = self.compute_algebra(inputs)
            elif self.calc_table.index == 1:
                from functions.derivative import derivative
                result = derivative(inputs[0], inputs[1], inputs[2], "", self.fs)
            elif self.calc_table.index == 2:
                from functions.integral import integral
                result = integral(inputs[0], inputs[1], self.fs)
            elif self.calc_table.index == 3:
                from functions.solvers import solve_fangcheng
                result = solve_fangcheng(Eq(sympify(inputs[0], self.fs), sympify(inputs[1], self.fs)),
                                         inputs[2], inputs[3], self.fs)
            elif self.calc_table.index == 4:
                from functions.solvers import solve_budengshi
                result = solve_budengshi(Rel(sympify(inputs[0], self.fs), sympify(inputs[2], self.fs), inputs[1]),
                                         inputs[3], inputs[4], self.fs)
            else:
                result = self.solve_group(inputs)

            # 4. 渲染结果至预览框
            text = result if as_latex else latex(result)
            if self.calc_table.index == 5:
                text = text.replace(':', "=")
            setGraphicsView("", text, self.calc_preview)
            self.calc_output.setText(output if output is not None else
                                     (text if as_latex else str(result)))
            self.calc_value = None if as_latex else result

            # 5. 「保存为」：名称栏已填写则随本次计算自动保存
            self.save_calc_result()

        # 6. 错误处理
        except Exception as e:
            self.calc_value = None
            setGraphicsView("", str(e), self.calc_preview)
            self.calc_output.setText(str(e))

    def save_calc_result(self):
        """把刚算出的结果按「保存为」栏中的名称存为自定义函数。

        名称栏为空表示本次不打算保存，静默跳过；已填写但保存不了时，分别按
        「结果不是表达式」与「名称已被占用」给出具体原因。
        """

        from sympy import Expr

        # 1. 未填名称则不处理
        name = self.calc_result.text().strip()
        if not name:
            return

        # 2. 结果不是表达式（几何对象、方程组解、Latex 代码等）
        if self.calc_value is None or not isinstance(self.calc_value, Expr):
            QMessageBox.critical(self, "Error",
                                 tr("functions", "该结果不是表达式，无法保存为函数"),
                                 QMessageBox.StandardButton.Ok)
            return

        # 3. 名称已被占用
        if name in self.fs:
            QMessageBox.critical(self, "Error",
                                 tr("functions", "名称已存在，请更换：") + name,
                                 QMessageBox.StandardButton.Ok)
            return

        # 4. 以结果的自由符号（缺省 x）作为自变量存入函数表
        symbols = sorted(self.calc_value.free_symbols, key = str)
        var = str(symbols[0]) if symbols else "x"
        self.fs[name] = [name, str(self.calc_value), "Reals", var]

        # 5. 同步定义区各处列表
        self.update_def_objs()
        self.refresh_objects()
        self.calc_result.clear()

    def compute_algebra(self, inputs):
        """按所选计算引擎计算代数式。

        返回 (结果, 结果是否已是 LaTeX, 输出框文本或 None)。
        Mpmath 的结果对象离开 workdps 后 str() 会退回默认精度，故输出文本在
        精度上下文内取出，与「计算」标签页一致。
        """

        from sympy import radsimp
        engine, expr = inputs[0], inputs[1]

        if engine == CALC_ENGINE_NAMES[0]:
            import sys
            sys.set_int_max_str_digits(0)
            return eval(expr), False, None

        if engine == CALC_ENGINE_NAMES[1]:
            import mpmath as mp
            from mpmath import (sin, cos, tan, cot, sec, csc, sinh, cosh, tanh, coth,
                                sech, csch, exp, log, ln, sqrt, root, pi, e, phi)
            with mp.workdps(int_value(inputs[2], 16)):
                result = eval(expr)
                text = str(result)
            return result, False, text

        if engine == CALC_ENGINE_NAMES[2]:
            import sys
            sys.set_int_max_str_digits(0)
            return radsimp(sympify(expr, self.fs, is_simplify = True)), False, None

        code = latex(sympify(expr, fs = {}))
        return code, True, code

    def transform_algebra(self, inputs):
        """按所选变形方法变形代数式。"""

        from functions.simplification import simplifies
        method = TRANSFORM_NAMES.index(inputs[0])
        zhuyuan = inputs[2] if len(inputs) > 2 else None
        huanyuan = inputs[3] if len(inputs) > 3 else None
        huanyuanshi = inputs[4] if len(inputs) > 4 else None
        return simplifies(inputs[1], method, zhuyuan, huanyuan, huanyuanshi, self.fs)

    def solve_triangle(self, inputs):
        """解三角形：返回 (LaTeX 结果, 输出文本)。

        inputs 每两个元素是一组「条件类型 + 条件值」，与「解三角形」标签页一致。
        """

        from functions.solvers import solve_sanjiaoxing

        # 1. 解析三组条件
        angles, sides = {}, {}
        for i in range(0, len(inputs) - 1, 2):
            index = TRIANGLE_PARTS.index(inputs[i])
            text = inputs[i + 1].strip()
            if index == 0 or not text:
                continue
            try:
                value = sympify(text, self.fs)
            except Exception:
                raise ValueError(tr("functions", "条件值格式错误"))
            # core.sympify 解析失败时返回字符串而非抛异常，需另行判断
            if isinstance(value, str):
                raise ValueError(tr("functions", "条件值格式错误"))
            key = TRIANGLE_KEYS[index]
            (angles if key.isupper() else sides)[key] = value
        if len(angles) + len(sides) != 3:
            raise ValueError(tr("functions", "请填入恰好3个有效且不重复的条件"))

        # 2. 求解
        result = solve_sanjiaoxing(angles, sides, self.fs)
        if not result:
            raise ValueError(tr("functions", "无解"))
        if isinstance(result, str):
            raise ValueError(result)

        # 3. 多解时逐条编号，结果与「解三角形」标签页排版一致
        lines, flat = [], []
        for i, (res_angles, res_sides) in enumerate(result):
            parts = ["{} = {}".format(k, latex(v)) for k, v in res_angles.items()]
            parts += ["{} = {}".format(k, latex(v)) for k, v in res_sides.items()]
            prefix = r"\text{" + tr("functions", "解") + "}" + str(i + 1) + r":\ " if len(result) > 1 else ""
            lines.append(prefix + r",\ ".join(parts))
            flat.append(" | ".join("{} = {}".format(k, v)
                                   for k, v in list(res_angles.items()) + list(res_sides.items())))
        return r" \\ ".join(lines), "  ||  ".join(flat)

    def compute_geometry_result(self, inputs):
        """按当前「对象类型 + 计算方式」对已定义几何对象执行运算。"""

        dim = CALC_GEO_INDEX[self.calc_table.index]
        obj_type, op_title = inputs[0], inputs[1]
        params = op_params(dim, obj_type, op_title)
        args = resolve_args(params, inputs[2:], self.geo_lookup(dim))
        return compute_geometry(dim, obj_type, op_title, args, self.fs)

    def solve_group(self, inputs):
        """求解方程组 / 不等式组（数量 + 求解变量 + 每项的左右式）。"""

        count = int_value(inputs[0])
        from functions.solvers import solve_fangchengzu, solve_budengshizu
        try:
            if self.calc_table.index == 5:
                equations = [Eq(sympify(inputs[2 + 2 * i], self.fs), sympify(inputs[3 + 2 * i], self.fs))
                             for i in range(count)]
                return solve_fangchengzu(equations, [Symbol(v.strip()) for v in inputs[1].split(',')], self.fs)
            relations = [Rel(sympify(inputs[2 + 3 * i], self.fs), sympify(inputs[4 + 3 * i], self.fs),
                             inputs[3 + 3 * i]) for i in range(count)]
            return solve_budengshizu(relations, Symbol(inputs[1].strip()), self.fs) \
                or tr("functions", "无解")
        except Exception:
            return tr("functions", "无解")
