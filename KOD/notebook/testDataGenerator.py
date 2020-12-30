from random import uniform, randint
from math import sin, pi, cos


class TestDataGen:

    def inRect(self, n=100, x1=0, x2=10, y1=0, y2=10):
        return [(uniform(x1, x2), uniform(y1, y2)) for _ in range(n)]

    def sinus(self, n=100, x1=0, x2=10, y1=0, y2=10, lapses=1, fi=0):
        P = []
        for _ in range(n):
            x = uniform(x1, x2)
            y = sin(lapses * 2 * pi * (x - x1) / (x2 - x1) + fi) * (y2 - y1) / 2 + (y2 - y1) / 2
            P.append((x, y))
        return P

    def rectEdges(self, n=100, x1=0, x2=10, y1=0, y2=10):
        def calcNumb(S, i):
            Si = 0
            for s in S:
                if s == i:
                    Si += 1
            return Si

        pointsAffiliation = [randint(0, 3) for _ in range(n)]
        Scalc = [calcNumb(pointsAffiliation, s) for s in range(4)]

        P = [[uniform(x1, x2), y1] for _ in range(Scalc[0])] \
            + [[x1, uniform(y1, y2)] for _ in range(Scalc[1])] \
            + [[uniform(x1, x2), y2] for _ in range(Scalc[2])] \
            + [[x2, uniform(y1, y2)] for _ in range(Scalc[3])]

        return P

    def cirque(self, n=100, x=0, y=0, R=10):
        return [(cos(fi) * R + x, sin(fi) * R + y) for fi in [uniform(0, 2 * pi + 0.001) for _ in range(n)]]

    def circle(self, n=100, x=0, y=0, R=10):
        return [(cos(fi) * uniform(0, R) + x, sin(fi) * uniform(0, R) + y) for
                fi in [uniform(0, 2 * pi + 0.001) for _ in range(n)]]

    def archimedeanSpiral(self, n=500, x=0, y=0, maxR=10, lapses=5, direct=1):
        _E_ = 1.6
        if direct not in [-1, 1]:
            raise ValueError('direct must be 1 or -1')
        return [(cos(t * lapses / pi * _E_ * direct) * t + x, sin(t * lapses / pi * _E_ * direct) * t + y) for t in [uniform(0, maxR) for _ in range(n)]]

    def rectDiagonals(self, n1=50, n2=50, x1=0, x2=10, y1=0, y2=10):
        a = (y2 - y1) / (x2 - x1)
        b1 = y1 - a * x1
        b2 = y2 + a * x1
        return [(x, a * x + b1) for x in [uniform(x1, x2) for _ in range(n1)]] \
               + [(x, -a * x + b2) for x in [uniform(x1, x2) for _ in range(n2)]]

    def quadSplitLines(self, n1=50, n2=50, x1=0, x2=10, y1=0, y2=10):
        return [(uniform(x1, x2), (y2+y1)/2) for _ in range(n1)] \
                + [((x2+x1)/2, uniform(y1, y2)) for _ in range(n2)]





