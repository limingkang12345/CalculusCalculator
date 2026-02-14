from sympy import symbols, sympify,  solveset

def solve_fangcheng(eq, zhuyuan, domain):
    # eq(sympy.core.relational.Equality):方程等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # return(sympy.sets.sets.FiniteSet):解集

    return solveset(eq, symbols(zhuyuan), sympify(domain))

def solve_budengshi(rel, zhuyuan, domain):
    # rel(sympy.core.relational.Relational):不等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # return(sympy.sets.sets.FiniteSet):解集

    return solveset(rel, symbols(zhuyuan), sympify(domain))