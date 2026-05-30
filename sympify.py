import re
from sympy import sympify as sympify_sympy
from sympy import Symbol, simplify, radsimp

# 该函数为AI生成
def _preprocess_func_calls(expr_str, fs):
    """预处理函数调用表达式，将 f(arg) 形式替换为函数体表达式
    例如 fs={"f":["f","x**2","Reals","x"]} 时，"f(3)" 被替换为 "(3**2)"
    支持嵌套调用如 f(g(2)) 和同时使用 f(2)+f(3)
    """
    if not fs:
        return expr_str

    # 按函数名长度降序排列，避免短名称优先于长名称匹配
    func_names = sorted(fs.keys(), key=len, reverse=True)
    result = expr_str

    while True:
        # 查找最左侧的函数调用
        best_pos = len(result)
        best_func = None
        for func_name in func_names:
            pos = result.find(f"{func_name}(")
            if pos != -1 and pos < best_pos:
                best_pos = pos
                best_func = func_name

        if best_func is None:
            break

        # 查找匹配的右括号（支持嵌套括号）
        start_arg = best_pos + len(best_func) + 1
        depth = 1
        end_arg = start_arg
        while depth > 0 and end_arg < len(result):
            if result[end_arg] == '(':
                depth += 1
            elif result[end_arg] == ')':
                depth -= 1
            end_arg += 1

        if depth != 0:
            break  # 括号不匹配，跳过

        arg_str = result[start_arg:end_arg - 1]
        var_name = fs[best_func][3]
        body_str = fs[best_func][1]

        # 在函数体中将自变量替换为参数值，带 \b 避免部分匹配（如 x0 被误替换）
        expanded_body = re.sub(r'\b' + re.escape(var_name) + r'\b', f'({arg_str})', body_str)
        replacement = f'({expanded_body})'
        result = result[:best_pos] + replacement + result[end_arg:]

    return result


def sympify(expr, fs, locals = None, is_simplify = False, is_rationalize = False):
    # 用于处理输入的表达式
    # expr(str):符合Python和Sympy规范的表达式
    # fs(dict):函数字典
    # locals(dict):自变量映射
    # is_simplify(bool):是否自动化简
    # is_rationalize(bool):是否对结果执行分母有理化
    # return:处理后的表达式

    # 预处理函数调用表达式
    expr = _preprocess_func_calls(expr, fs)

    origin_expr = sympify_sympy(expr, locals = locals)
    for f in fs.keys():
        if Symbol(f) in origin_expr.free_symbols:
            origin_expr = origin_expr.subs(f, sympify_sympy(fs[f][1], locals = locals))
    result = sympify_sympy(simplify(origin_expr), locals = locals) if is_simplify else sympify_sympy(origin_expr, locals = locals)
    if is_rationalize:
        result = radsimp(result)

    return result