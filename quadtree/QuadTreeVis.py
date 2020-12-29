from tool import *
from QuadTree import *

class QuadTreeVis:
    def __init__(self, quadTree):
        self.quadTree = quadTree
        self.colors = {'initPoint': 'orange',
                       'normalPoint': 'turquoise',
                       'reportedPoint': 'red',
                       'normalLine': 'blue',
                       'activeLine': 'chartreuse',
                       'queryRectFill': 'grey',
                       'queryRectEdge': 'black',
                       'alphaLine': 0.80}

    def makeConsecutiveScenes(self, consecutiveElements, patches=None):
        sides0 = qt.root.quad.getListOfSides()
        scenes = []
        points0 = [[p.x, p.y] for p in qt.P]
        reportedPoints = []
        maxDepth = self.quadTree.calculateDepth()
        lineWidth0 = 2.5
        pointSize = 17
        prevLines = [LinesCollection(lines=sides0, linewidth=lineWidth0)]

        scenes.append(Scene(points=[PointsCollection(points=points0, color=self.colors['initPoint'], s=pointSize)],
                            lines=[LinesCollection(lines=sides0, alpha=self.colors['alphaLine'])]))

        for el in consecutiveElements:
            reportedPoints = reportedPoints + [[p.x, p.y] for p in el['points']]
            scenes.append(
                Scene(points=[PointsCollection(points=points0, color=self.colors['normalPoint'], s=pointSize),
                              PointsCollection(points=reportedPoints, color=self.colors['reportedPoint'], s=pointSize)],
                      lines=prevLines + [
                          LinesCollection(lines=el['lines'], color=self.colors['activeLine'],
                                          linewidth=lineWidth0 * (maxDepth - el['depth'] / 2) / maxDepth,
                                          alpha=self.colors['alphaLine'])])
            )
            prevLines = prevLines + [LinesCollection(lines=el['lines'],
                                                     linewidth=lineWidth0 * (maxDepth - el['depth']) / maxDepth,
                                                     color=self.colors['normalLine'],
                                                     alpha=self.colors['alphaLine'])]
        scenes.append(
            Scene(points=[PointsCollection(points=reportedPoints, color=self.colors['reportedPoint'], s=pointSize)],
                  lines=prevLines)
        )
        if patches is not None:
            for s in scenes:
                s.patches = patches


        return scenes


    def getInitVis(self):
        consecutiveElements = []
        qt = self.quadTree

        def addConsElements(v: QTNode, conEl, depth):
            if v.isLeaf:
                conEl.append({'depth': depth, 'lines': v.quad.getListOfSides(), 'points': v.points})

            else:
                conEl.append({'depth': depth, 'lines': v.quad.getSplittingLines(), 'points': []})
                addConsElements(v.SW, conEl, depth + 1)
                addConsElements(v.SE, conEl, depth + 1)
                addConsElements(v.NE, conEl, depth + 1)
                addConsElements(v.NW, conEl, depth + 1)


        addConsElements(qt.root, consecutiveElements, 0)

        scenes = self.makeConsecutiveScenes(consecutiveElements)

        return Plot(scenes=scenes)

    def getRangeQueryVis(self, queryRect: Rect):
        x = queryRect.x1
        y = queryRect.y1
        dx = queryRect.x2 - queryRect.x1
        dy = queryRect.y2 - queryRect.y1
        queryRectVis = patches.Rectangle((x, y), dx, dy,
                                         edgecolor=self.colors['queryRectEdge'],
                                         facecolor=self.colors['queryRectFill'],
                                         alpha=0.3)

        def _search(v, queryRect, conEl, depth):
            if v.isLeaf:
                conEl.append({'depth': depth, 'lines': v.quad.getListOfSides(),
                              'points': list(filter(lambda p: queryRect.contains(p), v.points))})

            else:
                conEl.append({'depth': depth, 'lines': v.quad.getSplittingLines(), 'points': []})
                if queryRect.isIntersecting(v.SW.quad):
                    _search(v.SW, queryRect, conEl, depth+1)
                if queryRect.isIntersecting(v.SE.quad):
                    _search(v.SE, queryRect, conEl, depth+1)
                if queryRect.isIntersecting(v.NE.quad):
                    _search(v.NE, queryRect, conEl, depth+1)
                if queryRect.isIntersecting(v.NW.quad):
                    _search(v.NW, queryRect, conEl, depth+1)


        consecutiveElements = []
        _search(self.quadTree.root, queryRect, consecutiveElements, 0)
        scenes = self.makeConsecutiveScenes(consecutiveElements, patches=[queryRectVis])

        return Plot(scenes=scenes)


if __name__ == '__main__':
    m = 0
    M = 10
    n = 150

    P = [(uniform(m, M), uniform(m, M)) for _ in range(n)]
    # P = [Point(x, y) for (x, y) in pp]
    # print(P)
    qt = QuadTree(P=P)

    queryRect = Rect(2.5, 7, 3.3, 6.1)
    repP = qt.searchInRange(queryRect)
    repP2 = qt.searchInRangeWithConsiInclusions(queryRect)
    print(repP)
    print(len(repP) == len(repP2))

    qtVis = QuadTreeVis(qt)
    plotInit = qtVis.getInitVis()
    plotInit.draw()
    plotSearch = qtVis.getRangeQueryVis(queryRect)
    plotSearch.draw()


