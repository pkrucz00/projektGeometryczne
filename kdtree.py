from math import inf, ceil

class Range:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def isContainedIn(self, other):
        return other.x1 <= self.x1 and self.x2 <= other.x2\
            and other.y1 <= self.y1 and self.y2 <= self.y2


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
        self.kdTreeRoot = self.__initAux(pointsXSorted, pointsYSorted, 0)

    def __initAux(self, pointsXSorted, pointsYSorted, depth):
        axis = depth % 2

        if len(pointsXSorted) == 1:
            singleton = pointsXSorted[0]  # in this case same as pointsYSorted
            return LeafNode(singleton)

        leftXSorted, rightXSorted, leftYSorted, rightYSorted = self.__split(pointsXSorted, pointsYSorted, axis)
        splitLine = leftXSorted[-1][0] if axis == 0 else leftYSorted[-1][0]
        return Node(splitLine,
                    self.__initAux(leftXSorted, leftYSorted, depth+1),
                    self.__initAux(rightXSorted, rightYSorted, depth+1))


    def __split(self, x_sorted, y_sorted, axis):
        arrWithMedian = x_sorted if axis == 0 else y_sorted
        otherArr = y_sorted if axis == 0 else x_sorted


        med_ind = ceil(len(arrWithMedian) / 2)
        leftArr1, rightArr1 = arrWithMedian[:med_ind], arrWithMedian[med_ind:]  # TODO change name of the array for something more suitable

        splitPointCoordinate = leftArr1[-1][axis]
        leftArr2 = list(filter(lambda x: x[axis] <= splitPointCoordinate, otherArr))
        rightArr2 = list(filter(lambda x: x[axis] > splitPointCoordinate, otherArr))

        if axis == 0:
            return leftArr1, rightArr1, leftArr2, rightArr2
        else:
            return leftArr2, rightArr2, leftArr1, rightArr2

    def printTree(self, node):
        if node.__class__ == LeafNode:
            print(node.point)
            return

        self.printTree(node.left)
        print(node.splitCoord)
        self.printTree(node.right)


    # def search(self, node, searchRange, nodeRange=Range(-inf, -inf, inf, inf)):
    #     if node.__class__ == LeafNode:
    #         return node.point
    #
    #
    #     if



testTree = KDTree([(3,1), (1,2), (6,0), (7,5), (4,3)])
testTree.printTree(testTree.kdTreeRoot)

