from PySide6.QtWidgets import QLineEdit, QVBoxLayout, QWidget

from core.webengine import ensure_webengine_ready
from expr_calculator.expr_viewer import MainWindow as ExprCanvas


class Expr(QWidget):
    def __init__(self, parent, fs):
        super().__init__(parent)
        ensure_webengine_ready()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.viewer = ExprCanvas()
        layout.addWidget(self.viewer)
        '''for lineedit in self.viewer.findChildren(QLineEdit):
            lineedit.actions_wired = True'''
