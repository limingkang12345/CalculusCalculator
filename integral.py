from sympy import integrate, latex, sympify

def integral(f, v, a = None, b = None):
    # 该函数用于计算被积函数的积分并返回Latex表达式
    # f(str):被积函数表达式
    # v(str):积分变量表达式
    # a(str):定积分下限
    # b(str):定积分上限
    # return(str):返回导函数Latex表达式

    if a is None and b is None:
        return latex(integrate(sympify(f), sympify(v)))
    else:
        return latex(integrate(sympify(f), (sympify(v), sympify(a), sympify(b))))
