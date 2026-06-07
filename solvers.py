from sympy import symbols, solveset, dsolve, Function, solve, simplify, Eq, radsimp, pi, sin, acos, cos, sqrt, asin
from sympy.abc import x
from sympify import sympify

#该函数由AI生成
def _radsimp_safe(expr):
    # 安全应用radsimp，处理Eq、dict等不可直接应用radsimp的对象
    if isinstance(expr, Eq):
        return Eq(radsimp(expr.lhs), radsimp(expr.rhs))
    if isinstance(expr, dict):
        return {k: _radsimp_safe(v) for k, v in expr.items()}
    try:
        return radsimp(expr)
    except Exception:
        return expr

def solve_fangcheng(eq, zhuyuan, domain, fs):
    # eq(sympy.core.relational.Equality):方程等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return _radsimp_safe(simplify(solveset(eq, symbols(zhuyuan), sympify(domain, fs))))

def solve_weifenfangcheng(eq, zhuyuan, fs):
    # eq(sympy.core.relational.Equality):微分方程等式
    # zhuyuan(str):主元符号,默认f(x)
    # fs(dict):函数列表
    # return:解

    f = symbols("f", cls = Function)
    return _radsimp_safe(simplify(dsolve(eq, f(x))))

def solve_fangchengzu(eqs, zhuyuan, fs):
    # eq(list of sympy.core.relational.Equality):方程组等式列表
    # zhuyuan(list of Symbol):主元符号列表
    # fs(dict):函数列表
    # return:解
    
    result = solve(eqs, zhuyuan)
    if type(result) == type(list()):
        return [[Eq(j[0], _radsimp_safe(simplify(j[1]))) for j in zip(zhuyuan, i)] for i in result]
    else:
        return _radsimp_safe(simplify(result))

def solve_budengshi(rel, zhuyuan, domain, fs):
    # rel(sympy.core.relational.Relational):不等式
    # zhuyuan(str):主元符号
    # domain(str):主元取值范围
    # fs(dict):函数列表
    # return(sympy.sets.sets.FiniteSet):解集

    return _radsimp_safe(simplify(solveset(rel, symbols(zhuyuan), sympify(domain, fs))))

def solve_budengshizu(rels, zhuyuan, fs):
    # rels(list of sympy.core.relational.Relational):不等式列表
    # zhuyuan(Symbol):主元符号
    # fs(dict):函数列表
    # return:解集

    return _radsimp_safe(simplify(solve(rels, zhuyuan)).as_set())

def solve_sanjiaoxing(angles, sides, fs):
    # 实现解三角形相关功能
    # angles(dict):已知角
    # sides(dict):已知边
    # fs(dict):函数列表
    # return(list of list of dicts): 所有解的列表，每个解为[角度字典, 边长字典]

    def get_cos(side1, side2, side3):
        # 余弦定理之边求角
        return acos((side1**2 + side2**2 - side3**2)/(2*side1*side2))

    if len(angles) == 2:
        if list(sides.keys())[0].upper() in angles.keys():
            # 已知两角和其中一角对边
            R = list(sides.values())[0] / sin(angles[list(sides.keys())[0].upper()]) / 2
            second_side = 2 * R * sin(angles[[angle for angle in angles.keys() if list(sides.keys())[0].upper() != angle][0]])
            third_angle = pi - list(angles.values())[0] - list(angles.values())[1]
            third_side = 2 * R * sin(third_angle)
            result_angles = angles.copy()
            result_angles[[angle for angle in ["A", "B", "C"] if angle not in list(angles.keys())][0]] = third_angle
            result_sides = sides.copy()
            result_sides[[angle for angle in angles.keys() if list(sides.keys())[0].upper() != angle][0].lower()] = second_side
            result_sides[[side for side in ["a", "b", "c"] if side not in result_sides.keys()][0]] = third_side
        else:
            # 已知两角和第三边
            third_angle = pi - list(angles.values())[0] - list(angles.values())[1]
            third_side = list(sides.values())[0]
            R = third_side / sin(third_angle) / 2
            result_angles = angles.copy()
            result_angles[[angle for angle in ["A", "B", "C"] if angle not in list(angles.keys())][0]] = third_angle
            result_sides = sides.copy()
            result_sides[list(angles.keys())[0].lower()] = 2 * R * sin(list(angles.values())[0])
            result_sides[list(angles.keys())[1].lower()] = 2 * R * sin(list(angles.values())[1])
        # 单个解，包装为列表的列表，并对所有值化简
        return [[{k: simplify(v) for k, v in result_angles.items()},
                 {k: simplify(v) for k, v in result_sides.items()}]]

    elif len(angles) == 1:
        if list(angles.keys())[0].lower() in sides.keys():
            # 已知两边和其中一边对角 (SSA)
            angle_name = list(angles.keys())[0]
            opposite_side = sides[angle_name.lower()]
            other_side_name = [s for s in sides.keys() if s != angle_name.lower()][0]
            other_side = sides[other_side_name]
            angle_val = list(angles.values())[0]

            sin_other = other_side * sin(angle_val) / opposite_side
            if sin_other > 1 + 1e-12:
                return []
            if sin_other > 1:
                sin_other = 1
            if sin_other < -1e-12:
                return []

            other_angle1 = asin(sin_other)
            other_angle2 = pi - other_angle1

            solutions = []
            for other_angle in (other_angle1, other_angle2):
                if other_angle <= 0 or other_angle >= pi:
                    continue
                third_angle = pi - angle_val - other_angle
                if third_angle <= 0:
                    continue
                third_side = opposite_side * sin(third_angle) / sin(angle_val)

                result_angles = angles.copy()
                other_angle_name = other_side_name.upper()
                result_angles[other_angle_name] = other_angle
                third_angle_name = [n for n in ['A','B','C'] if n not in result_angles][0]
                result_angles[third_angle_name] = third_angle

                result_sides = sides.copy()
                third_side_name = [s for s in ['a','b','c'] if s not in result_sides][0]
                result_sides[third_side_name] = third_side

                solutions.append([{k: simplify(v) for k, v in result_angles.items()},
                                  {k: simplify(v) for k, v in result_sides.items()}])

            if len(solutions) == 2 and abs(solutions[0][0][other_angle_name] - solutions[1][0][other_angle_name]) < 1e-12:
                solutions = solutions[:1]
            return solutions
        else:
            # 已知两边和夹角 (SAS)
            third_side = sqrt(list(sides.values())[0]**2 + list(sides.values())[1]**2 - 2*list(sides.values())[0]*list(sides.values())[1]*cos(list(angles.values())[0]))
            result_sides = sides.copy()
            result_sides[list(angles.keys())[0].lower()] = third_side
            result_angles = angles.copy()
            result_angles[list(sides.keys())[0].upper()] = get_cos(list(sides.values())[1], third_side, list(sides.values())[0])
            result_angles[list(sides.keys())[1].upper()] = get_cos(list(sides.values())[0], third_side, list(sides.values())[1])
            return [[{k: simplify(v) for k, v in result_angles.items()},
                     {k: simplify(v) for k, v in result_sides.items()}]]

    elif len(angles) == 0:  
        # 已知三边 (SSS)
        result_sides = sides.copy()
        a, b, c = sides["a"], sides["b"], sides["c"]
        result_angles = {"A": get_cos(b, c, a), "B": get_cos(a, c, b), "C": get_cos(a, b, c)}
        return [[{k: simplify(v) for k, v in result_angles.items()},
                 {k: simplify(v) for k, v in result_sides.items()}]]

    else:
        # AAA
        return "无解"