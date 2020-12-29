from AlgGeometryczne.jupyter.pyChJu.tool import *
from AlgGeometryczne.project.QuadTree import *


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
                       'finalLine': 'grey',
                       'finalLineAlpha': 0.30,
                       'alphaLine': 0.80,
                       'queryRectAlpha': 0.3,
                       'pointAlpha': 0.7}

    def getFinalSetOfLines(self):

        lines = [{'depth': 0, 'lines': self.quadTree.root.quad.getListOfSides()}]

        def _FinalLinesAddConsElements(v: QTNode, depth):
            if v.isLeaf:
                return
            else:
                lines.append({'depth': depth, 'lines': v.quad.getSplittingLines()})
                _FinalLinesAddConsElements(v.SW, depth + 1)
                _FinalLinesAddConsElements(v.SE, depth + 1)
                _FinalLinesAddConsElements(v.NE, depth + 1)
                _FinalLinesAddConsElements(v.NW, depth + 1)

        _FinalLinesAddConsElements(self.quadTree.root, 0)
        return lines

    def makeConsecutiveScenes(self, consecutiveElements, patches=None, withFinalSetOfLines=False):
        sides0 = qt.root.quad.getListOfSides()
        scenes = []
        points0 = [[p.x, p.y] for p in qt.P]
        reportedPoints = []
        maxDepth = self.quadTree.getDepth()
        lineWidth0 = 2.5
        pointSize = 17
        finalLinesSet = [] if not withFinalSetOfLines else self.getFinalSetOfLines()
        finalLinesLinesCollections = []
        for el in finalLinesSet:
            finalLinesLinesCollections.append(LinesCollection(lines=el['lines'],
                                                              linewidth=lineWidth0 * (
                                                                      maxDepth - el['depth']) / maxDepth,
                                                              color=self.colors['finalLine'],
                                                              alpha=self.colors['finalLineAlpha']))

        prevLines = [LinesCollection(lines=sides0, linewidth=lineWidth0)]

        scenes.append(Scene(points=[PointsCollection(points=points0, color=self.colors['initPoint'], s=pointSize,
                                                     alpha=self.colors['pointAlpha'])],
                            lines=[LinesCollection(lines=sides0, alpha=self.colors['alphaLine'])]))

        for el in consecutiveElements:
            reportedPoints = reportedPoints + [[p.x, p.y] for p in el['points']]
            scenes.append(
                Scene(points=[PointsCollection(points=points0, color=self.colors['normalPoint'], s=pointSize,
                                               alpha=self.colors['pointAlpha']),
                              PointsCollection(points=reportedPoints, color=self.colors['reportedPoint'], s=pointSize,
                                               alpha=self.colors['pointAlpha'])],
                      lines=finalLinesLinesCollections + prevLines + [
                          LinesCollection(lines=el['lines'], color=self.colors['activeLine'],
                                          linewidth=lineWidth0 * (maxDepth - el['depth']) / maxDepth,
                                          alpha=self.colors['alphaLine'])])
            )
            prevLines = prevLines + [LinesCollection(lines=el['lines'],
                                                     linewidth=lineWidth0 * (maxDepth - el['depth']) / maxDepth,
                                                     color=self.colors['normalLine'],
                                                     alpha=self.colors['alphaLine'])]
        scenes.append(
            Scene(points=[PointsCollection(points=points0, color=self.colors['normalPoint'], s=pointSize,
                                           alpha=self.colors['pointAlpha']),
                          PointsCollection(points=reportedPoints, color=self.colors['reportedPoint'], s=pointSize,
                                           alpha=self.colors['pointAlpha'])],
                  lines=prevLines)
        )
        scenes.append(
            Scene(points=[PointsCollection(points=points0, color=self.colors['normalPoint'], s=pointSize,
                                           alpha=self.colors['pointAlpha']),
                          PointsCollection(points=reportedPoints, color=self.colors['reportedPoint'], s=pointSize,
                                           alpha=self.colors['pointAlpha'])])
        )
        if patches is not None:
            for s in scenes:
                s.patches = patches

        return scenes

    def getInitVis(self, withFinalSetOfLines=False):
        consecutiveElements = []
        qt = self.quadTree

        def _InitAddConsElements(v: QTNode, conEl, depth):
            if v.isLeaf:
                conEl.append({'depth': depth, 'lines': v.quad.getListOfSides(), 'points': v.points})

            else:
                conEl.append({'depth': depth, 'lines': v.quad.getSplittingLines(), 'points': []})
                _InitAddConsElements(v.SW, conEl, depth + 1)
                _InitAddConsElements(v.SE, conEl, depth + 1)
                _InitAddConsElements(v.NE, conEl, depth + 1)
                _InitAddConsElements(v.NW, conEl, depth + 1)

        _InitAddConsElements(qt.root, consecutiveElements, 0)

        scenes = self.makeConsecutiveScenes(consecutiveElements, withFinalSetOfLines=withFinalSetOfLines)

        return Plot(scenes=scenes)

    def getRangeQueryVis(self, queryRect: Rect, instantReportingAtInternalNode=True, withFinalSetOfLines=True):

        if instantReportingAtInternalNode and not self.quadTree.eachNodeContainsPoints:
            raise ValueError('If searching is going to instantly report points in internal node they must be there ')

        x = queryRect.x1
        y = queryRect.y1
        dx = queryRect.x2 - queryRect.x1
        dy = queryRect.y2 - queryRect.y1
        queryRectVis = patches.Rectangle((x, y), dx, dy,
                                         edgecolor=self.colors['queryRectEdge'],
                                         facecolor=self.colors['queryRectFill'],
                                         alpha=self.colors['queryRectAlpha'])

        def _searchAddConsElements(v, queryRect, conEl, depth):
            if queryRect.isDisjointWith(v.quad):
                conEl.append({'depth': depth, 'lines': v.quad.getListOfSides(),
                              'points': []})
                return
            if v.isLeaf or (instantReportingAtInternalNode and queryRect.include(v.quad)):
                conEl.append({'depth': depth, 'lines': v.quad.getListOfSides(),
                              'points': list(filter(lambda p: queryRect.contains(p), v.points))})

            else:
                conEl.append({'depth': depth, 'lines': v.quad.getSplittingLines(), 'points': []})
                _searchAddConsElements(v.SW, queryRect, conEl, depth + 1)
                _searchAddConsElements(v.SE, queryRect, conEl, depth + 1)
                _searchAddConsElements(v.NE, queryRect, conEl, depth + 1)
                _searchAddConsElements(v.NW, queryRect, conEl, depth + 1)

        consecutiveElements = []
        _searchAddConsElements(self.quadTree.root, queryRect, consecutiveElements, 0)
        scenes = self.makeConsecutiveScenes(consecutiveElements, patches=[queryRectVis],
                                            withFinalSetOfLines=withFinalSetOfLines)

        return Plot(scenes=scenes)


if __name__ == '__main__':
    m = 0
    M = 10
    n = 200
    quad0 = Rect(m, M, m, M)
    # pp = [(0.3217695332114623, 8.38710084343614), (4.807811304583016, 6.28993753478563), (3.342179791394102, 3.918754659311504), (3.9260851849110545, 2.8261212482508813), (4.593398704213815, 5.87123319344286), (3.6945084815606966, 8.329586917224209), (7.2887412346819005, 8.93224986764876), (9.23146863179297, 2.7530763401751592), (5.698549629416206, 4.9775753495154476), (3.2301987011595514, 6.631469040140986)]
    #
    P = [(uniform(m, M), uniform(m, M)) for _ in range(n)]
    # P = [Point(x, y) for (x, y) in pp]
    print(P)
    qt = QuadTree(P=P, eachNodeContainsPoints=True)

    queryRect = Rect(2.5, 7, 3.3, 6.1)
    repP = qt.searchInRange(queryRect)
    repP2 = qt.searchInRangeWithConsiInclusions(queryRect)
    print(qt.root.quad)

    qtVis = QuadTreeVis(qt)

    plotInit = qtVis.getInitVis(withFinalSetOfLines=True)
    plotInit.draw()

    plotSearch = qtVis.getRangeQueryVis(queryRect)
    plotSearch.draw()
