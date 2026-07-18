from ui.ui_ljjisuan import *
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex
from PySide6.QtWidgets import QWidget

class Ljjisuan(QWidget, Ui_ljjisuan):
    """立体几何计算页面 —— 使用已定义的 ljs 对象进行三维几何运算"""
    def __init__(self, parent, fs):
        super(Ljjisuan, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

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
        setGraphicsView('', latex_str, self.ljjisuan_result)
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
            from functions.solids import (
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
