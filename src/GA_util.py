import numpy as np
import src.problem.SCH  as SCH
import src.problem.ZDT1 as ZDT1
import src.problem.ZDT2 as ZDT2
import src.problem.ZDT4 as ZDT4

'''
遗传算法的一些辅助操作
'''
# 交叉率
c_rate = 0.8
# 突变了
m_rate = 0.2
# 测试函数/基于你自己的应用修改
test_fun = ZDT4
# 个体/class Individual 对象
idv = None


def cross(p1, p2):
    # p1 tp p2
    if np.random.rand() < c_rate:
        p2 = idv.reset_one(p2)
        r1 = 0.7
        r2 = 1 - r1
        x1 = r1 * p1.X + r2 * p2.X
        x2 = r2 * p1.X + r1 * p2.X
        p1.X = x1
        p2.X = x2
        p2.F_value = test_fun.Func(p2.X)
        p1.F_value = test_fun.Func(p1.X)
    return p2


def mutate(p):
    # 对p节点变异
    gen_len = len(p.X)
    if np.random.rand() < m_rate:
        p = idv.reset_one(p)
        # 变异5%的基因对
        for l in range(int(gen_len * 0.1)):
            j = np.random.randint(0, gen_len, size=1)[0]
            d = np.random.randint(0, gen_len, size=1)[0]
            p.X[j], p.X[d] = p.X[d], p.X[j]
            p.F_value = test_fun.Func(p.X)
    return p


def select(P):
    # 洗牌产生新P
    new_P = []
    for ip in P:
        if ip.p_rank <= 3:
            new_P.append(ip)
    while len(new_P) != len(P):
        p = idv.creat_one()
        new_P.append(p)
    return P
