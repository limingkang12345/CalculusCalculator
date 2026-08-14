from sympy import integrate, radsimp
from core.sympify import sympify


def integral(f, v, fs, a = None, b = None):
    # 该函数用于计算被积函数的积分并返回表达式
    # f(str):被积函数表达式
    # v(str):积分变量表达式
    # fs(dict):函数列表
    # a(str):定积分下限（None 或空字符串表示不定积分）
    # b(str):定积分上限
    # return:返回导函数表达式

    # 空字符串或 None 都视为"未指定上下限"（不定积分），避免把空串 sympify 成空符号。
    if not a and not b:
        return radsimp(integrate(sympify(f, fs), sympify(v, fs)))
    else:
        return radsimp(integrate(sympify(f, fs), (sympify(v, fs), sympify(a, fs), sympify(b, fs))))
