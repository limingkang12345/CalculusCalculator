from sympy import diff, solveset, Rel, symbols, maximum, minimum, Interval, Intersection, oo, imageset, Lambda, periodicity, simplify, radsimp
from sympy.calculus.util import function_range
from sympify import sympify

def frange(f, s, d, is_increase, fs):
    # 求出给定函数的值域
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # fs(dict):函数列表
    # return:函数值域

    return function_range(sympify(f, fs), symbols(s), domain = sympify(d, fs))

def monotonic_interval(f, s, d, is_increase, fs):
    # 求出给定函数的单调区间
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # is_increase(bool):是否求单调递增区间，否则为单调递减区间
    # fs(dict):函数列表
    # return:函数单调递增区间或单调递减区间

    return solveset(Rel(diff(sympify(f, fs)), 0, ">"), symbols(s), domain = sympify(d, fs)) if is_increase \
        else solveset(Rel(diff(sympify(f, fs)), 0, "<"), symbols(s), domain = sympify(d, fs))

def odd_or_even(f, s, d, arg, fs):
    # 求出给定函数的奇偶性
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # arg(None):占位参数
    # fs(dict):函数列表
    # return:函数奇偶性

    if Intersection(Interval.open(-oo,0),sympify(d, fs)).symmetric_difference( \
        imageset(Lambda(sympify(s, fs),-sympify(s, fs)), Intersection(Interval.open(0,oo),sympify(d, fs)))).is_empty:  # 判断定义域是否关于0对称
        if sympify(f, fs).equals(0):  # 判断f(x) = 0
            return "既奇又偶函数"
        elif sympify(f, fs).equals(-(sympify(f, fs).subs(symbols(s), -symbols(s)))):  # 判断f(x) = -f(-x)
            return "奇函数"
        elif sympify(f, fs).equals(sympify(f, fs).subs(symbols(s), -symbols(s))):  # 判断f(x) = f(-x)
            return "偶函数"
        else:
            return "非奇非偶函数"
    else:
        return "非奇非偶函数"

def period(f, s, d, arg, fs):
    # 求出给定函数的周期
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # arg(None):占位参数
    # fs(dict):函数列表
    # return:函数周期

    p = periodicity(sympify(f, fs), symbols(s))

    try:
        if sympify(d, fs).sup == oo:
            return p if p is not None else "该函数无周期"
        elif sympify(d, fs).sup != oo and sympify(d, fs) == -oo:
            return -p if p is not None else "该函数无周期"
        else:
            return "该函数无周期"
    except:
        return "该函数无周期"

def mvalues(f, s, d, is_max, fs):
    # 求出给定函数的最值
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # is_max(bool):是否求最大值，否则为最小值
    # fs(dict):函数列表
    # return:函数最大值或最小值

    return maximum(sympify(f, fs), symbols(s), domain = sympify(d, fs)) if is_max \
        else minimum(sympify(f, fs), symbols(s), domain = sympify(d, fs))

def get_function_attr(f, s, d, attr, fs):
    # 调用上述函数
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # attr(int):表示要求的函数属性种类
    # fs(dict):函数列表
    # return:返回函数属性

    attrs = [[frange, None], [monotonic_interval, True], [monotonic_interval, False], [odd_or_even, None], \
        [period, None], [mvalues, True], [mvalues, False]]

    return simplify(attrs[attr - 1][0](f, s, d, attrs[attr - 1][1], fs)) if attr != 0 else (radsimp(sympify(f, fs)), sympify(d, fs))
