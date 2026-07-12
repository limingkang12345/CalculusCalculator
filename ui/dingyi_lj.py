from ui.ui_dingyi_lj import *
from PySide6.QtWidgets import QWidget, QMessageBox
from core.render import setGraphicsView, setGraphicsViewTheme

class Dingyi_lj(QWidget, Ui_dingyi_lj):
    """立体几何对象定义页面"""
    def __init__(self, parent, fs):
        super(Dingyi_lj, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

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
            from functions.solids import (create_point3d, create_line3d,
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
