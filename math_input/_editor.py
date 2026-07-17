from __future__ import annotations
from typing import Optional, List, Tuple
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QSizePolicy, QScrollArea, QFrame, QApplication
)
from PySide6.QtCore import Qt, Signal, QTimer, QRectF, QPointF, QSize
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont, QKeyEvent,
    QMouseEvent, QWheelEvent, QPixmap
)
from ._renderer import (
    HitRegion, COLOR_FG, FONT_SIZE_NORMAL,
    COLOR_CURSOR, CURSOR_WIDTH,
)
from ._model import FormulaModel, GREEK_MAP, OPERATOR_MAP

_PAD_X = 18
_PAD_Y = 14
_CANVAS_MIN_H = 72
_BG_NORMAL = QColor(255, 255, 255)
_BG_READONLY = QColor(248, 248, 248)
_BORDER_NORMAL = QColor(200, 210, 230)
_BORDER_FOCUS = QColor(52, 152, 219)
_CURSOR_BLINK_MS = 530
_TOOLBAR_MAX_H = 260

_S_BTN = (
    "QPushButton{border:1px solid #ddd;border-radius:4px;background:#fafafa;"
    "font-size:12px;padding:3px 6px;color:#222;min-width:26px;}"
    "QPushButton:hover{background:#e8f4fd;border-color:#3498db;color:#1a6fa3;}"
    "QPushButton:pressed{background:#d0eaf9;}"
)
_S_BTN_OP = (
    "QPushButton{border:1px solid #e0e0e0;border-radius:4px;background:#f5f0ff;"
    "font-size:12px;padding:3px 6px;color:#5b2d8e;min-width:26px;}"
    "QPushButton:hover{background:#e8deff;border-color:#8e44ad;}"
    "QPushButton:pressed{background:#d5c5ff;}"
)
_S_BTN_FN = (
    "QPushButton{border:1px solid #e0e0e0;border-radius:4px;background:#f0fff4;"
    "font-size:11px;padding:3px 5px;color:#1a6b3a;min-width:26px;}"
    "QPushButton:hover{background:#d4f5e0;border-color:#27ae60;}"
    "QPushButton:pressed{background:#bde8cc;}"
)
_S_GRP = (
    "QGroupBox{font-size:10px;font-weight:bold;color:#777;"
    "border:1px solid #e8e8e8;border-radius:5px;margin-top:6px;"
    "padding:4px 4px 4px 4px;}"
    "QGroupBox::title{subcontrol-origin:margin;left:6px;padding:0 3px;}"
)

STRUCT_BUTTONS: List[Tuple[str, str, str, str]] = [
    ("a/b",      "frac",       _S_BTN,    "Fraction"),
    ("\u221Ax",  "sqrt",       _S_BTN,    "Square root"),
    ("\u221A[n]x","nth_root",  _S_BTN,    "Nth root"),
    ("x^n",      "power",      _S_BTN,    "Superscript / Power"),
    ("x_n",      "sub",        _S_BTN,    "Subscript"),
    ("x^n_m",    "power_sub",  _S_BTN,    "Power + subscript"),
    ("(x)",      "parens",     _S_BTN,    "Round brackets"),
    ("[x]",      "brackets",   _S_BTN,    "Square brackets"),
    ("{x}",      "braces",     _S_BTN,    "Curly braces"),
    ("|x|",      "abs",        _S_BTN,    "Absolute value"),
    ("\u222B",   "int",        _S_BTN_OP, "Definite integral"),
    ("\u222B*",  "int_indef",  _S_BTN_OP, "Indefinite integral"),
    ("\u03A3",   "sum",        _S_BTN_OP, "Sum with limits"),
    ("\u03A0",   "prod",       _S_BTN_OP, "Product with limits"),
    ("lim",      "limit",      _S_BTN_OP, "Limit"),
    ("\u00AF",   "overline",   _S_BTN,    "Overline"),
    ("_",        "underline",  _S_BTN,    "Underline"),
    ("2x2",      "matrix22",   _S_BTN,    "2x2 matrix"),
    ("3x3",      "matrix33",   _S_BTN,    "3x3 matrix"),
    ("2x1",      "matrix21",   _S_BTN,    "2x1 column vector"),
]

OPERATOR_BUTTONS: List[Tuple[str, str]] = [
    ("+","+"), ("\u2212","-"), ("\u00B7","*"), ("\u00D7","times"),
    ("\u00F7","div"), ("=","="), ("\u2260","!="),
    ("\u2264","<="), ("\u2265",">="), ("<","<"), (">",">"),
    ("\u00B1","pm"), ("\u2213","mp"),
    ("\u2248","approx"), ("\u2261","equiv"), ("\u223C","sim"),
    ("\u2202","partial"), ("\u2207","nabla"),
    ("\u2208","in"), ("\u2282","subset"), ("\u222A","cup"), ("\u2229","cap"),
    ("\u2200","forall"), ("\u2203","exists"),
    ("\u2192","->"), ("\u21D2","=>"), ("\u2295","oplus"), ("\u2297","otimes"),
]

GREEK_BUTTONS: List[Tuple[str, str]] = [
    ("\u03B1","alpha"), ("\u03B2","beta"), ("\u03B3","gamma"),
    ("\u03B4","delta"), ("\u03B5","epsilon"), ("\u03B8","theta"),
    ("\u03BB","lambda"), ("\u03BC","mu"), ("\u03BD","nu"),
    ("\u03C0","pi"), ("\u03C1","rho"), ("\u03C3","sigma"),
    ("\u03C4","tau"), ("\u03C6","phi"), ("\u03C8","psi"),
    ("\u03C9","omega"), ("\u03A3","Sigma"), ("\u03A0","Pi"),
    ("\u0393","Gamma"), ("\u0394","Delta"), ("\u0398","Theta"),
    ("\u039B","Lambda"), ("\u03A6","Phi"), ("\u03A9","Omega"),
    ("\u221E","inf"), ("\u2202","partial"), ("\u210F","hbar"),
]

FUNCTION_BUTTONS: List[str] = [
    "\\sin", "\\cos", "\\tan", "\\cot", "\\sec", "\\csc",
    "\\arcsin", "\\arccos", "\\arctan",
    "\\sinh", "\\cosh", "\\tanh",
    "\\log", "\\ln", "\\exp",
    "\\max", "\\min", "\\gcd", "\\lcm",
    "\\det", "\\tr",
]


def _btn(label: str, style: str, tip: str = "") -> QPushButton:
    b = QPushButton(label)
    b.setStyleSheet(style)
    b.setFocusPolicy(Qt.NoFocus)
    b.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    if tip:
        b.setToolTip(tip)
    return b


def _grp(title: str) -> QGroupBox:
    g = QGroupBox(title)
    g.setStyleSheet(_S_GRP)
    return g


class _Canvas(QWidget):
    """Formula editing canvas with Word-style keyboard and mouse handling."""
    changed = Signal()

    def __init__(self, model: FormulaModel, parent=None):
        super().__init__(parent)
        self._model = model
        self._hits: List[HitRegion] = []
        self._focused = False
        self._cursor_vis = True
        self._zoom = 1.0
        self._readonly = False
        self._mouse_pressed = False
        self._drag_anchor_id: Optional[int] = None
        self._blink = QTimer(self)
        self._blink.setInterval(_CURSOR_BLINK_MS)
        self._blink.timeout.connect(self._blink_tick)
        self.setMinimumHeight(_CANVAS_MIN_H)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.IBeamCursor)
        self.setMouseTracking(True)

    def _blink_tick(self):
        self._cursor_vis = not self._cursor_vis
        self.update()

    def focusInEvent(self, e):
        if self._readonly:
            return
        self._focused = True
        self._cursor_vis = True
        self._model._validate_cursor()
        self._blink.start()
        self.update()

    def focusOutEvent(self, e):
        self._focused = False
        self._blink.stop()
        self._cursor_vis = False
        self.update()

    def set_zoom(self, z: float):
        self._zoom = max(0.2, min(8.0, z))
        self.update()

    def set_readonly(self, v: bool):
        self._readonly = v
        if v:
            self._focused = False
            self._blink.stop()
        self.update()

    def _hit_at(self, lx: float, ly: float) -> Optional[HitRegion]:
        best, best_d = None, float("inf")
        for hr in self._hits:
            if hr.rect.contains(QPointF(lx, ly)):
                mid = (hr.cursor_x_before + hr.cursor_x_after) / 2
                d = abs(lx - mid)
                if d < best_d:
                    best_d, best = d, hr
        if best is None:
            min_dist = float("inf")
            for hr in self._hits:
                mid_x = (hr.cursor_x_before + hr.cursor_x_after) / 2
                mid_y = (hr.rect.top() + hr.rect.bottom()) / 2
                d = (lx - mid_x) ** 2 + (ly - mid_y) ** 2
                if d < min_dist:
                    min_dist = d
                    best = hr
        return best

    def _click_is_after(self, lx: float, hr: HitRegion) -> bool:
        """Return True if click position is in the right half of the hit region."""
        mid = (hr.cursor_x_before + hr.cursor_x_after) / 2
        return lx >= mid

    def mousePressEvent(self, e: QMouseEvent):
        if self._readonly:
            return
        self.setFocus()
        lx, ly = e.x() / self._zoom, e.y() / self._zoom
        hr = self._hit_at(lx, ly)
        if hr is None:
            return
        at_end = self._click_is_after(lx, hr)
        if e.modifiers() & Qt.ShiftModifier:
            self._model.set_cursor_range(
                self._model.cursor_id or hr.node_id,
                hr.node_id
            )
        else:
            self._model.set_cursor(hr.node_id, at_end)
            self._drag_anchor_id = hr.node_id
            self._mouse_pressed = True
        self._cursor_vis = True
        self._blink.start()
        self.update()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._readonly or not self._mouse_pressed:
            return
        lx, ly = e.x() / self._zoom, e.y() / self._zoom
        hr = self._hit_at(lx, ly)
        if hr is None or self._drag_anchor_id is None:
            return
        if hr.node_id != self._drag_anchor_id:
            self._model.set_cursor_range(self._drag_anchor_id, hr.node_id)
            self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self._mouse_pressed = False

    def mouseDoubleClickEvent(self, e: QMouseEvent):
        if self._readonly:
            return
        self._model.select_all()
        self._cursor_vis = True
        self.update()

    def _reset_blink(self):
        self._cursor_vis = True
        self._blink.start()

    def keyPressEvent(self, e: QKeyEvent):
        if self._readonly:
            return
        key = e.key()
        mods = e.modifiers()
        ctrl = bool(mods & Qt.ControlModifier)
        shift = bool(mods & Qt.ShiftModifier)
        text = e.text()
        if ctrl and key == Qt.Key_Z:
            self._model.undo()
            self.changed.emit()
            self.update()
            return
        if ctrl and (key == Qt.Key_Y or (shift and key == Qt.Key_Z)):
            self._model.redo()
            self.changed.emit()
            self.update()
            return
        if ctrl and key == Qt.Key_A:
            self._model.select_all()
            self._reset_blink()
            self.update()
            return
        if ctrl and key == Qt.Key_C:
            self._model.copy_selection()
            return
        if ctrl and key == Qt.Key_X:
            self._model.cut_selection()
            self.changed.emit()
            self._reset_blink()
            self.update()
            return
        if ctrl and key == Qt.Key_V:
            self._model.paste()
            self.changed.emit()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Left:
            if shift:
                self._model.extend_selection_left()
            else:
                self._model.move_left()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Right:
            if shift:
                self._model.extend_selection_right()
            else:
                self._model.move_right()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Home:
            if shift:
                self._model.extend_selection_home()
            else:
                self._model.move_home()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_End:
            if shift:
                self._model.extend_selection_end()
            else:
                self._model.move_end()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Tab:
            self._model.tab_next_placeholder()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Backspace:
            self._model.backspace()
            self.changed.emit()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Delete:
            self._model.delete_forward()
            self.changed.emit()
            self._reset_blink()
            self.update()
            return
        if key == Qt.Key_Escape:
            self._model.clear_selection()
            self.update()
            return
        if text and text.isprintable() and not ctrl:
            self._model.insert_text(text)
            self.changed.emit()
            self._reset_blink()
            self.update()

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.ControlModifier:
            d = e.angleDelta().y()
            self._zoom = max(0.4, min(4.0, self._zoom * (1.1 if d > 0 else 1 / 1.1)))
            self._cursor_vis = True
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        bg = _BG_READONLY if self._readonly else _BG_NORMAL
        p.fillRect(self.rect(), bg)
        bc = _BORDER_FOCUS if self._focused else _BORDER_NORMAL
        p.setPen(QPen(bc, 1.5))
        p.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 6, 6)
        p.save()
        p.scale(self._zoom, self._zoom)
        self._hits = []
        root = self._model.root
        m = root.measure(p)
        cx = _PAD_X / self._zoom
        cy = _PAD_Y / self._zoom + m.ascent
        show_cursor = self._focused and self._cursor_vis and not self._readonly
        render_cursor_id = self._model.cursor_id if show_cursor else None
        render_cursor_at_end = self._model.cursor_at_end if show_cursor else False
        root.draw(p, cx, cy, self._hits, self._model.selected_ids,
                  render_cursor_id, render_cursor_at_end)
        new_h = max(_CANVAS_MIN_H, int((m.height + _PAD_Y * 2) * self._zoom) + 4)
        p.restore()
        p.end()
        if self.height() != new_h:
            self.setFixedHeight(new_h)


class MathEditor(QWidget):
    """
    Interactive mathematical formula editor widget.

    Signals
    -------
    formula_changed(str): emitted on modification, carries SymPy string.
    latex_changed(str): emitted on modification, carries LaTeX string.

    Usage
    -----
    ::

        editor = MathEditor()
        editor.formula_changed.connect(print)
        layout.addWidget(editor)

    Keyboard shortcuts
    ------------------
    Left/Right: move cursor
    Shift+Left/Right: extend selection
    Home/End: jump to start/end of sequence
    Shift+Home/End: select to start/end
    Tab: jump to next placeholder
    Backspace: delete left
    Delete: delete right
    Ctrl+A: select all
    Ctrl+C/X/V: copy/cut/paste
    Ctrl+Z/Y: undo/redo
    Escape: clear selection
    """
    formula_changed = Signal(str)
    latex_changed = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None,
                 show_toolbar: bool = True,
                 toolbar_groups: Optional[List[str]] = None,
                 zoom: float = 1.0,
                 readonly: bool = False):
        super().__init__(parent)
        self._model = FormulaModel()
        self._show_toolbar = show_toolbar
        self._groups = toolbar_groups or ["struct", "operators", "greek", "functions", "edit"]
        self._zoom = zoom
        self._readonly = readonly
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(4)
        self._canvas = _Canvas(self._model)
        self._canvas.set_zoom(self._zoom)
        self._canvas.set_readonly(self._readonly)
        self._canvas.changed.connect(self._on_changed)
        root.addWidget(self._canvas)
        if self._show_toolbar and not self._readonly:
            self._toolbar = self._build_toolbar()
            root.addWidget(self._toolbar)

    def _build_toolbar(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMaximumHeight(_TOOLBAR_MAX_H)
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(2, 2, 2, 2)
        lay.setSpacing(4)
        if "struct" in self._groups:
            grp = _grp("Structure")
            gl = QHBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            gl.setSpacing(3)
            for lbl, action, style, tip in STRUCT_BUTTONS:
                b = _btn(lbl, style, tip)
                b.clicked.connect(lambda _, a=action: self._struct(a))
                gl.addWidget(b)
            gl.addStretch()
            lay.addWidget(grp)
        if "operators" in self._groups:
            grp = _grp("Operators & Relations")
            gl = QHBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            gl.setSpacing(3)
            for sym, op in OPERATOR_BUTTONS:
                b = _btn(sym, _S_BTN, op)
                b.clicked.connect(lambda _, o=op: self._op(o))
                gl.addWidget(b)
            gl.addStretch()
            lay.addWidget(grp)
        if "greek" in self._groups:
            grp = _grp("Greek Letters")
            gl = QHBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            gl.setSpacing(3)
            for sym, name in GREEK_BUTTONS:
                b = _btn(sym, _S_BTN_OP, name)
                b.clicked.connect(lambda _, n=name: self._greek(n))
                gl.addWidget(b)
            gl.addStretch()
            lay.addWidget(grp)
        if "functions" in self._groups:
            grp = _grp("Functions")
            gl = QHBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            gl.setSpacing(3)
            for fn in FUNCTION_BUTTONS:
                b = _btn(fn, _S_BTN_FN, fn)
                b.clicked.connect(lambda _, f=fn: self._func(f))
                gl.addWidget(b)
            gl.addStretch()
            lay.addWidget(grp)
        if "edit" in self._groups:
            grp = _grp("Edit")
            gl = QHBoxLayout(grp)
            gl.setContentsMargins(4, 8, 4, 4)
            gl.setSpacing(3)
            for lbl, fn, tip in [
                ("\u232B", self.delete_at_cursor, "Backspace"),
                ("Del",    self.delete_forward,   "Delete forward"),
                ("Clear",  self.clear,            "Clear all"),
                ("\u2190", self.cursor_left,       "Move cursor left"),
                ("\u2192", self.cursor_right,      "Move cursor right"),
                ("Undo",   self.undo,              "Ctrl+Z"),
                ("Redo",   self.redo,              "Ctrl+Y"),
            ]:
                b = _btn(lbl, _S_BTN, tip)
                b.clicked.connect(fn)
                gl.addWidget(b)
            gl.addStretch()
            lay.addWidget(grp)
        scroll.setWidget(w)
        return scroll

    def _focus(self):
        self._canvas.setFocus()

    def _on_changed(self):
        self.formula_changed.emit(self._model.to_sympy())
        self.latex_changed.emit(self._model.to_latex())

    def _struct(self, action: str):
        dispatch = {
            "frac":       self._model.insert_frac,
            "sqrt":       lambda: self._model.insert_sqrt(False),
            "nth_root":   lambda: self._model.insert_sqrt(True),
            "power":      self._model.insert_power,
            "sub":        self._model.insert_subscript,
            "power_sub":  self._model.insert_power_sub,
            "parens":     lambda: self._model.insert_parens("(", ")"),
            "brackets":   lambda: self._model.insert_parens("[", "]"),
            "braces":     lambda: self._model.insert_parens("{", "}"),
            "abs":        self._model.insert_abs,
            "int":        lambda: self._model.insert_integral(True),
            "int_indef":  lambda: self._model.insert_integral(False),
            "sum":        lambda: self._model.insert_sum(True),
            "prod":       lambda: self._model.insert_product(True),
            "limit":      self._model.insert_limit,
            "overline":   self._model.insert_overline,
            "underline":  self._model.insert_underline,
            "matrix22":   lambda: self._model.insert_matrix(2, 2, "("),
            "matrix33":   lambda: self._model.insert_matrix(3, 3, "("),
            "matrix21":   lambda: self._model.insert_matrix(2, 1, "("),
        }
        if action in dispatch:
            dispatch[action]()
        self._canvas.update()
        self._on_changed()
        self._focus()

    def _op(self, op: str):
        self._model.insert_operator(op)
        self._canvas.update()
        self._on_changed()
        self._focus()

    def _greek(self, name: str):
        self._model.insert_greek(name)
        self._canvas.update()
        self._on_changed()
        self._focus()

    def _func(self, name: str):
        self._model.insert_func(name)
        self._canvas.update()
        self._on_changed()
        self._focus()

    def model(self) -> FormulaModel:
        """Return the underlying FormulaModel."""
        return self._model

    def set_model(self, model: FormulaModel):
        """Replace the underlying model."""
        self._model = model
        self._canvas._model = model
        self._canvas.update()
        self._on_changed()

    def set_zoom(self, zoom: float):
        """Set canvas zoom level."""
        self._zoom = zoom
        self._canvas.set_zoom(zoom)

    def zoom(self) -> float:
        return self._zoom

    def set_readonly(self, value: bool):
        """Disable editing."""
        self._readonly = value
        self._canvas.set_readonly(value)
        if hasattr(self, "_toolbar"):
            self._toolbar.setVisible(not value)

    def is_readonly(self) -> bool:
        return self._readonly

    def set_toolbar_visible(self, visible: bool):
        """Show or hide the formula toolbar."""
        if hasattr(self, "_toolbar"):
            self._toolbar.setVisible(visible)

    def set_toolbar_groups(self, groups: List[str]):
        """Rebuild the toolbar with a subset of groups.

        Available: "struct", "operators", "greek", "functions", "edit".
        """
        self._groups = groups
        if hasattr(self, "_toolbar"):
            self.layout().removeWidget(self._toolbar)
            self._toolbar.deleteLater()
        if not self._readonly:
            self._toolbar = self._build_toolbar()
            self.layout().addWidget(self._toolbar)

    def insert_frac(self):
        """Insert a fraction structure."""
        self._model.insert_frac()
        self._canvas.update()
        self._on_changed()

    def insert_sqrt(self, nth: bool = False):
        """Insert a square root (or nth root if nth=True)."""
        self._model.insert_sqrt(nth)
        self._canvas.update()
        self._on_changed()

    def insert_power(self, wrap_current: bool = True):
        """Wrap current node in a power expression."""
        self._model.insert_power(wrap_current)
        self._canvas.update()
        self._on_changed()

    def insert_subscript(self, wrap_current: bool = True):
        """Wrap current node in a subscript expression."""
        self._model.insert_subscript(wrap_current)
        self._canvas.update()
        self._on_changed()

    def insert_power_sub(self):
        """Insert combined power+subscript expression."""
        self._model.insert_power_sub()
        self._canvas.update()
        self._on_changed()

    def insert_parens(self, left: str = "(", right: str = ")"):
        """Insert parentheses / brackets."""
        self._model.insert_parens(left, right)
        self._canvas.update()
        self._on_changed()

    def insert_abs(self):
        """Insert absolute value bars."""
        self._model.insert_abs()
        self._canvas.update()
        self._on_changed()

    def insert_integral(self, definite: bool = True):
        """Insert an integral with optional limits."""
        self._model.insert_integral(definite)
        self._canvas.update()
        self._on_changed()

    def insert_sum(self, with_limits: bool = True):
        """Insert a sum symbol with optional limits."""
        self._model.insert_sum(with_limits)
        self._canvas.update()
        self._on_changed()

    def insert_product(self, with_limits: bool = True):
        """Insert a product symbol with optional limits."""
        self._model.insert_product(with_limits)
        self._canvas.update()
        self._on_changed()

    def insert_limit(self):
        """Insert a limit expression."""
        self._model.insert_limit()
        self._canvas.update()
        self._on_changed()

    def insert_matrix(self, rows: int = 2, cols: int = 2, bracket: str = "("):
        """Insert a matrix with the given dimensions."""
        self._model.insert_matrix(rows, cols, bracket)
        self._canvas.update()
        self._on_changed()

    def insert_overline(self):
        """Insert overline decoration."""
        self._model.insert_overline()
        self._canvas.update()
        self._on_changed()

    def insert_underline(self):
        """Insert underline decoration."""
        self._model.insert_underline()
        self._canvas.update()
        self._on_changed()

    def insert_func(self, name: str):
        """Insert a named function call: name(...)."""
        self._model.insert_func(name)
        self._canvas.update()
        self._on_changed()

    def insert_operator(self, op: str):
        """Insert an operator by key."""
        self._model.insert_operator(op)
        self._canvas.update()
        self._on_changed()

    def insert_greek(self, name: str):
        """Insert a Greek letter by name."""
        self._model.insert_greek(name)
        self._canvas.update()
        self._on_changed()

    def insert_text(self, text: str, italic: bool = True):
        """Insert a plain text character or string."""
        self._model.insert_text(text, italic)
        self._canvas.update()
        self._on_changed()

    def insert_node(self, node):
        """Insert a raw FormulaNode at the current cursor position."""
        self._model.insert_node(node)
        self._canvas.update()
        self._on_changed()

    def delete_at_cursor(self):
        """Backspace: delete node to the left of cursor."""
        self._model.backspace()
        self._canvas.update()
        self._on_changed()

    def delete_forward(self):
        """Delete: delete node to the right of cursor."""
        self._model.delete_forward()
        self._canvas.update()
        self._on_changed()

    def clear(self):
        """Clear the entire formula."""
        self._model.clear()
        self._canvas.update()
        self._on_changed()

    def undo(self):
        """Undo the last action."""
        self._model.undo()
        self._canvas.update()
        self._on_changed()

    def redo(self):
        """Redo the previously undone action."""
        self._model.redo()
        self._canvas.update()
        self._on_changed()

    def can_undo(self) -> bool:
        return self._model.can_undo()

    def can_redo(self) -> bool:
        return self._model.can_redo()

    def cursor_left(self):
        """Move the cursor one position to the left."""
        self._model.move_left()
        self._canvas.update()

    def cursor_right(self):
        """Move the cursor one position to the right."""
        self._model.move_right()
        self._canvas.update()

    def select_all(self):
        """Select all nodes."""
        self._model.select_all()
        self._canvas.update()

    def clear_selection(self):
        """Clear the current selection."""
        self._model.clear_selection()
        self._canvas.update()

    def to_sympy(self) -> str:
        """Return a SymPy-compatible expression string."""
        return self._model.to_sympy()

    def to_latex(self) -> str:
        """Return a LaTeX string."""
        return self._model.to_latex()

    def to_text(self) -> str:
        """Return a plain-text representation."""
        return self._model.to_text()

    def to_pixmap(self, scale: float = 1.0) -> QPixmap:
        """Render the formula canvas to a QPixmap."""
        px = QPixmap(int(self._canvas.width() * scale),
                     int(self._canvas.height() * scale))
        px.fill(_BG_NORMAL)
        p = QPainter(px)
        p.scale(scale, scale)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)
        self._canvas.render(p)
        p.end()
        return px