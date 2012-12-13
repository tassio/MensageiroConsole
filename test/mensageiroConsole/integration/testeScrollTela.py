#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.baseApplication import CApplication
from engineConsole.layoutConsole import VLayoutConsole
from engineConsole.scrollConsole import ScrollTela
from engineConsole.labelConsole import LabelConsole

cApp = CApplication()
vlayout = VLayoutConsole()

label = LabelConsole("ASDASDASDASDTESTANDO TUDO")
scrollTela = ScrollTela(label, 5)

vlayout.addTela(20, scrollTela)

vlayout.show()

cApp.exec_()
