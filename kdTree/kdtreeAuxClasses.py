class Range:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.__coordValidation()

    def isContainedIn(self, other):
        return other.x1 < self.x1 and self.x2 <= other.x2 \
               and other.y1 < self.y1 and self.y2 <= other.y2

    def isPointInRange(self, point):
        x, y = point
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def intersects(self, other):  # self - nodeRange (open left and upper bound), other - searchRange (closed range)
        return (self.x1 < other.x2 and other.x1 <= self.x2) and \
               (self.y1 < other.y2 and other.y1 <= self.y2)

    def returnSplit(self, axis, line):
        resultLeft, resultRight = self.__copy__(), self.__copy__()
        if axis == 0:  # x axis
            resultLeft.x2 = line
            resultRight.x1 = line
        elif axis == 1:  # y axis
            resultLeft.y2 = line
            resultRight.y1 = line

        assert resultLeft != self and resultRight != self, "output range is the same as the input"
        resultLeft.__coordValidation()
        resultRight.__coordValidation()

        return resultLeft, resultRight

    def __str__(self):
        return f"[{self.x1}, {self.x2}]x[{self.y1}, {self.y2}]"

    def __copy__(self):
        return Range(self.x1, self.x2, self.y1, self.y2)

    def __coordValidation(self):
        assert self.x1 <= self.x2 and self.y1 <= self.y2, str(self) + "had points inserted wrong way around"


class LeafNode:
    def __init__(self, point):
        self.point = point


class Node:
    def __init__(self, splitCoord, left, right):
        self.splitCoord = splitCoord
        self.left = left
        self.right = right
