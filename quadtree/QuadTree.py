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

    def __hash__(self):
        return hash((self.x, self.y))


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
        return ((self.x1 <= rect.x1 and rect.x1 <= self.x2) or (self.x1 <= rect.x2 and rect.x2 <= self.x2)) \
               and ((self.y1 <= rect.y1 and rect.y1 <= self.y2) or (self.y1 <= rect.y2 and rect.y2 <= self.y2))

    def isDisjointWith(self, rect):
        return self.x2 < rect.x1 or rect.x2 < self.x1 or self.y2 < rect.y1 or rect.y2 < self.y1

    def isIntersectingInternally(self, rect):
        f = lambda r, p: r.containsInner(p)
        return self._containsCorner(rect, f) or rect._containsCorner(self, f)

    def __str__(self):
        return "rect(" + str(round(self.x1, 3)) + ", " + str(round(self.x2, 3)) + ", " + str(round(self.y1, 3)) + ", " + str(round(self.y2, 3)) + ")"

    def __repr__(self):
        return self.__str__()

class Quad(Rect):
    def __init__(self, x1, x2, y1, y2):
        super().__init__(x1, x2, y1, y2)


class QTNode:
    def __init__(self, quad, isLeaf=False, points=None):
        self.isLeaf = isLeaf
        self.quad = quad
        self.SW = None
        self.SE = None
        self.NE = None
        self.NW = None
        self.points = [] if isLeaf else None
        if points:
            self.points = points

    def splitQTNode(self, P, nodeCapacity, nodeContainsPoints=False):

        if len(P) <= nodeCapacity:
            self.points = P
            self.isLeaf = True
            return
        else:
            self.isLeaf = False
            if nodeContainsPoints:
                self.points = P
            else:
                self.points = None
            quad = self.quad
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
            v_SW = QTNode(quad_SW)
            v_SE = QTNode(quad_SE)
            v_NE = QTNode(quad_NE)
            v_NW = QTNode(quad_NW)

            self.SW = v_SW
            self.SE = v_SE
            self.NE = v_NE
            self.NW = v_NW

            self.SW.splitQTNode(P_SW, nodeCapacity, nodeContainsPoints)
            self.SE.splitQTNode(P_SE, nodeCapacity, nodeContainsPoints)
            self.NE.splitQTNode(P_NE, nodeCapacity, nodeContainsPoints)
            self.NW.splitQTNode(P_NW, nodeCapacity, nodeContainsPoints)

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
        if self.quad.isDisjointWith(queryRect):
            return
        if self.isLeaf:
            repPoints += list(filter(lambda p: queryRect.contains(p), self.points))
        else:
            self.SW._search(queryRect, repPoints)
            self.SE._search(queryRect, repPoints)
            self.NE._search(queryRect, repPoints)
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
        if self.quad.isDisjointWith(queryRect):
            return
        if queryRect.include(self.quad):
            rep = self.instantReportAll()
            if rep is not None:
                repPoints += rep
            else:
                self.reportAllRec(repPoints)
            return
        if self.isLeaf:
            repPoints += list(filter(lambda p: queryRect.contains(p), self.points))
        else:
            self.SW._search(queryRect, repPoints)
            self.SE._search(queryRect, repPoints)
            self.NE._search(queryRect, repPoints)
            self.NW._search(queryRect, repPoints)


class QuadTree:
    def __init__(self, P=None, quad_0=None, nodeCapacity=1, eachNodeContainsPoints=False, allowDuplicate=False):
        if (not P or len(P) < 2) and quad_0 is None:
            raise ValueError('no points no quad => no tree')
        self.nodeCapacity = nodeCapacity
        self.eachNodeContainsPoints = eachNodeContainsPoints
        self.allowDuplicate = allowDuplicate

        if P is not None and len(P) > 0 and not isinstance(P[0], Point):
            P = [Point(x, y) for (x, y) in P]
        if P is None:
            P = []
        if not allowDuplicate:
            P = list(set(P))
        self.P = P

        if quad_0 is None:
            x1 = min(P, key=lambda p: p.x).x - QUAD_0_EPSILON
            x2 = max(P, key=lambda p: p.x).x + QUAD_0_EPSILON
            y1 = min(P, key=lambda p: p.y).y - QUAD_0_EPSILON
            y2 = max(P, key=lambda p: p.y).y + QUAD_0_EPSILON
            quad_0 = Quad(x1, x2, y1, y2)
            quad_0.normalizeToSquare()

        self.root = QTNode(quad=quad_0)
        self.root.splitQTNode(P, nodeCapacity=nodeCapacity, nodeContainsPoints=eachNodeContainsPoints)

    def getDepth(self):
        return self.root.getDepth()

    def searchInRange(self, queryRect):
        reportedPoints = []
        self.root._search(queryRect, reportedPoints)
        return reportedPoints

    def searchInRangeWithConsiInclusions(self, queryRect):
        reportedPoints = []
        self.root._searchWithConsiInclusions(queryRect, reportedPoints)
        return reportedPoints

    def searchLeafForPoint(self, p: Point, withAdding=True, withDeleting=False):
        if withAdding and withDeleting:
            raise ValueError('It is not allowed to add and delete point during traversing')
        parent = None
        X = self.root
        while not X.isLeaf:
            parent = X
            if self.eachNodeContainsPoints:
                if withAdding and (p not in X.points or self.allowDuplicate):
                    X.points.append(p)
                if withDeleting:
                    if p in X.points:
                        X.points.remove(p)

            if p.x <= X.quad.mid.x:
                if p.y <= X.quad.mid.y:
                    X = X.SW
                else:
                    X = X.NW
            else:
                if p.y <= X.quad.mid.y:
                    X = X.SE
                else:
                    X = X.NE
        return X, parent

    def addPoint(self, p: Point):
        if not self.root.quad.contains(p):
            raise ValueError('Point being added must belong to root\'s quad')

        X, _ = self.searchLeafForPoint(p)

        if not (p not in X.points or self.allowDuplicate):
            return False
        X.points.append(p)
        self.P.append(p)
        if len(X.points) > self.nodeCapacity:
            X.splitQTNode(X.points, nodeCapacity=self.nodeCapacity, nodeContainsPoints=self.eachNodeContainsPoints)

        return True

    def deletePoint(self, p):
        X, parent = self.searchLeafForPoint(p, withAdding=False, withDeleting=True)
        if p in X.points:
            X.points.remove(p)
        if p in self.P:
            self.P.remove(p)
        if parent is not None:
            P = parent.SW.points + parent.SE.points + parent.NE.points + parent.NW.points
            if len(P) <= self.nodeCapacity:
                del parent.SW
                del parent.SE
                del parent.NE
                del parent.NW
                parent.SW = None
                parent.SE = None
                parent.NE = None
                parent.NW = None
                parent.isLeaf = True
                parent.points = P


if __name__ == '__main__':
    P = [Point(1, 1), Point(1, 2), Point(1, 1)]
    print(P)
    print(list(set(P)))

