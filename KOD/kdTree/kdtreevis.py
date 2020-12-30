from kdTree.tool import *
from kdTree.kdtreeAuxClasses import *
from kdTree.kdtree import KDTree


class Visualizer:
    def __init__(self, setOfPoints):
        self.__colors = {"maxRange": "aquamarine",
                         "currentRange": "red",
                         "searchRange": "yellow",
                         "lines": "blue",
                         "reportedPoints": "fuchsia",
                         "currentPoints": "yellow",
                         "normalPoints": "teal"}
        self.setOfPoints = setOfPoints

        self.maxRange = None
        self.searchRange = None

        self.lines = []
        self.reportedPoints = []
        self.initScenes = [Scene(points=[PointsCollection(setOfPoints)])]  # first scene with only the initial points
        self.searchScenes = []

    def setMaxRange(self, maxRange):
        self.maxRange = maxRange

    def setSearchRange(self, searchRange):
        self.searchRange = searchRange

    def addLine(self, splitCoord, smallerBound, biggerBound, axis):
        if axis == 0:
            x, y1, y2 = splitCoord, smallerBound, biggerBound
            line = ((x, y1), (x, y2))

        elif axis == 1:
            y, x1, x2 = splitCoord, smallerBound, biggerBound
            line = ((x1, y), (x2, y))

        assert line is not None, "Added line is None. Check function arguments"
        self.lines.append(line)

    def addPoint(self, point):
        self.reportedPoints.append(point)

    def _getRangeLines(self, rangeObj):
        result = []
        if rangeObj is not None:
            p1 = (rangeObj.x1, rangeObj.y1)
            p2 = (rangeObj.x1, rangeObj.y2)
            p3 = (rangeObj.x2, rangeObj.y2)
            p4 = (rangeObj.x2, rangeObj.y1)
            result = [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]

        return result

    def makeScene(self, currPoints=None, currRange=None):
        if currPoints is None:
            currPoints = []

        points = [PointsCollection(self.setOfPoints[:], color=self.__colors["normalPoints"]),
                  PointsCollection(currPoints[:], color=self.__colors["currentPoints"]),
                  PointsCollection(self.reportedPoints[:], color=self.__colors["reportedPoints"])]
        lines = [LinesCollection(self._getRangeLines(self.maxRange), color=self.__colors["maxRange"]),
                 LinesCollection(self.lines[:], color=self.__colors["lines"]),
                 LinesCollection(self._getRangeLines(self.searchRange), color=self.__colors["searchRange"]),
                 LinesCollection(self._getRangeLines(currRange), color=self.__colors["currentRange"])]

        if currRange is None:
            self.initScenes.append(Scene(points, lines))
        else:
            self.searchScenes.append(Scene(points, lines))

    def getInitScenes(self):
        return self.initScenes

    def getSearchScenes(self):
        endScene = Scene([PointsCollection(self.setOfPoints[:], color=self.__colors["normalPoints"]),
                          PointsCollection(self.reportedPoints[:], color=self.__colors["reportedPoints"])],
                         [LinesCollection(self._getRangeLines(self.searchRange), color=self.__colors["searchRange"])])
        self.searchScenes.append(endScene)

        return self.searchScenes

    def clear(self):  # after search so the lines don't collide
        self.searchRange = None
        self.reportedPoints = []
        self.searchScenes = []


class KDTreeVis(KDTree):
    def __init__(self, points):
        pointsXSorted = sorted(points, key=lambda x: x[0])
        pointsYSorted = sorted(points, key=lambda x: x[1])
        self.vis = Visualizer(points)
        if len(points) > 0:
            self.maxRange = super()._findMaxRange(pointsXSorted, pointsYSorted)
            self.vis.setMaxRange(self.maxRange)
            self.vis.makeScene(pointsXSorted)

            self.kdTreeRoot = self.__initAux(pointsXSorted, pointsYSorted)

    def __initAux(self, pointsXSorted, pointsYSorted, depth=0):
        axis = depth % 2
        otherAxis = (axis + 1) % 2

        self.vis.makeScene(pointsXSorted)

        if len(pointsXSorted) == 1:  # only one point in list
            singleton = pointsXSorted[0]  # in this case pointsXSorted is the same as pointsYSorted
            return LeafNode(singleton)

        leftXSorted, rightXSorted, leftYSorted, rightYSorted, splitLine = super()._split(pointsXSorted, pointsYSorted,
                                                                                         axis)

        smallerBound = min(pointsXSorted, key=lambda x: x[otherAxis])[otherAxis]
        biggerBound = max(pointsXSorted, key=lambda x: x[otherAxis])[otherAxis]
        self.vis.addLine(splitLine, smallerBound, biggerBound, axis)
        self.vis.makeScene(pointsXSorted)

        return Node(splitLine,
                    self.__initAux(leftXSorted, leftYSorted, depth + 1),
                    self.__initAux(rightXSorted, rightYSorted, depth + 1))

    def search(self, searchRange, node=None, nodeRange=None, depth=0):
        if node.__class__ == LeafNode:
            if searchRange.isPointInRange(node.point):
                self.vis.addPoint(node.point)
                self.vis.makeScene([node.point], nodeRange)
                return [node.point]
            else:
                return []

        if node is None:
            node = self.kdTreeRoot
            nodeRange = self.maxRange
            self.vis.setSearchRange(searchRange)
            self.vis.makeScene(currRange=self.maxRange)

        result = []

        leftChildRange, rightChildRange = nodeRange.returnSplit(depth % 2, node.splitCoord)

        self.vis.makeScene(currRange=leftChildRange)
        if leftChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.left)
        elif leftChildRange.intersects(searchRange):
            result += self.search(searchRange, node.left, leftChildRange, depth + 1)
        # self.vis.makeScene(currRange = leftChildRange)

        self.vis.makeScene(currRange=rightChildRange)
        if rightChildRange.isContainedIn(searchRange):
            result += self.__reportSubtree(node.right)
        elif rightChildRange.intersects(searchRange):
            result += self.search(searchRange, node.right, rightChildRange, depth + 1)
        # self.vis.makeScene(currRange = rightChildRange)

        return result

    def __reportSubtree(self, node):
        if node.__class__ == LeafNode:
            self.vis.addPoint(node.point)
            return [node.point]

        return self.__reportSubtree(node.left) + self.__reportSubtree(node.right)

    def getInitPlot(self):
        return Plot(scenes=self.vis.getInitScenes())

    def getSearchPlot(self):
        return Plot(scenes=self.vis.getSearchScenes())

    def clearVis(self):
        self.vis.clear()
