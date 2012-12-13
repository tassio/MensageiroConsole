#-*- coding: utf-8 -*-
import sys
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/mensageiroConsole/src")
sys.path.append("C:/Users/infox/My Documents/Aptana Studio 3 Workspace/base mensageiro/src")

from engineConsole.base.baseApplication import CApplication
from servicos.informacaoMensageiro import Usuario
from telasMensageiro.telaArquivo import TelaArquivo


cApp = CApplication()
a = TelaArquivo(Usuario("Teste", "qwe", "127.0.0.1"))
a.show()
cApp.exec_()
