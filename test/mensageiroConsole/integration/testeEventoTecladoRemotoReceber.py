#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/base mensageiro/src")

from engineConsole.base.baseApplication import CApplication
from engineConsole.telas import LabelEditConsole 
from remoto.eventoTecladoRemoto import EventoTecladoRemotoReceber


cApp = CApplication()
e = EventoTecladoRemotoReceber()
cApp.setEventoTeclado(e)

l = LabelEditConsole("Teste")
l.show()


cApp.exec_()