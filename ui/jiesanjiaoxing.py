from ui.ui_jiesanjiaoxing import *
from functions.solvers import solve_sanjiaoxing
from core.sympify import sympify
from core.render import setGraphicsView, setGraphicsViewTheme
from sympy import latex
from PySide6.QtWidgets import QWidget

class Jiesanjiaoxing(QWidget, Ui_jiesanjiaoxing):
    def __init__(self, parent, fs):
        super(Jiesanjiaoxing, self).__init__(parent)
        self.setupUi(self)
        setGraphicsViewTheme(self, parent)

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
            setGraphicsView('', condition_latex, self.jiesanjiaoxing_yuantiaojian)
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
            setGraphicsView('', result_latex, self.jiesanjiaoxing_jieguo)
        except Exception:
            pass
