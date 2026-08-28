# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'functionsLLDlXx.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGraphicsView, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_functions(object):
    def setupUi(self, functions):
        if not functions.objectName():
            functions.setObjectName(u"functions")
        functions.resize(1440, 855)
        self.gridLayout_3 = QGridLayout(functions)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.draw = QGroupBox(functions)
        self.draw.setObjectName(u"draw")
        self.verticalLayout = QVBoxLayout(self.draw)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.draw_mode = QComboBox(self.draw)
        self.draw_mode.addItem("")
        self.draw_mode.addItem("")
        self.draw_mode.setObjectName(u"draw_mode")

        self.verticalLayout.addWidget(self.draw_mode)

        self.draw_draw = QPushButton(self.draw)
        self.draw_draw.setObjectName(u"draw_draw")

        self.verticalLayout.addWidget(self.draw_draw)

        self.draw_objs = QListWidget(self.draw)
        self.draw_objs.setObjectName(u"draw_objs")

        self.verticalLayout.addWidget(self.draw_objs)

        self.draw_output = QGraphicsView(self.draw)
        self.draw_output.setObjectName(u"draw_output")

        self.verticalLayout.addWidget(self.draw_output)


        self.gridLayout_3.addWidget(self.draw, 0, 3, 1, 1)

        self.calc_groupbox = QGroupBox(functions)
        self.calc_groupbox.setObjectName(u"calc_groupbox")
        self.gridLayout_2 = QGridLayout(self.calc_groupbox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.calc_preview = QGraphicsView(self.calc_groupbox)
        self.calc_preview.setObjectName(u"calc_preview")

        self.gridLayout_2.addWidget(self.calc_preview, 5, 0, 1, 2)

        self.calc_input = QTableWidget(self.calc_groupbox)
        if (self.calc_input.columnCount() < 1):
            self.calc_input.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.calc_input.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.calc_input.setObjectName(u"calc_input")
        self.calc_input.horizontalHeader().setStretchLastSection(True)

        self.gridLayout_2.addWidget(self.calc_input, 3, 0, 1, 2)

        self.calc_output = QLineEdit(self.calc_groupbox)
        self.calc_output.setObjectName(u"calc_output")

        self.gridLayout_2.addWidget(self.calc_output, 6, 1, 1, 1)

        self.calc_result = QLineEdit(self.calc_groupbox)
        self.calc_result.setObjectName(u"calc_result")

        self.gridLayout_2.addWidget(self.calc_result, 1, 1, 1, 1)

        self.calc_label_output = QLabel(self.calc_groupbox)
        self.calc_label_output.setObjectName(u"calc_label_output")

        self.gridLayout_2.addWidget(self.calc_label_output, 6, 0, 1, 1)

        self.calc_function = QComboBox(self.calc_groupbox)
        self.calc_function.setObjectName(u"calc_function")

        self.gridLayout_2.addWidget(self.calc_function, 0, 1, 1, 1)

        self.calc_label_result = QLabel(self.calc_groupbox)
        self.calc_label_result.setObjectName(u"calc_label_result")

        self.gridLayout_2.addWidget(self.calc_label_result, 1, 0, 1, 1)

        self.calc_label_function = QLabel(self.calc_groupbox)
        self.calc_label_function.setObjectName(u"calc_label_function")

        self.gridLayout_2.addWidget(self.calc_label_function, 0, 0, 1, 1)

        self.calc_calc = QPushButton(self.calc_groupbox)
        self.calc_calc.setObjectName(u"calc_calc")

        self.gridLayout_2.addWidget(self.calc_calc, 2, 0, 1, 2)

        self.calc_label_preview = QLabel(self.calc_groupbox)
        self.calc_label_preview.setObjectName(u"calc_label_preview")

        self.gridLayout_2.addWidget(self.calc_label_preview, 4, 0, 1, 2)


        self.gridLayout_3.addWidget(self.calc_groupbox, 0, 1, 1, 1)

        self.def_groupbox = QGroupBox(functions)
        self.def_groupbox.setObjectName(u"def_groupbox")
        self.gridLayout = QGridLayout(self.def_groupbox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.def_objs = QTreeWidget(self.def_groupbox)
        QTreeWidgetItem(self.def_objs)
        QTreeWidgetItem(self.def_objs)
        QTreeWidgetItem(self.def_objs)
        self.def_objs.setObjectName(u"def_objs")
        self.def_objs.header().setDefaultSectionSize(150)

        self.gridLayout.addWidget(self.def_objs, 0, 0, 1, 2)

        self.def_input = QTableWidget(self.def_groupbox)
        if (self.def_input.columnCount() < 1):
            self.def_input.setColumnCount(1)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.def_input.setHorizontalHeaderItem(0, __qtablewidgetitem1)
        self.def_input.setObjectName(u"def_input")
        self.def_input.horizontalHeader().setCascadingSectionResizes(False)
        self.def_input.horizontalHeader().setStretchLastSection(True)
        self.def_input.verticalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.def_input, 5, 0, 1, 2)

        self.def_buttons = QHBoxLayout()
        self.def_buttons.setObjectName(u"def_buttons")
        self.def_save = QPushButton(self.def_groupbox)
        self.def_save.setObjectName(u"def_save")

        self.def_buttons.addWidget(self.def_save)

        self.def_clear = QPushButton(self.def_groupbox)
        self.def_clear.setObjectName(u"def_clear")

        self.def_buttons.addWidget(self.def_clear)


        self.gridLayout.addLayout(self.def_buttons, 6, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.def_edit = QPushButton(self.def_groupbox)
        self.def_edit.setObjectName(u"def_edit")

        self.horizontalLayout.addWidget(self.def_edit)

        self.def_del = QPushButton(self.def_groupbox)
        self.def_del.setObjectName(u"def_del")

        self.horizontalLayout.addWidget(self.def_del)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.def_label_type = QLabel(self.def_groupbox)
        self.def_label_type.setObjectName(u"def_label_type")

        self.gridLayout.addWidget(self.def_label_type, 2, 0, 1, 1)

        self.def_output = QLineEdit(self.def_groupbox)
        self.def_output.setObjectName(u"def_output")

        self.gridLayout.addWidget(self.def_output, 9, 1, 1, 1)

        self.def_label_output = QLabel(self.def_groupbox)
        self.def_label_output.setObjectName(u"def_label_output")

        self.gridLayout.addWidget(self.def_label_output, 9, 0, 1, 1)

        self.def_type = QComboBox(self.def_groupbox)
        self.def_type.addItem("")
        self.def_type.addItem("")
        self.def_type.addItem("")
        self.def_type.setObjectName(u"def_type")

        self.gridLayout.addWidget(self.def_type, 2, 1, 2, 1)

        self.def_preview = QGraphicsView(self.def_groupbox)
        self.def_preview.setObjectName(u"def_preview")

        self.gridLayout.addWidget(self.def_preview, 8, 0, 1, 2)

        self.def_label_preview = QLabel(self.def_groupbox)
        self.def_label_preview.setObjectName(u"def_label_preview")

        self.gridLayout.addWidget(self.def_label_preview, 7, 0, 1, 1)

        self.def_preview_mode = QComboBox(self.def_groupbox)
        self.def_preview_mode.addItem("")
        self.def_preview_mode.addItem("")
        self.def_preview_mode.setObjectName(u"def_preview_mode")

        self.gridLayout.addWidget(self.def_preview_mode, 7, 1, 1, 1)


        self.gridLayout_3.addWidget(self.def_groupbox, 0, 0, 1, 1)


        self.retranslateUi(functions)

        QMetaObject.connectSlotsByName(functions)
    # setupUi

    def retranslateUi(self, functions):
        functions.setWindowTitle(QCoreApplication.translate("functions", u"Form", None))
        self.draw.setTitle(QCoreApplication.translate("functions", u"\u7ed8\u56fe\u533a", None))
        self.draw_mode.setItemText(0, QCoreApplication.translate("functions", u"\u5e73\u9762\u51e0\u4f55\u6a21\u5f0f", None))
        self.draw_mode.setItemText(1, QCoreApplication.translate("functions", u"\u7acb\u4f53\u51e0\u4f55\u6a21\u5f0f", None))

        self.draw_draw.setText(QCoreApplication.translate("functions", u"\u7ed8\u5236", None))
        self.calc_groupbox.setTitle(QCoreApplication.translate("functions", u"\u8ba1\u7b97\u533a", None))
        ___qtablewidgetitem = self.calc_input.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("functions", u"\u8f93\u5165\u53c2\u6570", None))
        self.calc_label_output.setText(QCoreApplication.translate("functions", u"\u8f93\u51fa\uff1a", None))
        self.calc_label_result.setText(QCoreApplication.translate("functions", u"\u7ed3\u679c\u4fdd\u5b58\u4e3a\uff1a", None))
        self.calc_label_function.setText(QCoreApplication.translate("functions", u"\u8ba1\u7b97\u529f\u80fd\uff1a", None))
        self.calc_calc.setText(QCoreApplication.translate("functions", u"\u8ba1\u7b97(Enter)", None))
        self.calc_label_preview.setText(QCoreApplication.translate("functions", u"\u8ba1\u7b97\u7ed3\u679c\u9884\u89c8\uff1a", None))
        self.def_groupbox.setTitle(QCoreApplication.translate("functions", u"\u5b9a\u4e49\u533a", None))
        ___qtreewidgetitem = self.def_objs.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("functions", u"\u5c5e\u6027\u503c", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("functions", u"\u5bf9\u8c61/\u5c5e\u6027", None))

        __sortingEnabled = self.def_objs.isSortingEnabled()
        self.def_objs.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.def_objs.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("functions", u"\u51fd\u6570", None))
        ___qtreewidgetitem2 = self.def_objs.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("functions", u"\u96c6\u5408", None))
        ___qtreewidgetitem3 = self.def_objs.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("functions", u"\u5411\u91cf", None))
        self.def_objs.setSortingEnabled(__sortingEnabled)

        ___qtablewidgetitem1 = self.def_input.horizontalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("functions", u"\u8f93\u5165\u53c2\u6570", None))
        self.def_save.setText(QCoreApplication.translate("functions", u"\u4fdd\u5b58\u8f93\u5165", None))
        self.def_clear.setText(QCoreApplication.translate("functions", u"\u6e05\u7a7a\u8f93\u5165", None))
        self.def_edit.setText(QCoreApplication.translate("functions", u"\u7f16\u8f91\u5b9a\u4e49", None))
        self.def_del.setText(QCoreApplication.translate("functions", u"\u5220\u9664\u5b9a\u4e49", None))
        self.def_label_type.setText(QCoreApplication.translate("functions", u"\u7c7b\u578b\uff1a", None))
        self.def_label_output.setText(QCoreApplication.translate("functions", u"\u8f93\u51fa\uff1a", None))
        self.def_type.setItemText(0, QCoreApplication.translate("functions", u"\u51fd\u6570", None))
        self.def_type.setItemText(1, QCoreApplication.translate("functions", u"\u96c6\u5408", None))
        self.def_type.setItemText(2, QCoreApplication.translate("functions", u"\u5411\u91cf", None))

        self.def_label_preview.setText(QCoreApplication.translate("functions", u"\u9884\u89c8\uff1a", None))
        self.def_preview_mode.setItemText(0, QCoreApplication.translate("functions", u"\u76f4\u63a5\u6a21\u5f0f(\u4e0d\u81ea\u52a8\u66ff\u6362\u8868\u8fbe\u5f0f\u4e2d\u7684\u81ea\u5b9a\u4e49\u51fd\u6570)", None))
        self.def_preview_mode.setItemText(1, QCoreApplication.translate("functions", u"\u66ff\u6362\u6a21\u5f0f(\u81ea\u52a8\u66ff\u6362\u8868\u8fbe\u5f0f\u4e2d\u7684\u81ea\u5b9a\u4e49\u51fd\u6570)", None))

    # retranslateUi

