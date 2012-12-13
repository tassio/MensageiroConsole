#-*- coding: utf-8 -*-

from engineConsole.telas import PainelDiretorioConsole
from remoto.baseApplicationRemoto import CApplicationEnviar

cApp = CApplicationEnviar()
p = PainelDiretorioConsole()
p.show()
cApp.exec_()