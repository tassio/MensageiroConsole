#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from PyQt4.QtCore import QCoreApplication
from engineConsole.base.eventoTeclado import EventoTeclado, EventListener


class MyListener(EventListener):
    def onKey(self, key):
        print("Key:",key)
    def onEnter(self):
        print("Enter")
    def onEscape(self):
        print("Escape")
    def onDirecional(self, direc):
        print("Direcional:",direc)
    def onFuncional(self, func):
        print("Funcional:",func)
    def onEspecial(self, esp):
        print("Especial", esp)
    def onTab(self):
        print("Tab")

app = QCoreApplication([])

l = MyListener()
e = EventoTeclado()
e.addListener(l)
e.start()

app.exec()