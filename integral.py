from sympy import integrate
from sympify import sympify


def integral(f, v, fs, a = None, b = None):
    # 该函数用于计算被积函数的积分并返回表达式
    # f(str):被积函数表达式
    # v(str):积分变量表达式
    # fs(dict):函数列表
    # a(str):定积分下限
    # b(str):定积分上限
    # return:返回导函数表达式

    if a is None and b is None:
        return integrate(sympify(f, fs), sympify(v, fs))
    else:
        return integrate(sympify(f, fs), (sympify(v, fs), sympify(a, fs), sympify(b, fs)))
