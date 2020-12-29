from random import uniform
import time


def pointsInInterval(s, t, n):
    return [(uniform(s, t), uniform(s, t)) for _ in range(n)]


def checkTime(convFunc, pointSets):
    result = []
    for pSet in pointSets:
        a = time.time()
        convFunc(pSet)
        b = time.time()
        result.append(round(b - a, 4))
    return result

def generateTestPoints(a, b, s, t):
    result = []
    numberOfPoints = []
    start, stop = 10**a, 10**b
    n = start
    while n <= stop:
        result.append(pointsInInterval(s, t, n))
        numberOfPoints.append(n)
        n *= 10

    return result, numberOfPoints


print(generateTestPoints(3, 7, -100, 100))
