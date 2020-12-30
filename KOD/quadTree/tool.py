

# Narzędzie jest oparte o kilka zewnętrznych bibliotek, które potrzebujemy najpierw zaimportować.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib.colors as mcolors
from matplotlib import patches
from matplotlib.widgets import Button
import json as js

# Parametr określający jak blisko (w odsetku całego widocznego zakresu) punktu początkowego
# wielokąta musimy kliknąć, aby go zamknąć.

# TOLERANCE = 0.15
from typing import List

TOLERANCE = 0.05


def dist(point1, point2):
    return np.sqrt(np.power(point1[0] - point2[0], 2) + np.power(point1[1] - point2[1], 2))


# Klasa ta trzyma obecny stan wykresu oraz posiada metody, które mają zostać wykonane
# po naciśnięciu przycisków.
class _Button_callback(object):
    def __init__(self, scenes, k=1):
        self.i = 0
        self.k = k
        self.scenes = scenes
        self.adding_points = False
        self.added_points = []
        self.adding_lines = False
        self.added_lines = []
        self.adding_rects = False
        self.added_rects = []

        self.adding_points_toScene = False
        self.added_points_toScene = []
        self.adding_lines_toScene = False
        self.added_lines_toScene = []
        self.adding_rects_toScene = False
        self.added_rects_toScene = []



    def set_axes(self, ax):
        self.ax = ax

    # Metoda ta obsługuje logikę przejścia do następnej sceny.
    def changeScene(self, event, gap):
        self.adding_lines = False
        self.adding_rects = False
        self.adding_points = False
        self.adding_points_toScene = False
        self.adding_lines_toScene = False
        self.adding_rects_toScene = False

        self.i = (self.i + gap) % max(len(self.scenes), 1)
        self.draw(autoscaling=True)

    def next(self, event):
        self.changeScene(event, 1)

    def next_10(self, event):
        self.changeScene(event, 10)


    def next_100(self, event):
        self.changeScene(event, 100)



    # Metoda ta obsługuje logikę powrotu do poprzedniej sceny.
    def prev(self, event):
        self.changeScene(event, -1)


    def prev_10(self, event):
        self.changeScene(event, -10)


    def prev_100(self, event):
        self.changeScene(event, -100)


    # Metoda ta aktywuje funkcję rysowania punktów wyłączając równocześnie rysowanie
    # odcinków i wielokątów.
    def add_point(self, event):
        self.adding_points = not self.adding_points
        self.new_line_point = None
        if self.adding_points:
            self.adding_lines = False
            self.adding_rects = False

            self.adding_points_toScene = False
            self.adding_lines_toScene = False
            self.adding_rects_toScene = False

            self.added_points.append(PointsCollection([]))

    # Metoda ta aktywuje funkcję rysowania odcinków wyłączając równocześnie
    # rysowanie punktów i wielokątów.
    def add_line(self, event):
        self.adding_lines = not self.adding_lines
        self.new_line_point = None
        if self.adding_lines:
            self.adding_points = False
            self.adding_rects = False

            self.adding_points_toScene = False
            self.adding_lines_toScene = False
            self.adding_rects_toScene = False

            self.added_lines.append(LinesCollection([]))

    # Metoda ta aktywuje funkcję rysowania wielokątów wyłączając równocześnie
    # rysowanie punktów i odcinków.
    def add_rect(self, event):
        self.adding_rects = not self.adding_rects
        self.new_line_point = None
        if self.adding_rects:
            self.adding_points = False
            self.adding_lines = False

            self.adding_points_toScene = False
            self.adding_lines_toScene = False
            self.adding_rects_toScene = False

            self.new_rect()

    def new_rect(self):
        self.added_rects.append(LinesCollection([]))
        self.rect_points = []
#MyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMy
    def add_point_toScene(self, event):
        self.adding_points_toScene = not self.adding_points_toScene
        self.new_line_point = None
        if self.adding_points_toScene:
            self.adding_points = False
            self.adding_lines = False
            self.adding_rects = False

            self.adding_lines_toScene = False
            self.adding_rects_toScene = False

            self.scenes[self.i].points.append(PointsCollection([]))

    def add_line_toScene(self, event):
        self.adding_lines_toScene = not self.adding_lines_toScene
        self.new_line_point = None
        if self.adding_lines_toScene:
            self.adding_points = False
            self.adding_lines = False
            self.adding_rects = False

            self.adding_points_toScene = False
            self.adding_rects_toScene = False

            self.scenes[self.i].lines.append(LinesCollection([]))

    def add_rect_toScene(self, event):
        self.adding_rects_toScene = not self.adding_rects_toScene
        self.new_line_point = None
        if self.adding_rects_toScene:
            self.adding_points = False
            self.adding_lines = False
            self.adding_rects = False

            self.adding_points_toScene = False
            self.adding_lines_toScene = False

            self.new_rect_toScene()

    def new_rect_toScene(self):
        self.scenes[self.i].lines.append(LinesCollection([]))
        self.rect_points = []

    def addScene(self, event):
        self.scenes.append(Scene())
        self.changeScene(event, 0)
        self.i = len(self.scenes) - 1
        self.draw(autoscaling=False)

    def delScene(self, event):
        if len(self.scenes) > 1:
            del self.scenes[self.i]
            self.i = min(self.i, len(self.scenes) - 1)
            self.draw(autoscaling=False)
        else:
            self.scenes[0].points = []
            self.scenes[0].lines = []

        self.changeScene(event, 0)


    # MyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMyMy

    # Metoda odpowiedzialna za właściwą logikę rysowania nowych elementów. W
    # zależności od włączonego trybu dodaje nowe punkty, początek, koniec odcinka
    # lub poszczególne wierzchołki wielokąta. Istnieje ciekawa logika sprawdzania
    # czy dany punkt jest domykający dla danego wielokąta. Polega ona na tym, że
    # sprawdzamy czy odległość nowego punktu od początkowego jest większa od
    # średniej długości zakresu pomnożonej razy parametr TOLERANCE.
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        new_point = (event.xdata, event.ydata)
        if self.adding_points:
            self.added_points[-1].add_points([new_point])
            self.draw(autoscaling=False)
        elif self.adding_points_toScene:
            self.scenes[self.i].points[-1].add_points([new_point])
            self.draw(autoscaling=False)
        elif self.adding_lines:
            if self.new_line_point is not None:
                self.added_lines[-1].add([self.new_line_point, new_point])
                self.new_line_point = None
                self.draw(autoscaling=False)
            else:
                self.new_line_point = new_point
        elif self.adding_lines_toScene:
            if self.new_line_point is not None:
                self.scenes[self.i].lines[-1].add([self.new_line_point, new_point])
                self.new_line_point = None
                self.draw(autoscaling=False)
            else:
                self.new_line_point = new_point
        elif self.adding_rects:
            if len(self.rect_points) == 0:
                self.rect_points.append(new_point)
            elif len(self.rect_points) == 1:
                self.added_rects[-1].add([self.rect_points[-1], new_point])
                self.rect_points.append(new_point)
                self.draw(autoscaling=False)
            elif len(self.rect_points) > 1:
                if dist(self.rect_points[0], new_point) < (
                        np.mean([self.ax.get_xlim(), self.ax.get_ylim()]) * TOLERANCE):
                    self.added_rects[-1].add([self.rect_points[-1], self.rect_points[0]])
                    self.added_rects[-1].isPolygon = True
                    self.new_rect()
                else:
                    self.added_rects[-1].add([self.rect_points[-1], new_point])
                    self.rect_points.append(new_point)
                self.draw(autoscaling=False)
        elif self.adding_rects_toScene:
            if len(self.rect_points) == 0:
                self.rect_points.append(new_point)
            elif len(self.rect_points) == 1:
                self.scenes[self.i].lines[-1].add([self.rect_points[-1], new_point])
                self.rect_points.append(new_point)
                self.draw(autoscaling=False)
            elif len(self.rect_points) > 1:
                if dist(self.rect_points[0], new_point) < (
                        np.mean([self.ax.get_xlim(), self.ax.get_ylim()]) * TOLERANCE):
                    self.scenes[self.i].lines[-1].add([self.rect_points[-1], self.rect_points[0]])
                    self.scenes[self.i].lines[-1].isPolygon = True
                    self.new_rect_toScene()
                else:
                    self.scenes[self.i].lines[-1].add([self.rect_points[-1], new_point])
                    self.rect_points.append(new_point)
                self.draw(autoscaling=False)

    # Metoda odpowiedzialna za narysowanie całego wykresu. Warto zauważyć,
    # że zaczyna się ona od wyczyszczenia jego wcześniejszego stanu. Istnieje w
    # niej nietrywialna logika zarządzania zakresem wykresu, tak żeby, w zależności
    # od ustawionego parametru autoscaling, uniknąć sytuacji, kiedy dodawanie
    # nowych punktów przy brzegu obecnie widzianego zakresu powoduje niekorzystne
    # przeskalowanie.
    def draw(self, autoscaling=True):
        if not autoscaling:
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
        self.ax.clear()
        ##########################
        self.ax._axes.set_title(self.scenes[self.i].title + f"\nscene {str(self.i+1)}/{len(self.scenes)}")
        for patch in self.scenes[self.i].patches:
            self.ax.add_patch(patch)
        ##########################
        for collection in (self.scenes[self.i].points + self.added_points):
            if len(collection.points) > 0:
                self.ax.scatter(*zip(*(np.array(collection.points))), **collection.kwargs)
        for collection in (self.scenes[self.i].lines + self.added_lines + self.added_rects):
            self.ax.add_collection(collection.get_collection())
        self.ax.autoscale(autoscaling)
        if not autoscaling:
            self.ax.set_xlim(xlim)
            self.ax.set_ylim(ylim)
        plt.draw()

# Klasa PointsCollection gromadzi w sobie punkty jednego typu, a więc takie,
# które zostaną narysowane w takim samym kolorze i stylu. W konstruktorze
# przyjmuje listę punktów rozumianych jako pary współrzędnych (x, y). Parametr
# kwargs jest przekazywany do wywołania funkcji z biblioteki MatPlotLib przez
# co użytkownik może podawać wszystkie parametry tam zaproponowane.
class PointsCollection:
    def __init__(self, points, **kwargs):
        self.points = points
        self.kwargs = kwargs

    def add_points(self, points):
        self.points = self.points + points
    def getPointsAsList(self):
        return self.points.copy()

# Klasa LinesCollection podobnie jak jej punktowy odpowiednik gromadzi
# odcinki tego samego typu. Tworząc ją należy podać listę linii, gdzie każda
# z nich jest dwuelementową listą punktów – par (x, y). Parametr kwargs jest
# przekazywany do wywołania funkcji z biblioteki MatPlotLib przez co użytkownik
# może podawać wszystkie parametry tam zaproponowane.
class LinesCollection:
    def __init__(self, lines, isPolygon=False, **kwargs):
        self.lines = lines
        self.kwargs = kwargs
        self.isPolygon = isPolygon

    def add(self, line):
        self.lines.append(line)

    def get_collection(self):
        return mcoll.LineCollection(self.lines, **self.kwargs)
    def getLinesAsList(self):
        return self.lines.copy()

    def getPointsOfPolygon(self):
        if not self.isPolygon:
            print("It is not polygon")
            return None
        return [v for (v, _) in self.lines]


# Klasa Scene odpowiada za przechowywanie elementów, które mają być
# wyświetlane równocześnie. Konkretnie jest to lista PointsCollection i
# LinesCollection.


class Scene:
    def __init__(self, points=None, lines=None, patches=None, title=""):
        if points is None:
            points = []
        if lines is None:
            lines = []
        if patches is None:
            patches = []
        self.points = points
        self.lines = lines
        self.title = title
        self.patches = patches

    def getAllLines(self):
        L = []
        for linesColl in self.lines:
            L += linesColl.lines
        return L
    def getAllPoints(self):
        V = []
        for pointsColl in self.points:
            V += pointsColl.points
        return V

    def addPointsCollection(self, pc: PointsCollection):
        self.points.append(pc)

    def addAllPointsCollections(self, PC: List[PointsCollection]):
        self.points += PC

    def addLinesCollection(self, lc: LinesCollection):
        self.lines.append(lc)

    def addAllLinesCollections(self, LC: List[LinesCollection]):
        self.lines += LC

    def addPatch(self, patch: patches.Patch):
        self.patches.append(patch)

    def addAllPatches(self, PC: List[patches.Patch]):
        self.patches += PC



# Klasa Plot jest najważniejszą klasą w całym programie, ponieważ agreguje
# wszystkie przygotowane sceny, odpowiada za stworzenie wykresu i przechowuje
# referencje na przyciski, dzięki czemu nie będą one skasowane podczas tzw.
# garbage collectingu.
class Plot:
    def __init__(self, scenes=None, points=None, lines=None, json=None):
        if not scenes:
            scenes = [Scene()]
        if points == None:
            points = []
        if lines == None:
            lines = []

        if json is None:
            self.scenes = scenes
            if points or lines:
                self.scenes[0].points = points
                self.scenes[0].lines = lines
        else:
            self.scenes = [Scene([PointsCollection(pointsCol[0], **pointsCol[1]) for pointsCol in scene["points"]],
                                 [LinesCollection(linesCol[0], linesCol[1], **linesCol[2]) for linesCol in scene["lines"]])
                           for scene in js.loads(json)]

    # Ta metoda ma szczególne znaczenie, ponieważ konfiguruje przyciski i
    # wykonuje tym samym dość skomplikowaną logikę. Zauważmy, że konfigurując każdy
    # przycisk podajemy referencję na metodę obiektu _Button_callback, która
    # zostanie wykonana w momencie naciśnięcia.
    def __configure_buttons(self):
        plt.subplots_adjust(bottom=0.2)
        ax_prev = plt.axes([0.6, 0.07, 0.15, 0.055])
        ax_next = plt.axes([0.76, 0.07, 0.15, 0.055])
        ax_add_point = plt.axes([0.44, 0.07, 0.15, 0.055])
        ax_add_line = plt.axes([0.28, 0.07, 0.15, 0.055])
        ax_add_rect = plt.axes([0.12, 0.07, 0.15, 0.055])

        b_next = Button(ax_next, 'Następny')
        b_next.on_clicked(self.callback.next)
        b_prev = Button(ax_prev, 'Poprzedni')
        b_prev.on_clicked(self.callback.prev)
        b_add_point = Button(ax_add_point, 'Dodaj punkt')
        b_add_point.on_clicked(self.callback.add_point)
        b_add_line = Button(ax_add_line, 'Dodaj linię')
        b_add_line.on_clicked(self.callback.add_line)
        b_add_rect = Button(ax_add_rect, 'Dodaj figurę')
        b_add_rect.on_clicked(self.callback.add_rect)

        ax_prev10 = plt.axes([0.6, 0.035, 0.15, 0.025])
        ax_next10 = plt.axes([0.76, 0.035, 0.15, 0.025])
        b_next10 = Button(ax_next10, '10')
        b_prev10 = Button(ax_prev10, '10')
        b_next10.on_clicked(self.callback.next_10)
        b_prev10.on_clicked(self.callback.prev_10)

        ax_prev100 = plt.axes([0.6, 0.001, 0.15, 0.025])
        ax_next100 = plt.axes([0.76, 0.001, 0.15, 0.025])
        b_next100 = Button(ax_next100, '100')
        b_prev100 = Button(ax_prev100, '100')
        b_next100.on_clicked(self.callback.next_100)
        b_prev100.on_clicked(self.callback.prev_100)

        ax_add_point_toScene = plt.axes([0.44, 0.001, 0.15, 0.06])
        ax_add_line_toScene = plt.axes([0.28, 0.001, 0.15, 0.06])
        ax_add_rect_toScene = plt.axes([0.12, 0.001, 0.15, 0.06])
        b_add_point_toScene = Button(ax_add_point_toScene, 'Dodaj punkt\n do sceny')
        b_add_point_toScene.on_clicked(self.callback.add_point_toScene)
        b_add_line_toScene = Button(ax_add_line_toScene, 'Dodaj linię\n do sceny')
        b_add_line_toScene.on_clicked(self.callback.add_line_toScene)
        b_add_rect_toScene = Button(ax_add_rect_toScene, 'Dodaj figurę\n do sceny')
        b_add_rect_toScene.on_clicked(self.callback.add_rect_toScene)

        ax_addScene = plt.axes([0.92, 0.07, 0.07, 0.06])
        b_addScene = Button(ax_addScene, 'Nowa \nscena')
        b_addScene.on_clicked(self.callback.addScene)

        ax_delScene = plt.axes([0.92, 0.005, 0.07, 0.06])
        b_delScene = Button(ax_delScene, 'Usuń \nscenę')
        b_delScene.on_clicked(self.callback.delScene)

        return [b_prev, b_next, b_add_point, b_add_line, b_add_rect,
                b_prev10, b_next10, b_next100, b_prev100,
                b_add_point_toScene, b_add_line_toScene, b_add_rect_toScene,
                b_addScene, b_delScene
                ]


############################
    def add_scene(self, scene):
        self.scenes.append(scene)

    def add_scenes(self, scenes):
        self.scenes = self.scenes + scenes

    # Metoda toJson() odpowiada za zapisanie stanu obiektu do ciągu znaków w
    # formacie JSON.
    def toJson(self):
        return js.dumps([{"points": [[np.array(pointCol.points).tolist(), pointCol.kwargs] for pointCol in scene.points],
                          "lines": [[linesCol.lines, linesCol.isPolygon, linesCol.kwargs] for linesCol in scene.lines]}
                         for scene in self.scenes])

        # Metoda ta zwraca punkty dodane w trakcie rysowania.

    def get_added_points(self):
        if self.callback:
            return self.callback.added_points
        else:
            return None

    # Metoda ta zwraca odcinki dodane w trakcie rysowania.
    def get_added_lines(self):
        if self.callback:
            return self.callback.added_lines
        else:
            return None

    # Metoda ta zwraca wielokąty dodane w trakcie rysowania.
    def get_added_figure(self):
        if self.callback:
            return self.callback.added_rects
        else:
            return None

    # Metoda ta zwraca punkty, odcinki i wielokąty dodane w trakcie rysowania
    # jako scenę.
    def get_added_elements(self):
        if self.callback:
            return Scene(self.callback.added_points, self.callback.added_lines + self.callback.added_rects)
        else:
            return None

    # Główna metoda inicjalizująca wyświetlanie wykresu.
    def draw(self):
        plt.close()
        fig = plt.figure()
        self.callback = _Button_callback(self.scenes)
        self.widgets = self.__configure_buttons()
        ax = plt.axes(autoscale_on=False)
        self.callback.set_axes(ax)
        fig.canvas.mpl_connect('button_press_event', self.callback.on_click)
        plt.show()
        self.callback.draw()



