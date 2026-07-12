from sympy import diff, idiff, solve, Eq, radsimp
from core.sympify import sympify


def derivative(f, v, n, x, fs):
    # 该函数用于计算显函数的导函数并返回Latex表达式
    # f(str):原函数(显函数)表达式
    # v(str):自变量表达式
    # n(str):求导次数
    # x(str):自变量的值
    # fs(dict):函数列表
    # return:返回导函数表达式

    if x is None:
        return radsimp(diff(sympify(f, fs), sympify(v, fs), int(n)))
    else:
        return radsimp(diff(sympify(f, fs), sympify(v, fs), int(n)).subs(sympify(v, fs), sympify(x, fs)))

def yinhanshu_derivative(f, v1, v2, n, x, fs):
    # 该函数用于计算隐函数的导函数并返回Latex表达式
    # f(str):原函数(隐函数)表达式(值等于0)
    # v1(str):自变量表达式
    # v2(str):因变量表达式
    # n(str):求导次数
    # x(str):自变量的值
    # fs(dict):函数列表
    # return:返回导函数表达式

    if x is None:
        return radsimp(idiff(sympify(f, fs), sympify(v2, fs), sympify(v1, fs), int(n)))
    else:
        return radsimp(idiff(sympify(f, fs), sympify(v2, fs), sympify(v1, fs), int(n)).subs(sympify(v1, fs), sympify(x, fs)).subs(sympify(v2, fs), \
            solve(Eq(sympify(f, fs).subs(sympify(v1, fs), sympify(x, fs)), 0), sympify(v2, fs))[0]))
