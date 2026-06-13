from PySide6.QtWidgets import QFileDialog, QLineEdit, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
from sympy import latex, Line, Circle, Point
from sympify import sympify
import ui
import json


def _fix_old_format(obj, cat, val_str, fs):
    """向后兼容：旧格式用 equation() 存了线和圆的方程字符串，需从方程重建对象"""
    from sympy import Line, Circle
    if cat == "直线" and not isinstance(obj, Line):
        try:
            obj = Line(sympify(val_str, fs))
        except Exception: pass
    elif cat == "圆" and not isinstance(obj, Circle):
        try:
            obj = Circle(sympify(val_str, fs))
        except Exception: pass
    return obj


def _fix_old_format_3d(obj, cat, val_str, fs):
    """向后兼容：3D 旧格式用 equation() 存了平面方程"""
    from sympy.geometry import Line3D, Plane
    if cat == "直线" and not isinstance(obj, Line3D):
        try:
            obj = Line3D(sympify(val_str, fs))
        except Exception: pass
    elif cat == "平面" and not isinstance(obj, Plane):
        try:
            obj = Plane(sympify(val_str, fs))
        except Exception: pass
    return obj


def savefile(main_class):
    # 保存项目
    # main_class(class):主窗口类
    filename = QFileDialog.getSaveFileName(main_class, "Save File", "Project", "JSON Files (*.json)")[0]
    output = {}
    if filename:
        with open(filename, mode = "w") as file:
            item_output = {}
            for i in main_class.tabs.items():
                item_output[i[0]] = {}
                for lineedit in i[1].findChildren(QLineEdit, options = Qt.FindChildrenRecursively):
                    item_output[i[0]][lineedit.objectName()] = lineedit.text()
            output["texts"] = item_output
            output["fs"] = main_class.fs
            output["tabs_n"] = main_class.tabs_n
            output["eqs"] = list(main_class.eqs.keys())
            output["rels"] = list(main_class.rels.keys())
            output["vs"] = main_class.vs
            # 平面几何对象数据
            if hasattr(main_class, 'pjs'):
                pjs_save = {}
                for k, v in main_class.pjs.items():
                    cat = v[0]
                    pjs_save[k] = [cat, repr(v[1])]
                output["pjs"] = pjs_save
            # 立体几何对象数据
            if hasattr(main_class, 'ljs'):
                ljs_save = {}
                for k, v in main_class.ljs.items():
                    cat = v[0]
                    ljs_save[k] = [cat, repr(v[1])]
                output["ljs"] = ljs_save
            file.write(json.dumps(output))

def openfile(main_class):
    # 打开项目
    # main_class(class):主窗口类
    filename = QFileDialog.getOpenFileName(main_class, "Open File", "", "JSON Files (*.json)")[0]

    if filename:
        with open(filename, mode = "r") as file:
            json_data = json.loads(file.read())
            #try:
            if 1:
                main_class.fs = json_data["fs"]
                main_class.tabs_n = json_data["tabs_n"]
                main_class.eqs = {i:sympify(i, main_class.fs) for i in json_data["eqs"]}
                main_class.rels = {i:sympify(i, main_class.fs) for i in json_data["rels"]}
                main_class.vs = json_data["vs"]
                if "pjs" in json_data:
                    main_class.pjs = {}
                    for k, v in json_data["pjs"].items():
                        cat, val_str = v[0], v[1]
                        try:
                            obj = sympify(val_str, main_class.fs)
                        except Exception:
                            obj = None
                        if obj is not None:
                            obj = _fix_old_format(obj, cat, val_str, main_class.fs)
                        main_class.pjs[k] = (cat, obj)
                if "ljs" in json_data:
                    main_class.ljs = {}
                    for k, v in json_data["ljs"].items():
                        cat, val_str = v[0], v[1]
                        try:
                            obj = sympify(val_str, main_class.fs)
                        except Exception:
                            obj = None
                        if obj is not None:
                            obj = _fix_old_format_3d(obj, cat, val_str, main_class.fs)
                        main_class.ljs[k] = (cat, obj)
                for i in range(main_class.ui.tabWidget.count() - 1, -1, -1):
                    main_class.close_tab(i, auto_create = False)
                for tab_name in json_data["texts"].keys():
                    name_str = ''.join([c for c in tab_name if not c.isdigit()])
                    n_str = ''.join([c for c in tab_name if c.isdigit()])
                    main_class.create_tab(ui.tabs_dict[name_str], n = int(n_str) if n_str else 0)
                    # 将保存的文本框文本自动填入对应的 QLineEdit
                    saved_texts = json_data["texts"].get(tab_name, {})
                    if tab_name in main_class.tabs:
                        tab_widget = main_class.tabs[tab_name]
                        for lineedit in tab_widget.findChildren(QLineEdit):
                            if lineedit.objectName() in saved_texts:
                                lineedit.setText(saved_texts[lineedit.objectName()])
                        # 自动渲染数学公式：文本框名称后缀为"_lineedit"则去掉该后缀即为对应的Web浏览框对象名
                        for lineedit in tab_widget.findChildren(QLineEdit):
                            if lineedit.objectName().endswith('_lineedit') and lineedit.text():
                                view_name = lineedit.objectName()[:-9]
                                view = tab_widget.findChild(QWebEngineView, view_name)
                                if view is not None:
                                    try:
                                        expr = sympify(lineedit.text(), main_class.fs)
                                        ui.setWebEngineView('', latex(expr), view)
                                    except:
                                        pass
            #except:
                #QMessageBox.warning(main_class, "警告", "提供的配置文件错误")
