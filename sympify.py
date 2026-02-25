from sympy import sympify as sympify_sympy
from sympy import Symbol, simplify

def sympify(expr, fs, locals = None, is_simplify = True):
    # 用于处理输入的表达式
    # expr(str):符合Python和Sympy规范的表达式
    # fs(dict):函数字典
    # locals(dict):自变量映射
    # is_simplify(bool):是否自动化简
    # return:处理后的表达式

    origin_expr = sympify_sympy(expr, locals = locals)
    for f in fs.keys():
        if Symbol(f) in origin_expr.free_symbols:
            origin_expr = origin_expr.subs(f, sympify_sympy(fs[f][1], locals = locals))
    expr = sympify_sympy(simplify(origin_expr), locals = locals) if is_simplify else sympify_sympy(origin_expr, locals = locals)

    return expr