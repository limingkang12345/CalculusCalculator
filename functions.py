from sympy import sympify, diff, solveset, Rel, symbols, maximum, minimum, Interval, Intersection, oo, imageset, Lambda, periodicity
from sympy.calculus.util import function_range

def frange(f, s, d, is_increase):
    # 求出给定函数的值域
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # return:函数值域

    return function_range(sympify(f), symbols(s), domain = sympify(d))

def monotonic_interval(f, s, d, is_increase):
    # 求出给定函数的单调区间
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # is_increase(bool):是否求单调递增区间，否则为单调递减区间
    # return:函数单调递增区间或单调递减区间

    return solveset(Rel(diff(sympify(f)), 0, ">"), symbols(s), domain = sympify(d)) if is_increase \
        else solveset(Rel(diff(sympify(f)), 0, "<"), symbols(s), domain = sympify(d))

def odd_or_even(f, s, d, arg):
    # 求出给定函数的奇偶性
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # arg(None):占位参数
    # return:函数奇偶性

    if Intersection(Interval.open(-oo,0),sympify(d)).symmetric_difference( \
        imageset(Lambda(sympify(s),-sympify(s)), Intersection(Interval.open(0,oo),sympify(d)))).is_empty:  # 判断定义域是否关于0对称
        if sympify(f).equals(0):  # 判断f(x) = 0
            return "既奇又偶函数"
        elif sympify(f).equals(-(sympify(f).subs(symbols(s), -symbols(s)))):  # 判断f(x) = -f(-x)
            return "奇函数"
        elif sympify(f).equals(sympify(f).subs(symbols(s), -symbols(s))):  # 判断f(x) = f(-x)
            return "偶函数"
        else:
            return "非奇非偶函数"
    else:
        return "非奇非偶函数"

def period(f, s, d, arg):
    # 求出给定函数的周期
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # arg(None):占位参数
    # return:函数周期

    p = periodicity(sympify(f), symbols(s))

    try:
        if sympify(d).sup == oo:
            return p if p is not None else "该函数无周期"
        elif sympify(d).sup != oo and sympify(d) == -oo:
            return -p if p is not None else "该函数无周期"
        else:
            return "该函数无周期"
    except:
        return "该函数无周期"

def mvalues(f, s, d, is_max):
    # 求出给定函数的最值
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # is_max(bool):是否求最大值，否则为最小值
    # return:函数最大值或最小值

    return maximum(sympify(f), symbols(s), domain = sympify(d)) if is_max \
        else minimum(sympify(f), symbols(s), domain = sympify(d))

def get_function_attr(f, s, d, attr):
    # 调用上述函数
    # f(str):函数表达式
    # s(str):自变量符号
    # d(str):定义域
    # attr(int):表示要求的函数属性种类
    # return:返回函数属性

    attrs = [[frange, None], [monotonic_interval, True], [monotonic_interval, False], [odd_or_even, None], \
        [period, None], [mvalues, True], [mvalues, False]]

    return attrs[attr - 1][0](f, s, d, attrs[attr - 1][1]) if attr != 0 else (sympify(f), sympify(d))
