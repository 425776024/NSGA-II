from src.Individual import *
from src.GA_util import *


class Population:
    pop_size = 100

    idv = Individual()

    def __init__(self):
        pass

    def creat_pop(self):
        P = []
        for i in range(self.pop_size):
            P.append(self.idv.creat_one())
        return P

    def next_Pop(self, Pop):
        n_P = []
        idv = self.idv
        P = Pop
        p_size = len(P)
        for p in P:
            p = idv.reset_one(p)
            cp = idv.creat_one()
            cp.X[:] = p.X[:]
            cp.F_value[:] = p.F_value[:]
            n_P.append(cp)
        # 产生下一代
        select(n_P)
        for i in range(p_size):
            j = np.random.randint(0, p_size, size=1)[0]
            cross(n_P[i], n_P[j])
            n_P[j] = mutate(n_P[j])
        return n_P
