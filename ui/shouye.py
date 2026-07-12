from ui.ui_shouye import *
from PySide6.QtWidgets import QWidget

class Shouye(QWidget, Ui_shouye):
    def __init__(self, parent, fs):
        super(Shouye, self).__init__(parent)
        self.setupUi(self)