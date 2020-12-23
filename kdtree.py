from math import ceil


class Range:
    def __init__(self, x1, y1, x2, y2):
        assert x1 <= x2 and y1 <= y2, "Stary, wstawiłeś punkty na odwrót, weź co z tym zrób, brachu"
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def isContainedIn(self, other):
        return other.x1 < self.x1 and self.x2 <= other.x2 \
               and other.y1 < self.y1 and self.y2 <= other.y2

    def isPointInRange(self, point):
        x, y = point
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def intersects(self, other):
        pass

    def returnSplit(self, axis, side, line):
        result = Range(self.x1, self.x2, self.y1, self.y2)
        if axis == 0:  # x axis
            if side == "left":
                result.x1 = line
            elif side == "right":
                result.x2 = line
        elif axis == 1:  # y axis
            if side == "left":
                result.y1 = line
            elif side == "right":
                result.y2 = line

        assert result != self, "wyjściowy podział jest taki sam jak wejściowy"

        return result


class LeafNode:
    def __init__(self, point):
        self.point = point


class Node:
    def __init__(self, splitCoord, left, right):
        self.splitCoord = splitCoord
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, points):
        pointsXSorted = sorted(points, key=lambda x: x[0])
        pointsYSorted = sorted(points, key=lambda x: x[1])
        self.maxRange = self.__findMaxRange(pointsXSorted, pointsYSorted)
        self.kdTreeRoot = self.__initAux(pointsXSorted, pointsYSorted, 0)

    def __initAux(self, pointsXSorted, pointsYSorted, depth):
        axis = depth % 2

        if len(pointsXSorted) == 1:
            singleton = pointsXSorted[0]  # in this case same as pointsYSorted
            return LeafNode(singleton)

        leftXSorted, rightXSorted, leftYSorted, rightYSorted = self.__split(pointsXSorted, pointsYSorted, axis)
        splitLine = leftXSorted[-1][0] if axis == 0 else leftYSorted[-1][0]
        return Node(splitLine,
                    self.__initAux(leftXSorted, leftYSorted, depth + 1),
                    self.__initAux(rightXSorted, rightYSorted, depth + 1))

    def __split(self, x_sorted, y_sorted, axis):
        arrWithMedian = x_sorted if axis == 0 else y_sorted
        otherArr = y_sorted if axis == 0 else x_sorted

        med_ind = ceil(len(arrWithMedian) / 2)
        leftArr1, rightArr1 = arrWithMedian[:med_ind], arrWithMedian[med_ind:]
        # TODO change name of the array for something more suitable

        splitPointCoordinate = leftArr1[-1][axis]
        leftArr2 = list(filter(lambda x: x[axis] <= splitPointCoordinate, otherArr))
        rightArr2 = list(filter(lambda x: x[axis] > splitPointCoordinate, otherArr))

        if axis == 0:  # TODO simplify
            return leftArr1, rightArr1, leftArr2, rightArr2
        else:
            return leftArr2, rightArr2, leftArr1, rightArr2

    def __findMaxRange(self, pointsXSorted, pointsYSorted):
        min_x, max_x = pointsXSorted[0][0], pointsXSorted[-1][0]
        min_y, max_y = pointsYSorted[0][1], pointsYSorted[-1][1]
        return Range(min_x, max_x, min_y, max_y)

    def printTree(self, node, depth=0):
        if node.__class__ == LeafNode:
            print(node.point)
            return

        message = "x=" if depth % 2 == 0 else "y="

        self.printTree(node.left, depth + 1)
        print(message + str(node.splitCoord))
        self.printTree(node.right, depth + 1)

    def search(self, node, searchRange, nodeRange=self.maxRange, depth=0):
        if node.__class__ == LeafNode:
            return [node.point]

        result = []

        leftChildRange = nodeRange.returnSplit(depth % 2, "left", node.line)
        rightChildRange = nodeRange.returnSplit(depth % 2, "right", node.line)

        if leftChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.left)
        elif leftChildRange.intersects(searchRange):
            result += self.search(node.left, searchRange, leftChildRange)

        if rightChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.right)
        elif rightChildRange.intersects(searchRange):
            result += self.search(node.right, searchRange, rightChildRange)

        return result

    def __reportSubtree(self, node):
        if node.__class__ == LeafNode:
            return [node.point]

        return self.__reportSubtree(node.left) + self.__reportSubtree(node.right)


testTree = KDTree([(3, 1), (1, 2), (6, 0), (7, 5), (4, 3)])
testTree.printTree(testTree.kdTreeRoot)
