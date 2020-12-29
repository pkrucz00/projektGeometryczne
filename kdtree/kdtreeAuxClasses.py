class Range:
    def __init__(self, x1, x2, y1, y2):
        assert x1 <= x2 and y1 <= y2, "Points were inserted wrong way around"
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def isContainedIn(self, other):
        return other.x1 < self.x1 and self.x2 <= other.x2 \
               and other.y1 < self.y1 and self.y2 <= other.y2

    def isPointInRange(self, point):
        x, y = point
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def intersects(self, other):  # self - nodeRange (open left and upper bound), other - searchRange (closed range)
        return (self.x1 < other.x2 and other.x1 <= self.x2) and \
               (self.y1 < other.y2 and other.y1 <= self.y2)

    def returnSplit(self, axis, side, line):
        result = Range(self.x1, self.x2, self.y1, self.y2)
        if axis == 0:  # x axis
            if side == "left":
                result.x2 = line
            elif side == "right":
                result.x1 = line
        elif axis == 1:  # y axis
            if side == "left":
                result.y2 = line
            elif side == "right":
                result.y1 = line

        assert result != self, "wyjściowy podział jest taki sam jak wejściowy"
        assert result.x1 <= result.x2 and result.y1 <= result.y2, "Źle dokonany podział"

        return result

    def __str__(self):
        return f"[{self.x1}, {self.x2}]x[{self.y1}, {self.y2}]"


class LeafNode:
    def __init__(self, point):
        self.point = point


class Node:
    def __init__(self, splitCoord, left, right):
        self.splitCoord = splitCoord
        self.left = left
        self.right = right

