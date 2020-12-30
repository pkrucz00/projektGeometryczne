from quadTree.QuadTree import *
from kdTree.kdtree import *
from AuxFiles.testDataGenerator import TestDataGen

import time
from math import sqrt
SCAL = 1000000
MEASURMENTS = 1
SQR_LEN = 100

def specDataGenerator(n, treeConstructor, treeSearch, percentages, dataConstructor, rectangleConstructor):

    CONSTR_TIME = 0
    DEPTH = 0
    SEARCH_TIME = [0] * len(percentages)
    for _ in range(MEASURMENTS):
        P = dataConstructor(n)
        a = time.time_ns()/SCAL
        tree = treeConstructor(P)
        b = time.time_ns()/SCAL
        CONSTR_TIME += (b - a)
        if tree.__class__ == QuadTree:
            DEPTH += tree.getDepth()

        testRanges = [rectangleConstructor(-SQR_LEN * sqrt(p), SQR_LEN * sqrt(p),
                                           -SQR_LEN * sqrt(p), SQR_LEN * sqrt(p))
                      if p != 1.0 else rectangleConstructor(-SQR_LEN, SQR_LEN, -SQR_LEN, SQR_LEN)
                      for p in percentages]
        for i in range(len(testRanges)):
            a = time.time_ns()/SCAL
            sp = treeSearch(tree, testRanges[i])
            b = time.time_ns()/SCAL
            SEARCH_TIME[i] += (b - a)

    CONSTR_TIME /= MEASURMENTS
    SEARCH_TIME = [t/MEASURMENTS for t in SEARCH_TIME]
    DEPTH /= MEASURMENTS

    return (CONSTR_TIME, SEARCH_TIME, DEPTH)

def getResDict(sizes, percentge, dataConstructors: dict, treeConstructors: dict):

    treeTypes = treeConstructors.keys()
    dataTypes = dataConstructors.keys()
    resDict = {}
    for name in dataTypes:
        resDict[name] = {}
        for s in sizes:
            resDict[name][s] = {'kd': {}, 'quad': {}}
            # (CONSTR_TIME, SEARCH_TIME, DEPTH)
            resDict[name][s]['kd'] = specDataGenerator(s, treeConstructors['kd'],
                                                       lambda t, r: t.search(r),
                                                       percentge, dataConstructors[name],
                                                       Range)
            resDict[name][s]['quad'] = specDataGenerator(s, treeConstructors['quad'],
                                                       lambda t, r: t.searchInRange(r),
                                                       percentge, dataConstructors[name],
                                                       Rect)

    return resDict


def printConsRes(resDict, dataTypeNames, treesNames, sizes, percentages):
    print("CONSTRUCTION")
    for n in dataTypeNames:
        print("                                            " + n)
        print("size kd quad")
        for s in sizes:
            print(s, resDict[n][s][treesNames[0]][0], resDict[n][s][treesNames[1]][0])

def printDepthRes(resDict, dataTypeNames, treesNames, sizes, percentages):
    print("DEPTH")
    for n in dataTypeNames:
        print("                                            " + n)
        print("size kd quad")
        for s in sizes:
            print(s, resDict[n][s][treesNames[0]][2], resDict[n][s][treesNames[1]][2])

def printSerachTimeRes(resDict, dataTypeNames, treesNames, sizes, percentages):
    print('SEARCH')
    for n in dataTypeNames:
        print("                                            " + n)
        for (p, i) in zip(percentages, range(len(percentages))):
            print(f"        serach {p*100}%")
            print("size kd quad")
            for s in sizes:
                print(s, resDict[n][s][treesNames[0]][1][i], resDict[n][s][treesNames[1]][1][i])


if __name__ == '__main__':
    dataGen = TestDataGen()
    dataConstructors = {}
    dataConstructors['inRect'] = lambda n: dataGen.inRect(n=n, x1=-SQR_LEN, x2=SQR_LEN, y1=-SQR_LEN, y2=SQR_LEN)
    dataConstructors['cirque'] = lambda n: dataGen.cirque(n=n, R=SQR_LEN)
    dataConstructors['rectDiagonals'] = lambda n: dataGen.rectDiagonals(n1=n//2, n2=n//2, x1=-SQR_LEN, x2=SQR_LEN, y1=-SQR_LEN, y2=SQR_LEN)
    dataConstructors['doubleRectDiagonals'] = lambda n: dataGen.rectDiagonals(n1=n//2, n2=n//2, x1=-SQR_LEN, x2=SQR_LEN, y1=-SQR_LEN, y2=SQR_LEN) + dataGen.rectDiagonals(n1=n//2, n2=n//2, x1=-SQR_LEN/2, x2=SQR_LEN/2, y1=-SQR_LEN, y2=SQR_LEN)
    dataConstructors['archimedeanSpiral'] = lambda n: dataGen.archimedeanSpiral(n=n, maxR=SQR_LEN)


    treeConstructors = {'kd': lambda P: KDTree(P), 'quad': lambda P: QuadTree(P=P, eachNodeContainsPoints=True)}

    sizes = [10, 100, 1000, 10000, 100000, 1000000]
    percentages = [0.1, 0.5]
    resDict = getResDict(sizes, percentages, dataConstructors, treeConstructors)

    treeName = ['kd', 'quad']
    printConsRes(resDict, dataConstructors.keys(), treeName, sizes, percentages)
    print("**********************************************************************")
    printDepthRes(resDict, dataConstructors.keys(), treeName, sizes, percentages)
    print("**********************************************************************")
    printSerachTimeRes(resDict, dataConstructors.keys(), treeName, sizes, percentages)

