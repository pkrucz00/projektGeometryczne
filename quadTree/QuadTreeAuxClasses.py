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
