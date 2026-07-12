from ui.ui_pjjisuan import *
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex, radsimp
from PySide6.QtWidgets import QWidget

class Pjjisuan(QWidget, Ui_pjjisuan_2):
    """平面几何计算页面 —— 使用已定义的 pjs 对象进行几何运算"""
    def __init__(self, parent, fs):
        super(Pjjisuan, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

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
        setGraphicsView('', latex_str, self.pjjisuan_result)
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
            from functions.planes import (
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
