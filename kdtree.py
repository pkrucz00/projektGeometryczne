class Leaf:
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

        if pointsXSorted == 0:
            return None
        if pointsXSorted == 1:
            singleton = pointsXSorted[0]  # in this case same as pointsYSorted
            return Leaf(singleton)

        leftXSorted, rightXSorted, leftYSorted, rightYSorted = self.__split(pointsXSorted, pointsYSorted, axis)
        splitLine = leftXSorted[-1][0] if axis == 0 else leftYSorted[-1][0]
        return Node(splitLine, self.__initAux(leftXSorted, leftYSorted), self.__initAux(rightXSorted, rightYSorted))


    def __split(self, x_sorted, y_sorted, axis):
        arrWithMedian = x_sorted if axis == 0 else y_sorted
        otherArr = y_sorted if axis == 0 else x_sorted

        med_ind = len(arrWithMedian) // 2
        leftArr1, rightArr1 = arrWithMedian[:med_ind], arrWithMedian[med_ind:]  # TODO change name of the array for something more suitable

        splitPointCoordinate = leftArr1[-1][axis]
        leftArr2 = list(filter(lambda x: x[axis] <= splitPointCoordinate, otherArr))
        rightArr2 = list(filter(lambda x: x[axis] > splitPointCoordinate, otherArr))

        if axis == 0:
            return leftArr1, rightArr1, leftArr2, rightArr2
        else:
            return leftArr2, rightArr2, leftArr1, rightArr2
