from kdtree.kdtree import *
from quadtree.QuadTree import *

from random import uniform
from math import sqrt
import time

SQR_LEN = 100


def pointsInInterval(s, t, n):
    return [(uniform(s, t), uniform(s, t)) for _ in range(n)]


def tupleToPointObject(tupleList):
    return [Point(p[0], p[1]) for p in tupleList]


def testKDTree(pointsSet, percentages):
    result = []
    testRanges = [Range(-SQR_LEN * sqrt(p), SQR_LEN * sqrt(p),
                        -SQR_LEN * sqrt(p), SQR_LEN * sqrt(p))
                  if p != 1.0 else Range(-SQR_LEN, SQR_LEN, -SQR_LEN, SQR_LEN)
                  for p in percentages]

    # construction time
    a = time.time()
    kdtree = KDTree(pointsSet)
    b = time.time()
    result.append(b - a)

    # search time
    for testRange in testRanges:
        a = time.time()
        kdtree.search(testRange)
        b = time.time()
        result.append(b - a)

    return result


def testQuadTree(pointsSet, percentages):  # TODO merge this and above functions
    result = []
    testRanges = [Rect(-SQR_LEN * sqrt(p), SQR_LEN * sqrt(p),
                       -SQR_LEN * sqrt(p), SQR_LEN * sqrt(p))
                  if p != 1.0 else Rect(-SQR_LEN, SQR_LEN, -SQR_LEN, SQR_LEN)
                  for p in percentages]

    a = time.time()
    quadtree = QuadTree(pointsSet)
    b = time.time()
    result.append(b - a)

    for testRange in testRanges:
        a = time.time()
        quadtree.searchInRange(testRange)
        b = time.time()
        result.append(b - a)

    return result


def printResults(kdtreeResults, quadTreeResults, testPoints, percentages):
    print(f'n = {len(testPoints)}')
    percLabel = ["constr"] + [str(100 * percent) + "%" for percent in percentages]
    for label in percLabel:
        print("%8s" % label, end=' ')
    print()
    for res in kdtreeResults:
        print("%8f" % res, end=' ')
    print()
    for res in quadTreeResults:
        print("%8f" % res, end=' ')
    print('\n')


def testTable(numbersOfPoints, percentages):
    listOfTestPoints = [pointsInInterval(-100, 100, n) for n in numbersOfPoints]
    for testPoints in listOfTestPoints:
        kdtreeResults = testKDTree(testPoints, percentages)
        quadtreeResults = testQuadTree(tupleToPointObject(testPoints), percentages)
        printResults(kdtreeResults, quadtreeResults, testPoints, percentages)


numbersOfPoints = [100, 1000, 10000, 100000, 1000000]
percentages = [0.01, 0.1, 0.25, 0.5, 0.75, 1]

testTable(numbersOfPoints, percentages)
