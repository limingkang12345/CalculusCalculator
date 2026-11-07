"""表达式树基础模块。

将 SymPy 表达式转换为按书写顺序保存子节点的树结构：

    运算节点：Add、Mul、Pow、Div
    原子节点：Integer、Rational、Float、Symbol、Constant
    函数节点：Sin、Cos、Tan、Exp、Ln、Log ...

约定：
    * 多参数节点按传入顺序保存参数，可在任意位置插入、交换、替换、删除；
    * Pow 的指数不接受负整数，构造时自动改写为 Div 分式节点；
    * Div 提供通分（common_denominator）与约分（reduce）。

用法：
    from expr_tree import from_string, Div, Symbol, Integer

    tree = from_string("1/x + 1/(x+1)")
    print(list(tree.walk("pre")))
    print(tree.latex())
    print(Div(Integer(1), Symbol("x")).add(Div(Integer(1), Symbol("y"))).reduce())
"""

from __future__ import annotations

import math
import re
from fractions import Fraction

import sympy

__all__ = [
    "Expr",
    "Atom",
    "NaryOp",
    "Add",
    "Mul",
    "Pow",
    "Div",
    "Integer",
    "Rational",
    "Float",
    "Symbol",
    "Constant",
    "Function",
    "UnaryFunction",
    "Sin",
    "Cos",
    "Tan",
    "Cot",
    "Sec",
    "Csc",
    "Asin",
    "Acos",
    "Atan",
    "Acot",
    "Sinh",
    "Cosh",
    "Tanh",
    "Exp",
    "Ln",
    "Log",
    "Abs",
    "Sign",
    "Factorial",
    "as_expr",
    "function",
    "from_sympy",
    "from_string",
    "parse_sympy",
    "Eq",
    "LatexPrinter",
    "latex",
    "color_latex",
]

_CONSTANT_VALUES = {
    "pi": sympy.pi,
    "E": sympy.E,
    "I": sympy.I,
    "EulerGamma": sympy.EulerGamma,
    "GoldenRatio": sympy.GoldenRatio,
    "Catalan": sympy.Catalan,
    "Infinity": sympy.oo,
    "NegativeInfinity": -sympy.oo,
    "ComplexInfinity": sympy.zoo,
    "NaN": sympy.nan,
}

_CONSTANT_NAMES = {value: name for name, value in _CONSTANT_VALUES.items()}


class Expr:
    """所有表达式节点的基类，提供遍历、改写与 SymPy 互操作。"""

    __slots__ = ("_parent",)

    precedence = 100
    op = ""

    is_atom = False
    is_number = False
    is_symbol = False
    is_function = False
    is_operation = False
    is_add = False
    is_mul = False
    is_pow = False
    is_div = False

    def __init__(self) -> None:
        self._parent: Expr | None = None

    @property
    def args(self) -> tuple:
        return ()

    @property
    def children(self) -> tuple:
        return self.args

    @property
    def parent(self) -> "Expr | None":
        return self._parent

    @property
    def root(self) -> "Expr":
        node = self
        while node._parent is not None:
            node = node._parent
        return node

    @property
    def index_in_parent(self) -> int:
        parent = self._parent
        if parent is None:
            return -1
        for index, child in enumerate(parent.args):
            if child is self:
                return index
        return -1

    @property
    def free_symbols(self) -> set:
        return {node for node in self.walk() if node.is_symbol}

    def __bool__(self) -> bool:
        return True

    def __len__(self) -> int:
        return len(self.args)

    def __getitem__(self, index):
        return self.args[index]

    def __iter__(self):
        return iter(self.args)

    def _key(self) -> tuple:
        return (type(self).__name__, tuple(child._key() for child in self.args))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Expr):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())

    def __repr__(self) -> str:
        inner = ", ".join(repr(child) for child in self.args)
        return f"{type(self).__name__}({inner})"

    def __str__(self) -> str:
        return repr(self)

    def copy(self) -> "Expr":
        return self._rebuild([child.copy() for child in self.args])

    def _rebuild(self, args) -> "Expr":
        if not args:
            return self.copy()
        return type(self)(*args)

    def replace_with(self, node) -> "Expr":
        parent = self._parent
        if parent is None:
            raise ValueError("根节点没有父节点，无法替换")
        index = self.index_in_parent
        parent.replace(index, node)
        return parent.args[index]

    def walk(self, mode: str = "pre"):
        """按先序（pre）或后序（post）遍历整棵树。"""
        if mode == "pre":
            yield self
            for child in self.args:
                yield from child.walk("pre")
        elif mode == "post":
            for child in self.args:
                yield from child.walk("post")
            yield self
        else:
            raise ValueError("mode 只能是 'pre' 或 'post'")

    def nodes(self) -> list:
        return list(self.walk("pre"))

    def leaves(self) -> list:
        return [node for node in self.walk("pre") if not node.args]

    def depth(self) -> int:
        if not self.args:
            return 1
        return 1 + max(child.depth() for child in self.args)

    def size(self) -> int:
        return 1 + sum(child.size() for child in self.args)

    def find(self, predicate):
        for node in self.walk("pre"):
            if predicate(node):
                return node
        return None

    def find_all(self, predicate) -> list:
        return [node for node in self.walk("pre") if predicate(node)]

    def contains(self, node) -> bool:
        target = as_expr(node)
        return any(item == target for item in self.walk("pre"))

    def subs(self, old, new) -> "Expr":
        """返回把 old 子树替换为 new 后的新树，原树保持不变。"""
        source = as_expr(old)
        target = as_expr(new)
        return self._subs(source, target)

    def _subs(self, old: "Expr", new: "Expr") -> "Expr":
        if self == old:
            return new.copy()
        if not self.args:
            return self.copy()
        return self._rebuild([child._subs(old, new) for child in self.args])

    def transform(self, func) -> "Expr":
        """自底向上重建整棵树，并对每个节点调用 func。"""
        children = [child.transform(func) for child in self.args]
        return func(self._rebuild(children))

    def to_sympy(self):
        raise NotImplementedError(f"{type(self).__name__} 未实现 to_sympy")

    def _sympy_(self):
        return self.to_sympy()

    def simplify(self) -> "Expr":
        """交给 SymPy 化简，返回新树（顺序按 SymPy 规范排列）。"""
        return from_sympy(sympy.simplify(self.to_sympy()), ordered=True)

    def equals(self, other) -> bool:
        """判断两棵树在数学上是否相等。"""
        return bool(sympy.simplify(self.to_sympy() - as_expr(other).to_sympy()) == 0)

    def latex(self) -> str:
        """按本树结构生成 LaTeX，行为与 sympy.latex 类似。"""
        return latex(self)


class Atom(Expr):
    """原子节点，不包含子节点。"""

    __slots__ = ("_value",)

    is_atom = True

    def __init__(self, value) -> None:
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def args(self) -> tuple:
        return ()

    def _key(self) -> tuple:
        return (type(self).__name__, self._value)

    def copy(self) -> "Atom":
        return type(self)(self._value)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._value!r})"


class Symbol(Atom):
    __slots__ = ()

    is_symbol = True

    def __init__(self, name: str) -> None:
        if not isinstance(name, str) or not name:
            raise ValueError("符号名必须是非空字符串")
        super().__init__(name)

    @property
    def name(self) -> str:
        return self._value

    def to_sympy(self):
        return sympy.Symbol(self._value)

    def __str__(self) -> str:
        return self._value


class Integer(Atom):
    __slots__ = ()

    is_number = True

    def __init__(self, value) -> None:
        super().__init__(int(value))

    @property
    def is_zero(self) -> bool:
        return self._value == 0

    def __int__(self) -> int:
        return self._value

    def to_sympy(self):
        return sympy.Integer(self._value)

    def __str__(self) -> str:
        return str(self._value)


class Rational(Atom):
    __slots__ = ()

    is_number = True

    def __new__(cls, numerator, denominator=1):
        if cls is Rational:
            value = numerator if isinstance(numerator, Fraction) else Fraction(numerator, denominator)
            if value.denominator == 1:
                return Integer(value.numerator)
        return super().__new__(cls)

    def __init__(self, numerator, denominator=1) -> None:
        if isinstance(numerator, Fraction):
            value = numerator
        else:
            value = Fraction(numerator, denominator)
        super().__init__(value)

    @property
    def p(self) -> int:
        return self._value.numerator

    @property
    def q(self) -> int:
        return self._value.denominator

    @property
    def is_zero(self) -> bool:
        return self._value == 0

    def to_sympy(self):
        return sympy.Rational(self.p, self.q)

    def __str__(self) -> str:
        if self.q == 1:
            return str(self.p)
        return f"{self.p}/{self.q}"

    def __repr__(self) -> str:
        return f"Rational({self.p}, {self.q})"


class Float(Atom):
    __slots__ = ()

    is_number = True

    def __init__(self, value) -> None:
        super().__init__(float(value))

    def to_sympy(self):
        return sympy.Float(self._value)

    def __str__(self) -> str:
        return repr(self._value)


class Constant(Atom):
    __slots__ = ()

    is_number = True

    def __init__(self, name: str) -> None:
        if name not in _CONSTANT_VALUES:
            raise ValueError(f"未知常数: {name}")
        super().__init__(name)

    @property
    def name(self) -> str:
        return self._value

    def to_sympy(self):
        return _CONSTANT_VALUES[self._value]

    def __str__(self) -> str:
        return self._value


class NaryOp(Expr):
    """多参数运算节点，按传入顺序保存参数。"""

    __slots__ = ("_args",)

    min_args = 1
    max_args = None
    is_operation = True

    def __init__(self, *args) -> None:
        super().__init__()
        nodes = [as_expr(item) for item in args]
        self._check_arity(len(nodes))
        self._args = []
        for node in nodes:
            self._args.append(self._adopt(node))

    @property
    def args(self) -> tuple:
        return tuple(self._args)

    def _check_arity(self, count: int) -> None:
        name = type(self).__name__
        if count < self.min_args:
            raise ValueError(f"{name} 至少需要 {self.min_args} 个参数，实际传入 {count} 个")
        if self.max_args is not None and count > self.max_args:
            raise ValueError(f"{name} 最多支持 {self.max_args} 个参数，实际传入 {count} 个")

    def _check_cycle(self, node: Expr) -> None:
        current: Expr | None = self
        while current is not None:
            if current is node:
                raise ValueError("不能把节点放入它自身的子树")
            current = current._parent

    def _adopt(self, node: Expr) -> Expr:
        self._check_cycle(node)
        if node._parent is not None:
            node = node.copy()
        node._parent = self
        return node

    def _validate_child(self, index: int, node: Expr) -> None:
        return None

    def _normalize_index(self, index: int) -> int:
        count = len(self._args)
        if not -count <= index < count:
            raise IndexError(f"参数下标越界: {index}")
        return index % count

    def __setitem__(self, index: int, node) -> None:
        self.replace(index, node)

    def insert(self, index: int, node) -> "NaryOp":
        """在指定位置插入一个参数，index 语义与 list.insert 一致。"""
        item = as_expr(node)
        self._check_arity(len(self._args) + 1)
        self._args.insert(index, self._adopt(item))
        return self

    def append(self, node) -> "NaryOp":
        return self.insert(len(self._args), node)

    def replace(self, index: int, node) -> "NaryOp":
        """替换指定位置的参数。"""
        position = self._normalize_index(index)
        item = as_expr(node)
        if item is self._args[position]:
            return self
        self._validate_child(position, item)
        adopted = self._adopt(item)
        self._args[position]._parent = None
        self._args[position] = adopted
        return self

    def remove(self, index: int) -> Expr:
        """移除指定位置的参数并返回该节点。"""
        position = self._normalize_index(index)
        child = self._args.pop(position)
        child._parent = None
        return child

    def swap(self, first: int, second: int) -> "NaryOp":
        """交换两个参数的顺序。"""
        left = self._normalize_index(first)
        right = self._normalize_index(second)
        if left != right:
            self._args[left], self._args[right] = self._args[right], self._args[left]
        return self


class Add(NaryOp):
    __slots__ = ()

    min_args = 2
    max_args = None
    op = "+"
    precedence = 40
    is_add = True

    def to_sympy(self):
        return sympy.Add(*[child.to_sympy() for child in self.args])

    def __str__(self) -> str:
        text = ""
        for index, term in enumerate(self.args):
            piece = str(term)
            if index == 0:
                text = piece
            elif piece.startswith("-"):
                text += " - " + piece[1:]
            else:
                text += " + " + piece
        return text


class Mul(NaryOp):
    __slots__ = ()

    min_args = 2
    max_args = None
    op = "*"
    precedence = 60
    is_mul = True

    def to_sympy(self):
        return sympy.Mul(*[child.to_sympy() for child in self.args])

    def expand(self, index=None) -> Expr:
        """按分配律展开一个 Add 因子，返回新表达式（原树不变）。

        index 为 Add 因子在 args 中的位置；省略时取第一个 Add 因子。
        """
        if index is None:
            index = next((i for i, child in enumerate(self.args) if isinstance(child, Add)), None)
        if index is None or not isinstance(self.args[index], Add):
            return self.copy()
        add = self.args[index]
        others = [child for i, child in enumerate(self.args) if i != index]
        terms = []
        for term in add.args:
            terms.append(_mul_of([*others, term]))
        return _add_of(terms)

    def __str__(self) -> str:
        items = list(self.args)
        sign = ""
        if items:
            head = items[0]
            if isinstance(head, Integer) and head.value < 0:
                sign = "-"
                items[0] = Integer(-head.value)
            elif isinstance(head, Rational) and head.value < 0:
                sign = "-"
                items[0] = Rational(-head.p, head.q)
            elif isinstance(head, Float) and head.value < 0:
                sign = "-"
                items[0] = Float(-head.value)
        if sign and len(items) > 1 and isinstance(items[0], Integer) and items[0].value == 1:
            items = items[1:]
        parts = [_wrap(item, self.precedence) for item in items]
        return sign + "*".join(parts)



class Eq(NaryOp):
    """方程节点：左式 = 右式。"""

    __slots__ = ()

    min_args = 2
    max_args = 2
    op = "="
    precedence = 5
    is_equation = True

    @property
    def left(self) -> Expr:
        return self._args[0]

    @property
    def right(self) -> Expr:
        return self._args[1]

    def to_sympy(self):
        return sympy.Eq(
            self._args[0].to_sympy(),
            self._args[1].to_sympy(),
            evaluate=False,
        )

    def __str__(self) -> str:
        return f"{self._args[0]} = {self._args[1]}"


class Pow(NaryOp):
    __slots__ = ()

    min_args = 2
    max_args = 2
    op = "^"
    precedence = 80
    is_pow = True

    def __new__(cls, base, exponent):
        if cls is Pow:
            power = as_expr(exponent)
            if isinstance(power, Integer) and power.value < 0:
                value = -power.value
                inner = as_expr(base) if value == 1 else Pow(base, Integer(value))
                return Div(Integer(1), inner)
        return super().__new__(cls)

    @property
    def base(self) -> Expr:
        return self._args[0]

    @property
    def exponent(self) -> Expr:
        return self._args[1]

    def _validate_child(self, index: int, node: Expr) -> None:
        if index == 1 and isinstance(node, Integer) and node.value < 0:
            raise ValueError("Pow 的指数不能是负整数，请改用 Div 节点")

    def to_sympy(self):
        return sympy.Pow(self._args[0].to_sympy(), self._args[1].to_sympy())

    def expand(self) -> Expr:
        """展开底数为 Add 的正整数次幂（如 (x+1)^2），原树不变。"""
        if (
            isinstance(self._args[0], Add)
            and isinstance(self._args[1], Integer)
            and self._args[1].value > 1
        ):
            return from_sympy(sympy.expand(self.to_sympy()), ordered=True)
        return self.copy()

    def __str__(self) -> str:
        base, exponent = self.args
        base_text = str(base)
        if isinstance(base, Rational) or base.precedence <= self.precedence or base_text.startswith("-"):
            base_text = f"({base_text})"
        exponent_text = str(exponent)
        if isinstance(exponent, Rational) or exponent.precedence <= self.precedence or exponent_text.startswith("-"):
            exponent_text = f"({exponent_text})"
        return f"{base_text}**{exponent_text}"


class Div(NaryOp):
    __slots__ = ()

    min_args = 2
    max_args = 2
    op = "/"
    precedence = 55
    is_div = True

    def __init__(self, numerator, denominator) -> None:
        value = as_expr(denominator)
        if isinstance(value, (Integer, Rational)) and value.is_zero:
            raise ZeroDivisionError("分母不能为零")
        super().__init__(numerator, value)

    @property
    def numerator(self) -> Expr:
        return self._args[0]

    @property
    def denominator(self) -> Expr:
        return self._args[1]

    def _validate_child(self, index: int, node: Expr) -> None:
        if index == 1 and isinstance(node, (Integer, Rational)) and node.is_zero:
            raise ZeroDivisionError("分母不能为零")

    def to_sympy(self):
        return self._args[0].to_sympy() / self._args[1].to_sympy()

    def reduce(self) -> Expr:
        """约分：约去相同因式与数值公因数，不做多项式因式分解。"""
        numerator_items, numerator_denominators = _split_fraction(self._args[0])
        denominator_items, denominator_numerators = _split_fraction(self._args[1])
        numerator_items = [_fold_numbers(item) for item in numerator_items + denominator_numerators]
        denominator_items = [_fold_numbers(item) for item in denominator_items + numerator_denominators]

        numerator_coefficient, numerator_items = _extract_number(numerator_items)
        denominator_coefficient, denominator_items = _extract_number(denominator_items)
        if denominator_coefficient == 0:
            raise ZeroDivisionError("分母不能为零")
        coefficient = numerator_coefficient / denominator_coefficient
        if coefficient == 0:
            return Integer(0)

        positions: dict = {}
        for position, factor in enumerate(numerator_items):
            positions.setdefault(_base_key(factor), []).append(position)

        used = set()
        remaining = []
        for factor in denominator_items:
            key = _base_key(factor)
            target = next((item for item in positions.get(key, ()) if item not in used), None)
            if target is None:
                remaining.append(factor)
                continue
            used.add(target)
            base, exponent = _base_exponent(numerator_items[target])
            _, other = _base_exponent(factor)
            difference = exponent - other
            if difference == 0:
                numerator_items[target] = None
            elif difference > 0:
                numerator_items[target] = _power(base, difference)
            else:
                numerator_items[target] = None
                remaining.append(_power(base, -difference))

        items = [item for item in numerator_items if item is not None]
        if coefficient.numerator != 1:
            items.insert(0, Integer(coefficient.numerator))
        denominator_factors = []
        if coefficient.denominator != 1:
            denominator_factors.append(Integer(coefficient.denominator))
        denominator_factors.extend(remaining)

        numerator = _fold_numbers(_mul_of(items))
        if not denominator_factors:
            return _detached(numerator)
        denominator = _fold_numbers(_mul_of(denominator_factors))
        if isinstance(numerator, Integer) and isinstance(denominator, Integer):
            if numerator.value % denominator.value == 0:
                return Integer(numerator.value // denominator.value)
            return Rational(numerator.value, denominator.value)
        return Div(numerator, denominator)

    def common_denominator(self, other) -> tuple:
        """通分：返回分母相同的两个分式。"""
        target = as_expr(other)
        if isinstance(target, Div):
            other_numerator, other_denominator = target.args
        else:
            other_numerator, other_denominator = target, Integer(1)
        numerator, denominator = self.args
        common = _common_denominator(denominator, other_denominator)
        left = Div(_mul_of([numerator, _quotient(common, denominator)]), common)
        right = Div(_mul_of([other_numerator, _quotient(common, other_denominator)]), common)
        return left, right

    def add(self, other) -> Expr:
        """通分后相加并约分。"""
        left, right = self.common_denominator(other)
        return Div(_add_of([left.args[0], right.args[0]]), left.args[1]).reduce()

    def sub(self, other) -> Expr:
        """通分后相减并约分。"""
        left, right = self.common_denominator(other)
        numerator = _add_of([left.args[0], Mul(Integer(-1), right.args[0])])
        return Div(numerator, left.args[1]).reduce()

    def __str__(self) -> str:
        return f"{_fraction_text(self._args[0])}/{_fraction_text(self._args[1], True)}"


class Function(NaryOp):
    __slots__ = ()

    min_args = 1
    max_args = None
    function_name = "f"
    sympy_name = "f"
    precedence = 90
    is_function = True
    is_operation = False

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if "sympy_name" not in cls.__dict__:
            cls.sympy_name = cls.function_name

    @property
    def name(self) -> str:
        return self.function_name

    def to_sympy(self):
        target = getattr(sympy, self.sympy_name, None)
        if target is None:
            target = sympy.Function(self.sympy_name)
        return target(*[child.to_sympy() for child in self.args])

    def __str__(self) -> str:
        inner = ", ".join(str(child) for child in self.args)
        return f"{self.function_name}({inner})"


class UnaryFunction(Function):
    __slots__ = ()

    min_args = 1
    max_args = 1


_FUNCTION_REGISTRY: dict = {}
_SYMPY_REGISTRY: dict = {}


def _register(cls):
    _FUNCTION_REGISTRY[cls.function_name] = cls
    _SYMPY_REGISTRY[cls.sympy_name] = cls
    return cls


@_register
class Sin(UnaryFunction):
    function_name = "sin"


@_register
class Cos(UnaryFunction):
    function_name = "cos"


@_register
class Tan(UnaryFunction):
    function_name = "tan"


@_register
class Cot(UnaryFunction):
    function_name = "cot"


@_register
class Sec(UnaryFunction):
    function_name = "sec"


@_register
class Csc(UnaryFunction):
    function_name = "csc"


@_register
class Asin(UnaryFunction):
    function_name = "asin"


@_register
class Acos(UnaryFunction):
    function_name = "acos"


@_register
class Atan(UnaryFunction):
    function_name = "atan"


@_register
class Acot(UnaryFunction):
    function_name = "acot"


@_register
class Sinh(UnaryFunction):
    function_name = "sinh"


@_register
class Cosh(UnaryFunction):
    function_name = "cosh"


@_register
class Tanh(UnaryFunction):
    function_name = "tanh"


@_register
class Exp(UnaryFunction):
    function_name = "exp"


@_register
class Ln(UnaryFunction):
    function_name = "ln"
    sympy_name = "log"


@_register
class Abs(UnaryFunction):
    function_name = "abs"
    sympy_name = "Abs"


@_register
class Sign(UnaryFunction):
    function_name = "sign"


@_register
class Factorial(UnaryFunction):
    function_name = "factorial"


class Log(Function):
    __slots__ = ()

    min_args = 2
    max_args = 2
    function_name = "log"
    sympy_name = "log"


_FUNCTION_REGISTRY["log"] = Log


_GREEK_LETTERS = {
    "alpha": r"\alpha",
    "beta": r"\beta",
    "gamma": r"\gamma",
    "delta": r"\delta",
    "epsilon": r"\epsilon",
    "varepsilon": r"\varepsilon",
    "zeta": r"\zeta",
    "eta": r"\eta",
    "theta": r"\theta",
    "vartheta": r"\vartheta",
    "iota": r"\iota",
    "kappa": r"\kappa",
    "lambda": r"\lambda",
    "mu": r"\mu",
    "nu": r"\nu",
    "xi": r"\xi",
    "omicron": "o",
    "rho": r"\rho",
    "sigma": r"\sigma",
    "tau": r"\tau",
    "upsilon": r"\upsilon",
    "phi": r"\phi",
    "varphi": r"\varphi",
    "chi": r"\chi",
    "psi": r"\psi",
    "omega": r"\omega",
    "Gamma": r"\Gamma",
    "Delta": r"\Delta",
    "Theta": r"\Theta",
    "Lambda": r"\Lambda",
    "Xi": r"\Xi",
    "Pi": r"\Pi",
    "Sigma": r"\Sigma",
    "Upsilon": r"\Upsilon",
    "Phi": r"\Phi",
    "Psi": r"\Psi",
    "Omega": r"\Omega",
}

_CONSTANT_LATEX = {
    "pi": r"\pi",
    "E": "e",
    "I": "i",
    "EulerGamma": r"\gamma",
    "GoldenRatio": r"\phi",
    "Catalan": "G",
    "Infinity": r"\infty",
    "NegativeInfinity": r"-\infty",
    "ComplexInfinity": r"\tilde{\infty}",
    "NaN": r"\text{NaN}",
}

_FUNCTION_LATEX = {
    "sin": r"\sin",
    "cos": r"\cos",
    "tan": r"\tan",
    "cot": r"\cot",
    "sec": r"\sec",
    "csc": r"\csc",
    "asin": r"\arcsin",
    "acos": r"\arccos",
    "atan": r"\arctan",
    "acot": r"\operatorname{arccot}",
    "sinh": r"\sinh",
    "cosh": r"\cosh",
    "tanh": r"\tanh",
    "sign": r"\operatorname{sign}",
}


def _escape_name(name: str) -> str:
    return name.replace("_", r"\_")


def _symbol_latex(name: str) -> str:
    if name in _GREEK_LETTERS:
        return _GREEK_LETTERS[name]
    match = re.fullmatch(r"([A-Za-z]+)(?:_?([A-Za-z0-9]+))?", name)
    if match is None:
        return r"\mathrm{" + _escape_name(name) + "}"
    base, subscript = match.group(1), match.group(2)
    base_text = _GREEK_LETTERS.get(base, base)
    if subscript is None:
        return base_text
    if subscript in _GREEK_LETTERS:
        subscript_text = _GREEK_LETTERS[subscript]
    elif subscript.isdigit() or len(subscript) == 1:
        subscript_text = subscript
    else:
        subscript_text = r"\mathrm{" + subscript + "}"
    return base_text + "_{" + subscript_text + "}"


DEFAULT_DEPTH_COLORS = ("#e53935", "#2e7d32", "#1565c0", "#6a1b9a")


class LatexPrinter:
    """把表达式树打印为 LaTeX，接口与 sympy.latex 类似。

    colorize=True 时按节点深度着色（红、绿、蓝、紫循环），并为每个节点
    生成 ``l{层}-n{序号}`` 形式的 cssId，供前端点击选中。
    """

    def __init__(self, colorize: bool = False, colors=None, id_prefix: str = "") -> None:
        self.colorize = colorize
        self.colors = tuple(colors) if colors else DEFAULT_DEPTH_COLORS
        self.id_prefix = id_prefix
        self.node_info: dict = {}
        self.node_map: dict = {}
        self._depth = 0
        self._counter = 0

    def doprint(self, expr) -> str:
        self.node_info = {}
        self.node_map = {}
        self._depth = 0
        self._counter = 0
        return self._print(as_expr(expr))

    def _print(self, node: Expr) -> str:
        depth = self._depth
        self._depth += 1
        try:
            negative, text = self._print_body(node)
        finally:
            self._depth -= 1
        if negative:
            text = "- " + text
        return self._decorate(node, text, depth)

    def _print_term(self, node: Expr):
        depth = self._depth
        self._depth += 1
        try:
            negative, text = self._print_body(node)
        finally:
            self._depth -= 1
        return negative, self._decorate(node, text, depth)

    def _print_body(self, node: Expr):
        if isinstance(node, Integer):
            if node.value < 0:
                return True, str(-node.value)
            return False, str(node.value)
        if isinstance(node, Rational):
            if node.value < 0:
                return True, self._frac(str(-node.p), str(node.q))
            return False, self._frac(str(node.p), str(node.q))
        if isinstance(node, Float):
            if node.value < 0:
                return True, repr(-node.value)
            return False, repr(node.value)
        if isinstance(node, Constant) and node.name == "NegativeInfinity":
            return True, r"\infty"
        if isinstance(node, Mul):
            return self._mul_parts(node)
        if isinstance(node, Div):
            return self._div_parts(node)
        return False, self._render(node)

    def _decorate(self, node: Expr, text: str, depth: int | None = None) -> str:
        if not self.colorize:
            return text
        if depth is None:
            depth = self._depth
        layer = depth % len(self.colors)
        index = self._counter
        self._counter += 1
        node_id = f"{self.id_prefix}l{layer}-n{index}"
        parent = node.parent
        expandable = False
        if isinstance(node, Add):
            expandable = isinstance(parent, Mul) or (
                isinstance(parent, Pow)
                and isinstance(parent.exponent, Integer)
                and parent.exponent.value > 1
            )
        self.node_info[node_id] = {
            "type": type(node).__name__,
            "depth": depth,
            "color": self.colors[layer],
            "text": str(node),
            "parent": type(parent).__name__ if parent is not None else "",
            "expandable": expandable,
        }
        self.node_map[node_id] = node
        return r"\cssId{" + node_id + "}{" + text + "}"

    def _render(self, node: Expr) -> str:
        if isinstance(node, Function):
            return self._print_function(node)
        method = getattr(self, "_print_" + type(node).__name__, None)
        if method is None:
            return _escape_name(str(node))
        return method(node)

    def _paren(self, text: str) -> str:
        return r"\left(" + text + r"\right)"

    def _frac(self, numerator: str, denominator: str) -> str:
        return r"\frac{" + numerator + "}{" + denominator + "}"

    def _delimit(self, node: Expr) -> str:
        return r"\left(" + self._print(node) + r"\right)"

    def _print_Symbol(self, node: Symbol) -> str:
        return _symbol_latex(node.name)

    def _print_Constant(self, node: Constant) -> str:
        return _CONSTANT_LATEX.get(node.name, r"\mathrm{" + _escape_name(node.name) + "}")

    def _print_Add(self, node: Add) -> str:
        parts = []
        for index, term in enumerate(node.args):
            negative, body = self._print_term(term)
            if index == 0:
                parts.append(("- " if negative else "") + body)
            else:
                parts.append((" - " if negative else " + ") + body)
        return "".join(parts)

    def _print_Eq(self, node: Eq) -> str:
        return self._print(node.left) + " = " + self._print(node.right)

    def _print_Pow(self, node: Pow) -> str:
        base, exponent = node.args
        if isinstance(exponent, Integer):
            if exponent.value == 1:
                return self._base_text(base)
            if exponent.value == 0:
                return "1"
        if isinstance(exponent, Rational):
            if exponent.p == 1 and exponent.q == 2:
                return r"\sqrt{" + self._print(base) + "}"
            if exponent.p == 1 and exponent.q > 2:
                return r"\sqrt[" + str(exponent.q) + "]{" + self._print(base) + "}"
            if exponent.p == -1 and exponent.q == 2:
                return self._frac("1", r"\sqrt{" + self._print(base) + "}")
            if exponent.p == -1 and exponent.q > 2:
                return self._frac("1", r"\sqrt[" + str(exponent.q) + "]{" + self._print(base) + "}")
            if exponent.p < 0:
                power_text = self._frac(str(-exponent.p), str(exponent.q))
                inner = self._base_text(base) + "^{" + power_text + "}"
                return self._frac("1", inner)
        power = self._print(exponent)
        if (
            not self.colorize
            and isinstance(base, UnaryFunction)
            and base.function_name in _FUNCTION_LATEX
        ):
            command = _FUNCTION_LATEX[base.function_name]
            return command + "^{" + power + "}" + self._delimit(base.args[0])
        return self._base_text(base) + "^{" + power + "}"

    def _div_parts(self, node: Div):
        numerator, denominator = node.args
        if isinstance(numerator, Integer) and numerator.value == 0:
            return False, "0"
        if isinstance(denominator, Integer) and denominator.value == 1:
            return self._print_term(numerator)
        if self.colorize:
            negative, numerator_text = self._print_term(numerator)
            return negative, self._frac(numerator_text, self._print(denominator))
        negative, coefficient, factors = self._coefficient_parts(numerator)
        denominator_text = None
        if isinstance(denominator, (Integer, Rational)):
            value = Fraction(denominator.value)
            if value < 0:
                negative = not negative
                value = -value
            coefficient = coefficient / value
        else:
            denominator_text = self._print(denominator)
        numerator_text = self._number_factors(coefficient.numerator, factors)
        if coefficient.denominator != 1:
            if denominator_text is None:
                body = self._frac(numerator_text, str(coefficient.denominator))
            else:
                body = self._frac(numerator_text, str(coefficient.denominator) + " " + denominator_text)
        elif denominator_text is None:
            body = numerator_text
        else:
            body = self._frac(numerator_text, denominator_text)
        return negative, body

    def _print_function(self, node: Function) -> str:
        name = node.function_name
        args = node.args
        if name == "exp":
            exponent = self._print(args[0])
            return "e" if exponent == "1" else "e^{" + exponent + "}"
        if name == "ln":
            return r"\ln" + self._delimit(args[0])
        if name == "log":
            if len(args) == 1:
                return r"\ln" + self._delimit(args[0])
            return r"\log_{" + self._print(args[1]) + "}" + self._delimit(args[0])
        if name == "abs":
            return r"\left|" + self._print(args[0]) + r"\right|"
        if name == "factorial":
            body = self._print(args[0])
            if not isinstance(args[0], Atom):
                body = self._paren(body)
            return body + "!"
        command = _FUNCTION_LATEX.get(name)
        if command is None:
            command = r"\operatorname{" + _escape_name(name) + "}"
        if len(args) == 1:
            return command + self._delimit(args[0])
        inner = ", ".join(self._print(arg) for arg in args)
        return command + r"\left(" + inner + r"\right)"

    def _base_text(self, node: Expr) -> str:
        text = self._print(node)
        if isinstance(node, (Add, Mul, Div, Pow)):
            return self._paren(text)
        if isinstance(node, (Integer, Rational, Float)) and node.value < 0:
            return self._paren(text)
        return text

    def _factor(self, node: Expr) -> str:
        text = self._print(node)
        if isinstance(node, Add):
            return self._paren(text)
        if isinstance(node, (Integer, Rational, Float)) and node.value < 0:
            return self._paren(text)
        if not self.colorize and text.startswith("- "):
            return self._paren(text)
        return text

    def _mul_parts(self, node: Mul):
        coefficient = Fraction(1)
        numeric_nodes = []
        factors = []
        for child in node.args:
            if isinstance(child, Integer):
                coefficient *= child.value
                numeric_nodes.append(child)
            elif isinstance(child, Rational):
                coefficient *= child.value
                numeric_nodes.append(child)
            else:
                factors.append(child)
        if coefficient == 0:
            return False, "0"
        negative = coefficient < 0
        coefficient = abs(coefficient)
        coefficient_node = numeric_nodes[0] if len(numeric_nodes) == 1 else None
        parts = [self._factor(child) for child in factors]
        if coefficient.numerator != 1 or not parts:
            token = str(coefficient.numerator)
            if coefficient_node is not None:
                token = self._decorate(coefficient_node, token)
            parts.insert(0, token)
        body = " ".join(parts)
        if coefficient.denominator != 1:
            token = str(coefficient.denominator)
            if coefficient_node is not None:
                token = self._decorate(coefficient_node, token)
            body = self._frac(body, token)
        return negative, body

    def _coefficient_parts(self, node: Expr):
        coefficient = Fraction(1)
        factors = []
        for child in _factors(node):
            if isinstance(child, Integer):
                coefficient *= child.value
            elif isinstance(child, Rational):
                coefficient *= child.value
            else:
                factors.append(child)
        negative = coefficient < 0
        return negative, abs(coefficient), factors

    def _number_factors(self, number: int, factors) -> str:
        if not factors:
            return str(number)
        if len(factors) == 1 and number == 1:
            return self._print(factors[0])
        parts = []
        if number != 1:
            parts.append(str(number))
        for child in factors:
            text = self._print(child)
            if isinstance(child, Add):
                text = self._paren(text)
            parts.append(text)
        return " ".join(parts)


def latex(expr) -> str:
    """把表达式树或 SymPy 表达式转换为 LaTeX 文本。"""
    return LatexPrinter().doprint(expr)


def color_latex(expr, colors=None):
    """按节点深度着色生成 LaTeX，返回 (LaTeX, 节点信息字典)。"""
    printer = LatexPrinter(colorize=True, colors=colors)
    text = printer.doprint(expr)
    return text, printer.node_info



def _wrap(node: Expr, precedence: int) -> str:
    text = str(node)
    if node.precedence < precedence:
        return f"({text})"
    return text


def _fraction_text(node: Expr, denominator: bool = False) -> str:
    text = str(node)
    if not denominator and isinstance(node, Mul) and text.startswith("-"):
        return text
    if isinstance(node, (Add, Mul, Div, Rational)):
        return f"({text})"
    if denominator and text.startswith("-"):
        return f"({text})"
    return text


def _factors(node: Expr) -> list:
    if isinstance(node, Mul):
        result = []
        for child in node.args:
            result.extend(_factors(child))
        return result
    return [node]


def _base_exponent(factor: Expr) -> tuple:
    if isinstance(factor, Pow):
        base, exponent = factor.args
        if isinstance(exponent, Integer):
            return base, exponent.value
    return factor, 1


def _base_key(factor: Expr) -> tuple:
    base, _ = _base_exponent(factor)
    return base._key()


def _power(base: Expr, exponent: int) -> Expr:
    if exponent == 1:
        return base
    if exponent == 0:
        return Integer(1)
    return Pow(base, Integer(exponent))


def _detached(node: Expr) -> Expr:
    if node.parent is None:
        return node
    return node.copy()


def _fold_numbers(node: Expr) -> Expr:
    if node.is_atom:
        return node
    if all(item.is_number for item in node.walk("pre") if item.is_atom):
        return from_sympy(node.to_sympy())
    return node


def _mul_of(items) -> Expr:
    nodes = []
    for item in items:
        if item is None:
            continue
        if isinstance(item, Mul):
            nodes.extend(item.args)
        else:
            nodes.append(item)
    if len(nodes) > 1:
        nodes = [item for item in nodes if not (isinstance(item, Integer) and item.value == 1)]
    if not nodes:
        return Integer(1)
    if len(nodes) == 1:
        return nodes[0]
    return Mul(*nodes)


def _add_of(items) -> Expr:
    nodes = []
    for item in items:
        if item is None:
            continue
        if isinstance(item, Add):
            nodes.extend(item.args)
        else:
            nodes.append(item)
    if not nodes:
        return Integer(0)
    if len(nodes) == 1:
        return nodes[0]
    return Add(*nodes)


def _split_fraction(node: Expr) -> tuple:
    if isinstance(node, Div):
        numerator, denominator = node.args
        numerator_items, numerator_denominators = _split_fraction(numerator)
        denominator_items, denominator_numerators = _split_fraction(denominator)
        return numerator_items + denominator_numerators, numerator_denominators + denominator_items
    if isinstance(node, Mul):
        numerator_items = []
        denominator_items = []
        for child in node.args:
            items, denominators = _split_fraction(child)
            numerator_items.extend(items)
            denominator_items.extend(denominators)
        return numerator_items, denominator_items
    return [node], []


def _extract_number(factors) -> tuple:
    coefficient = Fraction(1)
    rest = []
    for factor in factors:
        if isinstance(factor, Integer):
            coefficient *= factor.value
        elif isinstance(factor, Rational):
            coefficient *= factor.value
        else:
            rest.append(factor)
    return coefficient, rest


def _factor_map(node: Expr) -> tuple:
    coefficient = Fraction(1)
    items: dict = {}
    for factor in _factors(node):
        if isinstance(factor, Integer):
            coefficient *= factor.value
            continue
        if isinstance(factor, Rational):
            coefficient *= factor.value
            continue
        base, exponent = _base_exponent(factor)
        key = base._key()
        if key in items:
            items[key][1] += exponent
        else:
            items[key] = [base, exponent]
    return coefficient, items


def _lcm(left: Fraction, right: Fraction) -> Fraction:
    if left == 0 or right == 0:
        return Fraction(0)
    left = abs(left)
    right = abs(right)
    numerator = math.lcm(left.numerator, right.numerator)
    denominator = math.gcd(left.denominator, right.denominator)
    return Fraction(numerator, denominator)


def _product(coefficient: Fraction, items) -> Expr:
    factors = []
    if coefficient != 1:
        if coefficient.denominator == 1:
            factors.append(Integer(coefficient.numerator))
        else:
            factors.append(Rational(coefficient.numerator, coefficient.denominator))
    for base, exponent in items.values():
        factors.append(_power(base, exponent))
    return _mul_of(factors)


def _common_denominator(left: Expr, right: Expr) -> Expr:
    if left == right:
        return left
    left_coefficient, left_items = _factor_map(left)
    right_coefficient, right_items = _factor_map(right)
    coefficient = _lcm(left_coefficient, right_coefficient)
    items: dict = {}
    for key, pair in left_items.items():
        items[key] = [pair[0], pair[1]]
    for key, pair in right_items.items():
        if key in items:
            items[key][1] = max(items[key][1], pair[1])
        else:
            items[key] = [pair[0], pair[1]]
    return _product(coefficient, items)


def _quotient(whole: Expr, part: Expr) -> Expr:
    whole_coefficient, whole_items = _factor_map(whole)
    part_coefficient, part_items = _factor_map(part)
    items: dict = {}
    for key, pair in whole_items.items():
        exponent = pair[1] - part_items[key][1] if key in part_items else pair[1]
        if exponent > 0:
            items[key] = [pair[0], exponent]
    return _product(whole_coefficient / part_coefficient, items)


def function(name: str, *args) -> Function:
    """按函数名创建函数节点，未注册的名称会自动生成函数类。"""
    cls = _FUNCTION_REGISTRY.get(name)
    if cls is None:
        cls = type(name.capitalize(), (Function,), {"function_name": name, "__slots__": ()})
        _register(cls)
    return cls(*args)


def as_expr(value) -> Expr:
    """把 Expr、Python 数值、字符串或 SymPy 对象转换为表达式节点。"""
    if isinstance(value, Expr):
        return value
    if isinstance(value, bool):
        raise TypeError("布尔值不能作为表达式节点")
    if isinstance(value, int):
        return Integer(value)
    if isinstance(value, Fraction):
        return Rational(value)
    if isinstance(value, float):
        return Float(value)
    if isinstance(value, str):
        return Symbol(value)
    if isinstance(value, sympy.Basic):
        return from_sympy(value)
    raise TypeError(f"无法转换为表达式节点: {type(value).__name__}")


def _build_mul(items, ordered: bool = False) -> Expr:
    coefficient = Fraction(1)
    factors = []
    for item in items:
        if isinstance(item, (sympy.Integer, sympy.Rational)):
            coefficient *= Fraction(int(item.p), int(item.q))
        else:
            factors.append(item)
    numerator = []
    denominator = []
    if coefficient != 1:
        numerator.append(Integer(coefficient.numerator))
        if coefficient.denominator != 1:
            denominator.append(Integer(coefficient.denominator))
    for item in factors:
        if isinstance(item, sympy.Pow) and isinstance(item.exp, sympy.Integer) and item.exp < 0:
            value = -int(item.exp)
            inner = item.base if value == 1 else sympy.Pow(item.base, value)
            denominator.append(_from_sympy(inner, ordered))
        else:
            numerator.append(_from_sympy(item, ordered))
    if not denominator:
        return _mul_of(numerator)
    return Div(_mul_of(numerator), _mul_of(denominator))


def _flatten_args(expr, cls) -> list:
    items = []
    for item in expr.args:
        if isinstance(item, cls):
            items.extend(_flatten_args(item, cls))
        else:
            items.append(item)
    return items


def from_sympy(expr, ordered: bool = True) -> Expr:
    """把 SymPy 表达式转换为表达式树。

    ordered=False 时沿用传入表达式的参数顺序，配合 evaluate=False 保留输入写法；
    ordered=True 时按 SymPy 的显示顺序排列，用于化简或展开后的结果。
    """
    return _from_sympy(expr, ordered)


def _from_sympy(expr, ordered: bool) -> Expr:
    if isinstance(expr, Expr):
        return expr
    if isinstance(expr, sympy.Symbol):
        return Symbol(expr.name)
    if isinstance(expr, sympy.Integer):
        return Integer(int(expr))
    if isinstance(expr, sympy.Rational):
        return Rational(int(expr.p), int(expr.q))
    if isinstance(expr, sympy.Float):
        return Float(float(expr))
    name = _CONSTANT_NAMES.get(expr) if isinstance(expr, sympy.Basic) else None
    if name is not None:
        return Constant(name)
    if expr is sympy.nan:
        return Constant("NaN")
    if isinstance(expr, sympy.Eq):
        return Eq(
            _from_sympy(expr.lhs, ordered),
            _from_sympy(expr.rhs, ordered),
        )
    if isinstance(expr, sympy.Add):
        items = expr.as_ordered_terms() if ordered else _flatten_args(expr, sympy.Add)
        nodes = [_from_sympy(item, ordered) for item in items]
        if len(nodes) == 1:
            return nodes[0]
        return Add(*nodes)
    if isinstance(expr, sympy.Mul):
        items = expr.as_ordered_factors() if ordered else _flatten_args(expr, sympy.Mul)
        return _build_mul(items, ordered)
    if isinstance(expr, sympy.Pow):
        return Pow(_from_sympy(expr.base, ordered), _from_sympy(expr.exp, ordered))
    if isinstance(expr, sympy.log):
        args = [_from_sympy(item, ordered) for item in expr.args]
        if len(args) == 1:
            return Ln(args[0])
        return Log(*args)
    if isinstance(expr, sympy.Function):
        args = [_from_sympy(item, ordered) for item in expr.args]
        cls = _SYMPY_REGISTRY.get(type(expr).__name__)
        if cls is not None and cls.min_args <= len(args) <= (cls.max_args or len(args)):
            return cls(*args)
        return function(type(expr).__name__, *args)
    raise TypeError(f"不支持的 SymPy 类型: {type(expr).__name__}")


def _strip_outer_parens(text: str) -> str:
    text = text.strip()
    while text.startswith("(") and text.endswith(")"):
        depth = 0
        closes_at_end = False
        for index, char in enumerate(text):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    closes_at_end = index == len(text) - 1
                    break
        if not closes_at_end:
            break
        text = text[1:-1].strip()
    return text


def _find_equation_equal(text: str):
    depth = 0
    found = None
    for index, char in enumerate(text):
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif char == "=" and depth == 0:
            previous = text[index - 1] if index > 0 else ""
            following = text[index + 1] if index + 1 < len(text) else ""
            if previous in "=<>!" or following == "=":
                continue
            if found is not None:
                raise ValueError("一个输入中只能包含一个等号")
            found = index
    return found


def parse_sympy(text: str, symbols=None, evaluate: bool = False):
    """把字符串解析为 SymPy 表达式（支持 ^ 与隐式乘法）。

    evaluate=False 时保留输入的括号与运算顺序，不做展开与合并。
    """
    from sympy.parsing.sympy_parser import (
        convert_xor,
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    local = {"ln": sympy.log, "log": sympy.log}
    if symbols:
        local.update(symbols)
    transformations = standard_transformations + (convert_xor, implicit_multiplication_application)

    def parse_part(part: str):
        return parse_expr(
            part,
            local_dict=local,
            transformations=transformations,
            evaluate=evaluate,
        )

    text = _strip_outer_parens(text)
    index = _find_equation_equal(text)
    if index is not None:
        left_text = text[:index].strip()
        right_text = text[index + 1:].strip()
        if not left_text or not right_text:
            raise ValueError("方程两侧都不能为空")
        return sympy.Eq(
            parse_part(left_text),
            parse_part(right_text),
            evaluate=False,
        )
    return parse_part(text)


def from_string(text: str, symbols=None, evaluate: bool = False) -> Expr:
    """解析字符串并构造表达式树。"""
    return from_sympy(parse_sympy(text, symbols, evaluate), ordered=evaluate)
