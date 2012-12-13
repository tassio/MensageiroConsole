#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.baseApplication import CApplication
from servicos.servicoMensageiro import ServicoClienteMensageiro, ServicoServidorMensageiro
from telasMensageiro.telaNome import TelaNome

cApp = CApplication()

serv = ServicoServidorMensageiro()
s = ServicoClienteMensageiro()
a = TelaNome(s)
a.show()

cApp.exec_()