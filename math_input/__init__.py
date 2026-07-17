"""
PySide6-math-widget
=================
A PySide6 library for rendering and editing mathematical formulas.

Quick start
-----------
Render a formula (read-only)::

    from PySide6_math_widget import MathView, FracNode, TextNode
    view = MathView()
    view.set_node(FracNode(TextNode("1"), TextNode("2")))

Interactive editor::

    from PySide6_math_widget import MathEditor
    editor = MathEditor()
    editor.formula_changed.connect(print)

Ready-made dialog::

    from PySide6_math_widget import MathDialog
    dlg = MathDialog()
    if dlg.exec():
        print(dlg.result_sympy())

Build a formula tree manually::

    from PySide6_math_widget import (
        SeqNode, TextNode, FracNode, SqrtNode,
        PowerNode, IntegralNode, SumProdNode,
    )
    root = SeqNode([
        TextNode("f(x)"),
        TextNode("="),
        FracNode(TextNode("1"), SqrtNode(TextNode("x"))),
    ])
    view.set_node(root)

Use the model API::

    from PySide6_math_widget import FormulaModel, MathView
    model = FormulaModel()
    model.insert_frac()
    model.insert_greek("alpha")
    view = MathView.from_model(model)

Exports (sympy / latex / text)::

    editor.to_sympy()
    editor.to_latex()
    editor.to_text()
"""
from ._renderer import (
    FormulaNode,
    TextNode,
    PlaceholderNode,
    SeqNode,
    FracNode,
    SqrtNode,
    PowerNode,
    SubNode,
    PowerSubNode,
    ParenNode,
    AbsNode,
    IntegralNode,
    SumProdNode,
    LimitNode,
    MatrixNode,
    OverlineNode,
    UnderlineNode,
    RenderMetrics,
    HitRegion,
    FONT_SIZE_NORMAL,
    FONT_SIZE_SMALL,
    FONT_SIZE_TINY,
    COLOR_FG,
    COLOR_CURSOR,
    COLOR_SELECT,
    COLOR_PLACEHOLDER,
)
from ._model import (
    FormulaModel,
    GREEK_MAP,
    OPERATOR_MAP,
)
from ._view import MathView
from ._editor import (
    MathEditor,
    STRUCT_BUTTONS,
    OPERATOR_BUTTONS,
    GREEK_BUTTONS,
    FUNCTION_BUTTONS,
)
from ._dialog import MathDialog
from ._label import MathLabel
from ._parser import parse_latex, parse_sympy

__version__ = "1.2.0"
__author__ = "PySide6-math-widget"
__all__ = [
    "MathView",
    "MathEditor",
    "MathDialog",
    "MathLabel",
    "parse_latex",
    "parse_sympy",
    "FormulaModel",
    "FormulaNode",
    "TextNode",
    "PlaceholderNode",
    "SeqNode",
    "FracNode",
    "SqrtNode",
    "PowerNode",
    "SubNode",
    "PowerSubNode",
    "ParenNode",
    "AbsNode",
    "IntegralNode",
    "SumProdNode",
    "LimitNode",
    "MatrixNode",
    "OverlineNode",
    "UnderlineNode",
    "RenderMetrics",
    "HitRegion",
    "GREEK_MAP",
    "OPERATOR_MAP",
    "STRUCT_BUTTONS",
    "OPERATOR_BUTTONS",
    "GREEK_BUTTONS",
    "FUNCTION_BUTTONS",
    "FONT_SIZE_NORMAL",
    "FONT_SIZE_SMALL",
    "FONT_SIZE_TINY",
    "COLOR_FG",
    "COLOR_CURSOR",
    "COLOR_SELECT",
    "COLOR_PLACEHOLDER",
]