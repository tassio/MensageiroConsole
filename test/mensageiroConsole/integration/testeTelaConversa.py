#-*- coding: utf-8 -*-
import sys
sys.path.append("D:/Documents and Settings/Tassio/Meus documentos/Tassio/Informatica/Python/mensageiro novo/base mensageiro/src")
sys.path.append("D:/Documents and Settings/Tassio/Meus documentos/Tassio/Informatica/Python/mensageiro novo/mensageiroConsole/src")

from servicos.servicoMensageiro import ServicoClienteMensageiro, ServicoServidorMensageiro
from engineConsole.base.baseApplication import CApplication
from telasMensageiro.telaConversa import TelaConversa
from servicos.informacaoMensageiro import Usuario

cApp = CApplication()

cli = ServicoClienteMensageiro()
serv = ServicoServidorMensageiro()

b = TelaConversa(cli)
b.setUsuario(Usuario("ABS", "TESTE","127.0.0.1"))
b.show()

cApp.exec_()