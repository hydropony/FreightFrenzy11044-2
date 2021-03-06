# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import (QColor, QPainter, QPen, QBrush)

from utils import L2Dist
from curve import Curve


class DrawingBoard(QFrame, QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.curves = []
        self.activeCurve = None
        self.pointDragged = None
        self.pointSelected = None
        self.selectedX = None
        self.selectedY = None
        self.c = None

    def loadCurves(self, points):
        self.addBCurve()
        self.curves[self.activeCurve].points = points
        print(len(self.curves[self.activeCurve].points))
        self.curves[self.activeCurve].points_no = len(points)
        self.pointSelected = self.curves[self.activeCurve].points_no - 1
        self.emitSignals()
        # self.activeCurve = list(self.curves.keys())[0]
        # self.c.selectedCurveName.emit(self.activeCurve)
        # self.pointDragged = None
        # self.pointSelected = None
        # self.selectedX = None
        # self.selectedY = None
        self.update()

    def mirrorLoad(self, points):
        self.addBCurve()
        self.curves[self.activeCurve].points = points
        print(len(self.curves[self.activeCurve].points))
        self.curves[self.activeCurve].points_no = len(points)
        for i in range(len(points)):
            self.curves[self.activeCurve].points[i] = (1-self.curves[self.activeCurve].points[i][0], self.curves[self.activeCurve].points[i][1])
        self.pointSelected = self.curves[self.activeCurve].points_no - 1
        self.emitSignals()
        # self.activeCurve = list(self.curves.keys())[0]
        # self.c.selectedCurveName.emit(self.activeCurve)
        # self.pointDragged = None
        # self.pointSelected = None
        # self.selectedX = None
        # self.selectedY = None
        self.update()

    def connectEvents(self, c):
        self.c = c

    def mousePressEvent(self, event):
        if self.activeCurve is not None:
            ex = event.x()
            ey = event.y()
            for (i, (x, y)) in enumerate(self.curves[self.activeCurve].points):
                if L2Dist(x * self.width(), y * self.height(),
                          ex, ey) < 8:
                    self.pointDragged = i
                    self.selectedX = ex
                    self.selectedY = ey
                    self.pointSelected = i
            if self.pointDragged is None:
                screenX = event.x() / self.width()
                screenY = event.y() / self.height()
                if self.activeCurve > 0:
                    if self.curves[self.activeCurve].points_no < 1:
                        self.curves[self.activeCurve].add_point(self.curves[self.activeCurve - 1].points[len(self.curves[self.activeCurve - 1].points) - 1][0],
                                                                self.curves[self.activeCurve - 1].points[len(self.curves[self.activeCurve - 1].points) - 1][1])
                        print("len of points list: " + str(len(self.curves[self.activeCurve].points)))
                    else:
                        self.curves[self.activeCurve].add_point(screenX, screenY)
                        print("hAHHAHAHAH")
                else:
                    self.curves[self.activeCurve].add_point(screenX, screenY)
                    if len(self.curves) > 1:
                        self.curves[self.activeCurve + 1].move_point_to(0, screenX, screenY)
                    print("hAHHAHAHAH")
                self.selectedX = screenX
                self.selectedY = screenY
                self.pointSelected = self.curves[self.activeCurve].points_no - 1
        self.emitSignals()
        self.update()

    def mouseMoveEvent(self, event):
        xdisp = (event.x() / self.width() - 0.5) * 144.0
        ydisp = -(event.y() / self.height() - 0.5) * 144.0
        x = event.x() / self.width()
        y = event.y() / self.height()
        text = "x: {0},  y: {1}".format(xdisp, ydisp)
        self.c.updateStatusBar.emit(text)
        if self.pointDragged is not None:
            distance = L2Dist(self.selectedX, self.selectedY, x, y)
            if distance > 5 / self.height():
                self.pointSelected = None
                i = self.pointDragged
                sw5 = 5 / self.width()
                sh5 = 5 / self.height()
                self.curves[self.activeCurve].move_point_to(i,
                                                            x - sw5,
                                                            y - sh5)
                print("poindragged: ", self.pointDragged)
                if i < 1 & self.activeCurve > 0:
                    self.curves[self.activeCurve - 1].move_point_to(self.curves[self.activeCurve - 1].points_no - 1,
                                                                x - sw5,
                                                                y - sh5)
                    print("worked")
                print("curveslen", len(self.curves))
                print("points_no", self.curves[self.activeCurve].points_no)
                if i > (self.curves[self.activeCurve].points_no - 2) and len(self.curves) > 1 and self.activeCurve < len(self.curves) - 1:
                    self.curves[self.activeCurve + 1].move_point_to(0,
                                                                    x - sw5,
                                                                    y - sh5)
                    print("ABASBDSBB")

                self.emitSignals()
                self.update()

    def mouseReleaseEvent(self, event):
        if self.pointSelected:
            distance = L2Dist(self.selectedX, self.selectedY,
                              event.x() / self.width(),
                              event.y() / self.height())
            if distance < 5:
                self.pointDragged = None
        if self.pointDragged is not None:
            self.pointSelected = self.pointDragged
        self.pointDragged = None
        if self.activeCurve is not None:
            for (i, (x, y)) in enumerate(self.curves[self.activeCurve].points):
                if L2Dist(x * self.width() + 5, y * self.height() + 5,
                          event.x(), event.y()) < 8:
                    print('SEL')
                    self.pointSelected = i
                    self.selectedX = event.x() / self.width()
                    self.selectedY = event.y() / self.height()
        self.emitSignals()
        self.update()

    def cyclePoint(self, order):
        if self.curves[self.activeCurve].points_no > 0:
            self.pointSelected = (self.pointSelected + order)
            self.pointSelected %= self.curves[self.activeCurve].points_no
            self.emitSignals()
            self.update()
            return self.pointSelected

    def gotoPoint(self, pointId):
        points_no = self.curves[self.activeCurve].points_no
        if points_no > 0 and pointId < points_no:
            self.pointSelected = pointId
            self.emitSignals()
            self.update()

    def moveXPoint(self, newCoord):
        # print("DEBUG moveXPoint: ", int(self.activeCurve), self.pointSelected, newCoord)
        self.curves[int(self.activeCurve)].move_point_by(self.pointSelected, newCoord, 0)
        if self.pointSelected < 1 & self.activeCurve > 0:
            self.curves[self.activeCurve - 1].move_point_by(self.curves[self.activeCurve - 1].points_no - 1, newCoord, 0)
        print("curveslen", len(self.curves))
        print("points_no", self.curves[self.activeCurve].points_no)
        if self.pointSelected > (self.curves[self.activeCurve].points_no - 2) and len(self.curves) > 1 and self.activeCurve < len(self.curves) - 1:
            self.curves[self.activeCurve + 1].move_point_by(0, newCoord, 0)
        self.emitSignals()
        self.update()

    def moveXPointTo(self, newCoord):
        self.curves[int(self.activeCurve)].move_point_to(self.pointSelected, x=newCoord)
        if self.pointSelected < 1 & self.activeCurve > 0:
            self.curves[self.activeCurve - 1].move_point_to(self.curves[self.activeCurve - 1].points_no - 1,
                                                            newCoord,
                                                            self.curves[int(self.activeCurve)].points[self.pointSelected][1])
            print("worked")
        print("curveslen", len(self.curves))
        print("points_no", self.curves[self.activeCurve].points_no)
        if self.pointSelected > (self.curves[self.activeCurve].points_no - 2) and len(self.curves) > 1 and self.activeCurve < len(self.curves) - 1:
            self.curves[self.activeCurve + 1].move_point_to(0,
                                                            newCoord,
                                                            self.curves[int(self.activeCurve)].points[self.pointSelected][1])
            print("ABASBDSBB")
        self.emitSignals()
        self.update()

    def moveYPoint(self, newCoord):
        self.curves[int(self.activeCurve)].move_point_by(self.pointSelected, 0, -newCoord)
        if self.pointSelected < 1 & self.activeCurve > 0:
            self.curves[self.activeCurve - 1].move_point_by(self.curves[self.activeCurve - 1].points_no - 1, 0, -newCoord)
        print("curveslen", len(self.curves))
        print("points_no", self.curves[self.activeCurve].points_no)
        if self.pointSelected > (self.curves[self.activeCurve].points_no - 2) and len(self.curves) > 1 and self.activeCurve < len(self.curves) - 1:
            self.curves[self.activeCurve + 1].move_point_by(0, 0, -newCoord)
        self.emitSignals()
        self.update()

    def moveYPointTo(self, newCoord):
        i = self.pointSelected
        self.curves[self.activeCurve].move_point_to(i, y=newCoord)
        if self.pointSelected < 1 & self.activeCurve > 0:
            self.curves[self.activeCurve - 1].move_point_to(self.curves[self.activeCurve - 1].points_no - 1,
                                                            self.curves[int(self.activeCurve)].points[self.pointSelected][0],
                                                            newCoord)
            print("worked")
        print("curveslen", len(self.curves))
        print("points_no", self.curves[self.activeCurve].points_no)
        if self.pointSelected > (self.curves[self.activeCurve].points_no - 2) and len(self.curves) > 1 and self.activeCurve < len(self.curves) - 1:
            self.curves[self.activeCurve + 1].move_point_to(0,
                                                            self.curves[int(self.activeCurve)].points[self.pointSelected][0],
                                                            newCoord)
            print("ABASBDSBB")
        self.emitSignals()
        self.update()

    def toggleHull(self, is_hull):
        self.curves[self.activeCurve].toggle_hull(is_hull)
        self.update()

    def toggleGuide(self, is_guide):
        self.curves[self.activeCurve].toggle_guide(is_guide)
        self.update()

    def addCurve(self, ctype, cname):
        print(len(self.curves))
        if cname == '':
            cname = str(len(self.curves))
        print('bef')
        print(cname)
        self.curves.append(Curve(ctype=ctype))
        print('aft')
        self.c.addCurve.emit(cname)
        self.selectCurve(cname)
        self.c.selectedCurveName.emit(cname)
        print('added')
        print(len(self.curves))
        self.update()

    def addBCurve(self):
        self.addCurve('bezier', '')

    def addICurve(self):
        self.addCurve('interp')

    def addNSCurve(self):
        self.addCurve('nspline')

    def addPSCurve(self):
        self.addCurve('pspline')

    def renameCurve(self, text):
        self.curves[text] = self.curves[self.activeCurve]
        self.curves.pop(self.activeCurve)
        self.activeCurve = text
        self.update()

    def removeCurveBoard(self, cname):
        print("my2")
        self.curves[self.activeCurve].points = None
        print("myasa")
        self.curves.pop(cname)
        self.update()

    def selectCurve(self, cnum):
        self.activeCurve = int(cnum)
        if len(self.curves[self.activeCurve].points) > 0:
            self.pointSelected = 0
        else:
            self.pointSelected = None
        print(cnum)
        self.emitSignals()
        self.update()

    def emitSignals(self):
        if self.pointSelected is not None:
            i = self.pointSelected
            point = self.curves[self.activeCurve].points[i]
            self.c.updateSelectedPoint.emit(str(i),
                                            str(point[0]),
                                            str(point[1]))

    def setActiveCurve(self, value):
        self.activeCurve = value
        print("acurve in drawb", self.activeCurve)

    def setAcNone(self):
        self.activeCurve = None

    def getActiveCurve(self):
        return self.activeCurve

    def paintEvent(self, event):
        # TODO scale all X by self.width() and all Y by self.height()
        painter = QPainter(self)

        print(self.curves)
        print('go')
        for curve_num in range(len(self.curves)):
            print(curve_num)
            self.curves[curve_num].make_plot(self.width(), self.height())
            print("zmejkplocony")
            print(curve_num)
            if self.activeCurve != curve_num:
                painter.setPen(QPen(QColor(0, 255, 0))) #120 120 120
                painter.drawPolyline(self.curves[curve_num].plot)
                print('drew')

        print('chmo')
        if self.activeCurve != None:
            # print(self.curves[self.activeCurve].points)
            print("nonnan")
            # if self.curves[self.activeCurve].is_hull:
            #     painter.setPen(QPen(QColor(0, 0, 255)))
            #     painter.drawPolygon(self.curves[self.activeCurve].hull)
            # if self.curves[self.activeCurve].is_guide:
            #     painter.setPen(QPen(QColor(255, 0, 0)))
            #     painter.drawPolyline(self.curves[self.activeCurve].guide)
            #  potem aktywna
            painter.setPen(QPen(QColor(0, 255, 0)))
            print('set')
            painter.drawPolyline(self.curves[int(self.activeCurve)].plot)

            #  potem zaznaczone punkty
            if self.pointSelected is not None:
                painter.setPen(QPen(QColor(255, 0, 0)))
                x, y = self.curves[self.activeCurve].points[self.pointSelected]
                painter.drawRect(self.width() * x - 5, self.height() * y - 5, 10, 10)

            print('abobs')
            #  i same punkty
            painter.setPen(QPen(QColor(0, 255, 0)))
            painter.setBrush(QBrush(QColor(0, 154, 0)))
            for (i, (x, y)) in enumerate(self.curves[self.activeCurve].points):
                painter.setPen(QPen(QColor(0, 0, 0)))
                painter.drawEllipse(self.width() * x - 5, self.height() * y - 5, 10, 10)
                painter.setPen(QPen(QColor(0, 255, 0)))
                painter.drawText(self.width() * x + 10,
                                 self.height() * y + 20, str(i))

        print('painted')
