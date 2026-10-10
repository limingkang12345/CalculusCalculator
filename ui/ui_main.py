# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 880)
        MainWindow.setMinimumSize(QSize(1024, 640))
        icon = QIcon()
        icon.addFile(u"../favicon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.actionshouye = QAction(MainWindow)
        self.actionshouye.setObjectName(u"actionshouye")
        self.actionhelp = QAction(MainWindow)
        self.actionhelp.setObjectName(u"actionhelp")
        self.actiongithub = QAction(MainWindow)
        self.actiongithub.setObjectName(u"actiongithub")
        self.actionwebsite = QAction(MainWindow)
        self.actionwebsite.setObjectName(u"actionwebsite")
        self.actionsaveas = QAction(MainWindow)
        self.actionsaveas.setObjectName(u"actionsaveas")
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.actionexit = QAction(MainWindow)
        self.actionexit.setObjectName(u"actionexit")
        self.actionshezhi = QAction(MainWindow)
        self.actionshezhi.setObjectName(u"actionshezhi")
        self.actionhuancun = QAction(MainWindow)
        self.actionhuancun.setObjectName(u"actionhuancun")
        self.actionblockly = QAction(MainWindow)
        self.actionblockly.setObjectName(u"actionblockly")
        self.actionyindao = QAction(MainWindow)
        self.actionyindao.setObjectName(u"actionyindao")
        self.actionfunctions = QAction(MainWindow)
        self.actionfunctions.setObjectName(u"actionfunctions")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideRight)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1440, 25))
        self.functions = QMenu(self.menubar)
        self.functions.setObjectName(u"functions")
        self.about = QMenu(self.menubar)
        self.about.setObjectName(u"about")
        self.file = QMenu(self.menubar)
        self.file.setObjectName(u"file")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.functions.menuAction())
        self.menubar.addAction(self.about.menuAction())
        self.functions.addAction(self.actionshouye)
        self.functions.addAction(self.actionfunctions)
        self.functions.addAction(self.actionblockly)
        self.about.addAction(self.actiongithub)
        self.about.addAction(self.actionwebsite)
        self.about.addAction(self.actionyindao)
        self.about.addAction(self.actionhelp)
        self.file.addAction(self.actionsaveas)
        self.file.addAction(self.actionopen)
        self.file.addAction(self.actionhuancun)
        self.file.addAction(self.actionshezhi)
        self.file.addAction(self.actionexit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CalculusCalculator", None))
        self.actionshouye.setText(QCoreApplication.translate("MainWindow", u"\u9996\u9875", None))
        self.actionhelp.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.actiongithub.setText(QCoreApplication.translate("MainWindow", u"Github\u94fe\u63a5", None))
        self.actionwebsite.setText(QCoreApplication.translate("MainWindow", u"\u7f51\u9875\u7248", None))
        self.actionsaveas.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4e3a", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.actionexit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.actionshezhi.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actionhuancun.setText(QCoreApplication.translate("MainWindow", u"\u7f13\u5b58\u533a", None))
        self.actionblockly.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u5668", None))
        self.actionyindao.setText(QCoreApplication.translate("MainWindow", u"\u5f15\u5bfc\u6559\u5b66", None))
        self.actionfunctions.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u96c6\u6210", None))
        self.functions.setTitle(QCoreApplication.translate("MainWindow", u"\u529f\u80fd", None))
        self.about.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.file.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
    # retranslateUi

