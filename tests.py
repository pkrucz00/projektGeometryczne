from kdTree.kdtree import *
from quadTree.QuadTree import *

from random import uniform
from math import sqrt
import time

SQR_LEN = 100


def pointsInInterval(s, t, n):
    return [(uniform(s, t), uniform(s, t)) for _ in range(n)]


def testTree(treeConstructor, treeSearchMethod, rectangleConstructor, pointsSet, percentages):
    result = []
    testRanges = [rectangleConstructor(-SQR_LEN * sqrt(p), SQR_LEN * sqrt(p),
                                       -SQR_LEN * sqrt(p), SQR_LEN * sqrt(p))
                  if p != 1.0 else rectangleConstructor(-SQR_LEN, SQR_LEN, -SQR_LEN, SQR_LEN)
                  for p in percentages]

    # construction time
    a = time.time()
    tree = treeConstructor(pointsSet)
    b = time.time()
    result.append(b - a)

    # search time
    for testRange in testRanges:
        a = time.time()
        treeSearchMethod(tree, testRange)
        b = time.time()
        result.append(b - a)

    return result


def averagedResults(results):
    m = len(results[0])
    n = len(results)
    avgTable = []
    for j in range(m):
        tmp = 0
        acc = 0
        for i in range(n):
            if results[i][j] > 0:
                tmp += results[i][j]
                acc += 1
        avg = tmp/acc if acc > 0 else 0
        avgTable.append(avg)

    return avgTable


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


def testTable(numbersOfPoints, percentages, testRepeats):
    listOfListOfTestPoints = [[pointsInInterval(-100, 100, n) for _ in range(testRepeats)]  #certain amount of test cases
                              for n in numbersOfPoints]
    for listOfTestPoints in listOfListOfTestPoints:
        kdtreeResults = [testTree(KDTree, KDTree.search, Range, testPoints, percentages)
                         for testPoints in listOfTestPoints]
        quadtreeResults = [testTree(QuadTree, QuadTree.searchInRange, Rect, testPoints, percentages)
                           for testPoints in listOfTestPoints]
        avgKdtreeResults = averagedResults(kdtreeResults)
        avgQuadtreeResults = averagedResults(quadtreeResults)
        printResults(avgKdtreeResults, avgQuadtreeResults, listOfTestPoints[0], percentages)

if __name__ == '__main__':
    numbersOfPoints = [100, 1000, 10000, 100000, 1000000]
    percentages = [0.01, 0.1, 0.25, 0.5, 0.75, 1]

    testTable(numbersOfPoints, percentages, 5)
