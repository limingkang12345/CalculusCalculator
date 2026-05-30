from sympy import symbols, solveset, dsolve, Function, solve, simplify, Eq, radsimp
from sympy.abc import x
from sympify import sympify

#该函数由AI生成
def _radsimp_safe(expr):
    # 安全应用radsimp，处理Eq、dict等不可直接应用radsimp的对象
    if isinstance(expr, Eq):
        return Eq(radsimp(expr.lhs), radsimp(expr.rhs))
    if isinstance(expr, dict):
        return {k: _radsimp_safe(v) for k, v in expr.items()}
    try:
        return radsimp(expr)
    except Exception:
        return expr

def solve_fangcheng(eq, zhuyuan, domain, fs):
    # eq(sympy.core.relational.Equality):方程等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return _radsimp_safe(simplify(solveset(eq, symbols(zhuyuan), sympify(domain, fs))))

def solve_weifenfangcheng(eq, zhuyuan, fs):
    # eq(sympy.core.relational.Equality):微分方程等式
    # zhuyuan(str):主元符号,默认f(x)
    # fs(dict):函数列表
    # return:解

    f = symbols("f", cls = Function)
    return _radsimp_safe(simplify(dsolve(eq, f(x))))

def solve_fangchengzu(eqs, zhuyuan, fs):
    # eq(list of sympy.core.relational.Equality):方程组等式列表
    # zhuyuan(list of Symbol):主元符号列表
    # fs(dict):函数列表
    # return:解
    
    result = solve(eqs, zhuyuan)
    if type(result) == type(list()):
        return [[Eq(j[0], _radsimp_safe(simplify(j[1]))) for j in zip(zhuyuan, i)] for i in result]
    else:
        return _radsimp_safe(simplify(result))

def solve_budengshi(rel, zhuyuan, domain, fs):
    # rel(sympy.core.relational.Relational):不等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return _radsimp_safe(simplify(solveset(rel, symbols(zhuyuan), sympify(domain, fs))))

def solve_budengshizu(rels, zhuyuan, fs):
    # rels(list of sympy.core.relational.Relational):不等式列表
    # zhuyuan(Symbol):主元符号
    # fs(dict):函数列表
    # return:解集

    return _radsimp_safe(simplify(solve(rels, zhuyuan)).as_set())