#-*- coding: utf-8 -*-
import sys
sys.path.append(r"C:\Users\Tassio\Downloads\MensageiroCore\src")
sys.path.append(r"C:\Users\Tassio\Downloads\EngineConsole\src")
sys.path.append(r"C:\Users\Tassio\Downloads\NetworkService\src")


from mensageiroCore.servicos.servicoMensageiro import ServicoServidorMensageiro

from engineConsole.telas import PainelConsole
from telasMensageiro.telaUsuarios import TelaUsuarios


class ServidorMensageiroConsole(PainelConsole):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._servico = ServicoServidorMensageiro()

        self._configurarGui()

    def _configurarGui(self):
        self._lista = TelaUsuarios(self._servico)
        self.addTela(self._lista)


if __name__ == '__main__':
    from engineConsole.base.baseApplication import CApplication
    cApp = CApplication()
    serv = ServidorMensageiroConsole()
    serv.show()
    cApp.exec_()
