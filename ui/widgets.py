from PySide6.QtWidgets import QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class ListWidgetWithDelete(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def add_item_with_delete(self, text):
        # 1. 创建一个 QListWidgetItem
        item = QListWidgetItem(self)
        item.setText(text)

        # 2. 创建自定义小部件（包含标签和删除按钮）
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        label = QLabel("")
        # 让标签占据尽可能多的空间，按钮靠右
        layout.addWidget(label, 1)

        delete_btn = QPushButton("✕")
        delete_btn.setFixedSize(20, 20)
        delete_btn.setCursor(Qt.PointingHandCursor)
        # 按钮点击时删除该项
        delete_btn.clicked.connect(lambda: self.remove_item(widget))

        layout.addWidget(delete_btn)

        # 3. 将自定义小部件设置给该项
        self.setItemWidget(item, widget)

        widget.adjustSize()  # 通知 widget 重新计算尺寸
        item.setSizeHint(widget.sizeHint())
    
    def remove_item(self, widget):
        """根据 widget 找到对应的 item 并删除"""
        for i in range(self.count()):
            if self.itemWidget(self.item(i)) == widget:
                item_to_remove = self.takeItem(i)
                w = self
                while w is not None:
                    if hasattr(w, 'cache') and hasattr(w, 'fs'):
                        break
                    w = w.parentWidget()
                #print(w)
                return w.cache.pop(i)
                break

    def addItems(self, texts):
        # 重写批量添加列表项方法

        for i in texts:
            self.add_item_with_delete(i)