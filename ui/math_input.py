from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QCoreApplication

from math_input import MathDialog

def open_formula_dialog(parent):
    from sympy import latex
    from core.sympify import sympify
    # 创建公式对话框
    dlg = MathDialog(
        parent=parent,
        title=QCoreApplication.translate("MainWindow", "插入公式"),
        initial_text = latex(sympify(parent.text(), {})),
        toolbar_groups=["struct", "greek", "edit", "operators", "functions"],
        show_output=True,
        zoom=1.2
    )

    if dlg.exec() == QDialog.Accepted:
        latex = dlg.result_latex()
        parent.setText(str(sympify('$' + latex, {})))
