#-*- coding: utf-8 -*-
import sys
sys.path.append(r"C:\Users\Tassio\Downloads\MensageiroCore\src")
sys.path.append(r"C:\Users\Tassio\Downloads\EngineConsole\src")
sys.path.append(r"C:\Users\Tassio\Downloads\NetworkService\src")

from engineConsole.painelConsole import PainelConsole
from engineConsole.layoutConsole import VLayoutConsole
from engineConsole.spacerConsole import SpacerConsole

from telasMensageiro.telaNome import TelaNome
from telasMensageiro.telaArquivo import TelaArquivo
from telasMensageiro.telaConexao import TelaConexao
from telasMensageiro.telaUsuarios import TelaUsuarios
from telasMensageiro.telaConversa import TelaConversa

from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro


class MensageiroConsole(PainelConsole):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._servico = ServicoClienteMensageiro()

        self._configurarGui()
        self._telaUsuarios.usuarioSelecionado.connect(self._selecionarUsuario)
        self._telaConversa.conversasNaoVisualizadas.connect(self._telaUsuarios.atualizarNumConversasNaoVisualizadas)
        
    def _configurarGui(self):
        layoutNomeConexao = VLayoutConsole()
        self._telaConexao = TelaConexao(self._servico)
        self._telaNome = TelaNome(self._servico)
        layoutNomeConexao.addTela(65, self._telaConexao)
        layoutNomeConexao.addTela("*", self._telaNome)

        self._telaArquivo = TelaArquivo()

        layoutListaConversa = VLayoutConsole()
        self._telaUsuarios = TelaUsuarios(self._servico)
        self._telaConversa = TelaConversa(self._servico)
        layoutListaConversa.addTela(40, self._telaUsuarios)
        layoutListaConversa.addTela("*", self._telaConversa)
        
        self.addTela(layoutNomeConexao)
        self.addTela(SpacerConsole(1))
        self.addTela(self._telaArquivo)
        self.addTela(SpacerConsole(1))
        self.addTela(layoutListaConversa)
        
    def _selecionarUsuario(self, usuario):
        self._telaConversa.setUsuario(usuario)
        self._telaArquivo.setUsuario(usuario)


if __name__ == '__main__':
    from engineConsole.base.baseApplication import CApplication
    
    cApp = CApplication()
    m = MensageiroConsole()
    m.show()
    cApp.exec_()
