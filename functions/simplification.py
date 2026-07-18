from sympy import latex, symbols, solve, Eq
from sympy import simplify, expand, factor, collect, cancel, apart, trigsimp, expand_trig, powsimp, expand_power_exp, expand_log, logcombine, radsimp
from core.sympify import sympify

def simplifies(in_expr, method, zhuyuan, huanyuan, huanyuanshi, fs):
    # 该函数用于变形表达式
    # in_expr(str):表达式
    # method(int):方法编号
    # zhuyuan(str):主元符号
    # huanyuan(str):换元符号
    # huanyuanshi(str):换元式
    # fs(dict):函数列表
    # return:变形后表达式

    expr = sympify(in_expr, fs, locals = {str(i):symbols(str(i), positive = True) for i in sympify(in_expr, fs).free_symbols})
    
    if method == 0:
        return radsimp(simplify(expr))
    elif method == 1:
        return radsimp(expand(expr))
    elif method == 2:
        return radsimp(factor(expr))
    elif method == 3:
        return radsimp(collect(expr, zhuyuan))
    elif method == 4:
        return radsimp(cancel(expr))
    elif method == 5:
        return radsimp(apart(expr))
    elif method == 6:
        return radsimp(trigsimp(expr))
    elif method == 7:
        return radsimp(expand_trig(expr))
    elif method == 8:
        return radsimp(powsimp(expr))
    elif method == 9:
        return radsimp(expand_power_exp(expr))
    elif method == 10:
        expr = sympify(in_expr, fs, locals = {str(i):symbols(str(i), positive = True) for i in sympify(in_expr, fs).free_symbols}, is_simplify = False)
        return radsimp(expand_log(expr))
    elif method == 11:
        return radsimp(logcombine(expr))
    elif method == 12:
        expr = sympify(in_expr, fs)
        return radsimp(expand(expr.subs(symbols(zhuyuan), solve(Eq(symbols(huanyuan, positive = True), sympify(huanyuanshi, fs)), symbols(zhuyuan))[0])))