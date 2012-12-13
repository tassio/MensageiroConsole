#-*- coding: utf-8 -*-
from PyQt4.QtCore import QPoint, Qt, QSize, QCoreApplication, QObject
from PyQt4.QtGui import QPaintEngine, QPaintDevice, QPainter, QFont, QLabel

from engineConsole.base.baseApplication import CApplication
from engineConsole.base.eventoUpdate import EventoUpdateConsole


class Ponto(QPoint):
    def __hash__(self):
        return (self.x()+1)*5 + (self.y()+2)*7


class PaintEngineConsole(QPaintEngine):
    def __init__(self, device):
        super().__init__()
        self.begin(device)

    def begin(self, pdev):
        print("BEGIN")
        self._device = pdev
        self.setActive(True)
        return True

    def end(self):
        print("END")
        self.setActive(False)
        return True

    def drawEllipse(self, rect):
        print("ELLIPSE", rect)

    def drawImage(self, rect, image, sr, flags=Qt.AutoColor):
        print("IMAGE", rect, image)

    def drawLines(self, lines, numLines=-1):
        print("LINES", lines)

    def drawPath(self, path):
        print("PATH", path)

    def drawPixmap(self, rect, pm, sr):
        print("PIXMAP", rect, pm)

    def drawPoints(self, points, numPoints=-1):
        print("POINTS", points)

    def drawPolygon(self, points, numPoints, mode):
        print("POLYGON", points)

    def drawRects(self, rects, numRects=-1):
        print("RECTS", rects)

    def drawTextItem(self, p, textItem):
        text = textItem.text()
        for i in range(len(text)):
            self._device.setChar(Ponto(int(p.y()), int(p.x()+i)), text[i])
            
        print("TEXT_ITEM", p, textItem.text())

    def drawTiledPixmap(self, rect, pixmap, p):
        print("TILED_PIXMAP", rect, pixmap, p)

    def hasFeature(self, feat):
        print("HAS_FEATURE", feat)
        return False

    def paintDevice(self):
        print("PAINT_DEVICE")
        return self._device

    def painter(self):
        print("PAINTER")

    def type(self):
        print("TYPE")
        return 0

    def updateState(self, state):
        print("UPDATE_STATE", state.backgroundBrush().color().getRgb())
        #return 0


class PaintDeviceConsole(QPaintDevice):
    def __init__(self, width=80, height=24):
        super().__init__()
        self._paintEngine = []
        self._pos = Ponto(1,1)
        self._size = QSize(width, height)
        self._mapa = {}

    def setPos(self, pos):
        self._pos = pos

    def getPos(self):
        return self._pos

    def setTela(self, tela):
        linhas = tela.split('\n')

        self._mapa = {}
        self.resize(QSize(len(linhas[0]), len(linhas)))
        for i in range(self.height()):
            for j in range(self.width()):
                char = linhas[i][j]
                if char != ' ':
                    self.setChar(Ponto(i, j), char)

        self.update()

    def contains(self, point):
        return 0 <= point.x() < self.height() and 0 <= point.y() < self.width()

    def update(self):
        painter = QPainter(self)#CApplication.getTelaPrincipal())
        painter.translate(self.getPos())
        self.paint(painter)
        painter.end()
        
        if not CApplication.updateRequested():
            CApplication.setUpdateRequested(True)
            QCoreApplication.postEvent(CApplication.getInstance(), EventoUpdateConsole(EventoUpdateConsole.UpdateRequest))
            return

    def resize(self, size):
        if self.size() == size:
            return

        oldW, oldH = self.width(), self.height()
        self._size = size
        if not self.contains(Ponto(oldW, oldH)):
            for point in self._mapa.copy().keys():
                if not self.contains(point):
                    self._mapa.pop(point)

        self.update()

    def size(self):
        return self._size
    def height(self):
        return self.size().height()
    def width(self):
        return self.size().width()

    def paintEngine(self):
        p = PaintEngineConsole(self)
        self._paintEngine.append(p)
        return p

    def setChar(self, point, char):
        if len(char) != 1:
            raise Exception("Tamanho deve deve ser igual a 1")

        if self.contains(point):
            self._mapa[point] = char

    def getChar(self, point):
        return self._mapa[point] if point in self._mapa.keys() else ' '

    def render(self, painter):
        painter.save()
        painter.setFont(QFont("Lucida Console"))
        for point, char in self._mapa.items():
            painter.drawText(Ponto(point.y()*8+5,point.x()*11+10), char)
        painter.restore()

    def desenhoTela(self, tam):
        s = []
        for i in range(self.height()):
            s.append([self.getChar(Ponto(i, j)) for j in range(self.width())])
            
        return '\n'.join(s)

    def paint(self, painter):
        raise Exception("Metodo abstrato")


class TelaDeviceConsole(PaintDeviceConsole):
    def paint(self, painter):
        painter.drawText(QPoint(3,3), "Aqui")
        

class WidgetConsole(QLabel):
    def __init__(self, parent=None):
        super().__init__("",parent)
        self._tela = TelaDeviceConsole()
        self.resize(80*8+5, 24*11+10)

        CApplication.getInstance().telaAtualizada.connect(self._atualizar) 

    def _atualizar(self):
        tela = CApplication.getScreenshot()
        self._tela.setTela(tela.rstrip('\n')+' ')
        self.update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        self._tela.render(p)
        p.end()


class Filter(QObject):
    def eventFilter(self, obj, evt):
        print("Evento:",obj,evt)
        return False
    
