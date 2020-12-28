from random import uniform

QUAD_0_EPSILON = 0.1


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__) and (self.x == other.x and self.y == other.y):
            return True
        return False

    def __str__(self):
        return "(" + str(round(self.x, 3)) + ", " + str(round(self.y, 3)) + ")"

    def __repr__(self):
        return self.__str__()


class Rect:
    def __init__(self, x1=0, x2=0, y1=0, y2=0):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.mid = Point((x2 + x1) / 2, (y2 + y1) / 2)

    def normalizeToSquare(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2
        sideLength = max(x2 - x1, y2 - y1)
        if sideLength == x2 - x1:
            self.y1 -= (sideLength - (y2 - y1)) / 2
            self.y2 = y1 + sideLength
        else:
            self.x1 -= (sideLength - (x2 - x1)) / 2
            self.x2 = x1 + sideLength

        self.mid = Point((self.x2 + self.x1) / 2, (self.y2 + self.y1) / 2)


    def getListOfSides(self):
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2

        sides = [[(x1, y1), (x2, y1)],
                 [(x2, y1), (x2, y2)],
                 [(x2, y2), (x1, y2)],
                 [(x1, y2), (x1, y1)]]
        return sides

    def getSplittingLines(self):
        lines = [[(self.mid.x, self.y1), (self.mid.x, self.y2)],
                 [(self.x1, self.mid.y), (self.x2, self.mid.y)]]
        return lines

    def contains(self, p):
        return self.x1 <= p.x and p.x <= self.x2 and self.y1 <= p.y and p.y <= self.y2

    def include(self, rect):
        return self.x1 <= rect.x1 and rect.x2 <= self.x2 and self.y1 <= rect.y1 and rect.y2 <= self.y2

    def containsInner(self, p):
        return self.x1 < p.x and p.x < self.x2 and self.y1 < p.y and p.y < self.y2

    def _containsCorner(self, rect, f):
        return f(self, Point(rect.x1, rect.y1)) \
               or f(self, Point(rect.x2, rect.y1)) \
               or f(self, Point(rect.x2, rect.y2)) \
               or f(self, Point(rect.x1, rect.y2))

    def isIntersecting(self, rect):
        f = lambda r, p: r.contains(p)
        return self._containsCorner(rect, f) or rect._containsCorner(self, f)

    def isIntersectingInternally(self, rect):
        f = lambda r, p: r.containsInner(p)
        return self._containsCorner(rect, f) or rect._containsCorner(self, f)



class Quad(Rect):
    def __init__(self, x1, x2, y1, y2):
        super().__init__(x1, x2, y1, y2)



class QTNode:
    def __init__(self, quad, isLeaf=False):
        self.isLeaf = isLeaf
        self.quad = quad
        self.SW = None
        self.SE = None
        self.NE = None
        self.NW = None
        self.points = [] if isLeaf else None

    def getDepth(self):
        if self.isLeaf:
            return 1
        else:
            currDepth = 0
            currDepth = max(currDepth, self.SW.getDepth() + 1)
            currDepth = max(currDepth, self.SE.getDepth() + 1)
            currDepth = max(currDepth, self.NE.getDepth() + 1)
            currDepth = max(currDepth, self.NW.getDepth() + 1)
            return currDepth

    def _search(self, queryRect, repPoints):
        if self.isLeaf:
            for p in self.points:
                if queryRect.contains(p):
                    repPoints.append(p)
        else:
            if queryRect.isIntersecting(self.SW.quad):
                self.SW._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.SE.quad):
                self.SE._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.NE.quad):
                self.NE._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.NW.quad):
                self.NW._search(queryRect, repPoints)

    def reportAllRec(self, repPoints):
        if self.isLeaf:
            repPoints += self.points
        else:
            self.SW.reportAll(repPoints)
            self.SE.reportAll(repPoints)
            self.NE.reportAll(repPoints)
            self.NW.reportAll(repPoints)

    def instantReportAll(self):
        return self.points


    def _searchWithConsiInclusions(self, queryRect, repPoints):
        if self.isLeaf:
            for p in self.points:
                if queryRect.contains(p):
                    repPoints.append(p)
        else:
            if queryRect.isIntersecting(self.SW.quad):
                if queryRect.include(self.SW.quad):
                    rep = self.SW.instantReportAll()
                    if rep is not None:
                        repPoints += rep
                    else:
                        self.SW.reportAllRec(repPoints)
                else:
                    self.SW._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.SE.quad):
                if queryRect.include(self.SE.quad):
                    rep = self.SE.instantReportAll()
                    if rep is not None:
                        repPoints += rep
                    else:
                        self.SE.reportAllRec(repPoints)
                else:
                    self.SE._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.NE.quad):
                if queryRect.include(self.NE.quad):
                    rep = self.NE.instantReportAll()
                    if rep is not None:
                        repPoints += rep
                    else:
                        self.NE.reportAllRec(repPoints)
                else:
                    self.NE._search(queryRect, repPoints)
            if queryRect.isIntersecting(self.NW.quad):
                if queryRect.include(self.NW.quad):
                    rep = self.NW.instantReportAll()
                    if rep is not None:
                        repPoints += rep
                    else:
                        self.NW.reportAllRec(repPoints)
                else:
                    self.NW._search(queryRect, repPoints)
        pass


class QuadTree:
    def __init__(self, P=None, quad_0=None, nodeCapacity=1, eachNodeContainsPoints=False):
        if P is None and quad_0 is None:
            raise ValueError
        self.nodeCapacity = nodeCapacity
        if P is not None and len(P) > 0 and not isinstance(P[0], Point):
            P = [Point(x, y) for (x, y) in P]
        if P is None:
            P = []
        self.P = P

        if quad_0 is None:
            x1 = min(P, key=lambda p: p.x).x - QUAD_0_EPSILON
            x2 = max(P, key=lambda p: p.x).x + QUAD_0_EPSILON
            y1 = min(P, key=lambda p: p.y).y - QUAD_0_EPSILON
            y2 = max(P, key=lambda p: p.y).y + QUAD_0_EPSILON
            quad_0 = Quad(x1, x2, y1, y2)
            quad_0.normalizeToSquare()

        def constructQuadTree(quad, P):

            if len(P) <= self.nodeCapacity:
                v = QTNode(quad=quad, isLeaf=True)
                v.points = P
                return v
            else:
                quad_SW = Quad(quad.x1, quad.mid.x, quad.y1, quad.mid.y)
                quad_SE = Quad(quad.mid.x, quad.x2, quad.y1, quad.mid.y)
                quad_NE = Quad(quad.mid.x, quad.x2, quad.mid.y, quad.y2)
                quad_NW = Quad(quad.x1, quad.mid.x, quad.mid.y, quad.y2)

                P_SW = []
                P_SE = []
                P_NE = []
                P_NW = []
                for p in P:
                    if p.x <= quad.mid.x:
                        if p.y <= quad.mid.y:
                            P_SW.append(p)
                        else:
                            P_NW.append(p)
                    else:
                        if p.y <= quad.mid.y:
                            P_SE.append(p)
                        else:
                            P_NE.append(p)
                v_SW = constructQuadTree(quad_SW, P_SW)
                v_SE = constructQuadTree(quad_SE, P_SE)
                v_NE = constructQuadTree(quad_NE, P_NE)
                v_NW = constructQuadTree(quad_NW, P_NW)

                v = QTNode(quad=quad, isLeaf=False)
                if eachNodeContainsPoints:
                    v.points = P
                v.SW = v_SW
                v.SE = v_SE
                v.NE = v_NE
                v.NW = v_NW

                return v

        self.root = constructQuadTree(quad=quad_0, P=P)

    def calculateDepth(self):
        return self.root.getDepth()

    def searchInRange(self, queryRect):
        reportedPoints = []
        self.root._search(queryRect, reportedPoints)
        return reportedPoints

    def searchInRangeWithConsiInclusions(self, queryRect):
        reportedPoints = []
        self.root._searchWithConsiInclusions(queryRect, reportedPoints)
        return reportedPoints


if __name__ == '__main__':
    m = 0
    M = 10
    n = 25
    P = [Point(uniform(m, M), uniform(m, M)) for _ in range(n)]
    qt = QuadTree(P=P)
    queryRect = Rect(1, 2, 3, 4)
    print(qt.searchInRange(queryRect))

    pass
