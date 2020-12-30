from kdtreevis import *
from testDataGenerator import TestDataGen

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

    testKDTreeVis = KDTreeVis(P)
    plot = testKDTreeVis.getInitPlot()
    plot.draw()

