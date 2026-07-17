from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
from PySide6.QtGui import QPainter, QFont, QFontMetricsF, QPen, QColor, QPixmap
from PySide6.QtCore import Qt, QRectF, QPointF

FONT_FAMILY = "Times New Roman"
FONT_SIZE_NORMAL = 22
FONT_SIZE_SMALL = 15
FONT_SIZE_TINY = 11
FONT_SIZE_OP_LARGE = 32
FRAC_BAR_THICK = 1.5
FRAC_BAR_MARGIN = 3.0
SQRT_OVERHANG = 4.0
SQRT_TICK_W = 9.0
SQRT_TICK_H_RATIO = 0.38
SUP_OFFSET = 0.46
SUB_OFFSET = 0.28
PAREN_MARGIN = 4.0
INTEGRAL_W_RATIO = 0.55
INTEGRAL_H_EXTRA = 18.0
SUM_EXTRA = 12.0
COLOR_FG = QColor(30, 30, 30)
COLOR_PLACEHOLDER = QColor(180, 180, 180)
COLOR_SELECT = QColor(180, 210, 255, 160)
COLOR_CURSOR = QColor(30, 30, 200)
CURSOR_WIDTH = 2
PLACEHOLDER_TEXT = "..."


@dataclass
class RenderMetrics:
    """Geometry of a rendered node: width, ascent above baseline, descent below."""
    width: float = 0.0
    ascent: float = 0.0
    descent: float = 0.0

    @property
    def height(self) -> float:
        return self.ascent + self.descent


@dataclass
class HitRegion:
    """Mouse hit area for a single node with cursor insertion positions."""
    node_id: int = 0
    rect: QRectF = field(default_factory=QRectF)
    cursor_x_before: float = 0.0
    cursor_x_after: float = 0.0
    is_placeholder: bool = False


def _font(painter: QPainter, size: int, italic: bool = False, bold: bool = False) -> QFont:
    f = QFont(FONT_FAMILY, size)
    f.setItalic(italic)
    f.setBold(bold)
    f.setStyleStrategy(QFont.PreferAntialias)
    return f


def _fm(painter: QPainter, font: QFont) -> QFontMetricsF:
    return QFontMetricsF(font)


def _draw_cursor(painter: QPainter, x: float, top_y: float, bot_y: float):
    """Draw a vertical text cursor line at x."""
    pen = painter.pen()
    painter.setPen(QPen(COLOR_CURSOR, CURSOR_WIDTH))
    painter.drawLine(QPointF(x, top_y), QPointF(x, bot_y))
    painter.setPen(pen)


def _draw_bracket(painter: QPainter, x: float, top: float, bot: float,
                  pw: float, sym: str):
    """Render a scalable bracket glyph using vertical painter scaling.

    Translates to (x, top), scales vertically so the native font height
    maps to (bot - top), then draws at the natural baseline.
    """
    target_h = bot - top
    f = QFont(FONT_FAMILY, FONT_SIZE_NORMAL)
    f.setStyleStrategy(QFont.PreferAntialias)
    fm = QFontMetricsF(f)
    native_h = fm.ascent() + fm.descent()
    scale_y = target_h / native_h if native_h > 0 else 1.0
    painter.save()
    painter.translate(x, top)
    painter.scale(1.0, scale_y)
    painter.setFont(f)
    painter.setPen(QPen(COLOR_FG))
    painter.drawText(QPointF(0, fm.ascent()), sym)
    painter.restore()


class FormulaNode:
    """Abstract base for all formula tree nodes."""
    _counter = 0

    def __init__(self):
        FormulaNode._counter += 1
        self.node_id = FormulaNode._counter

    def measure(self, painter: QPainter) -> RenderMetrics:
        raise NotImplementedError

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        raise NotImplementedError

    def collect_ids(self) -> List[int]:
        return [self.node_id]

    def to_sympy(self) -> str:
        return ""

    def to_latex(self) -> str:
        return ""

    def to_text(self) -> str:
        return ""

    def clone(self) -> "FormulaNode":
        import copy
        return copy.deepcopy(self)


class TextNode(FormulaNode):
    """Leaf node rendering a text string at a given font size.

    The cursor is drawn to the RIGHT of this node (after the text),
    so cursor_id == node_id means 'insertion point is after this character'.
    """

    def __init__(self, text: str, size: int = FONT_SIZE_NORMAL,
                 italic: bool = True, bold: bool = False,
                 color: Optional[QColor] = None):
        super().__init__()
        self.text = text
        self.size = size
        self.italic = italic
        self.bold = bold
        self.color = color or COLOR_FG

    def measure(self, painter: QPainter) -> RenderMetrics:
        f = _font(painter, self.size, self.italic, self.bold)
        fm = _fm(painter, f)
        return RenderMetrics(fm.horizontalAdvance(self.text), fm.ascent(), fm.descent())

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        f = _font(painter, self.size, self.italic, self.bold)
        fm = _fm(painter, f)
        w = fm.horizontalAdvance(self.text)
        m = RenderMetrics(w, fm.ascent(), fm.descent())
        r = QRectF(x, y - m.ascent, w, m.height)
        if self.node_id in selected:
            painter.fillRect(r, COLOR_SELECT)
        painter.setFont(f)
        painter.setPen(QPen(self.color))
        painter.drawText(QPointF(x, y), self.text)
        if cursor_id == self.node_id and not cursor_at_end:
            _draw_cursor(painter, x, y - m.ascent, y + m.descent)
        hits.append(HitRegion(self.node_id, r, x, x + w))

    def to_sympy(self) -> str:
        return self.text

    def to_latex(self) -> str:
        return self.text

    def to_text(self) -> str:
        return self.text


class PlaceholderNode(FormulaNode):
    """Empty editable slot shown as a faint placeholder text.

    Cursor is drawn to the LEFT (before) the placeholder,
    indicating 'type here to replace this slot'.
    """

    def __init__(self, size: int = FONT_SIZE_NORMAL):
        super().__init__()
        self.size = size

    def measure(self, painter: QPainter) -> RenderMetrics:
        f = _font(painter, self.size, False)
        fm = _fm(painter, f)
        return RenderMetrics(fm.horizontalAdvance(PLACEHOLDER_TEXT), fm.ascent(), fm.descent())

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        f = _font(painter, self.size, False)
        fm = _fm(painter, f)
        w = fm.horizontalAdvance(PLACEHOLDER_TEXT)
        m = RenderMetrics(w, fm.ascent(), fm.descent())
        r = QRectF(x, y - m.ascent, w, m.height)
        if self.node_id in selected:
            painter.fillRect(r, COLOR_SELECT)
        painter.setFont(f)
        painter.setPen(QPen(COLOR_PLACEHOLDER))
        painter.drawText(QPointF(x, y), PLACEHOLDER_TEXT)
        if cursor_id == self.node_id and not cursor_at_end:
            _draw_cursor(painter, x, y - m.ascent, y + m.descent)
        hits.append(HitRegion(self.node_id, r, x, x + w, True))

    def to_sympy(self) -> str:
        return "x"

    def to_latex(self) -> str:
        return r"\square"

    def to_text(self) -> str:
        return "_"


class SeqNode(FormulaNode):
    """Horizontal sequence of child nodes drawn left to right.

    Cursor placement rules
    ----------------------
    * cursor_id == some_leaf AND cursor_at_end == False
        → the leaf draws its own "before-me" cursor (left edge).
    * cursor_id == last_leaf AND cursor_at_end == True
        → THIS SeqNode draws one cursor at its right edge; children
          receive cursor_at_end=False so they don't draw a duplicate.
    """

    def __init__(self, children: List[FormulaNode]):
        super().__init__()
        self.children = children

    def measure(self, painter: QPainter) -> RenderMetrics:
        if not self.children:
            return RenderMetrics(0, 0, 0)
        metrics = [c.measure(painter) for c in self.children]
        return RenderMetrics(
            sum(m.width for m in metrics),
            max(m.ascent for m in metrics),
            max(m.descent for m in metrics),
        )

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        if not self.children:
            return
        metrics = [c.measure(painter) for c in self.children]
        total_w = sum(m.width for m in metrics)
        max_asc = max(m.ascent for m in metrics)
        max_desc = max(m.descent for m in metrics)

        # Determine whether the "end-of-sequence" cursor belongs to us
        last_child = self.children[-1]
        last_leaf_ids = last_child.collect_ids()
        last_leaf_id = last_leaf_ids[-1] if last_leaf_ids else None
        draw_end_cursor = (cursor_at_end and cursor_id == last_leaf_id
                           and cursor_id is not None)

        cx = x
        for i, c in enumerate(self.children):
            # Never pass cursor_at_end=True into children — we own that cursor.
            c.draw(painter, cx, y, hits, selected, cursor_id, False)
            cx += metrics[i].width

        if draw_end_cursor:
            _draw_cursor(painter, x + total_w, y - max_asc, y + max_desc)

    def collect_ids(self) -> List[int]:
        ids = [self.node_id]
        for c in self.children:
            ids.extend(c.collect_ids())
        return ids

    def to_sympy(self) -> str:
        return "".join(c.to_sympy() for c in self.children)

    def to_latex(self) -> str:
        return "".join(c.to_latex() for c in self.children)

    def to_text(self) -> str:
        return "".join(c.to_text() for c in self.children)


class FracNode(FormulaNode):
    """Fraction with numerator above and denominator below a horizontal bar.

    The baseline (y) is at the fraction bar itself.
    Ascent  = numerator_height   + bar_margin
    Descent = denominator_height + bar_margin
    """

    def __init__(self, num: FormulaNode, den: FormulaNode):
        super().__init__()
        self.num = num
        self.den = den

    def measure(self, painter: QPainter) -> RenderMetrics:
        nm = self.num.measure(painter)
        dm = self.den.measure(painter)
        w = max(nm.width, dm.width) + FRAC_BAR_MARGIN * 2
        return RenderMetrics(w,
                             nm.height + FRAC_BAR_MARGIN + FRAC_BAR_THICK,
                             dm.height + FRAC_BAR_MARGIN)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        nm = self.num.measure(painter)
        dm = self.den.measure(painter)
        m = self.measure(painter)
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        painter.drawLine(QPointF(x, y), QPointF(x + m.width, y))
        painter.setPen(pen)
        self.num.draw(painter, x + (m.width - nm.width) / 2,
                      y - FRAC_BAR_MARGIN - nm.descent, hits, selected, cursor_id)
        self.den.draw(painter, x + (m.width - dm.width) / 2,
                      y + FRAC_BAR_MARGIN + dm.ascent, hits, selected, cursor_id)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.num.collect_ids() + self.den.collect_ids()

    def to_sympy(self) -> str:
        return f"({self.num.to_sympy()}) / ({self.den.to_sympy()})"

    def to_latex(self) -> str:
        return r"\frac{" + self.num.to_latex() + "}{" + self.den.to_latex() + "}"

    def to_text(self) -> str:
        return f"({self.num.to_text()}) / ({self.den.to_text()})"


class SqrtNode(FormulaNode):
    """Square root or nth root node with a radical sign."""

    def __init__(self, body: FormulaNode, index: Optional[FormulaNode] = None):
        super().__init__()
        self.body = body
        self.index = index

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        return RenderMetrics(SQRT_TICK_W + bm.width + SQRT_OVERHANG,
                             bm.ascent + SQRT_OVERHANG, bm.descent)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        m = self.measure(painter)
        top_y = y - m.ascent
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        painter.drawLine(QPointF(x, y - bm.height * SQRT_TICK_H_RATIO),
                         QPointF(x + SQRT_TICK_W * 0.4, y + bm.descent))
        painter.drawLine(QPointF(x + SQRT_TICK_W * 0.4, y + bm.descent),
                         QPointF(x + SQRT_TICK_W, top_y))
        painter.drawLine(QPointF(x + SQRT_TICK_W, top_y),
                         QPointF(x + m.width - SQRT_OVERHANG / 2, top_y))
        painter.setPen(pen)
        self.body.draw(painter, x + SQRT_TICK_W, y, hits, selected, cursor_id, cursor_at_end)
        if self.index:
            idxm = self.index.measure(painter)
            self.index.draw(painter, x, top_y + idxm.ascent * 0.5, hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        ids = [self.node_id] + self.body.collect_ids()
        if self.index:
            ids.extend(self.index.collect_ids())
        return ids

    def to_sympy(self) -> str:
        if self.index:
            return f"({self.body.to_sympy()}) ** (1 / ({self.index.to_sympy()}))"
        return f"sqrt({self.body.to_sympy()})"

    def to_latex(self) -> str:
        if self.index:
            return r"\sqrt[" + self.index.to_latex() + "]{" + self.body.to_latex() + "}"
        return r"\sqrt{" + self.body.to_latex() + "}"

    def to_text(self) -> str:
        return f"sqrt({self.body.to_text()})"


class PowerNode(FormulaNode):
    """Superscript: base raised to an exponent."""

    def __init__(self, base: FormulaNode, exp: FormulaNode):
        super().__init__()
        self.base = base
        self.exp = exp

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.base.measure(painter)
        em = self.exp.measure(painter)
        return RenderMetrics(bm.width + em.width,
                             bm.ascent + em.height * SUP_OFFSET, bm.descent)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.base.measure(painter)
        em = self.exp.measure(painter)
        self.base.draw(painter, x, y, hits, selected, cursor_id, cursor_at_end)
        self.exp.draw(painter, x + bm.width,
                      y - bm.ascent + em.ascent * (1 - SUP_OFFSET),
                      hits, selected, cursor_id)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.base.collect_ids() + self.exp.collect_ids()

    def to_sympy(self) -> str:
        return f"({self.base.to_sympy()}) ** ({self.exp.to_sympy()})"

    def to_latex(self) -> str:
        return self.base.to_latex() + "^{" + self.exp.to_latex() + "}"

    def to_text(self) -> str:
        return f"({self.base.to_text()})^({self.exp.to_text()})"


class SubNode(FormulaNode):
    """Subscript: base with a sub-expression below."""

    def __init__(self, base: FormulaNode, sub: FormulaNode):
        super().__init__()
        self.base = base
        self.sub = sub

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.base.measure(painter)
        sm = self.sub.measure(painter)
        return RenderMetrics(bm.width + sm.width,
                             bm.ascent, bm.descent + sm.height * SUB_OFFSET)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.base.measure(painter)
        sm = self.sub.measure(painter)
        self.base.draw(painter, x, y, hits, selected, cursor_id, cursor_at_end)
        self.sub.draw(painter, x + bm.width,
                      y + bm.descent + sm.ascent * SUB_OFFSET,
                      hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.base.collect_ids() + self.sub.collect_ids()

    def to_sympy(self) -> str:
        return self.base.to_sympy()

    def to_latex(self) -> str:
        return self.base.to_latex() + "_{" + self.sub.to_latex() + "}"

    def to_text(self) -> str:
        return f"{self.base.to_text()}_{self.sub.to_text()}"


class PowerSubNode(FormulaNode):
    """Combined superscript and subscript on a base node."""

    def __init__(self, base: FormulaNode, exp: FormulaNode, sub: FormulaNode):
        super().__init__()
        self.base = base
        self.exp = exp
        self.sub = sub

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.base.measure(painter)
        em = self.exp.measure(painter)
        sm = self.sub.measure(painter)
        script_w = max(em.width, sm.width)
        return RenderMetrics(bm.width + script_w,
                             bm.ascent + em.height * SUP_OFFSET,
                             bm.descent + sm.height * SUB_OFFSET)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.base.measure(painter)
        em = self.exp.measure(painter)
        sm = self.sub.measure(painter)
        self.base.draw(painter, x, y, hits, selected, cursor_id, cursor_at_end)
        self.exp.draw(painter, x + bm.width,
                      y - bm.ascent + em.ascent * (1 - SUP_OFFSET),
                      hits, selected, cursor_id)
        self.sub.draw(painter, x + bm.width,
                      y + bm.descent + sm.ascent * SUB_OFFSET,
                      hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        return ([self.node_id] + self.base.collect_ids()
                + self.exp.collect_ids() + self.sub.collect_ids())

    def to_sympy(self) -> str:
        return f"({self.base.to_sympy()}) ** ({self.exp.to_sympy()})"

    def to_latex(self) -> str:
        return (self.base.to_latex()
                + "^{" + self.exp.to_latex() + "}"
                + "_{" + self.sub.to_latex() + "}")


class ParenNode(FormulaNode):
    """Scalable bracket pair surrounding a body node."""

    def __init__(self, body: FormulaNode, left: str = "(", right: str = ")"):
        super().__init__()
        self.body = body
        self.left = left
        self.right = right

    def _paren_w(self, painter: QPainter) -> float:
        f = _font(painter, FONT_SIZE_NORMAL, False)
        return _fm(painter, f).horizontalAdvance("(")

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        pw = self._paren_w(painter)
        return RenderMetrics(bm.width + pw * 2,
                             bm.ascent + PAREN_MARGIN, bm.descent + PAREN_MARGIN)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        m = self.measure(painter)
        f = _font(painter, FONT_SIZE_NORMAL, False)
        pw = _fm(painter, f).horizontalAdvance("(")
        top = y - m.ascent
        bot = y + m.descent
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        for bar_x, sym in ((x, self.left), (x + pw + bm.width, self.right)):
            _draw_bracket(painter, bar_x, top, bot, pw, sym)
        painter.setPen(pen)
        self.body.draw(painter, x + pw, y, hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.body.collect_ids()

    def to_sympy(self) -> str:
        return f"({self.body.to_sympy()})"

    def to_latex(self) -> str:
        return r"\left" + self.left + self.body.to_latex() + r"\right" + self.right

    def to_text(self) -> str:
        return f"{self.left}{self.body.to_text()}{self.right}"


class AbsNode(FormulaNode):
    """Absolute value: body enclosed in vertical bars."""

    def __init__(self, body: FormulaNode):
        super().__init__()
        self.body = body

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        f = _font(painter, FONT_SIZE_NORMAL, False)
        pw = _fm(painter, f).horizontalAdvance("|")
        return RenderMetrics(bm.width + pw * 2,
                             bm.ascent + PAREN_MARGIN, bm.descent + PAREN_MARGIN)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        m = self.measure(painter)
        f = _font(painter, FONT_SIZE_NORMAL, False)
        pw = _fm(painter, f).horizontalAdvance("|")
        top = y - m.ascent
        bot = y + m.descent
        _draw_bracket(painter, x, top, bot, pw, "|")
        _draw_bracket(painter, x + pw + bm.width, top, bot, pw, "|")
        self.body.draw(painter, x + pw, y, hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.body.collect_ids()

    def to_sympy(self) -> str:
        return f"Abs({self.body.to_sympy()})"

    def to_latex(self) -> str:
        return r"\left|" + self.body.to_latex() + r"\right|"

    def to_text(self) -> str:
        return f"|{self.body.to_text()}|"


class IntegralNode(FormulaNode):
    """Definite or indefinite integral.

    Layout (matches Word / LaTeX):
    ─────────────────────────────────────────────────────────
      upper_limit          (small, top-right of ∫)
        ∫
      lower_limit   body  d  var
    ─────────────────────────────────────────────────────────

    The ∫ glyph is drawn by _draw_bracket style: translate to the top
    of the desired bounding box, scale vertically, then draw at the
    native font baseline.  This is identical to what _draw_bracket does
    for ( ) [ ] and avoids the double-zoom problem.
    """
    _SIGN = "\u222B"  # ∫

    def __init__(self, body: FormulaNode, var: FormulaNode,
                 lower: Optional[FormulaNode] = None,
                 upper: Optional[FormulaNode] = None):
        super().__init__()
        self.body = body
        self.var = var
        self.lower = lower
        self.upper = upper

    # ── private geometry ──────────────────────────────────────────────

    def _ref_font(self) -> QFont:
        """Reference font used for the ∫ glyph (large, italic, serif)."""
        f = QFont(FONT_FAMILY, FONT_SIZE_OP_LARGE)
        f.setItalic(True)
        f.setStyleStrategy(QFont.PreferAntialias)
        return f

    def _sign_size(self, painter: QPainter):
        """Return (sign_w, sign_h, asc_frac).

        sign_h   – total height of the ∫ mark in logical pixels
        sign_w   – width  of the ∫ mark in logical pixels
        asc_frac – fraction of sign_h sitting above the math baseline
        """
        # sign height = 2× a normal text line height
        f_norm = _font(painter, FONT_SIZE_NORMAL, False)
        fm_norm = QFontMetricsF(f_norm)
        line_h = fm_norm.ascent() + fm_norm.descent()
        sign_h = line_h * 2.2

        # compute width by scaling the reference glyph proportionally
        f_ref = self._ref_font()
        fm_ref = QFontMetricsF(f_ref)
        ref_h = fm_ref.ascent() + fm_ref.descent()
        ref_w = fm_ref.horizontalAdvance(self._SIGN)
        # keep the natural aspect ratio, but limit to a reasonable width
        sign_w = min(ref_w * (sign_h / ref_h), sign_h * 0.45)

        # ∫ baseline sits ~68 % down from the top of the glyph in TNR
        asc_frac = 0.68
        return sign_w, sign_h, asc_frac

    def _lim_font(self, painter: QPainter) -> QFont:
        return _font(painter, FONT_SIZE_SMALL, True)

    # ── measure ───────────────────────────────────────────────────────

    def measure(self, painter: QPainter) -> RenderMetrics:
        sign_w, sign_h, asc_frac = self._sign_size(painter)
        sign_asc = sign_h * asc_frac
        sign_dsc = sign_h * (1.0 - asc_frac)

        bm = self.body.measure(painter)
        vm = self.var.measure(painter)
        fw = QFontMetricsF(_font(painter, FONT_SIZE_NORMAL, True)).horizontalAdvance("d")

        # limit column width (right of ∫)
        f_lim = self._lim_font(painter)
        fm_lim = QFontMetricsF(f_lim)
        lim_h = fm_lim.ascent() + fm_lim.descent()
        lw_lo = self.lower.measure(painter).width if self.lower else 0.0
        lw_hi = self.upper.measure(painter).width if self.upper else 0.0
        lw = max(lw_lo, lw_hi)

        total_w = sign_w + lw + bm.width + fw + vm.width + 10

        # vertical extent
        ascent = sign_asc
        descent = sign_dsc
        if self.upper:
            ascent = max(ascent, sign_asc + lim_h)
        if self.lower:
            descent = max(descent, sign_dsc + lim_h)
        ascent = max(ascent, bm.ascent)
        descent = max(descent, bm.descent)
        return RenderMetrics(total_w, ascent, descent)

    # ── draw ──────────────────────────────────────────────────────────

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        sign_w, sign_h, asc_frac = self._sign_size(painter)
        sign_asc = sign_h * asc_frac
        sign_dsc = sign_h * (1.0 - asc_frac)

        bm = self.body.measure(painter)
        f_lim = self._lim_font(painter)
        fm_lim = QFontMetricsF(f_lim)
        lim_h = fm_lim.ascent() + fm_lim.descent()
        lw_lo = self.lower.measure(painter).width if self.lower else 0.0
        lw_hi = self.upper.measure(painter).width if self.upper else 0.0
        lw = max(lw_lo, lw_hi)

        # ── draw ∫ glyph, scaled to fit sign_w × sign_h box ─────────
        f_ref = self._ref_font()
        fm_ref = QFontMetricsF(f_ref)
        ref_h = fm_ref.ascent() + fm_ref.descent()
        ref_w = fm_ref.horizontalAdvance(self._SIGN)
        scale_y = sign_h / ref_h if ref_h > 0 else 1.0
        scale_x = sign_w / ref_w if ref_w > 0 else 1.0

        top_y = y - sign_asc  # top of the ∫ bounding box

        painter.save()
        painter.translate(x, top_y)
        painter.scale(scale_x, scale_y)
        painter.setFont(f_ref)
        painter.setPen(QPen(COLOR_FG))
        painter.drawText(QPointF(0.0, fm_ref.ascent()), self._SIGN)
        painter.restore()

        # ── limits (right of ∫, small font) ──────────────────────────
        lim_x = x + sign_w
        if self.upper:
            # upper limit: sits just above the top of ∫
            up_y = y - sign_asc + fm_lim.ascent()
            self.upper.draw(painter, lim_x, up_y,
                            hits, selected, cursor_id, cursor_at_end)
        if self.lower:
            # lower limit: sits just below the bottom of ∫
            lo_y = y + sign_dsc + fm_lim.ascent()
            self.lower.draw(painter, lim_x, lo_y,
                            hits, selected, cursor_id, cursor_at_end)

        # ── integrand  d var ─────────────────────────────────────────
        cx = x + sign_w + lw
        self.body.draw(painter, cx, y, hits, selected, cursor_id, cursor_at_end)

        f_dx = _font(painter, FONT_SIZE_NORMAL, True)
        fm_dx = QFontMetricsF(f_dx)
        dw = fm_dx.horizontalAdvance("d")
        dx_x = cx + bm.width + 4
        painter.setFont(f_dx)
        painter.setPen(QPen(COLOR_FG))
        painter.drawText(QPointF(dx_x, y), "d")
        self.var.draw(painter, dx_x + dw, y,
                      hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        ids = [self.node_id] + self.body.collect_ids() + self.var.collect_ids()
        if self.lower:
            ids.extend(self.lower.collect_ids())
        if self.upper:
            ids.extend(self.upper.collect_ids())
        return ids

    def to_sympy(self) -> str:
        v = self.var.to_sympy()
        b = self.body.to_sympy()
        if self.lower and self.upper:
            return f"integrate({b}, ({v}, {self.lower.to_sympy()}, {self.upper.to_sympy()}))"
        return f"integrate({b}, {v})"

    def to_latex(self) -> str:
        lim = ""
        if self.lower:
            lim += "_{" + self.lower.to_latex() + "}"
        if self.upper:
            lim += "^{" + self.upper.to_latex() + "}"
        return r"\int" + lim + " " + self.body.to_latex() + r"\,d" + self.var.to_latex()


class LimitNode(FormulaNode):
    """Limit expression: lim with subscript variable -> approach value."""

    def __init__(self, body: FormulaNode, var: FormulaNode,
                 approach: FormulaNode, direction: str = ""):
        super().__init__()
        self.body = body
        self.var = var
        self.approach = approach
        self.direction = direction

    def _lim_label(self, painter: QPainter) -> Tuple[float, float, float]:
        f = _font(painter, FONT_SIZE_NORMAL, False, True)
        fm = _fm(painter, f)
        return fm.horizontalAdvance("lim"), fm.ascent(), fm.descent()

    def measure(self, painter: QPainter) -> RenderMetrics:
        lw, la, ld = self._lim_label(painter)
        bm = self.body.measure(painter)
        vm = self.var.measure(painter)
        am = self.approach.measure(painter)
        arr_w = _fm(painter, _font(painter, FONT_SIZE_TINY)).horizontalAdvance("\u2192")
        sub_w = vm.width + arr_w + am.width
        sym_w = max(lw, sub_w)
        extra = FONT_SIZE_TINY * 1.3
        return RenderMetrics(sym_w + bm.width + 6, bm.ascent + extra, bm.descent)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        lw, la, ld = self._lim_label(painter)
        vm = self.var.measure(painter)
        am = self.approach.measure(painter)
        f_lim = _font(painter, FONT_SIZE_NORMAL, False, True)
        fm_lim = _fm(painter, f_lim)
        sym_w = max(lw, vm.width + 8 + am.width)
        painter.setFont(f_lim)
        painter.setPen(QPen(COLOR_FG))
        painter.drawText(QPointF(x + (sym_w - lw) / 2, y), "lim")
        f_sub = _font(painter, FONT_SIZE_TINY, True)
        fm_sub = _fm(painter, f_sub)
        sub_y = y + ld + fm_sub.ascent() * 0.8
        painter.setFont(f_sub)
        arr_w = fm_sub.horizontalAdvance("\u2192")
        self.var.draw(painter, x, sub_y, hits, selected, cursor_id, cursor_at_end)
        painter.setFont(f_sub)
        painter.setPen(QPen(COLOR_FG))
        painter.drawText(QPointF(x + vm.width, sub_y), "\u2192")
        self.approach.draw(painter, x + vm.width + arr_w, sub_y, hits, selected, cursor_id, cursor_at_end)
        if self.direction:
            painter.setFont(f_sub)
            painter.setPen(QPen(COLOR_FG))
            painter.drawText(QPointF(x + vm.width + arr_w + am.width, sub_y), self.direction)
        self.body.draw(painter, x + sym_w + 6, y, hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        return ([self.node_id] + self.body.collect_ids()
                + self.var.collect_ids() + self.approach.collect_ids())

    def to_sympy(self) -> str:
        d = {"+": "'+'", "-": "'-'", "": "'+'"}.get(self.direction, "'+'")
        return f"limit({self.body.to_sympy()}, {self.var.to_sympy()}, {self.approach.to_sympy()}, {d})"

    def to_latex(self) -> str:
        sub = self.var.to_latex() + r"\to " + self.approach.to_latex()
        if self.direction:
            sub += "^{" + self.direction + "}"
        return r"\lim_{" + sub + "} " + self.body.to_latex()


class SumProdNode(FormulaNode):
    """Summation or product with large operator symbol and optional limits.

    Lower limit renders as "var=lower" (e.g. n=1), upper limit above.
    Symbol size matches Word/LaTeX style.
    """

    def __init__(self, kind: str, body: FormulaNode,
                 var: Optional[FormulaNode] = None,
                 lower: Optional[FormulaNode] = None,
                 upper: Optional[FormulaNode] = None):
        super().__init__()
        self.kind = kind
        self.body = body
        self.var = var
        self.lower = lower
        self.upper = upper
        self._sym = "\u03A3" if kind == "sum" else "\u03A0"

    def _sym_font_size(self) -> int:
        return FONT_SIZE_NORMAL + 14  # Large Σ like Word

    def _sym_dim(self, painter: QPainter) -> Tuple[float, float, float]:
        f = _font(painter, self._sym_font_size(), False, False)
        fm = _fm(painter, f)
        w = fm.horizontalAdvance(self._sym) + 2
        return w, fm.ascent(), fm.descent()

    def _limit_font_size(self) -> int:
        return FONT_SIZE_SMALL  # 15pt for limits

    def _lower_label_width(self, painter: QPainter) -> float:
        """Width of 'var=lower' label."""
        if not self.lower:
            return 0.0
        f_lim = _font(painter, self._limit_font_size(), True)
        fm_lim = _fm(painter, f_lim)
        eq_w = fm_lim.horizontalAdvance("=")
        var_w = self.var.measure(painter).width if self.var else 0
        # Temporarily measure var at limit size
        lm = self.lower.measure(painter)
        return var_w + eq_w + lm.width

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        sw, sa, sd = self._sym_dim(painter)

        f_lim = _font(painter, self._limit_font_size(), True)
        fm_lim = _fm(painter, f_lim)
        lim_h = fm_lim.ascent() + fm_lim.descent()

        lower_w = self._lower_label_width(painter)
        upper_w = self.upper.measure(painter).width if self.upper else 0
        sym_w = max(sw, lower_w, upper_w)

        gap = 3.0
        ascent = sa + (lim_h + gap if self.upper else 0) + SUM_EXTRA * 0.3
        descent = sd + (lim_h + gap if self.lower else 0) + SUM_EXTRA * 0.3
        ascent = max(ascent, bm.ascent)
        descent = max(descent, bm.descent)

        return RenderMetrics(sym_w + bm.width + 6, ascent, descent)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        sw, sa, sd = self._sym_dim(painter)

        f_lim = _font(painter, self._limit_font_size(), True)
        fm_lim = _fm(painter, f_lim)
        lim_h = fm_lim.ascent() + fm_lim.descent()

        lower_w = self._lower_label_width(painter)
        upper_w = self.upper.measure(painter).width if self.upper else 0
        sym_w = max(sw, lower_w, upper_w)

        # Draw big sigma/pi symbol, centered under limits
        f_sym = _font(painter, self._sym_font_size(), False, False)
        painter.setFont(f_sym)
        painter.setPen(QPen(COLOR_FG))
        sym_x = x + (sym_w - sw) / 2
        painter.drawText(QPointF(sym_x, y), self._sym)

        gap = 3.0

        # Draw lower limit: "var=lower" centered below symbol
        if self.lower:
            lm = self.lower.measure(painter)
            eq_w = fm_lim.horizontalAdvance("=")
            var_w = self.var.measure(painter).width if self.var else 0
            total_low_w = lower_w
            low_x = x + (sym_w - total_low_w) / 2
            low_y = y + sd + gap + fm_lim.ascent()

            # Draw var at limit size
            if self.var:
                # Temporarily override size by drawing char at limit font
                painter.setFont(f_lim)
                painter.setPen(QPen(COLOR_FG))
                # We need to draw var using its own draw, but it uses its stored size
                # Draw var text directly
                var_text = self.var.to_text()
                painter.drawText(QPointF(low_x, low_y), var_text)
                painter.drawText(QPointF(low_x + var_w, low_y), "=")
            else:
                painter.setFont(f_lim)
                painter.setPen(QPen(COLOR_FG))
                painter.drawText(QPointF(low_x, low_y), "=")

            self.lower.draw(painter, low_x + var_w + eq_w, low_y,
                            hits, selected, cursor_id)

        # Draw upper limit centered above symbol
        if self.upper:
            um = self.upper.measure(painter)
            up_x = x + (sym_w - um.width) / 2
            up_y = y - sa - gap
            self.upper.draw(painter, up_x, up_y, hits, selected, cursor_id)

        self.body.draw(painter, x + sym_w + 6, y, hits, selected, cursor_id, cursor_at_end)

    def collect_ids(self) -> List[int]:
        ids = [self.node_id] + self.body.collect_ids()
        if self.var:
            ids.extend(self.var.collect_ids())
        if self.lower:
            ids.extend(self.lower.collect_ids())
        if self.upper:
            ids.extend(self.upper.collect_ids())
        return ids

    def to_sympy(self) -> str:
        b = self.body.to_sympy()
        v = self.var.to_sympy() if self.var else "k"
        fn = "Sum" if self.kind == "sum" else "Product"
        if self.lower and self.upper:
            return f"{fn}({b}, ({v}, {self.lower.to_sympy()}, {self.upper.to_sympy()}))"
        return b

    def to_latex(self) -> str:
        sym = r"\sum" if self.kind == "sum" else r"\prod"
        lim = ""
        if self.lower:
            v = self.var.to_latex() if self.var else "k"
            lim += "_{" + v + "=" + self.lower.to_latex() + "}"
        if self.upper:
            lim += "^{" + self.upper.to_latex() + "}"
        return sym + lim + " " + self.body.to_latex()


class MatrixNode(FormulaNode):
    """Matrix node with configurable rows, columns and bracket type."""

    def __init__(self, rows: List[List[FormulaNode]],
                 left: str = "(", right: str = ")"):
        super().__init__()
        self.rows = rows
        self.left = left
        self.right = right

    def _dims(self, painter: QPainter) -> Tuple[List[float], List[float], List[float]]:
        col_w = [0.0] * (max(len(r) for r in self.rows) if self.rows else 0)
        row_asc, row_desc = [], []
        for row in self.rows:
            ra, rd = 0.0, 0.0
            for ci, cell in enumerate(row):
                m = cell.measure(painter)
                col_w[ci] = max(col_w[ci], m.width + 12)
                ra = max(ra, m.ascent)
                rd = max(rd, m.descent)
            row_asc.append(ra)
            row_desc.append(rd)
        return col_w, row_asc, row_desc

    def measure(self, painter: QPainter) -> RenderMetrics:
        col_w, row_asc, row_desc = self._dims(painter)
        total_w = sum(col_w) + 8
        total_h = sum(a + d for a, d in zip(row_asc, row_desc)) + 6 * len(self.rows)
        f = _font(painter, FONT_SIZE_NORMAL, False)
        pw = _fm(painter, f).horizontalAdvance("(") * 1.2
        return RenderMetrics(total_w + pw * 2, total_h / 2 + 4, total_h / 2 + 4)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        col_w, row_asc, row_desc = self._dims(painter)
        m = self.measure(painter)
        f = _font(painter, FONT_SIZE_NORMAL, False)
        pw = _fm(painter, f).horizontalAdvance("(") * 1.2
        top = y - m.ascent
        bot = y + m.descent
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        _draw_bracket(painter, x, top, bot, pw, self.left)
        _draw_bracket(painter, x + m.width - pw, top, bot, pw, self.right)
        painter.setPen(pen)
        cy = y - m.ascent + 4
        for ri, row in enumerate(self.rows):
            cy += row_asc[ri]
            cx = x + pw
            for ci, cell in enumerate(row):
                cell.draw(painter, cx, cy, hits, selected, cursor_id, cursor_at_end)
                cx += col_w[ci]
            cy += row_desc[ri] + 6

    def collect_ids(self) -> List[int]:
        ids = [self.node_id]
        for row in self.rows:
            for cell in row:
                ids.extend(cell.collect_ids())
        return ids

    def to_latex(self) -> str:
        env = "pmatrix" if self.left == "(" else "bmatrix"
        rows = r" \\ ".join(" & ".join(c.to_latex() for c in row) for row in self.rows)
        return r"\begin{" + env + "}" + rows + r"\end{" + env + "}"

    def to_sympy(self) -> str:
        rows = ", ".join("[" + ", ".join(c.to_sympy() for c in row) + "]" for row in self.rows)
        return f"Matrix([{rows}])"


class OverlineNode(FormulaNode):
    """Node with a horizontal bar drawn above the body."""

    def __init__(self, body: FormulaNode):
        super().__init__()
        self.body = body

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        return RenderMetrics(bm.width, bm.ascent + 4, bm.descent)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        self.body.draw(painter, x, y, hits, selected, cursor_id, cursor_at_end)
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        painter.drawLine(QPointF(x, y - bm.ascent - 2),
                         QPointF(x + bm.width, y - bm.ascent - 2))
        painter.setPen(pen)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.body.collect_ids()

    def to_latex(self) -> str:
        return r"\overline{" + self.body.to_latex() + "}"

    def to_sympy(self) -> str:
        return f"conjugate({self.body.to_sympy()})"


class UnderlineNode(FormulaNode):
    """Node with a horizontal bar drawn below the body."""

    def __init__(self, body: FormulaNode):
        super().__init__()
        self.body = body

    def measure(self, painter: QPainter) -> RenderMetrics:
        bm = self.body.measure(painter)
        return RenderMetrics(bm.width, bm.ascent, bm.descent + 4)

    def draw(self, painter: QPainter, x: float, y: float,
             hits: List[HitRegion], selected: set, cursor_id: Optional[int],
             cursor_at_end: bool = False):
        bm = self.body.measure(painter)
        self.body.draw(painter, x, y, hits, selected, cursor_id, cursor_at_end)
        pen = painter.pen()
        painter.setPen(QPen(COLOR_FG, FRAC_BAR_THICK))
        painter.drawLine(QPointF(x, y + bm.descent + 2),
                         QPointF(x + bm.width, y + bm.descent + 2))
        painter.setPen(pen)

    def collect_ids(self) -> List[int]:
        return [self.node_id] + self.body.collect_ids()

    def to_latex(self) -> str:
        return r"\underline{" + self.body.to_latex() + "}"

    def to_sympy(self) -> str:
        return self.body.to_sympy()