from sympy import symbols, solveset, dsolve, Function, solve, simplify
from sympy.abc import x
from sympify import sympify

def solve_fangcheng(eq, zhuyuan, domain, fs):
    # eq(sympy.core.relational.Equality):方程等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return simplify(solveset(eq, symbols(zhuyuan), sympify(domain, fs)))

def solve_weifenfangcheng(eq, zhuyuan, fs):
    # eq(sympy.core.relational.Equality):微分方程等式
    # zhuyuan(str):主元符号,默认f(x)
    # fs(dict):函数列表
    # return:解

    f = symbols("f", cls = Function)
    return simplify(dsolve(eq, f(x)))

def solve_fangchengzu(eqs, zhuyuan, fs):
    # eq(list of sympy.core.relational.Equality):方程组等式列表
    # zhuyuan(list of Symbol):主元符号列表
    # fs(dict):函数列表
    # return:解

    return simplify(solve(eqs, zhuyuan))

def solve_budengshi(rel, zhuyuan, domain, fs):
    # rel(sympy.core.relational.Relational):不等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return simplify(solveset(rel, symbols(zhuyuan), sympify(domain, fs)))

def solve_budengshizu(rels, zhuyuan, fs):
    # rels(list of sympy.core.relational.Relational):不等式列表
    # zhuyuan(Symbol):主元符号
    # fs(dict):函数列表
    # return:解集

    return simplify(solve(rels, zhuyuan))