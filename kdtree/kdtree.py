from kdtree.kdtreeAuxClasses import *

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

        leftXSorted, rightXSorted, leftYSorted, rightYSorted, splitLine = self.__split(pointsXSorted, pointsYSorted,
                                                                                       axis)
        return Node(splitLine,
                    self.__initAux(leftXSorted, leftYSorted, depth + 1),
                    self.__initAux(rightXSorted, rightYSorted, depth + 1))

    def __split(self, x_sorted, y_sorted, axis):
        arrWithMedian = x_sorted if axis == 0 else y_sorted
        otherArr = y_sorted if axis == 0 else x_sorted

        med_ind = (len(arrWithMedian) - 1) // 2
        leftArr1, rightArr1 = arrWithMedian[:med_ind + 1], arrWithMedian[med_ind + 1:]
        # TODO change name of the array for something more suitable

        splitPointCoordinate = leftArr1[-1][axis]
        leftArr2 = list(filter(lambda x: x[axis] <= splitPointCoordinate, otherArr))
        rightArr2 = list(filter(lambda x: x[axis] > splitPointCoordinate, otherArr))

        if axis == 0:  # TODO simplify
            return leftArr1, rightArr1, leftArr2, rightArr2, splitPointCoordinate
        else:
            return leftArr2, rightArr2, leftArr1, rightArr1, splitPointCoordinate

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

    def search(self, searchRange, node=None, nodeRange=None, depth=0):
        if node.__class__ == LeafNode:
            if searchRange.isPointInRange(node.point):
                return [node.point]
            else:
                return []

        if node is None:
            node = self.kdTreeRoot
            nodeRange = self.maxRange

        result = []

        leftChildRange = nodeRange.returnSplit(depth % 2, "left", node.splitCoord)
        rightChildRange = nodeRange.returnSplit(depth % 2, "right", node.splitCoord)

        if leftChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.left)
        elif leftChildRange.intersects(searchRange):
            result += self.search(searchRange, node.left, leftChildRange, depth + 1)

        if rightChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.right)
        elif rightChildRange.intersects(searchRange):
            result += self.search(searchRange, node.right, rightChildRange, depth + 1)

        return result

    def __reportSubtree(self, node):
        if node.__class__ == LeafNode:
            return [node.point]

        return self.__reportSubtree(node.left) + self.__reportSubtree(node.right)
