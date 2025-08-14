from sympy import diff, idiff, latex, sympify, solve, Eq

def derivative(f, v, n, x):
    # 该函数用于计算显函数的导函数并返回Latex表达式
    # f(str):原函数(显函数)表达式
    # v(str):自变量表达式
    # n(str):求导次数
    # x(str):自变量的值
    # return(str):返回导函数Latex表达式

    if x is None:
        return latex(diff(sympify(f), sympify(v), int(n)))
    else:
        return latex(diff(sympify(f), sympify(v), int(n)).subs(sympify(v), sympify(x)))

def yinhanshu_derivative(f, v1, v2, n, x):
    # 该函数用于计算隐函数的导函数并返回Latex表达式
    # f(str):原函数(隐函数)表达式(值等于0)
    # v1(str):自变量表达式
    # v2(str):因变量表达式
    # n(str):求导次数
    # x(str):自变量的值
    # return(str):返回导函数Latex表达式

    if x is None:
        return latex(idiff(sympify(f), sympify(v2), sympify(v1), int(n)))
    else:
        return latex(idiff(sympify(f), sympify(v2), sympify(v1), int(n)).subs(sympify(v1), sympify(x)).subs(sympify(v2), solve(Eq(sympify(f).subs(sympify(v1), sympify(x)), 0), sympify(v2))[0]))