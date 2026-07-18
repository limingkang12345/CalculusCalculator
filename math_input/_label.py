from __future__ import annotations
from typing import Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QPushButton, QSizePolicy, QApplication,
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QPainter, QPen, QColor, QCursor

from ._view import MathView
from ._editor import MathEditor
from ._model import FormulaModel
from ._renderer import SeqNode
from ._parser import parse_latex, parse_sympy

_S_PANEL = (
    "QFrame#math_edit_panel{"
    "background:#ffffff;"
    "border:1px solid #b8ccee;"
    "border-radius:6px;"
    "}"
)
_S_CLOSE = (
    "QPushButton{"
    "background:transparent;color:#999;border:none;"
    "font-size:13px;padding:2px 7px;border-radius:3px;"
    "min-width:22px;min-height:22px;"
    "}"
    "QPushButton:hover{background:#f0f0f0;color:#444;}"
)


class _HoverOverlay(QWidget):
    """Transparent click-capture overlay drawn over the formula display."""
    clicked = Signal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.IBeamCursor))
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self._hovered = False

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def paintEvent(self, e):
        if self._hovered:
            p = QPainter(self)
            p.setPen(QPen(QColor(80, 140, 220, 100), 1, Qt.DashLine))
            p.drawRect(self.rect().adjusted(0, 0, -1, -1))


class MathLabel(QWidget):
    """
    Displays a mathematical formula. Clicking it reveals an inline editor.
    Both display and editor share one FormulaModel — no duplication.

    Initialise with a LaTeX or SymPy string::

        label = MathLabel(latex=r"\\frac{1}{\\sqrt{x}}")
        label = MathLabel(sympy="1 / sqrt(x)")

    Signals
    -------
    formula_changed(str)   sympy string on every edit
    editing_started()      editor panel became visible
    editing_finished()     editor panel was closed
    """
    formula_changed = Signal(str)
    editing_started  = Signal()
    editing_finished = Signal()

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        zoom: float = 1.0,
        toolbar_groups: Optional[list] = None,
        latex: Optional[str] = None,
        sympy: Optional[str] = None,
    ):
        super().__init__(parent)
        self._zoom = zoom
        self._toolbar_groups = toolbar_groups
        self._editing = False
        self._shared_model = FormulaModel()
        self._build_ui()
        if latex is not None:
            self.set_latex(latex)
        elif sympy is not None:
            self.set_sympy(sympy)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._view_wrap = QWidget()
        self._view_wrap.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vw_lay = QVBoxLayout(self._view_wrap)
        vw_lay.setContentsMargins(0, 0, 0, 0)
        vw_lay.setSpacing(0)

        self._view = MathView.from_model(self._shared_model)
        self._view.set_zoom(self._zoom)
        self._view.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vw_lay.addWidget(self._view)

        self._overlay = _HoverOverlay(self._view_wrap)
        self._overlay.clicked.connect(self._open_editor)
        self._view_wrap.installEventFilter(self)
        root.addWidget(self._view_wrap)

        self._panel = self._make_panel()
        self._panel.setVisible(False)
        root.addWidget(self._panel)

    def _make_panel(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("math_edit_panel")
        frame.setStyleSheet(_S_PANEL)
        frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        lay = QVBoxLayout(frame)
        lay.setContentsMargins(6, 4, 6, 6)
        lay.setSpacing(4)

        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.addStretch()
        close = QPushButton("\u2715")
        close.setStyleSheet(_S_CLOSE)
        close.setFixedSize(24, 24)
        close.setFocusPolicy(Qt.NoFocus)
        close.clicked.connect(self._close_editor)
        hdr.addWidget(close)
        lay.addLayout(hdr)

        self._editor = MathEditor(
            show_toolbar=True,
            toolbar_groups=self._toolbar_groups,
            zoom=self._zoom,
        )
        self._editor.set_model(self._shared_model)
        self._editor.formula_changed.connect(self._on_editor_changed)
        lay.addWidget(self._editor)
        return frame

    def eventFilter(self, obj, event):
        if obj is self._view_wrap and event.type() == QEvent.Resize:
            self._refit_overlay()
        return super().eventFilter(obj, event)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._refit_overlay()

    def showEvent(self, e):
        super().showEvent(e)
        self._refit_overlay()

    def _refit_overlay(self):
        self._overlay.setGeometry(self._view.geometry())

    def _open_editor(self):
        if self._editing:
            return
        self._editing = True
        self._overlay.setVisible(False)
        self._panel.setVisible(True)
        self.updateGeometry()
        QApplication.processEvents()
        self._editor._canvas.setFocus()
        self.editing_started.emit()

    def _close_editor(self):
        if not self._editing:
            return
        self._editing = False
        self._panel.setVisible(False)
        self._overlay.setVisible(True)
        self._view.update()
        self._view.updateGeometry()
        self._refit_overlay()
        self.updateGeometry()
        self.editing_finished.emit()

    def _on_editor_changed(self, sympy_str: str):
        self._view.update()
        self.formula_changed.emit(sympy_str)

    def _set_root(self, node):
        self._shared_model._root = SeqNode([node])
        self._shared_model._cursor_id = self._shared_model._ids()[-1]
        self._shared_model._selected.clear()
        self._view.update()
        self._view.updateGeometry()

    def set_latex(self, latex: str):
        """Parse a LaTeX string and display it as the current formula."""
        self._set_root(parse_latex(latex))

    def set_sympy(self, sympy: str):
        """Parse a SymPy expression string and display it as the current formula."""
        self._set_root(parse_sympy(sympy))

    def set_zoom(self, zoom: float):
        """Set zoom for both display and editor."""
        self._zoom = zoom
        self._view.set_zoom(zoom)
        self._editor.set_zoom(zoom)

    def model(self) -> FormulaModel:
        """Return the shared FormulaModel."""
        return self._shared_model

    def to_sympy(self) -> str:
        return self._shared_model.to_sympy()

    def to_latex(self) -> str:
        return self._shared_model.to_latex()

    def to_text(self) -> str:
        return self._shared_model.to_text()

    def is_editing(self) -> bool:
        return self._editing