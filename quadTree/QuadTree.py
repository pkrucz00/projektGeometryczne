from quadTree.QuadTreeAuxClasses import *

QUAD_0_EPSILON = 0.1

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

    def _searchWithoutConsiInclusions(self, queryRect, repPoints):
        if self.quad.isDisjointWith(queryRect):
            return
        if self.isLeaf:
            repPoints += list(filter(lambda p: queryRect.contains(p), self.points))
        else:
            self.SW._searchWithoutConsiInclusions(queryRect, repPoints)
            self.SE._searchWithoutConsiInclusions(queryRect, repPoints)
            self.NE._searchWithoutConsiInclusions(queryRect, repPoints)
            self.NW._searchWithoutConsiInclusions(queryRect, repPoints)

    def reportAllRec(self, repPoints):
        if self.isLeaf:
            repPoints += self.points
        else:
            self.SW.reportAllRec(repPoints)
            self.SE.reportAllRec(repPoints)
            self.NE.reportAllRec(repPoints)
            self.NW.reportAllRec(repPoints)

    def instantReportAll(self):
        return self.points

    def _search(self, queryRect, repPoints):
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
            self.SW._searchWithoutConsiInclusions(queryRect, repPoints)
            self.SE._searchWithoutConsiInclusions(queryRect, repPoints)
            self.NE._searchWithoutConsiInclusions(queryRect, repPoints)
            self.NW._searchWithoutConsiInclusions(queryRect, repPoints)


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

    def searchInRangeWithoutConsiIncusions(self, queryRect):
        reportedPoints = []
        self.root._searchWithoutConsiInclusions(queryRect, reportedPoints)
        return reportedPoints

    def searchInRange(self, queryRect):
        reportedPoints = []
        self.root._search(queryRect, reportedPoints)
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

    def addPoint(self, p):
        if not isinstance(p, Point):
            p = Point(p[0], p[1])
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
        removed = False
        if not isinstance(p, Point):
            p = Point(p[0], p[1])
        X, parent = self.searchLeafForPoint(p, withAdding=False, withDeleting=True)
        if p in X.points:
            X.points.remove(p)
            removed = True
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

        return removed