
from quadTree.QuadTreeVis import *
from AuxFiles.testDataGenerator import TestDataGen

if __name__ == '__main__':

    # Konstrukcja generatora
    dataGenerator = TestDataGen()
    # Genrowanie przykładowych zestawów danych.
    # Każda metoda generująca zwraca listę punktów,
    # więc ich winiki można dowonie łączyć

    P = dataGenerator.inRect(n=100, x1=0, x2=10, y1=0, y2=10)
    # P = dataGenerator.cirque(n=100, x=0, y=0, R=10)#
    # P = dataGenerator.sinus(n=250, x1=0, x2=10, y1=0, y2=10)
    # P = dataGenerator.rectDiagonals(n1=100, n2=100, x1=0, x2=10, y1=0, y2=10)#
    # P = dataGenerator.archimedeanSpiral(n=450, x=0, y=0, maxR=10, lapses=5, direct=1)
    # P = dataGenerator.rectDiagonals() + dataGenerator.rectDiagonals()
    # P = dataGenerator.archimedeanSpiral() + dataGenerator.archimedeanSpiral(direct=-1)#

    eachNodeContainsPoints = True
    allowDuplicate = False
    qt = QuadTree(P=P, eachNodeContainsPoints=eachNodeContainsPoints, allowDuplicate=allowDuplicate)

    # Określenie przeszukiwanego obszaru
    queryRect = Rect(2.5, 7, 3.3, 6.1)
    qtVis = QuadTreeVis(qt)

    # plotInit = qtVis.getConstructionVis(withFinalSetOfLines=True)
    # plotInit.draw()

    plotSearch = qtVis.getRangeQueryVis(queryRect, instantReportingAtInternalNode=True)
    plotSearch.draw()

