from PySide6.QtWidgets import QFileDialog, QLineEdit, QMessageBox, QGraphicsView, QComboBox
from PySide6.QtCore import Qt
from sympy import latex, Line, Circle, Point
from core.sympify import sympify
from core.render import setGraphicsView, _svg_cache
import ui
import json
from core.settings import current_language


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
        # 读取存档过滤设置（若从未设置，默认全部保存）
        filters = getattr(main_class, 'save_filters', None)

        def _save(key):
            """检查 key 对应的存档项是否应保存。filters 为 None 时全存。"""
            if filters is None:
                return True
            return filters.get(key, True)

        with open(filename, mode = "w") as file:
            # ---- 文本框文本 ----
            if _save("texts"):
                item_output = {}
                for i in main_class.tabs.items():
                    item_output[i[0]] = {}
                    for lineedit in i[1].findChildren(QLineEdit, options=Qt.FindChildrenRecursively):
                        item_output[i[0]][lineedit.objectName()] = lineedit.text()
                output["texts"] = item_output

            # ---- QGraphicsView 公式渲染参数 ----
            if _save("views"):
                item_views = {}
                for tab_name, tab_widget in main_class.tabs.items():
                    views = {}
                    for view in tab_widget.findChildren(QGraphicsView, options=Qt.FindChildrenRecursively):
                        name = view.objectName()
                        if name and view in _svg_cache:
                            n, l, _ = _svg_cache[view]
                            views[name] = [n, l]
                    item_views[tab_name] = views
                output["views"] = item_views

            # ---- QComboBox 选中项索引 ----
            if _save("combos"):
                item_combos = {}
                for tab_name, tab_widget in main_class.tabs.items():
                    combos = {}
                    for combo in tab_widget.findChildren(QComboBox, options=Qt.FindChildrenRecursively):
                        name = combo.objectName()
                        if name and combo.count() > 0:
                            combos[name] = combo.currentIndex()
                    item_combos[tab_name] = combos
                output["combos"] = item_combos

            # ---- 函数列表（fs） ----
            if _save("fs"):
                output["fs"] = main_class.fs

            # ---- 框架与设置选项（tabs_n, 语言, 主题） ----
            if _save("save_settings"):
                output["tabs_n"] = main_class.tabs_n
                output["language"] = current_language()
                output["theme"] = getattr(main_class, "theme", "light")

            # ---- 方程列表（方程组） ----
            if _save("eqs"):
                output["eqs"] = list(main_class.eqs.keys())

            # ---- 不等式列表（不等式组） ----
            if _save("rels"):
                output["rels"] = list(main_class.rels.keys())

            # ---- 向量列表 ----
            if _save("vs"):
                output["vs"] = main_class.vs

            # ---- 所有缓存区内容 ----
            if _save("cache") and hasattr(main_class, 'cache'):
                output["cache"] = [item for item in main_class.cache]

            # ---- 平面几何对象数据 ----
            if _save("pjs") and hasattr(main_class, 'pjs'):
                pjs_save = {}
                for k, v in main_class.pjs.items():
                    cat = v[0]
                    pjs_save[k] = [cat, repr(v[1])]
                output["pjs"] = pjs_save

            # ---- 立体几何对象数据 ----
            if _save("ljs") and hasattr(main_class, 'ljs'):
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
            try:
                # ---- 框架与设置 ----
                main_class.fs = json_data.get("fs", {})
                if "tabs_n" in json_data:
                    if len(json_data["tabs_n"]) == len(ui.tabs_list):
                        main_class.tabs_n = json_data["tabs_n"]
                    else:
                        tabs_n = json_data['tabs_n']
                        tabs_n.extend((len(ui.tabs_list) - len(json_data["tabs_n"])) * [1])
                        main_class.tabs_n = tabs_n

                # ---- 函数列表 ----
                main_class.eqs = {i: sympify(i, main_class.fs) for i in json_data.get("eqs", [])}
                # ---- 方程/不等式列表 ----
                main_class.rels = {i: sympify(i, main_class.fs) for i in json_data.get("rels", [])}
                # ---- 向量列表 ----
                main_class.vs = json_data.get("vs", {})

                # ---- 所有缓存区内容 ----
                if "cache" in json_data:
                    main_class.cache = list(json_data["cache"])

                # ---- 平面几何对象数据 ----
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

                # ---- 立体几何对象数据 ----
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
                for tab_name in json_data.get("texts", {}).keys():
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
                        # 自动渲染数学公式：文本框名称后缀为"_lineedit"则去掉该后缀即为对应的图形视图对象名
                        for lineedit in tab_widget.findChildren(QLineEdit):
                            if lineedit.objectName().endswith('_lineedit') and lineedit.text():
                                view_name = lineedit.objectName()[:-9]
                                view = tab_widget.findChild(QGraphicsView, view_name)
                                if view is not None:
                                    try:
                                        expr = sympify(lineedit.text(), main_class.fs)
                                        setGraphicsView('', latex(expr), view)
                                    except:
                                        pass
                        # 恢复所有 QGraphicsView 的公式内容（包括非 _lineedit 驱动的视图）
                        saved_views = json_data.get("views", {})
                        if tab_name in saved_views:
                            for view in tab_widget.findChildren(QGraphicsView, options=Qt.FindChildrenRecursively):
                                name = view.objectName()
                                if name and name in saved_views[tab_name]:
                                    n, l = saved_views[tab_name][name]
                                    if l:
                                        try:
                                            setGraphicsView(n, l, view)
                                        except:
                                            pass
                        # 恢复所有 QComboBox 的选中项
                        saved_combos = json_data.get("combos", {})
                        if tab_name in saved_combos:
                            for combo in tab_widget.findChildren(QComboBox, options=Qt.FindChildrenRecursively):
                                name = combo.objectName()
                                if name and name in saved_combos[tab_name]:
                                    idx = saved_combos[tab_name][name]
                                    if 0 <= idx < combo.count():
                                        combo.setCurrentIndex(idx)
                # 仅当存档中显式包含语言/主题设置时才恢复，
                # 避免用户未勾选"所有设置选项"时当前设置被默认值覆盖
                if "language" in json_data:
                    lang = json_data["language"]
                    if hasattr(main_class, "change_language"):
                        main_class.change_language(lang)
                if "theme" in json_data:
                    theme = json_data["theme"]
                    if hasattr(main_class, "dark") and hasattr(main_class, "light"):
                        if theme == "dark":
                            main_class.dark()
                        else:
                            main_class.light()
            except:
                QMessageBox.warning(main_class, "警告", "提供的配置文件错误")
