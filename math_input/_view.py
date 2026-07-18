from __future__ import annotations
from typing import Optional
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt, QSize, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from ._renderer import (
    FormulaNode, SeqNode, RenderMetrics, HitRegion,
    COLOR_FG, FONT_SIZE_NORMAL,
    FracNode, SqrtNode, PowerNode, SubNode, ParenNode,
    TextNode, PlaceholderNode,
)
from ._model import FormulaModel

_PAD_X = 12
_PAD_Y = 10
_BG_DEFAULT = QColor(255, 255, 255, 0)
_BORDER_DEFAULT = QColor(0, 0, 0, 0)


class MathView(QWidget):
    """
    Read-only widget for rendering a mathematical formula tree.

    Usage
    -----
    Direct node assignment::

        view = MathView()
        view.set_node(FracNode(TextNode("1"), TextNode("2")))

    From a FormulaModel::

        model = FormulaModel()
        model.insert_frac()
        view = MathView.from_model(model)

    Latex-like text (basic)::

        view = MathView()
        view.set_text("sin(x)")

    Appearance customisation::

        view.set_zoom(1.5)
        view.set_background(QColor(240, 240, 255))
        view.set_foreground(QColor(20, 20, 80))
        view.set_padding(16, 12)
        view.set_transparent(True)

    Rendering to pixmap::

        px = view.to_pixmap()
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._model = FormulaModel()
        self._zoom = 1.0
        self._bg = _BG_DEFAULT
        self._transparent = True
        self._pad_x = _PAD_X
        self._pad_y = _PAD_Y
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    @classmethod
    def from_model(cls, model: FormulaModel,
                   parent: Optional[QWidget] = None) -> "MathView":
        v = cls(parent)
        v._model = model
        return v
    def set_node(self, node: FormulaNode):
        """Replace the displayed formula with a single node."""
        from ._renderer import SeqNode
        self._model._root = SeqNode([node])
        self.update()
        self.updateGeometry()
    def set_model(self, model: FormulaModel):
        """Attach an existing FormulaModel."""
        self._model = model
        self.update()
        self.updateGeometry()
    def model(self) -> FormulaModel:
        """Return the underlying FormulaModel."""
        return self._model
    def set_text(self, text: str):
        """Set formula from a plain text string (character by character)."""
        self._model.set_from_text(text)
        self.update()
        self.updateGeometry()
    def set_zoom(self, zoom: float):
        """Scale the rendered formula. Default 1.0."""
        self._zoom = max(0.2, min(8.0, zoom))
        self.update()
        self.updateGeometry()
    def zoom(self) -> float:
        return self._zoom
    def set_background(self, color: QColor):
        """Set background fill colour."""
        self._bg = color
        self._transparent = color.alpha() == 0
        self.setAttribute(Qt.WA_TranslucentBackground, self._transparent)
        self.update()
    def set_transparent(self, value: bool):
        """Make background fully transparent."""
        self._transparent = value
        if value:
            self._bg = QColor(255, 255, 255, 0)
        self.setAttribute(Qt.WA_TranslucentBackground, value)
        self.update()
    def set_padding(self, px: int, py: int):
        """Set horizontal and vertical padding in logical pixels."""
        self._pad_x = px
        self._pad_y = py
        self.update()
        self.updateGeometry()
    def set_foreground(self, color: QColor):
        """Override the default foreground colour for all nodes (global tint)."""
        from . import _renderer as r
        r.COLOR_FG = color
        self.update()
    def to_pixmap(self, scale: float = 1.0) -> QPixmap:
        """Render the formula to a QPixmap at the given extra scale factor."""
        sz = self.sizeHint()
        px = QPixmap(int(sz.width() * scale), int(sz.height() * scale))
        px.fill(self._bg if not self._transparent else QColor(0, 0, 0, 0))
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.scale(scale, scale)
        self._paint(p)
        p.end()
        return px
    def to_latex(self) -> str:
        """Return LaTeX string for the current formula."""
        return self._model.to_latex()
    def to_sympy(self) -> str:
        """Return SymPy-compatible expression string."""
        return self._model.to_sympy()
    def to_text(self) -> str:
        """Return plain-text representation."""
        return self._model.to_text()
    def _metrics(self, painter: QPainter) -> RenderMetrics:
        return self._model.root.measure(painter)
    def sizeHint(self) -> QSize:
        px = QPixmap(1, 1)
        p = QPainter(px)
        p.scale(self._zoom, self._zoom)
        m = self._metrics(p)
        p.end()
        w = int((m.width + self._pad_x * 2) * self._zoom) + 4
        h = int((m.height + self._pad_y * 2) * self._zoom) + 4
        return QSize(max(40, w), max(30, h))
    def minimumSizeHint(self) -> QSize:
        return QSize(40, 30)
    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        if not self._transparent:
            p.fillRect(self.rect(), self._bg)
        self._paint(p)
    def _paint(self, p: QPainter):
        p.save()
        p.scale(self._zoom, self._zoom)
        m = self._model.root.measure(p)
        cx = self._pad_x / self._zoom
        cy = self._pad_y / self._zoom + m.ascent
        hits: list = []
        self._model.root.draw(p, cx, cy, hits, set(), None, False)
        p.restore()