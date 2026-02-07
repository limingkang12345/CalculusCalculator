from sympy import integrate, latex, sympify
from sympy import simplify, expand, factor, collect, cancel, apart, trigsimp, expand_trig, powsimp, expand_power_exp, expand_log, logcombine


def simplifies(in_expr, method):
    # 该函数用于变形表达式
    # in_expr(str):表达式
    # method(int):方法编号
    # return(str):变形后表达式

    expr = sympify(in_expr)
    if method == 0:
        return simplify(expr)
    elif method == 1:
        return expand(expr)
    elif method == 2:
        return factor(expr)
    elif method == 3:
        return collect(expr, "x")
    elif method == 4:
        return cancel(expr)
    elif method == 5:
        return apart(expr)
    elif method == 6:
        return trigsimp(expr)
    elif method == 7:
        return expand_trig(expr)
    elif method == 8:
        return powsimp(expr)
    elif method == 9:
        return expand_power_exp(expr)
    elif method == 10:
        return expand_log(expr)
    elif method == 11:
        return logcombine(expr)