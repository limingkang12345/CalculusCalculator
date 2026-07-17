from __future__ import annotations
import copy
from typing import Optional, List, Dict, Tuple
from ._renderer import (
    FormulaNode, SeqNode, TextNode, PlaceholderNode,
    FracNode, SqrtNode, PowerNode, SubNode, PowerSubNode,
    ParenNode, AbsNode, IntegralNode, SumProdNode, LimitNode,
    MatrixNode, OverlineNode, UnderlineNode,
    FONT_SIZE_NORMAL, FONT_SIZE_SMALL, FONT_SIZE_TINY,
)

GREEK_MAP: Dict[str, str] = {
    "alpha": "\u03B1", "beta": "\u03B2", "gamma": "\u03B3", "delta": "\u03B4",
    "epsilon": "\u03B5", "varepsilon": "\u03B5", "zeta": "\u03B6", "eta": "\u03B7",
    "theta": "\u03B8", "vartheta": "\u03D1", "iota": "\u03B9", "kappa": "\u03BA",
    "lambda": "\u03BB", "mu": "\u03BC", "nu": "\u03BD", "xi": "\u03BE",
    "pi": "\u03C0", "varpi": "\u03D6", "rho": "\u03C1", "varrho": "\u03F1",
    "sigma": "\u03C3", "varsigma": "\u03C2", "tau": "\u03C4", "upsilon": "\u03C5",
    "phi": "\u03C6", "varphi": "\u03D5", "chi": "\u03C7", "psi": "\u03C8",
    "omega": "\u03C9",
    "Alpha": "\u0391", "Beta": "\u0392", "Gamma": "\u0393", "Delta": "\u0394",
    "Epsilon": "\u0395", "Zeta": "\u0396", "Eta": "\u0397", "Theta": "\u0398",
    "Iota": "\u0399", "Kappa": "\u039A", "Lambda": "\u039B", "Mu": "\u039C",
    "Nu": "\u039D", "Xi": "\u039E", "Pi": "\u03A0", "Rho": "\u03A1",
    "Sigma": "\u03A3", "Tau": "\u03A4", "Upsilon": "\u03A5", "Phi": "\u03A6",
    "Chi": "\u03A7", "Psi": "\u03A8", "Omega": "\u03A9",
    "inf": "\u221E", "infty": "\u221E", "partial": "\u2202",
    "nabla": "\u2207", "hbar": "\u210F",
}

OPERATOR_MAP: Dict[str, str] = {
    "+": "+", "-": "\u2212", "*": "\u00B7", "/": "/", "=": "=",
    "!=": "\u2260", "<=": "\u2264", ">=": "\u2265", "<": "<", ">": ">",
    "->": "\u2192", "<-": "\u2190", "<->": "\u2194", "=>": "\u21D2",
    "pm": "\u00B1", "mp": "\u2213", "times": "\u00D7", "div": "\u00F7",
    "cdot": "\u00B7", "approx": "\u2248", "sim": "\u223C", "equiv": "\u2261",
    "propto": "\u221D", "in": "\u2208", "notin": "\u2209",
    "subset": "\u2282", "supset": "\u2283", "cup": "\u222A", "cap": "\u2229",
    "forall": "\u2200", "exists": "\u2203",
    "oplus": "\u2295", "otimes": "\u2297", "circ": "\u2218",
}

_STRUCTURAL_ATTRS = ("num", "den", "body", "base", "exp", "sub",
                     "var", "lower", "upper", "index", "approach")


def _ph(size: int = FONT_SIZE_NORMAL) -> PlaceholderNode:
    return PlaceholderNode(size)


def _t(text: str, size: int = FONT_SIZE_NORMAL,
       italic: bool = True, bold: bool = False) -> TextNode:
    return TextNode(text, size, italic, bold)


def _op(text: str) -> TextNode:
    return TextNode(text, FONT_SIZE_NORMAL, False)


def _seq(*nodes: FormulaNode) -> SeqNode:
    return SeqNode(list(nodes))


def _collect_leaves(node: FormulaNode, out: List[FormulaNode]):
    if isinstance(node, (TextNode, PlaceholderNode)):
        out.append(node)
        return
    if isinstance(node, SeqNode):
        for c in node.children:
            _collect_leaves(c, out)
        return
    for attr in _STRUCTURAL_ATTRS:
        child = getattr(node, attr, None)
        if child is not None:
            _collect_leaves(child, out)
    if hasattr(node, "rows"):
        for row in node.rows:
            for cell in row:
                _collect_leaves(cell, out)


def _collect_leaf_ids(node: FormulaNode, out: List[int]):
    leaves: List[FormulaNode] = []
    _collect_leaves(node, leaves)
    out.extend(n.node_id for n in leaves)


def _collect_placeholders(node: FormulaNode, out: List[int]):
    leaves: List[FormulaNode] = []
    _collect_leaves(node, leaves)
    out.extend(n.node_id for n in leaves if isinstance(n, PlaceholderNode))


class CursorPos:
    """
    Word-style cursor position: (seq, index) where index is the insertion
    point BEFORE seq.children[index]. index == len(seq.children) means end.
    """
    __slots__ = ("seq", "index")
    def __init__(self, seq: SeqNode, index: int):
        self.seq = seq
        self.index = index


class FormulaModel:
    """
    Formula document model with Word-style editing semantics.

    Cursor is a position BETWEEN nodes in a SeqNode, not ON a node.
    cursor_id refers to the leaf node immediately AFTER the cursor,
    or the last leaf if cursor is at end of sequence.
    Selection is a range of leaf node ids between anchor and cursor.
    """
    MAX_HISTORY = 120

    def __init__(self):
        ph = _ph()
        self._root: SeqNode = _seq(ph)
        self._cursor_id: Optional[int] = ph.node_id
        self._cursor_at_end: bool = False
        self._selected: set = set()
        self._sel_anchor: Optional[int] = None
        self._sel_anchor_at_end: bool = False
        self._history: List[tuple] = []
        self._redo: List[tuple] = []
        self._clipboard: Optional[List[FormulaNode]] = None

    @property
    def root(self) -> FormulaNode:
        return self._root

    @property
    def cursor_id(self) -> Optional[int]:
        return self._cursor_id

    @property
    def cursor_at_end(self) -> bool:
        return self._cursor_at_end

    @property
    def selected_ids(self) -> set:
        return self._selected

    def _save(self):
        state = (copy.deepcopy(self._root), self._cursor_id, self._cursor_at_end)
        self._history.append(state)
        self._redo.clear()
        if len(self._history) > self.MAX_HISTORY:
            self._history.pop(0)

    def _ids(self) -> List[int]:
        return self._root.collect_ids()

    def _leaf_ids(self) -> List[int]:
        out: List[int] = []
        _collect_leaf_ids(self._root, out)
        return out

    def _leaves(self) -> List[FormulaNode]:
        out: List[FormulaNode] = []
        _collect_leaves(self._root, out)
        return out

    def _validate_cursor(self):
        leaf_ids = self._leaf_ids()
        if not leaf_ids:
            return
        if self._cursor_id not in leaf_ids:
            self._cursor_id = leaf_ids[-1]
            self._cursor_at_end = True

    def _find_seq(self, root: FormulaNode, target_id: int
                  ) -> Optional[Tuple[SeqNode, int]]:
        """Find (parent_seq, child_index) for the node with target_id."""
        if isinstance(root, SeqNode):
            for i, c in enumerate(root.children):
                if c.node_id == target_id:
                    return root, i
                r = self._find_seq(c, target_id)
                if r:
                    return r
        for attr in _STRUCTURAL_ATTRS:
            child = getattr(root, attr, None)
            if child is None:
                continue
            if child.node_id == target_id:
                if isinstance(child, SeqNode):
                    return child, 0
                return SeqNode([child]), 0
            r = self._find_seq(child, target_id)
            if r:
                return r
        if hasattr(root, "rows"):
            for row in root.rows:
                for cell in row:
                    r = self._find_seq(cell, target_id)
                    if r:
                        return r
        return None

    def _cursor_pos(self) -> Optional[CursorPos]:
        """Return CursorPos for the current cursor state."""
        if self._cursor_id is None:
            return None
        res = self._find_seq(self._root, self._cursor_id)
        if res is None:
            self._validate_cursor()
            if self._cursor_id is None:
                return None
            res = self._find_seq(self._root, self._cursor_id)
        if res is None:
            return None
        seq, idx = res
        if self._cursor_at_end:
            return CursorPos(seq, len(seq.children))
        return CursorPos(seq, idx)

    def _leaf_id_for_cursor(self, cp: CursorPos) -> Optional[int]:
        """Return the leaf id that represents this cursor position for rendering."""
        seq = cp.seq
        if not seq.children:
            return None
        idx = min(cp.index, len(seq.children) - 1)
        leaves: List[FormulaNode] = []
        _collect_leaves(seq.children[idx], leaves)
        if not leaves:
            return None
        if cp.index >= len(seq.children):
            return leaves[-1].node_id
        return leaves[0].node_id

    def _seq_leaf_ids(self, seq: SeqNode) -> List[int]:
        out: List[int] = []
        for c in seq.children:
            _collect_leaf_ids(c, out)
        return out

    def undo(self):
        if not self._history:
            return
        self._redo.append((copy.deepcopy(self._root), self._cursor_id, self._cursor_at_end))
        root, cid, cat_end = self._history.pop()
        self._root = root
        self._cursor_id = cid
        self._cursor_at_end = cat_end
        self._selected.clear()
        self._sel_anchor = None
        self._validate_cursor()

    def redo(self):
        if not self._redo:
            return
        self._history.append((copy.deepcopy(self._root), self._cursor_id, self._cursor_at_end))
        root, cid, cat_end = self._redo.pop()
        self._root = root
        self._cursor_id = cid
        self._cursor_at_end = cat_end
        self._selected.clear()
        self._sel_anchor = None
        self._validate_cursor()

    def can_undo(self) -> bool:
        return bool(self._history)

    def can_redo(self) -> bool:
        return bool(self._redo)

    def move_left(self):
        """Move cursor one position left (Word-style)."""
        if self._selected:
            sel_ids = self._leaf_ids()
            sel_sorted = [i for i in sel_ids if i in self._selected]
            if sel_sorted:
                first = sel_sorted[0]
                self._cursor_id = first
                self._cursor_at_end = False
            self._selected.clear()
            self._sel_anchor = None
            return
        cp = self._cursor_pos()
        if cp is None:
            return
        if cp.index > 0:
            new_idx = cp.index - 1
            child = cp.seq.children[new_idx]
            leaves: List[FormulaNode] = []
            _collect_leaves(child, leaves)
            if leaves:
                self._cursor_id = leaves[0].node_id
                self._cursor_at_end = False
        else:
            parent_res = self._find_parent_seq(self._root, cp.seq)
            if parent_res:
                parent_seq, seq_child_idx = parent_res
                if seq_child_idx > 0:
                    prev_child = parent_seq.children[seq_child_idx - 1]
                    leaves: List[FormulaNode] = []
                    _collect_leaves(prev_child, leaves)
                    if leaves:
                        self._cursor_id = leaves[0].node_id
                        self._cursor_at_end = False
                else:
                    inner_leaves = self._seq_leaf_ids(cp.seq)
                    if inner_leaves:
                        self._cursor_id = inner_leaves[0]
                        self._cursor_at_end = False

    def move_right(self):
        """Move cursor one position right (Word-style)."""
        if self._selected:
            sel_ids = self._leaf_ids()
            sel_sorted = [i for i in sel_ids if i in self._selected]
            if sel_sorted:
                last = sel_sorted[-1]
                leaves = self._leaves()
                last_leaf = next((l for l in leaves if l.node_id == last), None)
                if last_leaf:
                    res = self._find_seq(self._root, last_leaf.node_id)
                    if res:
                        seq, idx = res
                        if idx + 1 < len(seq.children):
                            nxt_leaves: List[FormulaNode] = []
                            _collect_leaves(seq.children[idx + 1], nxt_leaves)
                            if nxt_leaves:
                                self._cursor_id = nxt_leaves[0].node_id
                                self._cursor_at_end = False
                        else:
                            self._cursor_id = last
                            self._cursor_at_end = True
            self._selected.clear()
            self._sel_anchor = None
            return
        cp = self._cursor_pos()
        if cp is None:
            return
        cur_idx = cp.index if not self._cursor_at_end else len(cp.seq.children)
        if cur_idx < len(cp.seq.children):
            child = cp.seq.children[cur_idx]
            leaves: List[FormulaNode] = []
            _collect_leaves(child, leaves)
            if leaves:
                last_in_child = leaves[-1]
                res2 = self._find_seq(self._root, last_in_child.node_id)
                if res2:
                    s2, i2 = res2
                    if i2 + 1 < len(s2.children):
                        nxt: List[FormulaNode] = []
                        _collect_leaves(s2.children[i2 + 1], nxt)
                        if nxt:
                            self._cursor_id = nxt[0].node_id
                            self._cursor_at_end = False
                            return
                self._cursor_id = last_in_child.node_id
                self._cursor_at_end = True
        else:
            parent_res = self._find_parent_seq(self._root, cp.seq)
            if parent_res:
                parent_seq, seq_child_idx = parent_res
                if seq_child_idx + 1 < len(parent_seq.children):
                    nxt_child = parent_seq.children[seq_child_idx + 1]
                    nxt_leaves: List[FormulaNode] = []
                    _collect_leaves(nxt_child, nxt_leaves)
                    if nxt_leaves:
                        self._cursor_id = nxt_leaves[0].node_id
                        self._cursor_at_end = False

    def move_home(self):
        """Move cursor to the beginning of the current sequence."""
        cp = self._cursor_pos()
        if cp is None:
            return
        if cp.seq.children:
            leaves: List[FormulaNode] = []
            _collect_leaves(cp.seq.children[0], leaves)
            if leaves:
                self._cursor_id = leaves[0].node_id
                self._cursor_at_end = False
        self._selected.clear()
        self._sel_anchor = None

    def move_end(self):
        """Move cursor to the end of the current sequence."""
        cp = self._cursor_pos()
        if cp is None:
            return
        if cp.seq.children:
            leaves: List[FormulaNode] = []
            _collect_leaves(cp.seq.children[-1], leaves)
            if leaves:
                self._cursor_id = leaves[-1].node_id
                self._cursor_at_end = True
        self._selected.clear()
        self._sel_anchor = None

    def tab_next_placeholder(self):
        """Tab: move cursor to the next placeholder in document order."""
        ph_ids: List[int] = []
        _collect_placeholders(self._root, ph_ids)
        if not ph_ids:
            return
        leaf_ids = self._leaf_ids()
        cur_idx = leaf_ids.index(self._cursor_id) if self._cursor_id in leaf_ids else -1
        for ph_id in ph_ids:
            ph_idx = leaf_ids.index(ph_id) if ph_id in leaf_ids else -1
            if ph_idx > cur_idx:
                self._cursor_id = ph_id
                self._cursor_at_end = False
                self._selected.clear()
                self._sel_anchor = None
                return
        self._cursor_id = ph_ids[0]
        self._cursor_at_end = False
        self._selected.clear()
        self._sel_anchor = None

    def _find_parent_seq(self, root: FormulaNode, target_seq: SeqNode
                         ) -> Optional[Tuple[SeqNode, int]]:
        """Find (parent_seq, child_index) where parent_seq.children[i] contains target_seq."""
        if isinstance(root, SeqNode):
            for i, c in enumerate(root.children):
                if c is target_seq:
                    return root, i
                r = self._find_parent_seq(c, target_seq)
                if r:
                    return r
        for attr in _STRUCTURAL_ATTRS:
            child = getattr(root, attr, None)
            if child is None:
                continue
            if child is target_seq:
                return None
            r = self._find_parent_seq(child, target_seq)
            if r:
                return r
        if hasattr(root, "rows"):
            for row in root.rows:
                for cell in row:
                    if cell is target_seq:
                        return None
                    r = self._find_parent_seq(cell, target_seq)
                    if r:
                        return r
        return None

    def extend_selection_left(self):
        """Shift+Left: extend selection leftward."""
        leaf_ids = self._leaf_ids()
        if not leaf_ids:
            return
        if self._sel_anchor is None:
            self._sel_anchor = self._cursor_id
            self._sel_anchor_at_end = self._cursor_at_end
        if self._cursor_id not in leaf_ids:
            self._cursor_id = leaf_ids[-1]
            self._cursor_at_end = True
        idx = leaf_ids.index(self._cursor_id)
        if self._cursor_at_end:
            self._cursor_at_end = False
        elif idx > 0:
            self._cursor_id = leaf_ids[idx - 1]
            self._cursor_at_end = False
        self._rebuild_selection(leaf_ids)

    def extend_selection_right(self):
        """Shift+Right: extend selection rightward."""
        leaf_ids = self._leaf_ids()
        if not leaf_ids:
            return
        if self._sel_anchor is None:
            self._sel_anchor = self._cursor_id
            self._sel_anchor_at_end = self._cursor_at_end
        if self._cursor_id not in leaf_ids:
            self._cursor_id = leaf_ids[0]
            self._cursor_at_end = False
        idx = leaf_ids.index(self._cursor_id)
        if not self._cursor_at_end:
            self._cursor_at_end = True
        elif idx < len(leaf_ids) - 1:
            self._cursor_id = leaf_ids[idx + 1]
            self._cursor_at_end = True
        self._rebuild_selection(leaf_ids)

    def extend_selection_home(self):
        """Shift+Home: select from cursor to beginning."""
        leaf_ids = self._leaf_ids()
        if not leaf_ids:
            return
        if self._sel_anchor is None:
            self._sel_anchor = self._cursor_id
            self._sel_anchor_at_end = self._cursor_at_end
        self._cursor_id = leaf_ids[0]
        self._cursor_at_end = False
        self._rebuild_selection(leaf_ids)

    def extend_selection_end(self):
        """Shift+End: select from cursor to end."""
        leaf_ids = self._leaf_ids()
        if not leaf_ids:
            return
        if self._sel_anchor is None:
            self._sel_anchor = self._cursor_id
            self._sel_anchor_at_end = self._cursor_at_end
        self._cursor_id = leaf_ids[-1]
        self._cursor_at_end = True
        self._rebuild_selection(leaf_ids)

    def select_all(self):
        """Ctrl+A: select all leaves."""
        ids = self._leaf_ids()
        self._selected = set(ids)
        if ids:
            self._sel_anchor = ids[0]
            self._sel_anchor_at_end = False
            self._cursor_id = ids[-1]
            self._cursor_at_end = True

    def _rebuild_selection(self, ids: List[int]):
        if self._sel_anchor is None or self._sel_anchor not in ids:
            self._selected.clear()
            return
        ai = ids.index(self._sel_anchor)
        ci = ids.index(self._cursor_id) if self._cursor_id in ids else 0
        anch_end = getattr(self, "_sel_anchor_at_end", False)
        cur_end = self._cursor_at_end
        a_pos = ai * 2 + (1 if anch_end else 0)
        c_pos = ci * 2 + (1 if cur_end else 0)
        lo_pos, hi_pos = min(a_pos, c_pos), max(a_pos, c_pos)
        lo_i = lo_pos // 2
        hi_i = hi_pos // 2
        self._selected = set(ids[lo_i: hi_i + 1])

    def clear_selection(self):
        self._selected.clear()
        self._sel_anchor = None

    def set_cursor(self, node_id: int, at_end: bool = False):
        """Set cursor to a specific leaf node."""
        leaf_ids = self._leaf_ids()
        if node_id in leaf_ids:
            self._cursor_id = node_id
            self._cursor_at_end = at_end
            self._selected.clear()
            self._sel_anchor = None

    def set_cursor_range(self, anchor_id: int, cursor_id: int):
        """Set selection from anchor to cursor (for mouse drag)."""
        leaf_ids = self._leaf_ids()
        if anchor_id not in leaf_ids or cursor_id not in leaf_ids:
            return
        self._sel_anchor = anchor_id
        self._sel_anchor_at_end = False
        self._cursor_id = cursor_id
        self._cursor_at_end = True
        self._rebuild_selection(leaf_ids)

    def _delete_selected(self) -> bool:
        """Delete selected nodes. Return True if anything was deleted."""
        if not self._selected:
            return False
        leaf_ids = self._leaf_ids()
        sel_sorted = [i for i in leaf_ids if i in self._selected]
        if not sel_sorted:
            return False
        first_id = sel_sorted[0]
        res = self._find_seq(self._root, first_id)
        if res is None:
            return False
        self._delete_nodes_in_selected()
        self._selected.clear()
        self._sel_anchor = None
        return True

    def _delete_nodes_in_selected(self):
        """Remove all selected leaf nodes from the tree, replacing empty seqs with placeholders."""
        self._remove_selected_from_node(self._root, is_root_seq=True)
        self._cursor_at_end = False

    def _remove_selected_from_node(self, node: FormulaNode, is_root_seq: bool = False) -> bool:
        """Recursively remove selected nodes. Returns True if node itself should be removed."""
        if isinstance(node, (TextNode, PlaceholderNode)):
            return node.node_id in self._selected
        if isinstance(node, SeqNode):
            i = 0
            first_removed_idx = None
            while i < len(node.children):
                child = node.children[i]
                if self._remove_selected_from_node(child):
                    if first_removed_idx is None:
                        first_removed_idx = i
                    node.children.pop(i)
                else:
                    i += 1
            if not node.children:
                ph = _ph()
                node.children.append(ph)
                self._cursor_id = ph.node_id
            elif first_removed_idx is not None:
                idx = max(0, first_removed_idx - 1) if first_removed_idx > 0 else 0
                leaves: List[FormulaNode] = []
                _collect_leaves(node.children[idx], leaves)
                if leaves:
                    self._cursor_id = leaves[-1].node_id
                    self._cursor_at_end = True
            return False
        for attr in _STRUCTURAL_ATTRS:
            child = getattr(node, attr, None)
            if child is not None:
                self._remove_selected_from_node(child)
        if hasattr(node, "rows"):
            for row in node.rows:
                for cell in row:
                    self._remove_selected_from_node(cell)
        return False

    def _insert_into_seq(self, seq: SeqNode, idx: int, node: FormulaNode):
        """Insert node at position idx, replacing placeholder if present."""
        if idx < len(seq.children) and isinstance(seq.children[idx], PlaceholderNode):
            if isinstance(node, PlaceholderNode):
                return
            seq.children[idx] = node
        else:
            seq.children.insert(idx, node)

    def insert_node(self, node: FormulaNode):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        if self._cursor_at_end:
            # Check if last child is a placeholder — replace it
            if seq.children and isinstance(seq.children[-1], PlaceholderNode):
                seq.children[-1] = node
                new_idx = len(seq.children) - 1
            else:
                seq.children.append(node)
                new_idx = len(seq.children) - 1
        elif idx < len(seq.children) and isinstance(seq.children[idx], PlaceholderNode):
            seq.children[idx] = node
            new_idx = idx
        else:
            seq.children.insert(idx, node)
            new_idx = idx
        leaves: List[FormulaNode] = []
        _collect_leaves(node, leaves)
        if leaves:
            self._cursor_id = leaves[-1].node_id
            self._cursor_at_end = True
        self._validate_cursor()

    def insert_text(self, text: str, italic: bool = True):
        self.insert_node(_t(text, FONT_SIZE_NORMAL, italic))

    def insert_operator(self, op: str):
        sym = OPERATOR_MAP.get(op, op)
        self.insert_node(_op(sym))

    def insert_greek(self, name: str):
        sym = GREEK_MAP.get(name, name)
        self.insert_node(_t(sym, FONT_SIZE_NORMAL, True))

    def _insert_structural(self, node: FormulaNode, focus_id: int):
        """Insert structural node and move cursor to focus_id inside it."""
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        if self._cursor_at_end:
            if seq.children and isinstance(seq.children[-1], PlaceholderNode):
                seq.children[-1] = node
            else:
                seq.children.append(node)
        elif idx < len(seq.children) and isinstance(seq.children[idx], PlaceholderNode):
            seq.children[idx] = node
        else:
            seq.children.insert(idx, node)
        self._cursor_id = focus_id
        self._cursor_at_end = False
        self._validate_cursor()

    def insert_frac(self):
        n, d = _ph(), _ph()
        self._insert_structural(FracNode(_seq(n), _seq(d)), n.node_id)

    def insert_sqrt(self, nth: bool = False):
        b = _ph()
        idx_node = _ph(FONT_SIZE_TINY) if nth else None
        node = SqrtNode(_seq(b), _seq(idx_node) if idx_node else None)
        self._insert_structural(node, (idx_node or b).node_id)

    def insert_power(self, wrap_current: bool = True):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        e = _ph(FONT_SIZE_SMALL)
        if wrap_current and not self._cursor_at_end and idx < len(seq.children):
            cur = seq.children[idx]
            if not isinstance(cur, PlaceholderNode):
                node = PowerNode(cur, _seq(e))
                seq.children[idx] = node
                self._cursor_id = e.node_id
                self._cursor_at_end = False
                return
        base_ph = _ph()
        node = PowerNode(base_ph, _seq(e))
        if self._cursor_at_end:
            seq.children.append(node)
        else:
            seq.children.insert(idx, node)
        self._cursor_id = e.node_id
        self._cursor_at_end = False

    def insert_subscript(self, wrap_current: bool = True):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        s = _ph(FONT_SIZE_SMALL)
        if wrap_current and not self._cursor_at_end and idx < len(seq.children):
            base = seq.children[idx]
            if not isinstance(base, PlaceholderNode):
                node = SubNode(base, _seq(s))
                seq.children[idx] = node
                self._cursor_id = s.node_id
                self._cursor_at_end = False
                return
        base_ph = _ph()
        node = SubNode(base_ph, _seq(s))
        if self._cursor_at_end:
            seq.children.append(node)
        else:
            seq.children.insert(idx, node)
        self._cursor_id = s.node_id
        self._cursor_at_end = False

    def insert_power_sub(self):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        e, s = _ph(FONT_SIZE_SMALL), _ph(FONT_SIZE_SMALL)
        if not self._cursor_at_end and idx < len(seq.children):
            base = seq.children[idx]
            if not isinstance(base, PlaceholderNode):
                node = PowerSubNode(base, _seq(e), _seq(s))
                seq.children[idx] = node
                self._cursor_id = e.node_id
                self._cursor_at_end = False
                return
        base_ph = _ph()
        node = PowerSubNode(base_ph, _seq(e), _seq(s))
        if self._cursor_at_end:
            seq.children.append(node)
        else:
            seq.children.insert(idx, node)
        self._cursor_id = e.node_id
        self._cursor_at_end = False

    def insert_parens(self, left: str = "(", right: str = ")"):
        b = _ph()
        self._insert_structural(ParenNode(_seq(b), left, right), b.node_id)

    def insert_abs(self):
        b = _ph()
        self._insert_structural(AbsNode(_seq(b)), b.node_id)

    def insert_integral(self, definite: bool = True):
        b, v = _ph(), _ph(FONT_SIZE_SMALL)
        lo = _ph(FONT_SIZE_SMALL) if definite else None
        hi = _ph(FONT_SIZE_SMALL) if definite else None
        node = IntegralNode(_seq(b), _seq(v),
                            _seq(lo) if lo else None,
                            _seq(hi) if hi else None)
        self._insert_structural(node, b.node_id)

    def insert_sum(self, with_limits: bool = True):
        b = _ph()
        var = _t("n", FONT_SIZE_SMALL, True)
        lo = _ph(FONT_SIZE_SMALL) if with_limits else None
        hi = _ph(FONT_SIZE_SMALL) if with_limits else None
        node = SumProdNode("sum", _seq(b), _seq(var),
                           _seq(lo) if lo else None,
                           _seq(hi) if hi else None)
        self._insert_structural(node, b.node_id)

    def insert_product(self, with_limits: bool = True):
        b = _ph()
        var = _t("k", FONT_SIZE_SMALL, True)
        lo = _ph(FONT_SIZE_SMALL) if with_limits else None
        hi = _ph(FONT_SIZE_SMALL) if with_limits else None
        node = SumProdNode("prod", _seq(b), _seq(var),
                           _seq(lo) if lo else None,
                           _seq(hi) if hi else None)
        self._insert_structural(node, b.node_id)

    def insert_limit(self):
        b = _ph()
        v = _t("x", FONT_SIZE_TINY)
        a = _ph(FONT_SIZE_TINY)
        self._insert_structural(LimitNode(_seq(b), _seq(v), _seq(a)), b.node_id)

    def insert_matrix(self, rows: int = 2, cols: int = 2, bracket: str = "("):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        right = {"(": ")", "[": "]", "|": "|", "{": "}"}.get(bracket, ")")
        grid = [[_seq(_ph()) for _ in range(cols)] for _ in range(rows)]
        node = MatrixNode(grid, bracket, right)
        if self._cursor_at_end:
            seq.children.append(node)
        else:
            seq.children.insert(idx, node)
        self._cursor_id = grid[0][0].children[0].node_id
        self._cursor_at_end = False

    def insert_overline(self):
        b = _ph()
        self._insert_structural(OverlineNode(_seq(b)), b.node_id)

    def insert_underline(self):
        b = _ph()
        self._insert_structural(UnderlineNode(_seq(b)), b.node_id)

    def insert_func(self, name: str):
        self._save()
        if self._selected:
            self._delete_selected()
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        fn = TextNode(name, FONT_SIZE_NORMAL, False)
        b = _ph()
        paren = ParenNode(_seq(b))
        if self._cursor_at_end:
            seq.children.append(fn)
            seq.children.append(paren)
        else:
            seq.children.insert(idx, fn)
            seq.children.insert(idx + 1, paren)
        self._cursor_id = b.node_id
        self._cursor_at_end = False

    def _find_structural_owner(self, orphan_cursor_id: int
                                ) -> Optional[Tuple[SeqNode, int]]:
        """Find (parent_seq, idx) of structural node whose only leaf is orphan_cursor_id."""
        def _search(node, parent_seq, parent_idx):
            if isinstance(node, SeqNode) and len(node.children) == 1:
                if (isinstance(node.children[0], PlaceholderNode)
                        and node.children[0].node_id == orphan_cursor_id
                        and parent_seq is not None):
                    return parent_seq, parent_idx
            if isinstance(node, SeqNode):
                for i, child in enumerate(node.children):
                    r = _search(child, node, i)
                    if r is not None:
                        return r
            for attr in _STRUCTURAL_ATTRS:
                child = getattr(node, attr, None)
                if child is None:
                    continue
                r = _search(child, parent_seq, parent_idx)
                if r is not None:
                    return r
            if hasattr(node, "rows"):
                for row in node.rows:
                    for cell in row:
                        r = _search(cell, parent_seq, parent_idx)
                        if r is not None:
                            return r
            return None
        return _search(self._root, None, None)

    def backspace(self):
        """Backspace: delete node to the LEFT of cursor (Word-style)."""
        self._save()
        if self._selected:
            self._delete_selected()
            self._selected.clear()
            self._sel_anchor = None
            return
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        at_end = self._cursor_at_end
        if at_end:
            target_idx = len(seq.children) - 1
        else:
            target_idx = idx - 1
        if target_idx < 0:
            owner = self._find_structural_owner(self._cursor_id)
            if owner is not None:
                owner_seq, owner_idx = owner
                leaves_before: List[FormulaNode] = []
                if owner_idx > 0:
                    _collect_leaves(owner_seq.children[owner_idx - 1], leaves_before)
                ph = _ph()
                owner_seq.children[owner_idx] = ph
                self._cursor_id = ph.node_id
                self._cursor_at_end = False
            return
        target = seq.children[target_idx]
        if isinstance(target, PlaceholderNode):
            if len(seq.children) > 1:
                seq.children.pop(target_idx)
                new_idx = max(0, target_idx - 1)
                leaves: List[FormulaNode] = []
                _collect_leaves(seq.children[new_idx], leaves)
                if leaves:
                    self._cursor_id = leaves[-1].node_id
                    self._cursor_at_end = True
            else:
                owner = self._find_structural_owner(target.node_id)
                if owner is not None:
                    owner_seq, owner_idx = owner
                    ph = _ph()
                    owner_seq.children[owner_idx] = ph
                    self._cursor_id = ph.node_id
                    self._cursor_at_end = False
        else:
            inner_leaves: List[FormulaNode] = []
            _collect_leaves(target, inner_leaves)
            if len(inner_leaves) == 1 and isinstance(inner_leaves[0], (TextNode, PlaceholderNode)):
                seq.children.pop(target_idx)
                if not seq.children:
                    ph = _ph()
                    seq.children.append(ph)
                    self._cursor_id = ph.node_id
                    self._cursor_at_end = False
                else:
                    new_idx = max(0, target_idx - 1)
                    leaves2: List[FormulaNode] = []
                    _collect_leaves(seq.children[new_idx], leaves2)
                    if leaves2:
                        self._cursor_id = leaves2[-1].node_id
                        self._cursor_at_end = True
            else:
                seq.children.pop(target_idx)
                ph = _ph()
                seq.children.insert(target_idx, ph)
                if target_idx > 0:
                    prev_leaves: List[FormulaNode] = []
                    _collect_leaves(seq.children[target_idx - 1], prev_leaves)
                    if prev_leaves:
                        self._cursor_id = prev_leaves[-1].node_id
                        self._cursor_at_end = True
                else:
                    self._cursor_id = ph.node_id
                    self._cursor_at_end = False
        self._validate_cursor()

    def delete_forward(self):
        """Delete: delete node to the RIGHT of cursor (Word-style)."""
        self._save()
        if self._selected:
            self._delete_selected()
            self._selected.clear()
            self._sel_anchor = None
            return
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        at_end = self._cursor_at_end
        if at_end:
            target_idx = None
        else:
            target_idx = idx
        if target_idx is None or target_idx >= len(seq.children):
            return
        target = seq.children[target_idx]
        if isinstance(target, PlaceholderNode):
            if len(seq.children) > 1:
                seq.children.pop(target_idx)
                if target_idx < len(seq.children):
                    leaves: List[FormulaNode] = []
                    _collect_leaves(seq.children[target_idx], leaves)
                    if leaves:
                        self._cursor_id = leaves[0].node_id
                        self._cursor_at_end = False
                else:
                    new_idx = len(seq.children) - 1
                    leaves2: List[FormulaNode] = []
                    _collect_leaves(seq.children[new_idx], leaves2)
                    if leaves2:
                        self._cursor_id = leaves2[-1].node_id
                        self._cursor_at_end = True
        else:
            inner_leaves: List[FormulaNode] = []
            _collect_leaves(target, inner_leaves)
            if len(inner_leaves) == 1 and isinstance(inner_leaves[0], (TextNode, PlaceholderNode)):
                seq.children.pop(target_idx)
                if not seq.children:
                    ph = _ph()
                    seq.children.append(ph)
                    self._cursor_id = ph.node_id
                    self._cursor_at_end = False
                elif target_idx < len(seq.children):
                    leaves3: List[FormulaNode] = []
                    _collect_leaves(seq.children[target_idx], leaves3)
                    if leaves3:
                        self._cursor_id = leaves3[0].node_id
                        self._cursor_at_end = False
                else:
                    last_leaves: List[FormulaNode] = []
                    _collect_leaves(seq.children[-1], last_leaves)
                    if last_leaves:
                        self._cursor_id = last_leaves[-1].node_id
                        self._cursor_at_end = True
            else:
                seq.children.pop(target_idx)
                ph = _ph()
                seq.children.insert(target_idx, ph)
                self._cursor_id = ph.node_id
                self._cursor_at_end = False
        self._validate_cursor()

    def delete_at_cursor(self):
        """Legacy backspace for compatibility."""
        self.backspace()

    def copy_selection(self):
        """Copy selected nodes to internal clipboard."""
        if not self._selected:
            return
        leaf_ids = self._leaf_ids()
        sel_sorted = [i for i in leaf_ids if i in self._selected]
        if not sel_sorted:
            return
        nodes = self._collect_selected_top_nodes(sel_sorted)
        self._clipboard = [copy.deepcopy(n) for n in nodes]

    def cut_selection(self):
        """Cut selected nodes to internal clipboard."""
        self.copy_selection()
        if self._clipboard:
            self._save()
            self._delete_selected()
            self._selected.clear()
            self._sel_anchor = None

    def paste(self):
        """Paste from internal clipboard at cursor position."""
        if not self._clipboard:
            return
        self._save()
        if self._selected:
            self._delete_selected()
            self._selected.clear()
            self._sel_anchor = None
        for node in self._clipboard:
            cloned = copy.deepcopy(node)
            self._insert_single_at_cursor(cloned)

    def _insert_single_at_cursor(self, node: FormulaNode):
        """Insert one node at current cursor, advancing cursor after it."""
        cp = self._cursor_pos()
        if cp is None:
            return
        seq, idx = cp.seq, cp.index
        if self._cursor_at_end:
            seq.children.append(node)
        elif idx < len(seq.children) and isinstance(seq.children[idx], PlaceholderNode):
            seq.children[idx] = node
        else:
            seq.children.insert(idx, node)
        leaves: List[FormulaNode] = []
        _collect_leaves(node, leaves)
        if leaves:
            self._cursor_id = leaves[-1].node_id
            self._cursor_at_end = True
        self._validate_cursor()

    def _collect_selected_top_nodes(self, sel_ids: List[int]) -> List[FormulaNode]:
        """Collect highest-level nodes whose all leaves are selected."""
        result: List[FormulaNode] = []
        self._gather_top(self._root, set(sel_ids), result)
        return result

    def _gather_top(self, node: FormulaNode, sel: set, out: List[FormulaNode]):
        node_leaves: List[int] = []
        _collect_leaf_ids(node, node_leaves)
        if not node_leaves:
            return
        if all(lid in sel for lid in node_leaves):
            out.append(node)
            return
        if isinstance(node, SeqNode):
            for c in node.children:
                self._gather_top(c, sel, out)
        for attr in _STRUCTURAL_ATTRS:
            child = getattr(node, attr, None)
            if child is not None:
                self._gather_top(child, sel, out)
        if hasattr(node, "rows"):
            for row in node.rows:
                for cell in row:
                    self._gather_top(cell, sel, out)

    def clear(self):
        self._save()
        ph = _ph()
        self._root = _seq(ph)
        self._cursor_id = ph.node_id
        self._cursor_at_end = False
        self._selected.clear()
        self._sel_anchor = None

    def to_sympy(self) -> str:
        return self._root.to_sympy()

    def to_latex(self) -> str:
        return self._root.to_latex()

    def to_text(self) -> str:
        return self._root.to_text()

    def set_from_text(self, text: str):
        self.clear()
        for ch in text:
            if ch.isprintable():
                self.insert_text(ch, italic=False)