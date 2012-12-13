#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/base mensageiro/src")

from engineConsole.base.baseApplication import CApplication
from engineConsole.layoutConsole import VLayoutConsole
from servicos.servicoMensageiro import ServicoClienteMensageiro, ServicoServidorMensageiro
from telasMensageiro.telaNome import TelaNome
from telasMensageiro.telaConexao import TelaConexao


cApp = CApplication()

serv = ServicoServidorMensageiro()
s = ServicoClienteMensageiro()
a = TelaConexao(s)
b = TelaNome(s)
l = VLayoutConsole()

l.addTela(70, b)
l.addTela("*", a)
l.show()

cApp.exec_()