'''
种群个体部分，抽象成类
'''
import src.GA_util as ga


class Individual:
    Np = 0  # 支配当前个体的数量
    Sp = []  # 当前个体支配的个体集（所在种群编号）
    p_rank = 0  # 当前的序
    dp = 0  # 拥挤度
    # 个体的向量，（解）
    X = []
    # X解在函数中的值。2目标就是[a,b]
    F_value = []
    # 测试函数
    test_func = ga.test_fun

    def __init__(self):
        pass

    def creat_one(self):
        # 创建一个个体
        one = Individual()
        one.Np = 0
        one.Sp = []
        one.p_rank = 0
        one.dp = 0
        # 测试函数的边界，如果多个目标边界不一样，可以缩放成一样or,从写这些创建、突变、交叉等需要用到test_fun.bound的地方
        one.X = ga.test_fun.bound[0] + (ga.test_fun.bound[1] - ga.test_fun.bound[0]) * ga.np.random.rand(
            self.test_func.dimention)
        # 设置个体的函数值
        one.F_value = ga.test_fun.Func(one.X)
        return one

    def reset_one(self, one):
        # 重制这个个体
        one.Np = 0
        one.Sp = []
        one.p_rank = 0
        one.dp = 0
        return one
