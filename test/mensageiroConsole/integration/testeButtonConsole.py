#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.baseApplication import CApplication
from engineConsole.painelConsole import PainelConsole
from engineConsole.buttonConsole import ButtonConsole, CheckBoxConsole,\
    RadioButtonConsole
from engineConsole.spacerConsole import SpacerConsole

cApp = CApplication()

p = PainelConsole()
b = ButtonConsole("BOTAO")
c = CheckBoxConsole("CHECKBOX")
r = RadioButtonConsole("RADIO")

p.addTela(b)
p.addTela(SpacerConsole(3))
p.addTela(c)
p.addTela(SpacerConsole(3))
p.addTela(r)
p.show()

cApp.exec_()
