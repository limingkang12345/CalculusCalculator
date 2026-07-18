from __future__ import annotations
from typing import List, Optional, Tuple
from ._renderer import (
    FormulaNode, SeqNode, TextNode, PlaceholderNode,
    FracNode, SqrtNode, PowerNode, SubNode, PowerSubNode,
    ParenNode, AbsNode, IntegralNode, SumProdNode, LimitNode, MatrixNode,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL, FONT_SIZE_TINY,
)
from ._model import GREEK_MAP, _ph, _t, _op, _seq


def parse_latex(latex: str) -> FormulaNode:
    """Parse a LaTeX string into a FormulaNode tree."""
    tokens = _tokenize_latex(latex.strip())
    parser = _LatexParser(tokens)
    nodes = parser.parse_seq(0, len(tokens))
    if len(nodes) == 1:
        return nodes[0]
    return SeqNode(nodes) if nodes else _ph()


def parse_sympy(expr: str) -> FormulaNode:
    """Parse a SymPy expression string into a FormulaNode tree."""
    tokens = _tokenize_sympy(expr.strip())
    parser = _SympyParser(tokens)
    nodes, _ = parser.parse()
    if len(nodes) == 1:
        return nodes[0]
    return SeqNode(nodes) if nodes else _ph()


_LATEX_GREEK = {"\\" + k: v for k, v in GREEK_MAP.items()}

_LATEX_OPS = {
    r"\cdot": "\u00B7", r"\times": "\u00D7", r"\div": "\u00F7",
    r"\pm": "\u00B1", r"\mp": "\u2213",
    r"\leq": "\u2264", r"\geq": "\u2265", r"\neq": "\u2260",
    r"\approx": "\u2248", r"\equiv": "\u2261", r"\sim": "\u223C",
    r"\in": "\u2208", r"\notin": "\u2209",
    r"\subset": "\u2282", r"\supset": "\u2283",
    r"\cup": "\u222A", r"\cap": "\u2229",
    r"\forall": "\u2200", r"\exists": "\u2203",
    r"\to": "\u2192", r"\rightarrow": "\u2192",
    r"\leftarrow": "\u2190", r"\Rightarrow": "\u21D2",
    r"\infty": "\u221E", r"\partial": "\u2202",
    r"\nabla": "\u2207", r"\hbar": "\u210F",
    r"\oplus": "\u2295", r"\otimes": "\u2297",
    r"\circ": "\u2218", r"\propto": "\u221D",
    r"\ldots": "\u2026", r"\cdots": "\u22EF",
    r"\,": "", r"\;": "", r"\:": "", r"\!": "", r"\quad": " ", r"\qquad": "  ",
}

_LATEX_FUNC_NAMES = {
    r"\sin", r"\cos", r"\tan", r"\cot", r"\sec", r"\csc",
    r"\arcsin", r"\arccos", r"\arctan",
    r"\sinh", r"\cosh", r"\tanh",
    r"\log", r"\ln", r"\exp",
    r"\max", r"\min", r"\gcd", r"\lcm",
    r"\det", r"\tr",
}

_SKIP_TOKENS = {
    r"\left", r"\right", r"\big", r"\Big", r"\bigg", r"\Bigg",
    r"\!", r"\,", r"\;", r"\:",
}


def _tokenize_latex(s: str) -> List[str]:
    tokens: List[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            j = i + 1
            if j >= len(s):
                tokens.append('\\')
                i += 1
            elif not s[j].isalpha():
                tokens.append(s[i:j + 1])
                i = j + 1
            else:
                while j < len(s) and s[j].isalpha():
                    j += 1
                tokens.append(s[i:j])
                i = j
        elif c in '{}^_':
            tokens.append(c)
            i += 1
        elif c in '()[]|':
            tokens.append(c)
            i += 1
        elif c in ' \t\r\n':
            i += 1
        elif c == '&':
            tokens.append('&')
            i += 1
        elif s[i:i+2] == r'\\':
            tokens.append(r'\\')
            i += 2
        elif c.isdigit() or (c == '.' and i + 1 < len(s) and s[i + 1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(s[i:j])
            i = j
        else:
            tokens.append(c)
            i += 1
    return tokens


def _find_close_brace(tokens: List[str], start: int, end: int) -> int:
    """Return index of the closing '}' matching '{' at tokens[start]."""
    depth = 1
    j = start + 1
    while j < end and depth:
        if tokens[j] == '{':
            depth += 1
        elif tokens[j] == '}':
            depth -= 1
        j += 1
    return j


def _find_matching_bracket(tokens: List[str], start: int, end: int,
                            open_c: str, close_c: str) -> int:
    """Return index after the closing bracket matching open_c at tokens[start]."""
    depth = 1
    j = start + 1
    while j < end and depth:
        if tokens[j] == open_c:
            depth += 1
        elif tokens[j] == close_c:
            depth -= 1
        j += 1
    return j


class _LatexParser:
    """Iterative LaTeX token parser."""

    def __init__(self, tokens: List[str]):
        self.tokens = tokens

    def parse_seq(self, start: int, end: int) -> List[FormulaNode]:
        """Parse tokens[start:end] into a list of nodes."""
        nodes: List[FormulaNode] = []
        i = start
        while i < end:
            node, i = self._parse_one(i, end)
            if node is not None:
                nodes.append(node)
        return nodes

    def _parse_group(self, i: int, end: int) -> Tuple[List[FormulaNode], int]:
        """Parse one braced group {…} or a single token. Returns (nodes, new_i)."""
        if i >= end:
            return [_ph()], i
        tok = self.tokens[i]
        if tok == '{':
            j = _find_close_brace(self.tokens, i, end)
            inner = self.parse_seq(i + 1, j - 1)
            return inner if inner else [_ph()], j
        node, new_i = self._parse_one(i, end)
        return [node] if node is not None else [_ph()], new_i

    def _wrap(self, nodes: List[FormulaNode]) -> FormulaNode:
        if not nodes:
            return _ph()
        if len(nodes) == 1:
            return nodes[0]
        return SeqNode(nodes)

    def _parse_one(self, i: int, end: int) -> Tuple[Optional[FormulaNode], int]:
        """Parse a single logical token/construct. Returns (node_or_None, new_i)."""
        tok = self.tokens[i]

        if tok == '{':
            j = _find_close_brace(self.tokens, i, end)
            inner = self.parse_seq(i + 1, j - 1)
            return self._wrap(inner), j

        if tok == '}':
            return None, i + 1

        if tok == '&' or tok == r'\\':
            return None, i + 1

        if tok in _SKIP_TOKENS:
            return None, i + 1

        if tok in (r'\,', r'\;', r'\:', r'\!', r'\quad', r'\qquad'):
            sym = _LATEX_OPS.get(tok, "")
            if sym:
                return TextNode(sym, FONT_SIZE_NORMAL, False), i + 1
            return None, i + 1

        if tok == r'\frac':
            num_nodes, i = self._parse_group(i + 1, end)
            den_nodes, i = self._parse_group(i, end)
            return FracNode(self._wrap(num_nodes), self._wrap(den_nodes)), i

        if tok == r'\sqrt':
            i += 1
            idx_node: Optional[FormulaNode] = None
            if i < end and self.tokens[i] == '[':
                j = _find_matching_bracket(self.tokens, i, end, '[', ']')
                idx_inner = self.parse_seq(i + 1, j - 1)
                idx_node = self._wrap(idx_inner) if idx_inner else None
                i = j
            body_nodes, i = self._parse_group(i, end)
            return SqrtNode(self._wrap(body_nodes), idx_node), i

        if tok in (r'\int', r'\iint', r'\iiint'):
            i += 1
            lower: Optional[FormulaNode] = None
            upper: Optional[FormulaNode] = None
            if i < end and self.tokens[i] == '_':
                lo_nodes, i = self._parse_group(i + 1, end)
                lower = self._wrap(lo_nodes)
            if i < end and self.tokens[i] == '^':
                hi_nodes, i = self._parse_group(i + 1, end)
                upper = self._wrap(hi_nodes)
            if i < end and self.tokens[i] == '^' and upper is None:
                hi_nodes, i = self._parse_group(i + 1, end)
                upper = self._wrap(hi_nodes)
            body_nodes, i = self._parse_group(i, end)
            body = self._wrap(body_nodes)
            var = _t("x", FONT_SIZE_SMALL)
            if i < end and self.tokens[i] in (r'\,', r'\;', r'\:', r'\!'):
                i += 1
            if i < end and self.tokens[i] == 'd':
                i += 1
                if i < end and self.tokens[i] not in ('^', '_', '{', '}', '&', r'\\'):
                    var = _t(self.tokens[i], FONT_SIZE_SMALL)
                    i += 1
            return IntegralNode(body, var, lower, upper), i

        if tok in (r'\sum', r'\prod'):
            kind = "sum" if tok == r'\sum' else "prod"
            i += 1
            lower = None
            upper = None
            if i < end and self.tokens[i] == '_':
                lo_nodes, i = self._parse_group(i + 1, end)
                lower = self._wrap(lo_nodes)
            if i < end and self.tokens[i] == '^':
                hi_nodes, i = self._parse_group(i + 1, end)
                upper = self._wrap(hi_nodes)
            if i < end and self.tokens[i] == '^' and upper is None:
                hi_nodes, i = self._parse_group(i + 1, end)
                upper = self._wrap(hi_nodes)
            body_nodes, i = self._parse_group(i, end)
            body = self._wrap(body_nodes)
            var = _t("k", FONT_SIZE_SMALL)
            if lower is not None:
                var_node, lower = _extract_var_lower(lower)
                if var_node:
                    var = var_node
            return SumProdNode(kind, body, var, lower, upper), i

        if tok == r'\lim':
            i += 1
            lower = None
            if i < end and self.tokens[i] == '_':
                lo_nodes, i = self._parse_group(i + 1, end)
                lower = self._wrap(lo_nodes)
            body_nodes, i = self._parse_group(i, end)
            body = self._wrap(body_nodes)
            var_node = _t("x", FONT_SIZE_TINY)
            approach: FormulaNode = _ph(FONT_SIZE_TINY)
            if lower is not None:
                var_node, approach = _split_limit_sub(lower)
            return LimitNode(body, var_node, approach), i

        if tok in (r'\begin',):
            i += 1
            if i >= end:
                return None, i
            if self.tokens[i] == '{':
                j = _find_close_brace(self.tokens, i, end)
                env_name = "".join(self.tokens[i + 1:j - 1])
                i = j
            else:
                env_name = self.tokens[i]
                i += 1
            env_name = env_name.strip()
            matrix_envs = {'pmatrix': ('(', ')'), 'bmatrix': ('[', ']'),
                           'vmatrix': ('|', '|'), 'Bmatrix': ('{', '}'),
                           'Vmatrix': ('\u2016', '\u2016'), 'matrix': ('', ''),
                           'array': ('(', ')')}
            if env_name in matrix_envs:
                bracket_l, bracket_r = matrix_envs[env_name]
                if env_name == 'array':
                    if i < end and self.tokens[i] == '{':
                        k = _find_close_brace(self.tokens, i, end)
                        i = k
                end_pos = i
                while end_pos < end and self.tokens[end_pos] != r'\end':
                    end_pos += 1
                grid = self._parse_matrix_body(i, end_pos)
                j = end_pos
                if j < end and self.tokens[j] == r'\end':
                    j += 1
                    if j < end and self.tokens[j] == '{':
                        k = _find_close_brace(self.tokens, j, end)
                        j = k
                if bracket_l:
                    return MatrixNode(grid, bracket_l, bracket_r), j
                else:
                    all_cells = [cell for row in grid for cell in row]
                    return SeqNode(all_cells) if len(all_cells) > 1 else (all_cells[0] if all_cells else _ph()), j
            return None, i

        if tok == r'\end':
            _, i2 = self._parse_group(i + 1, end)
            return None, i2

        if tok in _LATEX_FUNC_NAMES:
            name = tok[1:]
            fn = TextNode(name, FONT_SIZE_NORMAL, False)
            i += 1
            if i < end and self.tokens[i] == '{':
                j = _find_close_brace(self.tokens, i, end)
                inner = self.parse_seq(i + 1, j - 1)
                body = self._wrap(inner)
                return SeqNode([fn, ParenNode(body)]), j
            if i < end and self.tokens[i] == '(':
                j = _find_matching_bracket(self.tokens, i, end, '(', ')')
                inner = self.parse_seq(i + 1, j - 1)
                body = self._wrap(inner)
                return SeqNode([fn, ParenNode(body)]), j
            return fn, i

        if tok in _LATEX_GREEK:
            node = TextNode(_LATEX_GREEK[tok], FONT_SIZE_NORMAL, True)
            i += 1
            return _maybe_power_sub(node, self, i, end)

        if tok in _LATEX_OPS:
            sym = _LATEX_OPS[tok]
            if not sym:
                return None, i + 1
            return TextNode(sym, FONT_SIZE_NORMAL, False), i + 1

        if tok == '^':
            exp_nodes, i = self._parse_group(i + 1, end)
            exp = self._wrap(exp_nodes)
            base = _ph()
            return PowerNode(base, exp), i

        if tok == '_':
            sub_nodes, i = self._parse_group(i + 1, end)
            sub = self._wrap(sub_nodes)
            base = _ph()
            return SubNode(base, sub), i

        if tok == '(':
            j = _find_matching_bracket(self.tokens, i, end, '(', ')')
            inner = self.parse_seq(i + 1, j - 1)
            body = self._wrap(inner)
            return ParenNode(body, '(', ')'), j

        if tok == '[':
            j = _find_matching_bracket(self.tokens, i, end, '[', ']')
            inner = self.parse_seq(i + 1, j - 1)
            body = self._wrap(inner)
            return ParenNode(body, '[', ']'), j

        if tok == '|':
            j = i + 1
            while j < end and self.tokens[j] != '|':
                j += 1
            inner = self.parse_seq(i + 1, j)
            body = self._wrap(inner)
            return AbsNode(body), j + 1

        if tok in (r'\text', r'\mathrm', r'\mathbf', r'\mathit', r'\mathbb'):
            bold = tok == r'\mathbf'
            italic = tok == r'\mathit'
            body_nodes, i = self._parse_group(i + 1, end)
            for n in body_nodes:
                if isinstance(n, TextNode):
                    n.italic = italic
                    n.bold = bold
            return self._wrap(body_nodes), i

        if tok.startswith('\\'):
            name = tok[1:]
            if not name:
                return None, i + 1
            return TextNode(name, FONT_SIZE_NORMAL, False), i + 1

        italic = tok.isalpha() and len(tok) == 1
        node = TextNode(tok, FONT_SIZE_NORMAL, italic)
        i += 1
        return _maybe_power_sub(node, self, i, end)

    def _parse_matrix_body(self, start: int, end: int) -> List[List[FormulaNode]]:
        """Parse matrix body tokens into a 2D grid of cells."""
        rows: List[List[FormulaNode]] = []
        current_row: List[FormulaNode] = []
        cell_start = start
        i = start
        while i <= end:
            is_end = (i == end)
            is_col_sep = (not is_end and self.tokens[i] == '&')
            is_row_sep = (not is_end and self.tokens[i] == r'\\')
            if is_end or is_col_sep or is_row_sep:
                cell_nodes = self.parse_seq(cell_start, i)
                cell = (SeqNode(cell_nodes) if len(cell_nodes) > 1
                        else (cell_nodes[0] if cell_nodes else _ph()))
                current_row.append(cell)
                if is_row_sep or is_end:
                    if current_row:
                        rows.append(current_row)
                    current_row = []
                cell_start = i + 1
            i += 1
        if current_row:
            rows.append(current_row)
        if not rows:
            rows = [[_ph()]]
        return rows


    def _postprocess(self, nodes: List[FormulaNode]) -> List[FormulaNode]:
        """Attach orphan ^ and _ nodes to their left neighbour."""
        result: List[FormulaNode] = []
        for node in nodes:
            if isinstance(node, PowerNode) and isinstance(node.base, PlaceholderNode):
                if result:
                    node.base = result.pop()
                result.append(node)
            elif isinstance(node, SubNode) and isinstance(node.base, PlaceholderNode):
                if result:
                    node.base = result.pop()
                result.append(node)
            else:
                result.append(node)
        return result

    def parse_seq(self, start: int, end: int) -> List[FormulaNode]:
        nodes: List[FormulaNode] = []
        i = start
        while i < end:
            node, i = self._parse_one(i, end)
            if node is not None:
                nodes.append(node)
        return self._postprocess(nodes)


def _maybe_power_sub(node: FormulaNode, parser: _LatexParser,
                     i: int, end: int) -> Tuple[FormulaNode, int]:
    """After parsing a base node, check for following ^ and/or _."""
    tokens = parser.tokens
    has_pow = False
    has_sub = False
    pow_node: Optional[FormulaNode] = None
    sub_node: Optional[FormulaNode] = None

    while i < end and tokens[i] in ('^', '_'):
        if tokens[i] == '^' and not has_pow:
            exp_nodes, i = parser._parse_group(i + 1, end)
            pow_node = parser._wrap(exp_nodes)
            has_pow = True
        elif tokens[i] == '_' and not has_sub:
            sub_nodes, i = parser._parse_group(i + 1, end)
            sub_node = parser._wrap(sub_nodes)
            has_sub = True
        else:
            break

    if has_pow and has_sub:
        return PowerSubNode(node, pow_node, sub_node), i
    if has_pow:
        return PowerNode(node, pow_node), i
    if has_sub:
        return SubNode(node, sub_node), i
    return node, i


def _extract_var_lower(lower: FormulaNode) -> Tuple[Optional[TextNode], FormulaNode]:
    """From a subscript like 'k=1' extract var='k' and lower='1'."""
    text = lower.to_text()
    if '=' in text:
        parts = text.split('=', 1)
        var_str = parts[0].strip()
        lo_str = parts[1].strip()
        if var_str:
            from ._model import GREEK_MAP
            sym = GREEK_MAP.get(var_str, var_str)
            return _t(sym, FONT_SIZE_SMALL), TextNode(lo_str, FONT_SIZE_TINY, lo_str.isalpha())
    return None, lower


def _split_limit_sub(sub: FormulaNode) -> Tuple[FormulaNode, FormulaNode]:
    """Split 'x -> 0' subscript into (var, approach)."""
    text = sub.to_text()
    arrow = "\u2192"
    if arrow in text:
        parts = text.split(arrow, 1)
    elif r'\to' in text:
        parts = text.split(r'\to', 1)
    elif '->' in text:
        parts = text.split('->', 1)
    else:
        return _t(text.strip(), FONT_SIZE_TINY), _ph(FONT_SIZE_TINY)
    var_str = parts[0].strip()
    app_str = parts[1].strip()
    var_node = _t(var_str, FONT_SIZE_TINY) if var_str else _t("x", FONT_SIZE_TINY)
    app_node = _t(app_str, FONT_SIZE_TINY) if app_str else _ph(FONT_SIZE_TINY)
    return var_node, app_node


def _nodes_to_matrix(nodes: List[FormulaNode]) -> List[List[FormulaNode]]:
    """Convert a flat list of nodes (with & and \\ separators) into a 2D grid."""
    rows: List[List[FormulaNode]] = []
    current_row: List[FormulaNode] = []
    current_cell: List[FormulaNode] = []
    for node in nodes:
        if isinstance(node, TextNode) and node.text == '&':
            current_row.append(_seq(*current_cell) if len(current_cell) > 1
                               else (current_cell[0] if current_cell else _ph()))
            current_cell = []
        elif isinstance(node, TextNode) and node.text in (r'\\', '\n'):
            current_row.append(_seq(*current_cell) if len(current_cell) > 1
                               else (current_cell[0] if current_cell else _ph()))
            current_cell = []
            rows.append(current_row)
            current_row = []
        else:
            current_cell.append(node)
    if current_cell:
        current_row.append(_seq(*current_cell) if len(current_cell) > 1
                           else (current_cell[0] if current_cell else _ph()))
    if current_row:
        rows.append(current_row)
    if not rows:
        rows = [[_ph()]]
    return rows


def _tokenize_sympy(s: str) -> List[str]:
    tokens: List[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in ' \t':
            i += 1
        elif s[i:i + 2] == '**':
            tokens.append('**')
            i += 2
        elif c in '+-*/()^,':
            tokens.append(c)
            i += 1
        elif c.isdigit() or (c == '.' and i + 1 < len(s) and s[i + 1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(s[i:j])
            i = j
        elif c.isalpha() or c == '_':
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == '_'):
                j += 1
            tokens.append(s[i:j])
            i = j
        else:
            tokens.append(c)
            i += 1
    return tokens


_SYMPY_FUNC_NAMES = {
    "sin", "cos", "tan", "cot", "sec", "csc",
    "asin", "acos", "atan", "arcsin", "arccos", "arctan",
    "sinh", "cosh", "tanh",
    "log", "ln", "exp",
    "Max", "Min", "max", "min",
    "Sum", "Product", "Integral", "Limit",
}


class _SympyParser:
    """Iterative SymPy expression parser."""

    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.n = len(tokens)

    def parse(self, start: int = 0, stop_at_paren: bool = False,
              stop_at_comma: bool = False) -> Tuple[List[FormulaNode], int]:
        nodes: List[FormulaNode] = []
        i = start
        while i < self.n:
            tok = self.tokens[i]

            if tok == ')' and stop_at_paren:
                break
            if tok == ',' and stop_at_comma:
                break

            if tok in ('+', '='):
                nodes.append(TextNode(tok, FONT_SIZE_NORMAL, False))
                i += 1
                continue

            if tok == '-':
                nodes.append(TextNode('\u2212', FONT_SIZE_NORMAL, False))
                i += 1
                continue

            if tok == '*':
                nodes.append(TextNode('\u00B7', FONT_SIZE_NORMAL, False))
                i += 1
                continue

            if tok == '/':
                num = nodes.pop() if nodes else _ph()
                rhs, i = self.parse(i + 1, stop_at_paren=stop_at_paren,
                                    stop_at_comma=True)
                den = rhs[0] if rhs else _ph()
                rest = rhs[1:]
                nodes.append(FracNode(_seq(num), _seq(den)))
                nodes.extend(rest)
                continue

            if tok == '**':
                base = nodes.pop() if nodes else _ph()
                rhs, i = self.parse(i + 1, stop_at_paren=stop_at_paren,
                                    stop_at_comma=True)
                exp = rhs[0] if rhs else _ph(FONT_SIZE_SMALL)
                rest = rhs[1:]
                nodes.append(PowerNode(base, SeqNode([exp]) if not isinstance(exp, SeqNode) else exp))
                nodes.extend(rest)
                continue

            if tok == '^':
                base = nodes.pop() if nodes else _ph()
                rhs, i = self.parse(i + 1, stop_at_paren=stop_at_paren,
                                    stop_at_comma=True)
                exp = rhs[0] if rhs else _ph(FONT_SIZE_SMALL)
                rest = rhs[1:]
                nodes.append(PowerNode(base, exp))
                nodes.extend(rest)
                continue

            if tok == ',':
                i += 1
                continue

            if tok == ')':
                i += 1
                continue

            if tok == '(':
                j = self._find_close(i)
                inner, _ = self.parse(i + 1, stop_at_paren=True)
                body = SeqNode(inner) if len(inner) != 1 else inner[0]
                nodes.append(ParenNode(body))
                i = j + 1
                continue

            if tok == 'sqrt':
                i += 1
                if i < self.n and self.tokens[i] == '(':
                    j = self._find_close(i)
                    inner, _ = self.parse(i + 1, stop_at_paren=True)
                    body = SeqNode(inner) if len(inner) != 1 else inner[0]
                    nodes.append(SqrtNode(body))
                    i = j + 1
                else:
                    nodes.append(TextNode("sqrt", FONT_SIZE_NORMAL, False))
                continue

            if tok in ('Abs', 'abs'):
                i += 1
                if i < self.n and self.tokens[i] == '(':
                    j = self._find_close(i)
                    inner, _ = self.parse(i + 1, stop_at_paren=True)
                    body = SeqNode(inner) if len(inner) != 1 else inner[0]
                    nodes.append(AbsNode(body))
                    i = j + 1
                continue

            if tok in _SYMPY_FUNC_NAMES:
                fn = TextNode(tok, FONT_SIZE_NORMAL, False)
                i += 1
                if i < self.n and self.tokens[i] == '(':
                    j = self._find_close(i)
                    inner, _ = self.parse(i + 1, stop_at_paren=True)
                    body = SeqNode(inner) if len(inner) != 1 else inner[0]
                    nodes.append(fn)
                    nodes.append(ParenNode(body))
                    i = j + 1
                else:
                    nodes.append(fn)
                continue

            if tok in GREEK_MAP:
                nodes.append(TextNode(GREEK_MAP[tok], FONT_SIZE_NORMAL, True))
                i += 1
                continue

            italic = tok.isalpha() and len(tok) == 1
            nodes.append(TextNode(tok, FONT_SIZE_NORMAL, italic))
            i += 1

        return nodes, i

    def _find_close(self, open_pos: int) -> int:
        depth = 1
        j = open_pos + 1
        while j < self.n and depth:
            if self.tokens[j] == '(':
                depth += 1
            elif self.tokens[j] == ')':
                depth -= 1
            j += 1
        return j - 1