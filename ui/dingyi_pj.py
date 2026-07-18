from ui.ui_dingyi_pj import *
from PySide6.QtWidgets import QWidget, QMessageBox
from core.render import setGraphicsView, setGraphicsViewTheme

class Dingyi_pj(QWidget, Ui_dingyi_pj):
    def __init__(self, parent, fs):
        super(Dingyi_pj, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

        self.fs = fs
        self.parent = parent

        if not hasattr(self.parent, 'pjs'):
            self.parent.pjs = {}  # {name: (类别, 对象, [元数据])}
            # 类别: "点","直线","线段","三角形","多边形","圆"

        self.pjs = self.parent.pjs

        # 下拉框选择方法后显示提示标签
        self.dingyi_pj_fangfa.currentIndexChanged.connect(self._on_method_changed)

        # 回车创建 / 点击"保存"按钮创建
        self.dingyi_pj_canshu.returnPressed.connect(self._do_create)
        self.dingyi_pj_baocun.clicked.connect(self._do_create)

        # 各列表的读取/删除按钮
        self.dingyi_pj_dian_read.clicked.connect(lambda: self._read_item("点"))
        self.dingyi_pj_dian_delete.clicked.connect(lambda: self._delete_item("点"))
        self.dingyi_pj_zhixian_read.clicked.connect(lambda: self._read_item("直线"))
        self.dingyi_pj_zhixian_delete.clicked.connect(lambda: self._delete_item("直线"))
        self.dingyi_pj_xianduan_read.clicked.connect(lambda: self._read_item("线段"))
        self.dingyi_pj_xianduan_delete.clicked.connect(lambda: self._delete_item("线段"))
        self.dingyi_pj_duobianxing_read.clicked.connect(lambda: self._read_item("三角形"))
        self.dingyi_pj_duobianxing_delete.clicked.connect(lambda: self._delete_item("三角形"))
        self.dingyi_pj_yuan_read.clicked.connect(lambda: self._read_item("圆"))
        self.dingyi_pj_yuan_delete.clicked.connect(lambda: self._delete_item("圆"))

        # 刷新全部列表
        self._refresh_all_lists()

    # ========== 方法索引 → 名称映射 ==========

    @staticmethod
    def _method_names():
        return [
            "未选择",
            "create_point",           # 1: x坐标, y坐标
            "create_line",            # 2: 点1名, 点2名
            "create_circle",          # 3: 圆心名, 半径
            "create_circle_three_points",  # 4: 点1名, 点2名, 点3名
            "create_triangle",        # 5: 点1名, 点2名, 点3名
            "create_polygon",         # 6: 点1名, 点2名, ..., 点n名
            "circle_with_diameter",   # 7: 点1名, 点2名
            "circle_by_center_and_point",  # 8: 点1名, 点2名
            "perpendicular_bisector",  # 9: 线段名
            "line_parallel_through_point",  # 10: 点名, 线段名
            "line_perpendicular_through_point",  # 11: 点名, 线段名
            "angle_bisector_line",    # 12: 直线名, 直线名
            "angle_bisector",         # 13: 点1名, 点2名, 点3名
            "triangle_median",        # 14: 三角形名, 顶点名(索引0,1,2)
            "triangle_altitude",      # 15: 三角形名, 顶点名(索引0,1,2)
            "triangle_midsegment",    # 16: 三角形名, 多余参数忽略
            "triangle_incircle",      # 17: 三角形名
            "triangle_excircle",      # 18: 三角形名, 顶点名(索引0,1,2)
            "segment_from_points",    # 19: 点1名, 点2名
        ]

    @classmethod
    def _method_params_hint(cls, idx):
        hints = {
            0:  "",
            1:  "x坐标, y坐标",
            2:  "点1名称, 点2名称",
            3:  "圆心名称, 半径",
            4:  "点1名称, 点2名称, 点3名称",
            5:  "点1名称, 点2名称, 点3名称",
            6:  "点1名称, 点2名称, ……",
            7:  "点1名称, 点2名称",
            8:  "圆心名称, 圆上点名称",
            9:  "线段名称",
            10: "点名, 线段名",
            11: "点名, 线段名",
            12: "直线1名称, 直线2名称",
            13: "点1名称, 点2名称(顶点), 点3名称",
            14: "三角形名称, 顶点索引(0/1/2)",
            15: "三角形名称, 顶点索引(0/1/2)",
            16: "三角形名称",
            17: "三角形名称",
            18: "三角形名称, 顶点索引(0/1/2)",
            19: "点1名称, 点2名称",
        }
        return hints.get(idx, "")

    def _on_method_changed(self, idx):
        hint = self._method_params_hint(idx)
        if idx > 0 and hint:
            self.label_2.setText("参数(" + hint + ")：")
        else:
            self.label_2.setText("参数(直接输入，以英文半角逗号分隔)：")

    # ========== 名称 → 对象 查找 ==========

    def _find_point(self, name):
        name = name.strip()
        if name in self.pjs and self.pjs[name][0] == "点":
            return self.pjs[name][1]
        return None

    def _find_line(self, name):
        name = name.strip()
        if name in self.pjs and self.pjs[name][0] == "直线":
            return self.pjs[name][1]
        return None

    def _find_segment(self, name):
        name = name.strip()
        if name in self.pjs and self.pjs[name][0] == "线段":
            return self.pjs[name][1]
        return None

    def _find_triangle(self, name):
        name = name.strip()
        if name in self.pjs and self.pjs[name][0] == "三角形":
            return self.pjs[name][1]
        return None

    def _find_circle(self, name):
        name = name.strip()
        if name in self.pjs and self.pjs[name][0] == "圆":
            return self.pjs[name][1]
        return None

    def _find_points(self, names_str):
        """将逗号分隔的点名称字符串解析为 Point 列表"""
        pts = []
        for n in names_str.split(','):
            p = self._find_point(n.strip())
            if p is None:
                raise ValueError(f"未找到点'{n.strip()}'")
            pts.append(p)
        return pts

    # ========== 对象存入与分类 ==========

    def _store(self, name, category, obj):
        """存入对象，同时更新 pjs 和各分类列表"""
        self.pjs[name] = (category, obj)
        self._refresh_all_lists()

    def _refresh_all_lists(self):
        """根据 pjs 刷新五个列表（仅显示对象名称）"""
        self.dingyi_pj_dian.clear()
        self.dingyi_pj_zhixian.clear()
        self.dingyi_pj_xianduan.clear()
        self.dingyi_pj_duobianxing.clear()
        self.dingyi_pj_yuan.clear()
        for name, val in self.pjs.items():
            cat = val[0]
            if cat == "点":
                self.dingyi_pj_dian.addItem(name)
            elif cat == "直线":
                self.dingyi_pj_zhixian.addItem(name)
            elif cat == "线段":
                self.dingyi_pj_xianduan.addItem(name)
            elif cat == "三角形" or cat == "多边形":
                self.dingyi_pj_duobianxing.addItem(name)
            elif cat == "圆":
                self.dingyi_pj_yuan.addItem(name)

    # ========== 创建核心逻辑 ==========

    def _do_create(self):
        idx = self.dingyi_pj_fangfa.currentIndex()
        if idx == 0:
            return
        name = self.dingyi_pj_mingcheng.text().strip()
        if not name:
            return
        params_str = self.dingyi_pj_canshu.text().strip()
        # 解析参数列表
        raw_params = [p.strip() for p in params_str.split(',')] if params_str else []

        try:
            from functions.planes import (
                create_point, create_line, create_circle, create_circle_three_points,
                create_triangle, create_polygon, circle_with_diameter, circle_by_center_and_point,
                perpendicular_bisector, line_parallel_through_point, line_perpendicular_through_point,
                angle_bisector_line, angle_bisector, triangle_median, triangle_altitude,
                triangle_midsegment, triangle_incircle, triangle_excircle, segment_from_points
            )
            from sympy import Point, Line

            if idx == 1:  # create_point: x, y
                if len(raw_params) < 2:
                    return
                pt = create_point(raw_params[0], raw_params[1], self.fs)
                self._store(name, "点", pt)

            elif idx == 2:  # create_line: point1_name, point2_name
                if len(raw_params) < 2:
                    return
                p1, p2 = self._find_points(raw_params[0] + "," + raw_params[1])
                line = create_line(p1, p2)
                self._store(name, "直线", line)

            elif idx == 3:  # create_circle: center_name, radius
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0])
                center = pts[0]
                c = create_circle(center, raw_params[1], self.fs)
                self._store(name, "圆", c)

            elif idx == 4:  # create_circle_three_points: p1, p2, p3
                if len(raw_params) < 3:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1] + "," + raw_params[2])
                c = create_circle_three_points(*pts)
                self._store(name, "圆", c)

            elif idx == 5:  # create_triangle: p1, p2, p3
                if len(raw_params) < 3:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1] + "," + raw_params[2])
                tri = create_triangle(*pts)
                self._store(name, "三角形", tri)

            elif idx == 6:  # create_polygon: p1, p2, ..., pn
                if len(raw_params) < 3:
                    return
                pts = self._find_points(",".join(raw_params))
                poly = create_polygon(pts)
                self._store(name, "多边形", poly)

            elif idx == 7:  # circle_with_diameter: p1, p2
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1])
                c = circle_with_diameter(*pts)
                self._store(name, "圆", c)

            elif idx == 8:  # circle_by_center_and_point:
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1])
                c = circle_by_center_and_point(pts[0], pts[1])
                self._store(name, "圆", c)

            elif idx == 9:  # perpendicular_bisector: 线段名
                if len(raw_params) < 1:
                    return
                seg = self._find_segment(raw_params[0])
                if seg is None:
                    return
                line = perpendicular_bisector(seg.points[0], seg.points[1])
                self._store(name, "直线", line)

            elif idx == 10:  # line_parallel_through_point: 点名, 线段名
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0])
                line_ref = self._find_line(raw_params[1]) or (
                    self._find_segment(raw_params[1]) and
                    Line(self._find_segment(raw_params[1]).points[0],
                         self._find_segment(raw_params[1]).points[1]))
                if line_ref is None:
                    return
                line = line_parallel_through_point(line_ref, pts[0])
                self._store(name, "直线", line)

            elif idx == 11:  # line_perpendicular_through_point: 点名, 线段名
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0])
                line_ref = self._find_line(raw_params[1]) or (
                    self._find_segment(raw_params[1]) and
                    Line(self._find_segment(raw_params[1]).points[0],
                         self._find_segment(raw_params[1]).points[1]))
                if line_ref is None:
                    return
                line = line_perpendicular_through_point(line_ref, pts[0])
                self._store(name, "直线", line)

            elif idx == 12:  # angle_bisector_line: 直线1名, 直线2名
                if len(raw_params) < 2:
                    return
                l1 = self._find_line(raw_params[0])
                l2 = self._find_line(raw_params[1])
                if l1 is None or l2 is None:
                    return
                result = angle_bisector_line(l1, l2)
                if isinstance(result, str):
                    return
                self._store(name, "直线", result)

            elif idx == 13:  # angle_bisector: p1, p2, p3
                if len(raw_params) < 3:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1] + "," + raw_params[2])
                line = angle_bisector(*pts)
                self._store(name, "直线", line)

            elif idx == 14:  # triangle_median: 三角形名, 顶点索引
                if len(raw_params) < 2:
                    return
                tri = self._find_triangle(raw_params[0])
                if tri is None:
                    return
                v_idx = int(raw_params[1])
                seg = triangle_median(tri, v_idx)
                self._store(name, "线段", seg)

            elif idx == 15:  # triangle_altitude: 三角形名, 顶点索引
                if len(raw_params) < 2:
                    return
                tri = self._find_triangle(raw_params[0])
                if tri is None:
                    return
                v_idx = int(raw_params[1])
                line = triangle_altitude(tri, v_idx)
                self._store(name, "直线", line)

            elif idx == 16:  # triangle_midsegment: 三角形名
                if len(raw_params) < 1:
                    return
                tri = self._find_triangle(raw_params[0])
                if tri is None:
                    return
                seg = triangle_midsegment(tri)
                self._store(name, "线段", seg)

            elif idx == 17:  # triangle_incircle: 三角形名
                if len(raw_params) < 1:
                    return
                tri = self._find_triangle(raw_params[0])
                if tri is None:
                    return
                c = triangle_incircle(tri)
                self._store(name, "圆", c)

            elif idx == 18:  # triangle_excircle: 三角形名, 顶点索引
                if len(raw_params) < 2:
                    return
                tri = self._find_triangle(raw_params[0])
                if tri is None:
                    return
                v_idx = int(raw_params[1])
                c = triangle_excircle(tri, v_idx)
                self._store(name, "圆", c)

            elif idx == 19:  # segment_from_points: p1, p2
                if len(raw_params) < 2:
                    return
                pts = self._find_points(raw_params[0] + "," + raw_params[1])
                seg = segment_from_points(*pts)
                self._store(name, "线段", seg)

        except Exception as e:
            QMessageBox.warning(self, "创建失败", f"创建对象时出错：\n{e}")

    # ========== 列表读取/删除 ==========
    _LIST_MAP = {
        "点":   "dingyi_pj_dian",
        "直线": "dingyi_pj_zhixian",
        "线段": "dingyi_pj_xianduan",
        "三角形": "dingyi_pj_duobianxing",
        "多边形": "dingyi_pj_duobianxing",
        "圆":   "dingyi_pj_yuan",
    }

    def _read_item(self, cat):
        """读取选中项到对象属性面板"""
        list_name = self._LIST_MAP.get(cat)
        if not list_name:
            return
        lst = getattr(self, list_name)
        item = lst.currentItem()
        if not item:
            return
        name = item.text().strip()
        if name not in self.pjs:
            return
        cat2, obj = self.pjs[name][0], self.pjs[name][1]
        self.dingyi_pj_shuxing_mingcheng.setText(name)
        try:
            eq = obj.equation() if hasattr(obj, 'equation') else None
            eq_str = str(eq) if eq is not None else str(obj)
        except:
            eq_str = str(obj)
        self.dingyi_pj_shuxing_fangcheng.setText(eq_str)

    def _delete_item(self, cat):
        """删除选中项"""
        list_name = self._LIST_MAP.get(cat)
        if not list_name:
            return
        lst = getattr(self, list_name)
        row = lst.currentRow()
        if row < 0:
            return
        name = lst.currentItem().text().strip()
        if name in self.pjs:
            del self.pjs[name]
        self._refresh_all_lists()
        # 清空属性面板
        self.dingyi_pj_shuxing_mingcheng.setText("")
        self.dingyi_pj_shuxing_fangcheng.setText("")