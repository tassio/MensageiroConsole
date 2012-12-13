#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from PyQt4.QtGui import QApplication

from engineConsole.base.baseApplication import CApplication
from engineConsole.telas import LabelEditConsole
from engineConsole.telasTeste.paintDeviceConsole import Filter, WidgetConsole

app = QApplication([])
f = Filter()
app.installEventFilter(f)
cApp = CApplication(app)
#tela = PaintDeviceConsole()
a = LabelEditConsole("Teste")
a.show()

w = WidgetConsole()
w.show()

cApp.exec_()
