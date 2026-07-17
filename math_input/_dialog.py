from __future__ import annotations
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QSizePolicy, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from ._editor import MathEditor, _S_BTN
from ._model import FormulaModel

_S_ACCEPT = (
    "QPushButton{background:#3498db;color:white;border:none;border-radius:5px;"
    "font-size:12px;padding:6px 20px;}"
    "QPushButton:hover{background:#2980b9;}"
    "QPushButton:pressed{background:#2471a3;}"
)
_S_CANCEL = (
    "QPushButton{background:#f0f0f0;color:#333;border:1px solid #ddd;"
    "border-radius:5px;font-size:12px;padding:6px 18px;}"
    "QPushButton:hover{background:#e0e0e0;}"
)
_S_OUTPUT = (
    "QTextEdit{border:1px solid #ddd;border-radius:4px;background:#f8f8f8;"
    "font-family:monospace;font-size:10px;color:#555;padding:3px;}"
)
_S_GRP = (
    "QGroupBox{font-size:10px;font-weight:bold;color:#777;"
    "border:1px solid #e8e8e8;border-radius:5px;margin-top:6px;"
    "padding:4px 4px 4px 4px;}"
    "QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px;}"
)


class MathDialog(QDialog):
    """
    A ready-to-use modal dialog wrapping MathEditor.

    Usage
    -----
    ::

        dlg = MathDialog(parent=self)
        if dlg.exec() == QDialog.Accepted:
            print(dlg.result_sympy())
            print(dlg.result_latex())

    With initial expression::

        dlg = MathDialog(initial_text="sin(x)", parent=self)

    With custom title and toolbar groups::

        dlg = MathDialog(
            title="Enter formula",
            toolbar_groups=["struct", "greek", "edit"],
        )

    Without the output preview panel::

        dlg = MathDialog(show_output=False)
    """
    accepted_formula = Signal(str)
    def __init__(self, parent: Optional[object] = None,
                 title: str = "公式编辑器",
                 initial_text: str = "",
                 toolbar_groups: Optional[list] = None,
                 show_output: bool = True,
                 zoom: float = 1.0):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(1200)
        self.setModal(True)
        self.setStyleSheet("QDialog{background:#fafafa;}")
        self._show_output = show_output
        self._result_sympy = ""
        self._result_latex = ""
        self._build_ui(toolbar_groups, zoom)
        if initial_text:
            self._editor.model().set_from_text(initial_text)
            self._editor._canvas.update()
    def _build_ui(self, toolbar_groups, zoom):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 10)
        root.setSpacing(8)
        self._editor = MathEditor(
            show_toolbar=True,
            toolbar_groups=toolbar_groups,
            zoom=zoom,
        )
        self._editor.formula_changed.connect(self._on_changed)
        self._editor.latex_changed.connect(self._on_latex_changed)
        root.addWidget(self._editor)
        if self._show_output:
            grp = QGroupBox("输出")
            grp.setStyleSheet(_S_GRP)
            gl = QVBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            self._output = QTextEdit()
            self._output.setReadOnly(True)
            self._output.setStyleSheet(_S_OUTPUT)
            self._output.setMaximumHeight(55)
            gl.addWidget(self._output)
            root.addWidget(grp)
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        cancel = QPushButton("取消")
        cancel.setStyleSheet(_S_CANCEL)
        cancel.setFocusPolicy(Qt.NoFocus)
        cancel.clicked.connect(self.reject)
        accept = QPushButton("插入")
        accept.setStyleSheet(_S_ACCEPT)
        accept.setFocusPolicy(Qt.NoFocus)
        accept.clicked.connect(self._accept)
        btn_row.addStretch()
        btn_row.addWidget(cancel)
        btn_row.addWidget(accept)
        root.addLayout(btn_row)
    def _on_changed(self, sympy_str: str):
        self._result_sympy = sympy_str
        if self._show_output:
            self._output.setPlainText(f"sympy: {sympy_str}")
    def _on_latex_changed(self, latex_str: str):
        self._result_latex = latex_str
        if self._show_output:
            current = self._output.toPlainText().split("\n")[0]
            self._output.setPlainText(f"{current}\nlatex: {latex_str}")
    def _accept(self):
        self._result_sympy = self._editor.to_sympy()
        self._result_latex = self._editor.to_latex()
        self.accepted_formula.emit(self._result_sympy)
        self.accept()
    def result_sympy(self) -> str:
        """Return the SymPy-compatible expression from the accepted formula."""
        return self._result_sympy
    def result_latex(self) -> str:
        """Return the LaTeX string from the accepted formula."""
        return self._result_latex
    def result_text(self) -> str:
        """Return the plain-text representation from the accepted formula."""
        return self._editor.to_text()
    def editor(self) -> MathEditor:
        """Access the embedded MathEditor for direct manipulation."""
        return self._editor