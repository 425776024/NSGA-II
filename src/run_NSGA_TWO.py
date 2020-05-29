from src.Populations import *
import src.GA_util as ga
from src.Individual import *
import matplotlib.pyplot as plt


class NSGA_II:
    # 进化轮数
    max_evo = 50
    # 支配前沿
    pareto_f = []
    # 种群数组
    Pop = []
    # 对Pop进化一代，组成下一代Qt
    Qt = []
    # Pop+Qt后去支配排序的
    Rt = []
    # 种群操作类
    populations = None

    def __init__(self):
        self.populations = Population()
        ga.idv = Individual()

    def fast_nodominate_sort(self, P):
        # 快速非支配排序
        F = []
        i = 1
        F1 = self.cpt_F1_dominate(P)
        while len(F1) != 0:
            F.append(F1)
            Q = []
            for pi in F1:
                p = P[pi]
                for q in p.Sp:
                    one_q = P[q]
                    one_q.Np = one_q.Np - 1
                    if one_q.Np == 0:
                        one_q.p_rank = i + 1
                        Q.append(q)
            i = i + 1
            F1 = Q
        return F

    def cpt_F1_dominate(self, P):
        # 计算更新种群支配关系
        F1 = []
        for j, p in enumerate(P):
            for i, q in enumerate(P):
                if j != i:
                    if self.is_dominate(p, q):
                        if i not in p.Sp:
                            p.Sp.append(i)
                    elif self.is_dominate(q, p):
                        p.Np = p.Np + 1
            if p.Np == 0:
                p.p_rank = 1
                F1.append(j)
        return F1

    def is_dominate(self, a, b):
        # a是否支配b
        a_f = a.F_value
        b_f = b.F_value
        i = 0
        for av, bv in zip(a_f, b_f):
            if av < bv:
                i = i + 1
            if av > bv:
                return False
        if i != 0:
            return True
        return False

    def crowding_dist(self, Fi):
        # 拥挤度计算,只计算P内Fi位置部分的拥挤度
        f_max = Fi[0].F_value[:]
        f_min = Fi[0].F_value[:]
        f_num = len(f_max)
        for p in Fi:
            p.dp = 0
            for fm in range(f_num):
                if p.F_value[fm] > f_max[fm]:
                    f_max[fm] = p.F_value[fm]
                if p.F_value[fm] < f_min[fm]:
                    f_min[fm] = p.F_value[fm]
        Fi_len = len(Fi)
        for m in range(f_num):
            Fi = self.sort_func(Fi, m)
            Fi[0].dp = 1000000
            Fi[Fi_len - 1].dp = 1000000
            for f in range(1, Fi_len - 1):
                a = Fi[f + 1].F_value[m] - Fi[f - 1].F_value[m]
                b = f_max[m] - f_min[m]
                Fi[f].dp = Fi[f].dp + a / b

    def sort_func(self, Fi, m):
        # 对P中Fi索引对应的个体按照第m个函数排序
        FL = len(Fi)
        for i in range(FL - 1):
            p = Fi[i]
            for j in range(i + 1, FL):
                q = Fi[j]
                if p != q and p.F_value[m] > q.F_value[m]:
                    Fi[i], Fi[j] = Fi[j], Fi[i]
        return Fi

    def inv_append(self, idx, P, to):
        # 把P中idx的索引的添加到to中去
        for i in idx:
            to.append(P[i])

    def run(self):
        # Pt，Qt父子代种群集,ndarray
        gen = 0
        while gen < self.max_evo:
            gen += 1
            # Rt：前面种群+前面种群进化一轮后的总的个体
            self.Rt = []
            # 前面种群self.Pop进化一轮，变成新种群self.Qt
            self.Qt = self.populations.next_Pop(self.Pop)
            # 全部合并到self.Rt
            self.append(self.Pop, self.Rt)
            self.append(self.Qt, self.Rt)
            # 找到前沿层F1,F2,....
            F = self.fast_nodominate_sort(self.Rt)
            # pareto前沿
            self.pareto_f = []
            # self.Rt中的第0层（F[0]）（pareto前沿层），放到self.pareto_f
            self.inv_append(F[0], self.Rt, self.pareto_f)
            print('%s th pareto len %s:' % (gen, len(F[0])))
            Pt_next = []
            i = 0
            # 保留前沿层最好的popsize个，组成下一代种群Pt_next
            while (len(Pt_next) + len(F[i])) <= self.populations.pop_size:
                self.inv_append(F[i], self.Rt, Pt_next)
                i += 1

            Fi = []
            # 把最后一层加上来。管它先排个位置
            self.inv_append(F[i], self.Rt, Fi)
            for ip in Fi:
                Pt_next.append(ip)
            # 你们上面随便排位置，反正我最后只取前pop_size个组成下一代
            Pt_next = Pt_next[0:self.populations.pop_size]
            self.Pop = Pt_next

    def append(self, fro, to):
        # 添加函数
        for i in range(len(fro)):
            to.append(fro[i])

    def draw(self):

        pf1_data = []
        pf2_data = []

        for p in self.pareto_f:
            pf1_data.append(p.F_value[0])
            pf2_data.append(p.F_value[1])
        f1_data = []
        f2_data = []
        for a in self.Rt:
            f1_data.append(a.F_value[0])
            f2_data.append(a.F_value[1])
        plt.xlabel('Function 1', fontsize=15)
        plt.ylabel('Function 2', fontsize=15)
        plt.title('ZDT4')

        plt.scatter(f1_data, f2_data, c='black', s=5)
        plt.scatter(pf1_data, pf2_data, c='red', s=10)
        plt.show()


def main():
    nsga_II = NSGA_II()
    nsga_II.Pop = nsga_II.populations.creat_pop()
    nsga_II.run()
    nsga_II.draw()


if __name__ == '__main__':
    main()
