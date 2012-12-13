#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")

from engineConsole.base.baseApplication import CApplication
from servicos.servicoMensageiro import ServicoServidorMensageiro, ServicoClienteMensageiro
from telasMensageiro.telaUsuarios import TelaUsuarios

cApp = CApplication()

s = ServicoServidorMensageiro()
sc = ServicoClienteMensageiro()
t = TelaUsuarios(sc)
t.show()

cApp.exec_()