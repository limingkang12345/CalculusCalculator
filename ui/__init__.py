from ui.ui_main import *
from ui.ui_shouye import *
from ui.ui_dingyi import *
from ui.ui_qiudao import *
from ui.ui_jifen import *
from ui.ui_bianxing import *
from ui.ui_fangcheng import *
from ui.ui_fangchengzu import *
from ui.ui_budengshi import *
from ui.ui_budengshizu import *
from ui.ui_jisuan import *
from ui.ui_help import *
from ui.ui_dingyixiangliang import *
from ui.ui_huitu_hanshu import *
from ui.ui_jiesanjiaoxing import *
from ui.ui_dingyi_pj import *
from ui.ui_huitu_pj import *
from ui.ui_dingyi_lj import *
from ui.ui_huitu_lj import *
from ui.ui_pjjisuan import *
from ui.ui_ljjisuan import *

import resources_rc
from derivative import derivative, yinhanshu_derivative
from integral import integral
from simplification import simplifies
from solvers import solve_fangcheng, solve_weifenfangcheng, solve_fangchengzu, solve_budengshi, solve_budengshizu, solve_sanjiaoxing
from functions import get_function_attr

from sympy import latex, Eq, Rel, symbols, Symbol, radsimp, radsimp, simplify
from sympify import sympify

from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QListWidgetItem
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt

def setWebEngineView(n, l, w):
        # 显示表达式
        # n:函数名
        # l:要显示的Latex表达式
        # w:要设置的WebEngineView
        
        html = r'<html><head><script src="qrc:///MathJax/es5/tex-svg.js"></script></head><body><div><p style="font-size:34px">\({}{}\)</p></div></body></html>'.format(n, l)
        w.setHtml(html)

class Shouye(QWidget, Ui_shouye):
    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)

class Dingyi(QWidget, Ui_dingyi):
    def __init__(self, parent, fs):
        super(Dingyi, self).__init__(parent)
        self.setupUi(self)
        
        self.dingyi_hanshuliebiao.itemClicked.connect(self.read_function)
        self.dingyi_baocun.clicked.connect(self.save_function)
        self.dingyi_shanchu.clicked.connect(self.delete_function)
        self.dingyi_mingcheng.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_biaodashi.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_dingyiyu.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_zibianliang.returnPressed.connect(self.dingyi_baocun.click)
        self.dingyi_hanshushuxing_cbx.addItems(["表达式&定义域", "值域", "单调递增区间", "单调递减区间", "奇偶性", "周期", "最大值", "最小值"])
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.dingyi_hanshushuxing_cbx.currentIndexChanged.connect(self.update_function_attr)
        self.dingyi_zibianliangzhi.textChanged.connect(self.function_value)

        self.fs = fs
        self.parent = parent
        self.dingyi_hanshuliebiao.insertItems(0, list("{}({})".format(self.fs[i][0], self.fs[i][3]) for i in self.fs.keys()))

    def read_function(self, item):
        # 读取函数信息，显示在文本框中
        fn = item.text().split('(')[0]
        if fn != '':
            self.dingyi_mingcheng.setText(self.fs[fn][0])
            self.dingyi_biaodashi.setText(self.fs[fn][1])
            self.dingyi_dingyiyu.setText(self.fs[fn][2])
            self.dingyi_zibianliang.setText(self.fs[fn][3])
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def setdingyi_hanshushuxing_view(self):
        # 切换至定义页面渲染公式
        self.read_function(self.dingyi_hanshuliebiao.currentItem())

    def save_function(self):
        # 保存函数信息，显示在列表中
        if self.dingyi_mingcheng.text() not in self.fs.keys():
            self.dingyi_hanshuliebiao.insertItem(0, "{}({})".format(self.dingyi_mingcheng.text(), self.dingyi_zibianliang.text()))
            self.dingyi_hanshuliebiao.setCurrentRow(0)
        self.fs[self.dingyi_mingcheng.text()] = [self.dingyi_mingcheng.text(), self.dingyi_biaodashi.text(), self.dingyi_dingyiyu.text(), self.dingyi_zibianliang.text()]
        self.dingyi_hanshushuxing_cbx.setCurrentIndex(0)
        self.update_function_attr(0)
        self.function_value()

    def delete_function(self):
        # 删除相应的函数
        f = self.dingyi_hanshuliebiao.takeItem(self.dingyi_hanshuliebiao.currentRow())
        del f
        del self.fs[self.dingyi_mingcheng.text()]
        if self.fs != {}:
            self.read_function(self.dingyi_hanshuliebiao.currentItem())
        self.update_function_attr(0)
        self.function_value()

    def update_function_attr(self, attr):
        # 获取函数属性并显示
        function_attr = get_function_attr(self.dingyi_biaodashi.text(), self.dingyi_zibianliang.text(), self.dingyi_dingyiyu.text(), attr, self.fs)
        self.dingyi_hanshushuxing_lineedit.setText(str(function_attr))
        try:
            setWebEngineView('' if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else self.dingyi_hanshuliebiao.currentItem().text() + "=", \
                latex(function_attr) if self.dingyi_hanshushuxing_cbx.currentIndex() != 0 else latex(function_attr[0]) + '({}\\in {})'.format(self.dingyi_zibianliang.text(), latex(function_attr[1])), \
                self.dingyi_hanshushuxing)
        except:
            pass

    def function_value(self):
        # 根据给定自变量值求出函数值
        f_value = radsimp(sympify(self.dingyi_biaodashi.text(), self.fs).subs(symbols(self.dingyi_zibianliang.text()), sympify(self.dingyi_zibianliangzhi.text(), self.fs)))
        self.dingyi_qiuzhi_lineedit.setText(str(f_value))
        try:
            setWebEngineView("{}({})=".format(self.dingyi_mingcheng.text(), latex(sympify(self.dingyi_zibianliangzhi.text(), self.fs))), latex(f_value), self.dingyi_qiuzhi)
        except:
            pass

# 该类为AI生成
class Dingyixiangliang(QWidget, Ui_dingyixiangliang):
    def __init__(self, parent, fs):
        super(Dingyixiangliang, self).__init__(parent)
        self.setupUi(self)

        self.dingyixiangliang_xiangliangliebiao.itemClicked.connect(self.read_vector)
        self.dingyixiangliang_baocun.clicked.connect(self.save_vector)
        self.dingyixiangliang_shanchu.clicked.connect(self.delete_vector)
        self.dingyixiangliang_mingcheng.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self.dingyixiangliang_x.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self.dingyixiangliang_y.returnPressed.connect(self.dingyixiangliang_baocun.click)
        self.dingyixiangliang_xiangliangshuxing_cbx.addItems(["表达式", "模", "方向角", "单位向量"])
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.dingyixiangliang_xiangliangshuxing_cbx.currentIndexChanged.connect(self.update_vector_attr)
        self.dingyixiangliang_jisuanfangfa.addItems(["加法", "减法", "点积", "夹角"])
        self.dingyixiangliang_jisuanfangfa.setCurrentIndex(0)
        self.dingyixiangliang_jisuan_button.clicked.connect(self.compute_vector)

        self.fs = fs
        self.parent = parent

        if not hasattr(self.parent, 'vs'):
            self.parent.vs = {}
        self.vs = self.parent.vs

        self.update_vector_list()
        self.update_vector_combos()

    def update_vector_list(self):
        # 刷新向量列表
        self.dingyixiangliang_xiangliangliebiao.clear()
        self.dingyixiangliang_xiangliangliebiao.insertItems(0,
            list("{}=({}, {})".format(self.vs[n][0], self.vs[n][1], self.vs[n][2]) for n in self.vs.keys()))

    def update_vector_combos(self):
        # 刷新向量运算区的下拉框
        self.dingyixiangliang_xiangliang1.clear()
        self.dingyixiangliang_xiangliang2.clear()
        names = list(self.vs.keys())
        self.dingyixiangliang_xiangliang1.addItems(names)
        self.dingyixiangliang_xiangliang2.addItems(names)

    def read_vector(self, item):
        # 读取向量信息，显示在编辑区
        name = item.text().split('=')[0]
        if name in self.vs:
            self.dingyixiangliang_mingcheng.setText(self.vs[name][0])
            self.dingyixiangliang_x.setText(self.vs[name][1])
            self.dingyixiangliang_y.setText(self.vs[name][2])
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def save_vector(self):
        # 保存向量信息
        name = self.dingyixiangliang_mingcheng.text()
        x = self.dingyixiangliang_x.text()
        y = self.dingyixiangliang_y.text()
        if name not in self.vs:
            self.dingyixiangliang_xiangliangliebiao.insertItem(0, "{}=({}, {})".format(name, x, y))
            self.dingyixiangliang_xiangliangliebiao.setCurrentRow(0)
        self.vs[name] = [name, x, y]
        self.update_vector_combos()
        self.dingyixiangliang_xiangliangshuxing_cbx.setCurrentIndex(0)
        self.update_vector_attr(0)

    def delete_vector(self):
        # 删除向量
        row = self.dingyixiangliang_xiangliangliebiao.currentRow()
        if row < 0:
            return
        item = self.dingyixiangliang_xiangliangliebiao.takeItem(row)
        name = self.dingyixiangliang_mingcheng.text()
        if name in self.vs:
            del self.vs[name]
        del item
        self.update_vector_combos()
        if self.vs:
            self.read_vector(self.dingyixiangliang_xiangliangliebiao.currentItem())
        self.update_vector_attr(0)

    def update_vector_attr(self, attr):
        # 计算并显示向量属性
        x_str = self.dingyixiangliang_x.text()
        y_str = self.dingyixiangliang_y.text()
        name = self.dingyixiangliang_mingcheng.text()
        try:
            x = sympify(x_str, self.fs)
            y = sympify(y_str, self.fs)
        except:
            return

        from sympy import sqrt, atan2

        if attr == 0:  # 表达式
            result = "({}, {})".format(x, y)
            latex_str = "\\vec{{{}}}=({}, {})".format(name, latex(x), latex(y))
        elif attr == 1:  # 模
            result = simplify(sqrt(x**2 + y**2))
            latex_str = "|\\vec{{{}}}|=".format(name) + latex(result)
        elif attr == 2:  # 方向角
            result = simplify(atan2(y, x))
            latex_str = "\\theta_{{{}}}=".format(name) + latex(result)
        elif attr == 3:  # 单位向量
            mag = sqrt(x**2 + y**2)
            ux = simplify(x / mag)
            uy = simplify(y / mag)
            result = "({}, {})".format(ux, uy)
            latex_str = "\\hat{{\\vec{{{}}}}}=({}, {})".format(name, latex(ux), latex(uy))
        else:
            return

        self.dingyixiangliang_xiangliangshuxing_lineedit.setText(str(result))
        try:
            setWebEngineView('', latex_str, self.dingyixiangliang_xiangliangshuxing)
        except:
            pass

    def compute_vector(self):
        # 执行向量运算
        v1_name = self.dingyixiangliang_xiangliang1.currentText()
        v2_name = self.dingyixiangliang_xiangliang2.currentText()
        method = self.dingyixiangliang_jisuanfangfa.currentIndex()

        if not v1_name or not v2_name or v1_name not in self.vs or v2_name not in self.vs:
            return

        try:
            x1 = sympify(self.vs[v1_name][1], self.fs)
            y1 = sympify(self.vs[v1_name][2], self.fs)
            x2 = sympify(self.vs[v2_name][1], self.fs)
            y2 = sympify(self.vs[v2_name][2], self.fs)
        except:
            return

        from sympy import sqrt, acos

        if method == 0:  # 加法
            rx = simplify(x1 + x2)
            ry = simplify(y1 + y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}+\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 1:  # 减法
            rx = simplify(x1 - x2)
            ry = simplify(y1 - y2)
            result = "({}, {})".format(rx, ry)
            latex_str = "\\vec{{{}}}-\\vec{{{}}}=({}, {})".format(v1_name, v2_name, latex(rx), latex(ry))
        elif method == 2:  # 点积
            dot = simplify(x1 * x2 + y1 * y2)
            result = dot
            latex_str = "\\vec{{{}}}\\cdot\\vec{{{}}}=".format(v1_name, v2_name) + latex(dot)
        elif method == 3:  # 夹角
            dot = x1 * x2 + y1 * y2
            mag1 = sqrt(x1**2 + y1**2)
            mag2 = sqrt(x2**2 + y2**2)
            cos_theta = simplify(dot / (mag1 * mag2))
            angle = simplify(acos(cos_theta))
            result = angle
            latex_str = "\\angle(\\vec{{{}}},\\vec{{{}}})=".format(v1_name, v2_name) + latex(angle)
        else:
            return

        self.dingyixiangliang_jisuan_lineedit.setText(str(result))
        try:
            setWebEngineView('', latex_str, self.dingyixiangliang_jisuan)
        except:
            pass

# 该类为AI生成
class Dingyi_pj(QWidget, Ui_dingyi_pj):
    def __init__(self, parent, fs):
        super(Dingyi_pj, self).__init__(parent)
        self.setupUi(self)

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
            from planes import (
                create_point, create_line, create_circle, create_circle_three_points,
                create_triangle, create_polygon, circle_with_diameter, circle_by_center_and_point,
                perpendicular_bisector, line_parallel_through_point, line_perpendicular_through_point,
                angle_bisector_line, angle_bisector, triangle_median, triangle_altitude,
                triangle_midsegment, triangle_incircle, triangle_excircle, segment_from_points
            )
            from sympy import Point

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

# 该类为AI生成
class Qiudao(QWidget, Ui_qiudao):
    def __init__(self, parent, fs):
        super(Qiudao, self).__init__(parent)
        self.setupUi(self)
        
        self.qiudao_input.textChanged.connect(self.setqiudao_yuanhanshu)
        self.qiudao_input.returnPressed.connect(self.qiudao_qiudao_button.click)
        self.qiudao_qiudao_button.clicked.connect(self.qiudao_button_f)
        self.qiudao_yinhanshu.stateChanged.connect(self.qiudao_yinhanshu_f)
        self.qiudao_qiuchujutizhi.stateChanged.connect(self.qiudao_jutizhi_f)

        self.fs = fs
        self.parent = parent
        
    def setqiudao_yuanhanshu(self):
        # 加载原函数
        try:
            setWebEngineView('f(x)=', latex(sympify(self.qiudao_input.text(), self.fs)), self.qiudao_yuanhanshu)
        except:
            pass

    def qiudao_yinhanshu_f(self):
        # 更改求解模式:是否隐函数
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.qiudao_yinbianliang.setEnabled(self.qiudao_yinhanshu.isChecked())

    def qiudao_jutizhi_f(self):
        # 更改求解模式:是否具体值
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        self.qiudao_zibianliangzhi.setEnabled(self.qiudao_qiuchujutizhi.isChecked())

    def qiudao_button_f(self):
        # 求导
        self.is_yinhanshu = self.qiudao_yinhanshu.isChecked()
        self.is_jutizhi = self.qiudao_qiuchujutizhi.isChecked()
        if self.is_yinhanshu:
            if self.is_jutizhi:
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setWebEngineView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = yinhanshu_derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_yinbianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
        else:
            if self.is_jutizhi:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), self.qiudao_zibianliangzhi.text(), self.fs)
                setWebEngineView("f'({})=".format(self.qiudao_zibianliangzhi.text()), latex(dif), self.qiudao_daoshuzhi)
                self.qiudao_daoshuzhi_lineedit.setText(str(dif))
            else:
                dif = derivative(self.qiudao_input.text(), self.qiudao_zibianliang.text(), self.qiudao_qiudaocishu.text(), None, self.fs)
                setWebEngineView("f'(x)=", latex(dif), self.qiudao_daohanshu)
                self.qiudao_daohanshu_lineedit.setText(str(dif))

class Jifen(QWidget, Ui_jifen):
    def __init__(self, parent, fs):
        super(Jifen, self).__init__(parent)
        self.setupUi(self)

        self.jifen_input.textChanged.connect(self.setjifen_beijihanshu)
        self.jifen_input.returnPressed.connect(self.jifen_jifen_button.click)
        self.jifen_jifen_button.clicked.connect(self.jifen_button_f)
        self.jifen_dingjifen.stateChanged.connect(self.jifen_dingjifen_f)

        self.fs = fs
        self.parent = parent

    def setjifen_beijihanshu(self):
        # 加载原函数
        try:
            setWebEngineView('f(x)=', latex(sympify(self.jifen_input.text(), self.fs)), self.jifen_beijihanshu)
        except:
            pass

    def jifen_dingjifen_f(self):
        # 更改求解模式:是否定积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        self.jifen_shangxianzhi.setEnabled(self.jifen_dingjifen.isChecked())
        self.jifen_xiaxianzhi.setEnabled(self.jifen_dingjifen.isChecked())

    def jifen_button_f(self):
        # 积分
        self.is_dingjifen = self.jifen_dingjifen.isChecked()
        if self.is_dingjifen:
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.fs)
            setWebEngineView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.jifen_xiaxianzhi.text(), self.jifen_shangxianzhi.text(), self.fs)
            setWebEngineView('F(x)=', latex(F), self.jifen_dingjifenzhi)
            self.jifen_dingjifenzhi_lineedit.setText(str(F))
            
        else:
            self.jifen_dingjifenzhi.setHtml("")
            F = integral(self.jifen_input.text(), self.jifen_jifenbianliang.text(), self.fs)
            setWebEngineView('F(x)=', latex(F), self.jifen_yuanhanshu)
            self.jifen_yuanhanshu_lineedit.setText(str(F))

class Bianxing(QWidget, Ui_bianxing):
    def __init__(self, parent, fs):
        super(Bianxing, self).__init__(parent)
        self.setupUi(self)

        self.bianxing_bianxingfangfa.addItems(["通用化简(simplify)", "展开(expand)", "因式分解(factor)", "主元(collect)", "通分(cancel)", "分离(apart)"])
        self.bianxing_bianxingfangfa.addItems(["三角变换(trigsimp)", "三角展开(expand_trig)", "指数合并(powsimp)", "指数展开(expand_power_exp)"])
        self.bianxing_bianxingfangfa.addItems(["对数展开(expand_log)", "对数合并(logcombine)", "换元"])
        self.bianxing_bianxingfangfa.currentIndexChanged.connect(self.bianxing_bianxingfangfa_f)
        self.bianxing_input.textChanged.connect(self.setbianxing_yuanshi)
        self.bianxing_input.returnPressed.connect(self.bianxing_bianxing_button.click)
        self.bianxing_bianxing_button.clicked.connect(self.bianxing_button_f)

        self.fs = fs
        self.parent = parent

    def setbianxing_yuanshi(self):
        # 加载原式
        try:
            setWebEngineView('', latex(sympify(self.bianxing_input.text(), self.fs)), self.bianxing_yuanshi)
        except:
            pass

    def bianxing_bianxingfangfa_f(self):
        # 识别变形方法并更改文本框状态
        if self.bianxing_bianxingfangfa.currentIndex() == 3:
            self.bianxing_zhuyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanshi.setEnabled(False)
        elif self.bianxing_bianxingfangfa.currentIndex() == 12:
            self.bianxing_zhuyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanfuhao.setEnabled(True)
            self.bianxing_huanyuanshi.setEnabled(True)
        else:
            self.bianxing_zhuyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanfuhao.setEnabled(False)
            self.bianxing_huanyuanshi.setEnabled(False)

    def bianxing_button_f(self):
        # 变形
        self.bianxingfangfa = self.bianxing_bianxingfangfa.currentIndex()
        self.bianxingshi = simplifies(self.bianxing_input.text(), self.bianxingfangfa, self.bianxing_zhuyuanfuhao.text() if self.bianxing_zhuyuanfuhao.isEnabled() else None, \
            self.bianxing_huanyuanfuhao.text() if self.bianxing_huanyuanfuhao.isEnabled() else None, self.bianxing_huanyuanshi.text() if self.bianxing_huanyuanshi.isEnabled() else None, self.fs)
        setWebEngineView('', latex(self.bianxingshi), self.bianxing_bianxingshi)
        self.bianxing_bianxingshi_lineedit.setText(str(self.bianxingshi))

class Fangcheng(QWidget, Ui_fangcheng):
    def __init__(self, parent, fs):
        super(Fangcheng, self).__init__(parent)
        self.setupUi(self)

        self.fangcheng_zuoshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_youshi.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_quzhifanwei.textChanged.connect(self.setfangcheng_yuanfangcheng)
        self.fangcheng_zuoshi.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_youshi.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_quzhifanwei.returnPressed.connect(self.fangcheng_qiujie.click)
        self.fangcheng_weifenfangcheng.stateChanged.connect(self.fangcheng_weifenfangcheng_f)
        self.fangcheng_qiujie.clicked.connect(self.fangcheng_button_f)

        self.fs = fs
        self.parent = parent

    def setfangcheng_yuanfangcheng(self):
        # 加载原方程
        try:
            self.eq_fangcheng = Eq(sympify(self.fangcheng_zuoshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}), \
                                   sympify(self.fangcheng_youshi.text(), self.fs if not self.fangcheng_weifenfangcheng.isChecked() else {}))
            setWebEngineView('','{} (x\\in {})'.format(latex(self.eq_fangcheng), latex(sympify(self.fangcheng_quzhifanwei.text(), self.fs))) if not self.fangcheng_weifenfangcheng.isChecked() \
                                  else latex(self.eq_fangcheng), self.fangcheng_yuanfangcheng)
        except:
            pass

    def fangcheng_weifenfangcheng_f(self):
        # 更改求解模式:是否微分方程
        self.fangcheng_zhuyuanfuhao.setText("f(x)" if self.fangcheng_weifenfangcheng.isChecked() else "x")
        self.fangcheng_zhuyuanfuhao.setEnabled(not self.fangcheng_weifenfangcheng.isChecked())
        self.fangcheng_quzhifanwei.setText("" if self.fangcheng_weifenfangcheng.isChecked() else "Reals")
        self.fangcheng_quzhifanwei.setEnabled(not self.fangcheng_weifenfangcheng.isChecked())

    def fangcheng_button_f(self):
        # 求解方程
        if self.fangcheng_weifenfangcheng.isChecked():
            self.jieji_fangcheng = solve_weifenfangcheng(self.eq_fangcheng, self.fangcheng_zhuyuanfuhao.text(), self.fs)
            setWebEngineView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))
        else:
            self.jieji_fangcheng = solve_fangcheng(self.eq_fangcheng, self.fangcheng_zhuyuanfuhao.text(), self.fangcheng_quzhifanwei.text(), self.fs)
            setWebEngineView('', latex(self.jieji_fangcheng), self.fangcheng_jieji)
            self.fangcheng_jieji_lineedit.setText(str(self.jieji_fangcheng))

class Fangchengzu(QWidget, Ui_fangchengzu):
    def __init__(self, parent, fs):
        super(Fangchengzu, self).__init__(parent)
        self.setupUi(self)

        self.fangchengzu_baocun.clicked.connect(self.save_fangcheng)
        self.fangchengzu_shanchu.clicked.connect(self.delete_fangcheng)
        self.fangchengzu_fangcheng.itemClicked.connect(self.read_fangcheng)
        self.fangchengzu_qiujie.clicked.connect(self.fangchengzu_button_f)
        self.fangchengzu_zuoshi.returnPressed.connect(self.fangchengzu_baocun.click)
        self.fangchengzu_youshi.returnPressed.connect(self.fangchengzu_baocun.click)

        self.fs = fs
        self.parent = parent

        for i in self.parent.eqs.keys():
            self.fangchengzu_fangcheng.addItem(i)
        
    def read_fangcheng(self, item):
        # 读取方程并显示
        setWebEngineView('', latex(self.parent.eqs[item.text()]), self.fangchengzu_yuanfangcheng)
        self.fangchengzu_zuoshi.setText(str(self.parent.eqs[item.text()].lhs))
        self.fangchengzu_youshi.setText(str(self.parent.eqs[item.text()].rhs))

    def setfangchengzu_yuanfangcheng(self):
        # 切换至当前选项卡时加载不等式
        if self.fangchengzu_fangcheng.count() != 0:
            self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def save_fangcheng(self):
        # 保存方程
        if Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)) not in self.parent.eqs.values():
            self.parent.eqs[str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))
            self.fangchengzu_fangcheng.addItem(str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))))
            self.fangchengzu_fangcheng.setCurrentRow(self.fangchengzu_fangcheng.count() - 1)
        else:
            self.parent.eqs[str(Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs)))] = Eq(sympify(self.fangchengzu_zuoshi.text(), self.fs), sympify(self.fangchengzu_youshi.text(), self.fs))
        self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def delete_fangcheng(self):
        # 删除方程
        fangcheng = self.fangchengzu_fangcheng.takeItem(self.fangchengzu_fangcheng.currentRow())
        del self.parent.eqs[fangcheng.text()]
        del fangcheng
        if self.parent.eqs != {}:
            self.read_fangcheng(self.fangchengzu_fangcheng.currentItem())

    def fangchengzu_button_f(self):
        # 求解方程组
        try:
            result = solve_fangchengzu(list(self.parent.eqs.values()), [Symbol(s) for s in self.fangchengzu_ziyoubianliang.text().split(',')], self.fs)
        except:
            result = "无解"
        setWebEngineView('', latex(result).replace(':', "="), self.fangchengzu_jieji)
        self.fangchengzu_jieji_lineedit.setText(str(result))

class Budengshi(QWidget, Ui_budengshi):
    def __init__(self, parent, fs):
        super(Budengshi, self).__init__(parent)
        self.setupUi(self)

        self.budengshi_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshi_budenghao.currentIndexChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_zuoshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_youshi.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_quzhifanwei.textChanged.connect(self.setbudengshi_yuanshi)
        self.budengshi_zuoshi.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_youshi.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_quzhifanwei.returnPressed.connect(self.budengshi_qiujie.click)
        self.budengshi_qiujie.clicked.connect(self.budengshi_button_f)

        self.fs = fs
        self.parent = parent

    def setbudengshi_yuanshi(self):
        # 加载原不等式
        try:
            self.rel_budengshi = Rel(sympify(self.budengshi_zuoshi.text(), self.fs), sympify(self.budengshi_youshi.text(), self.fs), self.budengshi_budenghao.currentText())
            setWebEngineView('', '{}\\quad (x\\in {})'.format(latex(self.rel_budengshi), latex(sympify(self.budengshi_quzhifanwei.text(), self.fs))), self.budengshi_yuanshi)
        except:
            pass

    def budengshi_button_f(self):
        # 求解不等式
        self.jieji_budengshi = solve_budengshi(self.rel_budengshi, self.budengshi_zhuyuanfuhao.text(), self.budengshi_quzhifanwei.text(), self.fs)
        setWebEngineView('', latex(self.jieji_budengshi), self.budengshi_jieji)
        self.budengshi_jieji_lineedit.setText(str(self.jieji_budengshi))

class Budengshizu(QWidget, Ui_budengshizu):
    def __init__(self, parent, fs):
        super(Budengshizu, self).__init__(parent)
        self.setupUi(self)

        self.budengshizu_budenghao.addItems(["!=", ">", ">=", "<", "<="])
        self.budengshizu_baocun.clicked.connect(self.save_budengshi)
        self.budengshizu_shanchu.clicked.connect(self.delete_budengshi)
        self.budengshizu_budengshi.itemClicked.connect(self.read_budengshi)
        self.budengshizu_qiujie.clicked.connect(self.budengshizu_button_f)
        self.budengshizu_zuoshi.returnPressed.connect(self.budengshizu_baocun.click)
        self.budengshizu_youshi.returnPressed.connect(self.budengshizu_baocun.click)

        self.fs = fs
        self.parent = parent

        for i in self.parent.rels.keys():
            self.budengshizu_budengshi.addItem(i)

    def read_budengshi(self, item):
        # 读取不等式并显示
        setWebEngineView('', latex(self.parent.rels[item.text()]), self.budengshizu_yuanbudengshi)
        self.budengshizu_zuoshi.setText(str(self.parent.rels[item.text()].lhs))
        self.budengshizu_youshi.setText(str(self.parent.rels[item.text()].rhs))

    def setbudengshizu_yuanbudengshi(self):
        # 切换至当前选项卡时加载不等式
        if self.budengshizu_budengshi.count() != 0:
            self.read_budengshi(self.budengshizu_budengshi.currentItem())

    def save_budengshi(self):
        # 保存不等式
        if Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()) not in self.parent.rels.values():
            self.parent.rels[str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())
            self.budengshizu_budengshi.addItem(str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())))
            self.budengshizu_budengshi.setCurrentRow(self.budengshizu_budengshi.count() - 1)
        else:
            self.parent.rels[str(Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText()))] = \
                Rel(sympify(self.budengshizu_zuoshi.text(), self.fs), sympify(self.budengshizu_youshi.text(), self.fs), self.budengshizu_budenghao.currentText())
        self.read_budengshi(self.budengshizu_budengshi.currentItem())
    
    def delete_budengshi(self):
        # 删除不等式
        budengshi = self.budengshizu_budengshi.takeItem(self.budengshizu_budengshi.currentRow())
        del self.parent.rels[budengshi.text()]
        del budengshi
        if self.parent.rels != {}:
            self.read_budengshi(self.budengshizu_budengshi.currentItem())

    def budengshizu_button_f(self):
        # 求解不等式组
        try:
            result = solve_budengshizu(list(self.parent.rels.values()), Symbol(self.budengshizu_ziyoubianliang.text()), self.fs) \
                if solve_budengshizu(list(self.parent.rels.values()), Symbol(self.budengshizu_ziyoubianliang.text()), self.fs) else "无解"
        except:
            result = "无解"
        setWebEngineView('', latex(result), self.budengshizu_jieji)
        self.budengshizu_jieji_lineedit.setText(str(result))

class Jisuan(QWidget, Ui_jisuan):
    def __init__(self, parent, fs):
        super(Jisuan, self).__init__(parent)
        self.setupUi(self)

        self.jisuan_jisuanyinqing.addItems(["Python内置引擎", "Mpmath高精度引擎", "Sympy符号引擎", "Latex代码生成引擎"])
        self.jisuan_jisuanyinqing.currentIndexChanged.connect(self.jisuan_jisuanyinqing_f)
        self.jisuan_jisuan_button.clicked.connect(self.jisuan_button_f)
        self.jisuan_input.textChanged.connect(self.setjisuan_yuanshi)
        self.jisuan_input.returnPressed.connect(self.jisuan_jisuan_button.click)

        self.fs = fs
        self.parent = parent

        self.jisuan_jisuanyinqing_f()
    
    def setjisuan_yuanshi(self):
        # 加载原式
        try:
            setWebEngineView("", self.jisuan_input.text(), self.jisuan_yuanshi)
        except:
            pass
    
    def jisuan_jisuanyinqing_f(self):
        # 识别计算引擎并更改文本框状态
        if self.jisuan_jisuanyinqing.currentIndex() == 1:
            self.jisuan_jingdu.setEnabled(True)
        else:
            self.jisuan_jingdu.setEnabled(False)

    def jisuan_button_f(self):
        # 计算结果
        import sys
        sys.set_int_max_str_digits(0)
        def show(result, view_is_latex = False, lineedit_is_latex = False):
            setWebEngineView("", latex(result) if view_is_latex else result, self.jisuan_jisuanjieguo)
            self.jisuan_jisuanjieguo_lineedit.setMaxLength(len(str(latex(result) if lineedit_is_latex else result)) + 1)
            self.jisuan_jisuanjieguo_lineedit.setText(str(latex(result) if lineedit_is_latex else result))
        if self.jisuan_jisuanyinqing.currentIndex() == 0:
            result = eval(self.jisuan_input.text())
            show(result)
        elif self.jisuan_jisuanyinqing.currentIndex() == 1:
            import mpmath as mp
            from mpmath import sin, cos, tan, cot, sec, csc, sinh, cosh, tanh, coth, sech, csch, exp, log, ln, sqrt, root, pi, e, phi
            with mp.workdps(int(self.jisuan_jingdu.text())):
                result = eval(self.jisuan_input.text())
                show(result)
        elif self.jisuan_jisuanyinqing.currentIndex() == 2:
            result = radsimp(sympify(self.jisuan_input.text(), self.fs, is_simplify = True))
            show(result, True)
        elif self.jisuan_jisuanyinqing.currentIndex() == 3:
            show(sympify(self.jisuan_input.text(), fs = {}), True, True)

class Help(QWidget, Ui_help):
    def __init__(self, parent, fs):
        super(Help, self).__init__(parent)
        self.setupUi(self)

        self.help_path = QUrl("qrc:///help.html")
        self.webEngineView.setUrl(self.help_path)

class Huitu_hanshu(QWidget, Ui_huitu_hanshu):
    def __init__(self, parent, fs):
        super(Huitu_hanshu, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.huitu_hanshu_biaodashi_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_hanshu_radio.toggled.connect(self.toggle_input_mode)
        self.huitu_hanshu_huizhi.clicked.connect(self.draw_function)
        self.huitu_hanshu_biaodashi.returnPressed.connect(self.huitu_hanshu_huizhi.click)

        self.canvas = None
        self.draw_layout = QVBoxLayout(self.huitu_hanshu_huitu)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.update_function_list()

    def toggle_input_mode(self):
        # 切换输入模式：表达式 / 选择函数
        is_expression = self.huitu_hanshu_biaodashi_radio.isChecked()
        self.huitu_hanshu_biaodashi.setEnabled(is_expression)
        self.huitu_hanshu_hanshu.setEnabled(not is_expression)

    def update_function_list(self):
        # 刷新已定义函数的下拉列表
        self.huitu_hanshu_hanshu.clear()
        for name in self.fs.keys():
            self.huitu_hanshu_hanshu.addItem("{}({})".format(name, self.fs[name][3]))

    def draw_function(self):
        # 销毁之前画的函数图像对象
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        import numpy as np
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        from sympy import lambdify

        # 获取表达式
        if self.huitu_hanshu_biaodashi_radio.isChecked():
            expr_str = self.huitu_hanshu_biaodashi.text()
            if not expr_str:
                return
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            free_syms = list(expr.free_symbols)
            if free_syms:
                var = list(free_syms)[0]
            else:
                var = Symbol('x')
        else:
            func_name = self.huitu_hanshu_hanshu.currentText().split('(')[0]
            if func_name not in self.fs:
                return
            expr_str = self.fs[func_name][1]
            var_str = self.fs[func_name][3]
            try:
                expr = sympify(expr_str, self.fs)
            except Exception:
                return
            var = Symbol(var_str)

        # 定义域
        left_str = self.huitu_hanshu_dingyiyu_left.text() or '-10'
        right_str = self.huitu_hanshu_dingyiyu_right.text() or '10'
        try:
            left = float(sympify(left_str, self.fs))
            right = float(sympify(right_str, self.fs))
        except Exception:
            left, right = -10, 10
        if left >= right:
            left, right = -10, 10

        try:
            # 将 SymPy 表达式转为 numpy 可调函数
            f = lambdify(var, expr, modules=['numpy', {'conjugate': np.conj}])

            # 生成密集的 x 采样点
            num_points = 2000
            x_vals = np.linspace(float(left), float(right), num_points)

            # 排除无穷大和 NaN 的 y 值，避免曲线断裂处连线
            with np.errstate(invalid='ignore', divide='ignore'):
                y_vals = np.asarray(f(x_vals), dtype=np.float64)

            # 构建 matplotlib 图形
            fig = Figure(figsize=(7.7, 3.9), dpi=100)
            ax = fig.add_subplot(111)

            # 在 NaN/Inf 处断开曲线
            mask = np.isfinite(y_vals)
            segments = []
            start = 0
            while start < len(mask):
                if mask[start]:
                    end = start
                    while end < len(mask) and mask[end]:
                        end += 1
                    segments.append((start, end))
                    start = end
                else:
                    start += 1

            for seg_start, seg_end in segments:
                ax.plot(x_vals[seg_start:seg_end], y_vals[seg_start:seg_end],
                        color='#1f77b4', linewidth=1.5)

            # 坐标轴和网格
            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.axvline(x=0, color='black', linewidth=0.5)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_xlim(float(left), float(right))

            # 自动缩放 y 轴到可见范围
            if np.any(mask):
                y_min, y_max = np.min(y_vals[mask]), np.max(y_vals[mask])
                margin = max((y_max - y_min) * 0.1, 1.0)
                ax.set_ylim(y_min - margin, y_max + margin)

            fig.tight_layout()

            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            self.draw_layout.addWidget(self.canvas)
        except Exception:
            pass

class Huitu_pj(QWidget, Ui_huitu_pj):
    def __init__(self, parent, fs):
        super(Huitu_pj, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.canvas = None
        self._pjs_hash = None  # 跟踪 pjs 变化，避免重复刷新列表
        self.draw_layout = QVBoxLayout(self.huitu_pingji)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.huitu_pj_button.clicked.connect(self._draw)

    def showEvent(self, event):
        """切换至本页时自动刷新对象列表（仅在 pjs 内容变化时重建）"""
        super().showEvent(event)
        if hasattr(self.parent, 'pjs'):
            new_hash = len(self.parent.pjs)
            if new_hash != self._pjs_hash:
                self._refresh_object_list()
                self._pjs_hash = new_hash
        elif self._pjs_hash is not None:
            self._refresh_object_list()
            self._pjs_hash = None

    def _refresh_object_list(self):
        """根据 pjs 刷新对象列表（全选 + 复选框），Qt 自动处理点击切换"""
        self.huitu_pj_list.clear()
        if not hasattr(self.parent, 'pjs') or not self.parent.pjs:
            return
        for name, val in self.parent.pjs.items():
            cat = val[0]
            display = f"[{cat}] {name}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, name)  # 存储原始名称
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)  # 默认选中
            self.huitu_pj_list.addItem(item)

    def _draw(self):
        """仅绘制列表中选中的对象"""
        # 销毁之前画的canvas
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        # 获取已定义的对象
        if not hasattr(self.parent, 'pjs') or not self.parent.pjs:
            return

        # 收集选中对象名称
        checked_names = set()
        for i in range(self.huitu_pj_list.count()):
            item = self.huitu_pj_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_names.add(item.data(Qt.ItemDataRole.UserRole))

        if not checked_names:
            return

        from paint2D import draw2d
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

        # 构建 (obj, style) 列表：仅选中的对象
        objects = []
        for name in checked_names:
            if name in self.parent.pjs:
                obj = self.parent.pjs[name][1]
                objects.append((obj, {'label': name}))

        if not objects:
            return

        try:
            fig = draw2d(objects, figsize=(6.0, 5.1), dpi=100)
            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            self.draw_layout.addWidget(self.canvas)
        except Exception as e:
            QMessageBox.warning(self, "绘制失败", f"绘制时出错：\n{e}")

class Jiesanjiaoxing(QWidget, Ui_jiesanjiaoxing):
    def __init__(self, parent, fs):
        super(Jiesanjiaoxing, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.jiesanjiaoxing_qiujie.clicked.connect(self.solve_triangle)
        self.jiesanjiaoxing_tiaojian1.returnPressed.connect(self.jiesanjiaoxing_qiujie.click)
        self.jiesanjiaoxing_tiaojian2.returnPressed.connect(self.jiesanjiaoxing_qiujie.click)
        self.jiesanjiaoxing_tiaojian3.returnPressed.connect(self.jiesanjiaoxing_qiujie.click)

    def _parse_conditions(self):
        """解析三个条件，返回 (angles_dict, sides_dict, error_msg)"""
        combos = [
            (self.jiesanjiaoxing_tiaojian1_cbx, self.jiesanjiaoxing_tiaojian1),
            (self.jiesanjiaoxing_tiaojian2_cbx, self.jiesanjiaoxing_tiaojian2),
            (self.jiesanjiaoxing_tiaojian3_cbx, self.jiesanjiaoxing_tiaojian3),
        ]

        angles = {}
        sides = {}
        angle_names = {1: 'A', 2: 'B', 3: 'C'}
        side_names = {4: 'a', 5: 'b', 6: 'c'}
        for cbx, line_edit in combos:
            idx = cbx.currentIndex()
            val_text = line_edit.text().strip()
            if idx == 0 or not val_text:
                continue

            try:
                val = sympify(val_text, self.fs)
            except Exception:
                return None, None, "条件值格式错误"

            if idx in angle_names:
                angles[angle_names[idx]] = val
            elif idx in side_names:
                sides[side_names[idx]] = val

        total = len(angles) + len(sides)
        if total != 3:
            return None, None, "请填入恰好3个有效且不重复的条件"

        return angles, sides, None

    def solve_triangle(self):
        """求解三角形"""
        # 清空上次结果
        self.jiesanjiaoxing_yuantiaojian.setHtml("")
        self.jiesanjiaoxing_jieguo.setHtml("")
        self.jiesanjiaoxing_jieguo_lineedit.setText("")

        angles, sides, error = self._parse_conditions()
        if error:
            self.jiesanjiaoxing_jieguo_lineedit.setText(error)
            return

        angle_display = {k: latex(v) for k, v in angles.items()}
        side_display = {k: latex(v) for k, v in sides.items()}
        known_parts = []
        for k, v in {**angle_display, **side_display}.items():
            known_parts.append(f"{k} = {v}")
        condition_latex = r"\triangle ABC \quad " + r",\ ".join(known_parts)
        try:
            setWebEngineView('', condition_latex, self.jiesanjiaoxing_yuantiaojian)
        except Exception:
            pass

        result = solve_sanjiaoxing(angles, sides, self.fs)

        if not result:
            self.jiesanjiaoxing_jieguo_lineedit.setText("无解")
            return
        if isinstance(result, str):
            self.jiesanjiaoxing_jieguo_lineedit.setText(str(result))
            return

        lines = []
        for i, (res_angles, res_sides) in enumerate(result):
            parts = []
            for k, v in res_angles.items():
                parts.append(f"{k} = {latex(v)}")
            for k, v in res_sides.items():
                parts.append(f"{k} = {latex(v)}")
            if len(result) > 1:
                lines.append(r"\text{解}" + str(i + 1) + r":\ " + r",\ ".join(parts))
            else:
                lines.append(r",\ ".join(parts))

        result_latex = r" \\ ".join(lines) if len(lines) > 1 else lines[0]

        flat = []
        for i, (res_angles, res_sides) in enumerate(result):
            seg = []
            for k, v in res_angles.items():
                seg.append(f"{k} = {v}")
            for k, v in res_sides.items():
                seg.append(f"{k} = {v}")
            flat.append(" | ".join(seg))
        self.jiesanjiaoxing_jieguo_lineedit.setText("  ||  ".join(flat))

        try:
            setWebEngineView('', result_latex, self.jiesanjiaoxing_jieguo)
        except Exception:
            pass

class Dingyi_lj(QWidget, Ui_dingyi_lj):
    """立体几何对象定义页面"""
    def __init__(self, parent, fs):
        super(Dingyi_lj, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        if not hasattr(self.parent, 'ljs'):
            self.parent.ljs = {}

        self.ljs = self.parent.ljs

        self.dingyi_lj_fangfa.currentIndexChanged.connect(self._on_method_changed)
        self.dingyi_lj_canshu.returnPressed.connect(self._do_create)
        self.dingyi_lj_baocun.clicked.connect(self._do_create)

        for cat, btn_read, btn_del in [
            ("点",   self.dingyi_lj_dian_read,     self.dingyi_lj_dian_delete),
            ("直线", self.dingyi_lj_zhixian_read,  self.dingyi_lj_zhixian_delete),
            ("平面", self.dingyi_lj_pingmian_read, self.dingyi_lj_pingmian_delete),
            ("线段", self.dingyi_lj_xianduan_read, self.dingyi_lj_xianduan_delete),
        ]:
            btn_read.clicked.connect(lambda ch=False, c=cat: self._read_item(c))
            btn_del.clicked.connect(lambda ch=False, c=cat: self._delete_item(c))

        self._refresh_all_lists()

    @staticmethod
    def _method_names():
        return [
            "未选择",
            "create_point3d",          # 1: x, y, z
            "create_line3d",           # 2: 点1名, 点2名
            "plane_parallel_through_point",    # 3: 平面名, 点名
            "plane_perpendicular_to_line_through_point",  # 4: 直线名, 点名
            "line_parallel_through_point_3d",  # 5: 直线名, 点名
            "line_perpendicular_to_line_through_point",  # 6: 点名, 直线名 (垂线)
            "line_perpendicular_to_plane_through_point",  # 7: 平面名, 点名
            "plane_through_line_and_point",    # 8: 直线名, 点名
            "plane_through_two_lines",         # 9: 直线1名, 直线2名
            "perpendicular_foot_to_plane",     # 10: 点名, 平面名
            "perpendicular_foot_to_line_3d",   # 11: 点名, 直线名
            "segment3d_from_points",  # 12: 点1名, 点2名
        ]

    @classmethod
    def _method_params_hint(cls, idx):
        hints = {
            0:  "", 1: "x坐标, y坐标, z坐标",
            2: "点1名称, 点2名称", 3: "平面名称, 点名称",
            4: "直线名称, 点名称", 5: "直线名称, 点名称",
            6: "点名称, 直线名称", 7: "平面名称, 点名称",
            8: "直线名称, 点名称", 9: "直线1名称, 直线2名称",
            10: "点名称, 平面名称", 11: "点名称, 直线名称",
            12: "点1名称, 点2名称",
        }
        return hints.get(idx, "")

    def _on_method_changed(self, idx):
        hint = self._method_params_hint(idx)
        if idx > 0 and hint:
            self.label_2.setText("参数(" + hint + ")：")
        else:
            self.label_2.setText("参数(直接输入，以英文半角逗号分隔)：")

    def _find_point3d(self, name):
        n = name.strip()
        return self.ljs[n][1] if n in self.ljs and self.ljs[n][0] == "点" else None

    def _find_line3d(self, name):
        n = name.strip()
        return self.ljs[n][1] if n in self.ljs and self.ljs[n][0] == "直线" else None

    def _find_plane(self, name):
        n = name.strip()
        return self.ljs[n][1] if n in self.ljs and self.ljs[n][0] == "平面" else None

    def _find_points3d(self, names_str):
        pts = []
        for n in names_str.split(','):
            p = self._find_point3d(n.strip())
            if p is None:
                raise ValueError(f"未找到点'{n.strip()}'")
            pts.append(p)
        return pts

    def _store(self, name, category, obj):
        self.ljs[name] = (category, obj)
        self._refresh_all_lists()

    _LJ_CATS = {"点":"dingyi_lj_dian","直线":"dingyi_lj_zhixian","平面":"dingyi_lj_pingmian","线段":"dingyi_lj_xianduan"}

    def _refresh_all_lists(self):
        getattr(self, "dingyi_lj_dian").clear()
        getattr(self, "dingyi_lj_zhixian").clear()
        getattr(self, "dingyi_lj_pingmian").clear()
        getattr(self, "dingyi_lj_xianduan").clear()
        for name, val in self.ljs.items():
            cat = val[0]
            lst_name = self._LJ_CATS.get(cat)
            if lst_name:
                getattr(self, lst_name).addItem(name)

    def _do_create(self):
        idx = self.dingyi_lj_fangfa.currentIndex()
        if idx == 0: return
        name = self.dingyi_lj_mingcheng.text().strip()
        if not name: return
        params_str = self.dingyi_lj_canshu.text().strip()
        raw_params = [p.strip() for p in params_str.split(',')] if params_str else []

        try:
            from solids import (create_point3d, create_line3d,
                plane_parallel_through_point, plane_perpendicular_to_line_through_point,
                line_parallel_through_point_3d, line_perpendicular_to_plane_through_point,
                plane_through_line_and_point, plane_through_two_lines,
                perpendicular_foot_to_plane, perpendicular_foot_to_line_3d, segment3d_from_points)

            if idx == 1:  # create_point3d
                if len(raw_params) < 3: return
                pt = create_point3d(raw_params[0], raw_params[1], raw_params[2], self.fs)
                self._store(name, "点", pt)

            elif idx == 2:  # create_line3d
                if len(raw_params) < 2: return
                pts = self._find_points3d(raw_params[0] + "," + raw_params[1])
                self._store(name, "直线", create_line3d(*pts))

            elif idx == 3:  # plane_parallel_through_point
                if len(raw_params) < 2: return
                pl = self._find_plane(raw_params[0])
                pt = self._find_point3d(raw_params[1])
                if pl and pt: self._store(name, "平面", plane_parallel_through_point(pl, pt))

            elif idx == 4:  # plane_perpendicular_to_line_through_point
                if len(raw_params) < 2: return
                line = self._find_line3d(raw_params[0])
                pt = self._find_point3d(raw_params[1])
                if line and pt: self._store(name, "平面", plane_perpendicular_to_line_through_point(line, pt))

            elif idx == 5:  # line_parallel_through_point_3d: 直线名, 点名
                if len(raw_params) < 2: return
                line = self._find_line3d(raw_params[0])
                pt = self._find_point3d(raw_params[1])
                if line and pt: self._store(name, "直线", line_parallel_through_point_3d(line, pt))

            elif idx == 6:  # 过一点作已知直线的垂线: 点名, 直线名
                if len(raw_params) < 2: return
                pt = self._find_point3d(raw_params[0])
                line = self._find_line3d(raw_params[1])
                if pt and line:
                    foot = perpendicular_foot_to_line_3d(pt, line)
                    self._store(name, "直线", create_line3d(pt, foot))

            elif idx == 7:  # line_perpendicular_to_plane_through_point: 平面名, 点名
                if len(raw_params) < 2: return
                pl = self._find_plane(raw_params[0])
                pt = self._find_point3d(raw_params[1])
                if pl and pt: self._store(name, "直线", line_perpendicular_to_plane_through_point(pl, pt))

            elif idx == 8:  # plane_through_line_and_point: 直线名, 点名
                if len(raw_params) < 2: return
                line = self._find_line3d(raw_params[0])
                pt = self._find_point3d(raw_params[1])
                if line and pt:
                    result = plane_through_line_and_point(line, pt)
                    if not isinstance(result, str): self._store(name, "平面", result)

            elif idx == 9:  # plane_through_two_lines: 直线1名, 直线2名
                if len(raw_params) < 2: return
                l1 = self._find_line3d(raw_params[0])
                l2 = self._find_line3d(raw_params[1])
                if l1 and l2:
                    result = plane_through_two_lines(l1, l2)
                    if not isinstance(result, str): self._store(name, "平面", result)

            elif idx == 10:  # perpendicular_foot_to_plane: 点名, 平面名
                if len(raw_params) < 2: return
                pt = self._find_point3d(raw_params[0])
                pl = self._find_plane(raw_params[1])
                if pt and pl: self._store(name, "点", perpendicular_foot_to_plane(pt, pl))

            elif idx == 11:  # perpendicular_foot_to_line_3d: 点名, 直线名
                if len(raw_params) < 2: return
                pt = self._find_point3d(raw_params[0])
                line = self._find_line3d(raw_params[1])
                if pt and line: self._store(name, "点", perpendicular_foot_to_line_3d(pt, line))

            elif idx == 12:  # segment3d_from_points: 点1名, 点2名
                if len(raw_params) < 2: return
                pts = self._find_points3d(raw_params[0] + "," + raw_params[1])
                self._store(name, "线段", segment3d_from_points(*pts))

        except Exception as e:
            QMessageBox.warning(self, "创建失败", f"创建对象时出错：\n{e}")

    def _read_item(self, cat):
        lst_name = self._LJ_CATS.get(cat)
        if not lst_name: return
        lst = getattr(self, lst_name)
        item = lst.currentItem()
        if not item: return
        name = item.text().strip()
        if name not in self.ljs: return
        _, obj = self.ljs[name]
        self.dingyi_lj_shuxing_mingcheng.setText(name)
        try:
            eq = obj.equation() if hasattr(obj, 'equation') else str(obj)
        except:
            eq = str(obj)
        self.dingyi_lj_shuxing_fangcheng.setText(str(eq))

    def _delete_item(self, cat):
        lst_name = self._LJ_CATS.get(cat)
        if not lst_name: return
        lst = getattr(self, lst_name)
        row = lst.currentRow()
        if row < 0: return
        name = lst.currentItem().text().strip()
        if name in self.ljs: del self.ljs[name]
        self._refresh_all_lists()
        self.dingyi_lj_shuxing_mingcheng.setText("")
        self.dingyi_lj_shuxing_fangcheng.setText("")


class Huitu_lj(QWidget, Ui_huitu_lj):
    """立体几何绘图页面"""
    def __init__(self, parent, fs):
        super(Huitu_lj, self).__init__(parent)
        self.setupUi(self)

        self.fs = fs
        self.parent = parent

        self.canvas = None
        self._ljs_hash = None
        self.draw_layout = QVBoxLayout(self.huitu_pingji)
        self.draw_layout.setContentsMargins(0, 0, 0, 0)

        self.huitu_lj_button.clicked.connect(self._draw)

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self.parent, 'ljs'):
            new_hash = len(self.parent.ljs)
            if new_hash != self._ljs_hash:
                self._refresh_object_list()
                self._ljs_hash = new_hash
        elif self._ljs_hash is not None:
            self._refresh_object_list()
            self._ljs_hash = None

    def _refresh_object_list(self):
        self.huitu_lj_list.clear()
        if not hasattr(self.parent, 'ljs') or not self.parent.ljs:
            return
        for name, val in self.parent.ljs.items():
            cat = val[0]
            display = f"[{cat}] {name}"
            item = QListWidgetItem(display)
            item.setData(Qt.ItemDataRole.UserRole, name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self.huitu_lj_list.addItem(item)

    def _draw(self):
        if self.canvas is not None:
            self.draw_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

        if not hasattr(self.parent, 'ljs') or not self.parent.ljs:
            return

        checked_names = set()
        for i in range(self.huitu_lj_list.count()):
            item = self.huitu_lj_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_names.add(item.data(Qt.ItemDataRole.UserRole))

        if not checked_names: return

        from paint3D import draw3d
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

        objects = []
        for name in checked_names:
            if name in self.parent.ljs:
                objects.append((self.parent.ljs[name][1], {'label': name}))

        if not objects: return

        try:
            fig = draw3d(objects, figsize=(6.0, 5.1), dpi=100)
            self.fig = fig
            self.canvas = FigureCanvas(self.fig)
            self.draw_layout.addWidget(self.canvas)
        except Exception as e:
            QMessageBox.warning(self, "绘制失败", f"绘制时出错：\n{e}")


class Pjjisuan(QWidget, Ui_pjjisuan_2):
    """平面几何计算页面 —— 使用已定义的 pjs 对象进行几何运算"""
    def __init__(self, parent, fs):
        super(Pjjisuan, self).__init__(parent)
        self.setupUi(self)
        self.fs = fs
        self.parent = parent
        self.pjjisuan_fangfa.currentIndexChanged.connect(self._on_method_changed)
        self.pjjisuan_jisuan.clicked.connect(self._compute)
        self.pjjisuan_canshu.returnPressed.connect(self._compute)
        self._on_method_changed(0)

    @property
    def pjs(self):
        if not hasattr(self.parent, 'pjs'):
            self.parent.pjs = {}
        return self.parent.pjs

    def _on_method_changed(self, idx):
        hints = {
            0: "", 1: "点1名,点2名", 2: "点1名,点2名",
            3: "点1名,点2名,...", 4: "点名,dx,dy",
            5: "点名,弧度,旋转中心名", 6: "点名,直线名",
            7: "点1名,点2名", 8: "点1名,点2名",
            9: "直线1名,直线2名", 10: "点名,直线名",
            11: "直线1名,直线2名", 12: "直线1名,直线2名",
            13: "直线1名,直线2名", 14: "圆名",
            15: "圆名", 16: "圆名", 17: "圆名",
            18: "圆1名,圆2名", 19: "点名,圆名",
            20: "三角形名", 21: "三角形名",
            22: "三角形名", 23: "三角形名",
            24: "三角形名", 25: "三角形名",
            26: "三角形名", 27: "三角形名",
            28: "三角形名", 29: "三角形名",
            30: "三角形名", 31: "顶点1名,顶点2名,...",
            32: "顶点1名,顶点2名,...",
        }
        hint = hints.get(idx, "")
        if hint:
            self.label_2.setText("参数(" + hint + ")：")
        else:
            self.label_2.setText("参数输入：")

    def _get_point(self, name):
        n = name.strip()
        if n in self.pjs and self.pjs[n][0] == "点":
            return self.pjs[n][1]
        raise ValueError(f"未找到点'{n}'")

    def _get_line_points(self, *params):
        """解析直线为两个点。用法: _get_line_points(line_name) 或 _get_line_points(pt1, pt2)"""
        if len(params) == 1:
            n = params[0].strip()
            if n in self.pjs and self.pjs[n][0] == "直线":
                return self.pjs[n][1].points[0], self.pjs[n][1].points[1]
        return tuple(self._get_point(p) for p in params[:2])

    def _get_circle(self, name):
        n = name.strip()
        if n in self.pjs and self.pjs[n][0] == "圆":
            return self.pjs[n][1]
        raise ValueError(f"未找到圆'{n}'")

    def _get_triangle_points(self, *params):
        """解析三角形为三个顶点。用法: _get_triangle_points(tri_name) 或 _get_triangle_points(p1,p2,p3)"""
        if len(params) == 1:
            n = params[0].strip()
            if n in self.pjs and self.pjs[n][0] == "三角形":
                return self.pjs[n][1].vertices
        return tuple(self._get_point(p) for p in params[:3])

    def _show_result(self, result):
        latex_str = latex(result)
        setWebEngineView('', latex_str, self.pjjisuan_result)
        self.pjjisuan_result_lineedit.setText(str(result))

    def _compute(self):
        idx = self.pjjisuan_fangfa.currentIndex()
        if idx == 0:
            return
        params_str = self.pjjisuan_canshu.text().strip()
        if not params_str:
            return
        raw = [p.strip() for p in params_str.split(',')]

        try:
            from planes import (
                point_distance, midpoint, collinear_check, translate_point,
                rotate_point, reflect_point, line_equation, line_slope,
                line_intersection, point_to_line_distance, angle_between_lines,
                parallel_check, perpendicular_check, circle_area_func,
                circle_circumference, circle_intersection, circle_tangent_lines,
                triangle_area, triangle_perimeter, triangle_circumcenter,
                triangle_circumradius, triangle_incenter, triangle_inradius,
                triangle_centroid, triangle_orthocenter, triangle_is_right,
                triangle_is_isosceles, triangle_is_equilateral,
                polygon_area_func, polygon_perimeter_func,
            )

            if idx == 1:  # 两点距离
                result = point_distance(self._get_point(raw[0]), self._get_point(raw[1]))
            elif idx == 2:  # 中点坐标
                result = midpoint(self._get_point(raw[0]), self._get_point(raw[1]))
            elif idx == 3:  # 共线判断
                pts = [self._get_point(p) for p in raw]
                result = collinear_check(pts)
            elif idx == 4:  # 平移点
                result = translate_point(self._get_point(raw[0]), raw[1], raw[2], self.fs)
            elif idx == 5:  # 绕定点旋转
                result = rotate_point(self._get_point(raw[0]), raw[1], self._get_point(raw[2]), self.fs)
            elif idx == 6:  # 点关于直线反射
                pt = self._get_point(raw[0])
                lp = self._get_line_points(*raw[1:])
                result = reflect_point(pt, lp[0], lp[1])
            elif idx == 7:  # 直线方程
                result = line_equation(self._get_point(raw[0]), self._get_point(raw[1]))
            elif idx == 8:  # 直线斜率
                result = line_slope(self._get_point(raw[0]), self._get_point(raw[1]))
            elif idx == 9:  # 两直线交点（2=两直线名, 4=四点名）
                if len(raw) <= 2:
                    lp1 = self._get_line_points(raw[0])
                    lp2 = self._get_line_points(raw[1])
                else:
                    lp1 = self._get_line_points(raw[0], raw[1])
                    lp2 = self._get_line_points(raw[2], raw[3])
                result = line_intersection(lp1[0], lp1[1], lp2[0], lp2[1])
            elif idx == 10:  # 点到直线距离
                pt = self._get_point(raw[0])
                lp = self._get_line_points(*raw[1:])
                result = point_to_line_distance(pt, lp[0], lp[1])
            elif idx == 11:  # 两直线夹角（2=两直线名, 4=四点名）
                if len(raw) <= 2:
                    lp1 = self._get_line_points(raw[0])
                    lp2 = self._get_line_points(raw[1])
                else:
                    lp1 = self._get_line_points(raw[0], raw[1])
                    lp2 = self._get_line_points(raw[2], raw[3])
                result = angle_between_lines(lp1[0], lp1[1], lp2[0], lp2[1])
            elif idx == 12:  # 平行判断（2=两直线名, 4=四点名）
                if len(raw) <= 2:
                    lp1 = self._get_line_points(raw[0])
                    lp2 = self._get_line_points(raw[1])
                else:
                    lp1 = self._get_line_points(raw[0], raw[1])
                    lp2 = self._get_line_points(raw[2], raw[3])
                result = parallel_check(lp1[0], lp1[1], lp2[0], lp2[1])
            elif idx == 13:  # 垂直判断（2=两直线名, 4=四点名）
                if len(raw) <= 2:
                    lp1 = self._get_line_points(raw[0])
                    lp2 = self._get_line_points(raw[1])
                else:
                    lp1 = self._get_line_points(raw[0], raw[1])
                    lp2 = self._get_line_points(raw[2], raw[3])
                result = perpendicular_check(lp1[0], lp1[1], lp2[0], lp2[1])
            elif idx == 14:  # 圆心坐标
                c = self._get_circle(raw[0])
                result = (radsimp(c.center.x), radsimp(c.center.y))
            elif idx == 15:  # 圆半径
                c = self._get_circle(raw[0])
                result = radsimp(c.radius)
            elif idx == 16:  # 圆面积
                c = self._get_circle(raw[0])
                result = radsimp(c.area)
            elif idx == 17:  # 圆周长
                c = self._get_circle(raw[0])
                result = radsimp(c.circumference)
            elif idx == 18:  # 两圆交点
                c1, c2 = self._get_circle(raw[0]), self._get_circle(raw[1])
                inter = c1.intersection(c2)
                result = []
                for pt in inter:
                    result.append((radsimp(pt.x), radsimp(pt.y)))
                result = result if result else "两圆不相交"
            elif idx == 19:  # 圆切线方程
                pt = self._get_point(raw[0])
                c = self._get_circle(raw[1])
                from sympy import simplify
                tangents = c.tangent_lines(pt)
                result = []
                for line in tangents:
                    result.append(simplify(line.equation()))
                result = result if result else "无切线"
            elif idx == 20:  # 三角形面积
                v = self._get_triangle_points(*raw)
                result = triangle_area(*v)
            elif idx == 21:  # 三角形周长
                v = self._get_triangle_points(*raw)
                result = triangle_perimeter(*v)
            elif idx == 22:  # 三角形外心
                v = self._get_triangle_points(*raw)
                result = triangle_circumcenter(*v)
            elif idx == 23:  # 三角形外接圆半径
                v = self._get_triangle_points(*raw)
                result = triangle_circumradius(*v)
            elif idx == 24:  # 三角形内心
                v = self._get_triangle_points(*raw)
                result = triangle_incenter(*v)
            elif idx == 25:  # 三角形内切圆半径
                v = self._get_triangle_points(*raw)
                result = triangle_inradius(*v)
            elif idx == 26:  # 三角形重心
                v = self._get_triangle_points(*raw)
                result = triangle_centroid(*v)
            elif idx == 27:  # 三角形垂心
                v = self._get_triangle_points(*raw)
                result = triangle_orthocenter(*v)
            elif idx == 28:  # 直角三角形判断
                v = self._get_triangle_points(*raw)
                result = triangle_is_right(*v)
            elif idx == 29:  # 等腰三角形判断
                v = self._get_triangle_points(*raw)
                result = triangle_is_isosceles(*v)
            elif idx == 30:  # 等边三角形判断
                v = self._get_triangle_points(*raw)
                result = triangle_is_equilateral(*v)
            elif idx == 31:  # 多边形面积
                pts = [self._get_point(p) for p in raw]
                result = polygon_area_func(pts)
            elif idx == 32:  # 多边形周长
                pts = [self._get_point(p) for p in raw]
                result = polygon_perimeter_func(pts)
            else:
                result = "未知操作"

            self._show_result(result)
        except Exception as e:
            self.pjjisuan_result.setHtml("")
            self.pjjisuan_result_lineedit.setText(f"计算错误: {e}")


class Ljjisuan(QWidget, Ui_ljjisuan):
    """立体几何计算页面 —— 使用已定义的 ljs 对象进行三维几何运算"""
    def __init__(self, parent, fs):
        super(Ljjisuan, self).__init__(parent)
        self.setupUi(self)
        self.fs = fs
        self.parent = parent
        self.ljjisuan_fangfa.currentIndexChanged.connect(self._on_method_changed)
        self.ljjisuan_jisuan.clicked.connect(self._compute)
        self.ljjisuan_canshu.returnPressed.connect(self._compute)
        self._on_method_changed(0)

    @property
    def ljs(self):
        if not hasattr(self.parent, 'ljs'):
            self.parent.ljs = {}
        return self.parent.ljs

    def _on_method_changed(self, idx):
        hints = {
            0: "", 1: "点1名,点2名", 2: "点1名,点2名",
            3: "点名,平面名", 4: "点名,直线名",
            5: "点名,平面名", 6: "点名,直线名",
            7: "点1名,点2名,...", 8: "直线名",
            9: "直线1名,直线2名", 10: "直线1名,直线2名",
            11: "直线1名,直线2名", 12: "直线1名,直线2名",
            13: "直线名,平面名", 14: "点1名,点2名,点3名",
            15: "平面名", 16: "平面1名,平面2名",
            17: "平面1名,平面2名", 18: "平面1名,平面2名",
            19: "平面1名,平面2名", 20: "平面名,直线名",
            21: "点A名,点B名,点C名,点D名", 22: "直线名,平面名",
        }
        hint = hints.get(idx, "")
        if hint:
            self.label_2.setText("参数(" + hint + ")：")
        else:
            self.label_2.setText("参数输入：")

    def _get_point3d(self, name):
        n = name.strip()
        if n in self.ljs and self.ljs[n][0] == "点":
            return self.ljs[n][1]
        raise ValueError(f"未找到三维点'{n}'")

    def _get_line3d(self, name):
        n = name.strip()
        if n in self.ljs and self.ljs[n][0] == "直线":
            return self.ljs[n][1]
        # 也尝试由两点名解析
        raise ValueError(f"未找到三维直线'{n}'")

    def _get_line3d_or_from_points(self, *params):
        """解析为 Line3D：单个直线名 或 两个点名"""
        if len(params) == 1:
            n = params[0].strip()
            if n in self.ljs and self.ljs[n][0] == "直线":
                return self.ljs[n][1]
            raise ValueError(f"未找到三维直线'{n}'")
        from sympy.geometry import Line3D
        return Line3D(self._get_point3d(params[0]), self._get_point3d(params[1]))

    def _get_plane(self, name):
        n = name.strip()
        if n in self.ljs and self.ljs[n][0] == "平面":
            return self.ljs[n][1]
        raise ValueError(f"未找到平面'{n}'")

    def _show_result(self, result):
        latex_str = latex(result)
        setWebEngineView('', latex_str, self.ljjisuan_result)
        self.ljjisuan_result_lineedit.setText(str(result))

    def _compute(self):
        idx = self.ljjisuan_fangfa.currentIndex()
        if idx == 0:
            return
        params_str = self.ljjisuan_canshu.text().strip()
        if not params_str:
            return
        raw = [p.strip() for p in params_str.split(',')]

        try:
            from solids import (
                point3d_distance, point3d_midpoint, point3d_to_plane_distance,
                point3d_to_line_distance, point3d_projection_on_plane,
                point3d_projection_on_line, are_coplanar, line3d_direction,
                line3d_intersection, line3d_angle, line3d_parallel_check,
                line3d_perpendicular_check, line3d_projection_on_plane,
                plane_equation_from_points, plane_normal_vector,
                plane_angle_between, plane_parallel_check,
                plane_perpendicular_check, plane_intersection,
                plane_line_intersection, tetrahedron_volume, line_plane_angle,
            )

            if idx == 1:  # 两点距离
                result = point3d_distance(self._get_point3d(raw[0]), self._get_point3d(raw[1]))
            elif idx == 2:  # 中点坐标
                result = point3d_midpoint(self._get_point3d(raw[0]), self._get_point3d(raw[1]))
            elif idx == 3:  # 点到平面距离
                result = point3d_to_plane_distance(self._get_point3d(raw[0]), self._get_plane(raw[1]))
            elif idx == 4:  # 点到直线距离
                result = point3d_to_line_distance(self._get_point3d(raw[0]), self._get_line3d_or_from_points(*raw[1:]))
            elif idx == 5:  # 点在平面投影
                result = point3d_projection_on_plane(self._get_point3d(raw[0]), self._get_plane(raw[1]))
            elif idx == 6:  # 点在直线投影
                result = point3d_projection_on_line(self._get_point3d(raw[0]), self._get_line3d_or_from_points(*raw[1:]))
            elif idx == 7:  # 共面判断
                pts = [self._get_point3d(p) for p in raw]
                result = are_coplanar(pts)
            elif idx == 8:  # 直线方向向量
                result = line3d_direction(self._get_line3d_or_from_points(*raw))
            elif idx == 9:  # 两直线交点
                result = line3d_intersection(
                    self._get_line3d_or_from_points(*raw[:len(raw)//2]),
                    self._get_line3d_or_from_points(*raw[len(raw)//2:]))
            elif idx == 10:  # 两直线夹角
                result = line3d_angle(
                    self._get_line3d_or_from_points(*raw[:len(raw)//2]),
                    self._get_line3d_or_from_points(*raw[len(raw)//2:]))
            elif idx == 11:  # 平行判断(线)
                result = line3d_parallel_check(
                    self._get_line3d_or_from_points(*raw[:len(raw)//2]),
                    self._get_line3d_or_from_points(*raw[len(raw)//2:]))
            elif idx == 12:  # 垂直判断(线)
                result = line3d_perpendicular_check(
                    self._get_line3d_or_from_points(*raw[:len(raw)//2]),
                    self._get_line3d_or_from_points(*raw[len(raw)//2:]))
            elif idx == 13:  # 直线在平面投影（参数：直线名,平面名 或 两点名,平面名）
                result = line3d_projection_on_plane(
                    self._get_line3d_or_from_points(*raw[:-1]),
                    self._get_plane(raw[-1]))
            elif idx == 14:  # 三点求平面方程
                result = plane_equation_from_points(
                    self._get_point3d(raw[0]), self._get_point3d(raw[1]), self._get_point3d(raw[2]))
            elif idx == 15:  # 平面法向量
                result = plane_normal_vector(self._get_plane(raw[0]))
            elif idx == 16:  # 两平面夹角
                result = plane_angle_between(self._get_plane(raw[0]), self._get_plane(raw[1]))
            elif idx == 17:  # 两平面交线
                result = plane_intersection(self._get_plane(raw[0]), self._get_plane(raw[1]))
            elif idx == 18:  # 平行判断(面)
                result = plane_parallel_check(self._get_plane(raw[0]), self._get_plane(raw[1]))
            elif idx == 19:  # 垂直判断(面)
                result = plane_perpendicular_check(self._get_plane(raw[0]), self._get_plane(raw[1]))
            elif idx == 20:  # 平面与直线交点
                result = plane_line_intersection(self._get_plane(raw[0]), self._get_line3d_or_from_points(*raw[1:]))
            elif idx == 21:  # 四面体体积
                result = tetrahedron_volume(
                    self._get_point3d(raw[0]), self._get_point3d(raw[1]),
                    self._get_point3d(raw[2]), self._get_point3d(raw[3]))
            elif idx == 22:  # 直线与平面夹角（参数：直线名,平面名 或 两点名,平面名）
                result = line_plane_angle(
                    self._get_line3d_or_from_points(*raw[:-1]),
                    self._get_plane(raw[-1]))
            else:
                result = "未知操作"

            self._show_result(result)
        except Exception as e:
            self.ljjisuan_result.setHtml("")
            self.ljjisuan_result_lineedit.setText(f"计算错误: {e}")


#tabs_name = ["首页", "定义", "求导", "积分", "变形", "方程", "方程组", "不等式", "不等式组", "帮助"]
tabs_list = [Shouye, Dingyi, Qiudao, Jifen, Bianxing, Fangcheng, Fangchengzu, Budengshi, Budengshizu, Jisuan, Help, Dingyixiangliang, Huitu_hanshu, Jiesanjiaoxing, Dingyi_pj, Huitu_pj, Dingyi_lj, Huitu_lj, Pjjisuan, Ljjisuan]
tabs_dict = {"首页":0, "定义":1, "求导":2, "积分":3, "变形":4, "方程":5, "方程组":6, "不等式":7, "不等式组":8, "计算":9, "帮助":10, "定义向量":11, "绘制函数":12, "解三角形":13, "平面几何":14, "平面绘图":15, "立体几何":16, "立体绘图":17, "平面计算":18, "立体计算":19}
