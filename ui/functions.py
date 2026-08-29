from PySide6.QtWidgets import QWidget, QMessageBox, QHeaderView, QTableWidgetItem, QTreeWidgetItem
from PySide6.QtCore import QCoreApplication
tr = QCoreApplication.translate
from ui.ui_functions import Ui_functions
from core.render import setGraphicsView
from core.sympify import sympify
from sympy import latex, Eq, Rel


class Functions(QWidget, Ui_functions):
    def __init__(self, parent, fs):
        super(Functions, self).__init__(parent)
        self.setupUi(self)

        # 1. 指定槽函数
        self.def_type.currentIndexChanged.connect(self.update_def_input)
        self.def_save.clicked.connect(self.click_def_save)
        self.def_clear.clicked.connect(self.clear_def_input)
        self.def_input.itemClicked.connect(self.update_def_preview)
        self.def_edit.clicked.connect(self.click_def_edit)
        self.def_del.clicked.connect(self.click_def_del)
        self.def_preview_mode.currentIndexChanged.connect(lambda: self.update_def_preview(self.def_input.currentItem()))
        self.calc_function.currentIndexChanged.connect(self.update_calc_input)
        self.calc_clear.clicked.connect(self.clear_calc_input)
        self.calc_calc.clicked.connect(self.click_calc_calc)

        # 2. 初始化对象字典
        self.fs = parent.fs
        self.vs = parent.vs
        self.ss = parent.ss
        self.objs_dicts = [self.fs, self.ss, self.vs]

        # 3. 初始化定义输入表格相关内容
        self.def_input.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        def_func_attr = [
            (tr("functions", "名称"), "f"), 
            (tr("functions", "表达式"), ""), 
            (tr("functions", "定义域"), tr("functions", "Reals")),
            (tr("functions", "自变量"), tr("functions", "x"))
            ]
        def_set_attr = [
            (tr("functions", "名称"), "set"), 
            (tr("functions", "表达式"), "")
            ]
        def_vec_attr = [
            (tr("functions", "名称"), "vec"), 
            (tr("functions", "x"), ""), 
            (tr("functions", "y"), "")
            ]
        def_pg_attr = [
            (tr("functions", "名称"), "pg"), 
            (tr("functions", "暂无"), "")
            ]
        def_sg_attr = [
            (tr("functions", "名称"), "sg"), 
            (tr("functions", "暂无"), "")
            ]
        self.def_attrs = [def_func_attr, def_set_attr, def_vec_attr, def_pg_attr, def_sg_attr]
        # 当前版本不启用: self.def_obj_name_index = [0] * len(self.def_attrs)
        self.def_input_temp = {self.def_attrs.index(attrs): [attr[1] for attr in attrs] for attrs in self.def_attrs}
        self.def_input_type = 0
        self.update_def_input(0)
        for i in range(self.def_input.rowCount()):
            self.def_input.setItem(i, 0, QTableWidgetItem("") 
                if self.def_attrs[self.def_input_type][i][1] in self.objs_dicts[self.def_input_type].keys() and i==0 
                else QTableWidgetItem(self.def_attrs[self.def_input_type][i][1]))

        # 初始化计算输入表格相关内容
        self.calc_input.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        calc_calc_attr = [
            (tr("functions", "表达式"), "")
        ]
        calc_diff_attr = [
            (tr("functions", "表达式"), ""),
            (tr("functions", "求导变量"), "x"),
            (tr("functions", "求导次数"), "1")
        ]
        calc_integral_attr = [
            (tr("functions", "表达式"), ""),
            (tr("functions", "积分变量"), "x")
        ]
        calc_equation_attr = [
            (tr("functions", "左式"), ""),
            (tr("functions", "右式"), "0"),
            (tr("functions", "求解变量"), "x"),
            (tr("functions", "求解定义域"), "Reals")
        ]
        calc_inequality_attr = [
            (tr("functions", "左式"), ""),
            (tr("functions", "不等号"), "!="),
            (tr("functions", "右式"), "0"),
            (tr("functions", "求解变量"), "x"),
            (tr("functions", "求解定义域"), "Reals")
        ]
        self.calc_attrs = [calc_calc_attr, calc_diff_attr, calc_integral_attr, calc_equation_attr, calc_inequality_attr]
        self.calc_input_temp = {self.calc_attrs.index(attrs): [attr[1] for attr in attrs] for attrs in self.calc_attrs}
        self.calc_input_type = 0
        self.update_calc_input(0)
        for i in range(self.calc_input.rowCount()):
                self.calc_input.setItem(i, 0, QTableWidgetItem(self.calc_attrs[self.calc_input_type][i][1]))

    def update_def_objs(self):
        """更新树状列表数据（三层结构：类型 → 对象 → 属性）"""

        def update_single_item(parent_item, attrs, attr_names):
            target_count = len(attrs)
            current_count = parent_item.childCount()

            while current_count > target_count:
                parent_item.removeChild(parent_item.child(current_count - 1))
                current_count -= 1
            while current_count < target_count:
                QTreeWidgetItem(parent_item)
                current_count += 1

            for i, (name, val) in enumerate(zip(attr_names, attrs)):
                child = parent_item.child(i)
                child.setText(0, name)
                child.setText(1, str(val))

        def update_single_type(top_item, datas, attr_names):
            existing = {}
            for i in range(top_item.childCount()):
                child = top_item.child(i)
                existing[child.text(0)] = child

            for obj_name, attrs in datas.items():
                if obj_name in existing:
                    update_single_item(existing[obj_name], attrs, attr_names)
                else:
                    new_item = QTreeWidgetItem([obj_name, ""])
                    top_item.addChild(new_item)
                    update_single_item(new_item, attrs, attr_names)

            current_names = set(datas.keys())
            for i in range(top_item.childCount() - 1, -1, -1):
                child = top_item.child(i)
                if child.text(0) not in current_names:
                    top_item.removeChild(child)

        for idx in range(self.def_objs.topLevelItemCount()):
            top_item = self.def_objs.topLevelItem(idx)
            datas = self.objs_dicts[idx]
            attr_names = [tup[0] for tup in self.def_attrs[idx]]
            update_single_type(top_item, datas, attr_names)

    def click_def_save(self):
        """保存对象"""

        # 1. 提取输入的数据
        inputs = [self.def_input.item(i, 0).text() for i in range(self.def_input.rowCount())]

        # 2. 检查数据是否完整
        if all(inputs):
            # 3. 保存至相应字典
            idx = self.def_type.currentIndex()
            self.objs_dicts[idx][inputs[0]] = inputs

            # 4. 更新树状列表
            self.update_def_objs()

            # 5. 清空数据
            self.clear_def_input()

        # 6. 参数遗漏报错
        else:
            QMessageBox.critical(self, "Error", tr("functions", "有参数未输入"), QMessageBox.StandardButton.Ok)

    def click_def_edit(self):
        """编辑对象"""

        # 1. 获取当前对象并检测是否为None
        current = self.def_objs.currentItem()
        if current is None:
            QMessageBox.warning(self, "Warning", tr("functions", "请先选择要编辑的对象"))
            return
        
        # 2. 判断选中项的层级，获取对象名称
        parent = current.parent()
        if parent is None:
            QMessageBox.warning(self, "Warning", tr("functions", "不能编辑类型节点，请选择具体的对象"))
            return
        
        grandparent = parent.parent()
        if grandparent is None:
            obj = current
        else:
            obj = parent

        # 3. 将表格选中信息写入表格缓存
        item_type = self.def_type.findText(obj.parent().text(0))
        for i in range(obj.childCount()):
            self.def_input_temp[item_type][i] = obj.child(i).text(1)

        # 4. 更新表格
        self.update_def_input(item_type, is_temp=False)

    def click_def_del(self):
        """删除对象"""

        # 1. 获取当前对象并检测是否为None
        current = self.def_objs.currentItem()
        if current is None:
            QMessageBox.warning(self, "Warning", tr("functions", "请先选择要删除的对象"))
            return

        # 2. 判断选中项的层级，获取对象名称
        parent = current.parent()
        if parent is None:
            QMessageBox.warning(self, "Warning", tr("functions", "不能删除类型节点，请选择具体的对象"))
            return

        grandparent = parent.parent()
        if grandparent is None:
            obj_name = current.text(0)
        else:
            obj_name = parent.text(0)

        # 3. 尝试从所有对象字典中删除
        deleted = False
        for objs_dict in self.objs_dicts:
            if obj_name in objs_dict:
                del objs_dict[obj_name]
                deleted = True
                break

        # 4. 反馈结果
        if deleted:
            QMessageBox.information(self, "Success", tr("functions", "删除成功"))
            self.update_def_objs()
        else:
            QMessageBox.warning(self, "Failed", tr("functions", "删除失败，请检查您选中的是否为对象"))

    def update_def_input(self, idx, is_temp = True):
        """更新输入表格信息"""

        # 1. 缓存内容
        if is_temp:
            for i in range(self.def_input.rowCount()):
                item = self.def_input.item(i, 0)
                self.def_input_temp[self.def_input_type][i] = item.text() if item else ""

        # 2. 清空内容并重写当前类型缓存
        self.def_input.clearContents()
        self.def_input_type = idx

        # 3. 重设表格行数与各行标题
        self.def_input.setRowCount(len(self.def_attrs[idx]))
        self.def_input.setVerticalHeaderLabels([i[0] for i in self.def_attrs[idx]])

        # 4. 读取缓存并覆盖已有项
        for i in range(self.def_input.rowCount()):
            try:
                item = QTableWidgetItem(self.def_input_temp[idx][i])
                self.def_input.setItem(i, 0, item)
            except Exception as e:
                print(e)

    def clear_def_input(self):
        """清空输入表格"""

        # 1. 清空表格内容和缓存列表对应内容
        self.def_input.clearContents()
        self.def_input_temp[self.def_input_type] = [attr[1] for attr in self.def_attrs[self.def_input_type]]

        # 2. 设置为默认文本
        for i in range(self.def_input.rowCount()):
            self.def_input.setItem(i, 0, QTableWidgetItem("") 
                                   if self.def_attrs[self.def_input_type][i][1] in self.objs_dicts[self.def_input_type].keys() and i==0 
                                   else QTableWidgetItem(self.def_attrs[self.def_input_type][i][1]))

    def update_def_preview(self, item):
        """预览表达式"""

        if hasattr(item, "text"):
            if item.text() != "":
                try:
                    expr = sympify(item.text(), self.fs if self.def_preview_mode.currentIndex() == 1 else {})
                except Exception as e:
                    setGraphicsView("", tr("functions", "不是合法的表达式"), self.def_preview)
                    self.def_output.setText("")
                else:
                    setGraphicsView("", latex(expr), self.def_preview)
                    self.def_output.setText(str(expr))

    def update_calc_input(self, idx, is_temp = True):
            """更新输入表格信息"""
    
            # 1. 缓存内容
            if is_temp:
                for i in range(self.calc_input.rowCount()):
                    item = self.calc_input.item(i, 0)
                    self.calc_input_temp[self.calc_input_type][i] = item.text() if item else ""
    
            # 2. 清空内容并重写当前类型缓存
            self.calc_input.clearContents()
            self.calc_input_type = idx
    
            # 3. 重设表格行数与各行标题
            self.calc_input.setRowCount(len(self.calc_attrs[idx]))
            self.calc_input.setVerticalHeaderLabels([i[0] for i in self.calc_attrs[idx]])
    
            # 4. 读取缓存并覆盖已有项
            for i in range(self.calc_input.rowCount()):
                try:
                    item = QTableWidgetItem(self.calc_input_temp[idx][i])
                    self.calc_input.setItem(i, 0, item)
                except Exception as e:
                    print(e)
    
    def clear_calc_input(self):
        """清空输入表格"""

        # 1. 清空表格内容和缓存列表对应内容
        self.calc_input.clearContents()
        self.calc_input_temp[self.calc_input_type] = [attr[1] for attr in self.calc_attrs[self.calc_input_type]]

        # 2. 设置为默认文本
        for i in range(self.calc_input.rowCount()):
            self.calc_input.setItem(i, 0, QTableWidgetItem(self.calc_attrs[self.calc_input_type][i][1]))
    
    def click_calc_calc(self):
        """保存对象"""

        # 1. 提取输入的数据
        inputs = [self.calc_input.item(i, 0).text() for i in range(self.calc_input.rowCount())]

        # 2. 检查数据是否完整
        if all(inputs):
            try:
                # 3. 根据计算类型执行运算
                if self.calc_input_type == 0:
                    # 设置计算结果长度上限
                    import sys; sys.set_int_max_str_digits(0)
                    # 调用sympy引擎计算
                    result = sympify(inputs[0], self.fs, is_simplify = True)
                elif self.calc_input_type == 1:
                    from functions.derivative import derivative
                    result = derivative(inputs[0], inputs[1], inputs[2], "", self.fs)
                elif self.calc_input_type == 2:
                    from functions.integral import integral
                    result = integral(inputs[0], inputs[1], self.fs)
                elif self.calc_input_type == 3:
                    from functions.solvers import solve_fangcheng
                    result = solve_fangcheng(Eq(sympify(inputs[0], self.fs), sympify(inputs[1], self.fs)), inputs[2], inputs[3], self.fs)
                elif self.calc_input_type == 4:
                    from functions.solvers import solve_budengshi
                    result = solve_budengshi(Rel(sympify(inputs[0], self.fs), sympify(inputs[2], self.fs), inputs[1]), inputs[3], inputs[4], self.fs)

                # 3. 渲染结果至预览框
                setGraphicsView("", latex(result), self.calc_preview)
                self.calc_output.setText(str(result))

            # 4. 错误处理
            except Exception as e:
                setGraphicsView("", "\\text{" + str(e) + "}", self.calc_preview)
                self.calc_output.setText(str(e))

        # 5. 参数遗漏报错
        else:
            QMessageBox.critical(self, "Error", tr("functions", "有参数未输入"), QMessageBox.StandardButton.Ok)
