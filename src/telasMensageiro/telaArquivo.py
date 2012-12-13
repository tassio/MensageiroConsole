# -*- coding: utf-8 -*-
from PyQt4.QtCore import QTimer, pyqtSignal, QFileInfo

from engineConsole.painelConsole import PainelConsole
from networkService.servicos.servicoArquivo import ServicoArquivoEnviar, ServicoArquivoReceber
from engineConsole.layoutConsole import VLayoutConsole
from engineConsole.labelConsole import LabelConsole
from engineConsole.progressBarConsole import ProgressBarConsole
from engineConsole.menuDiretorioConsole import MenuAbrirArquivoConsole,\
    MenuSalvarArquivoConsole
from engineConsole.popupConsole import PopupConsole
from engineConsole.buttonConsole import PainelBotoesConsole


#TODO: Ajustar telaArquivo com base no barraArquivo MensageiroQt
class TelaArquivo(PainelConsole):
    arquivoCancelado = pyqtSignal()
    arquivoFinalizado = pyqtSignal()
    def __init__(self, usuario=None, parent=None):
        super().__init__(parent)

        self._usuario = usuario
        self._servicoEnviar = ServicoArquivoEnviar(40000,40001)
        self._servicoReceber = ServicoArquivoReceber(40001,40000)     

        self._servicoReceber.pedidoReceberArquivo.connect(self._recebendoArquivo)
        self._servicoReceber.porcentagem.connect(self._alterarPorcentagem)
        self._servicoEnviar.porcentagem.connect(self._alterarPorcentagem)
        self._servicoReceber.cancelado.connect(self._estadoCancelado)
        self._servicoEnviar.cancelado.connect(self._estadoCancelado)
        self._servicoReceber.finalizado.connect(self._estadoFinalizado)
        self._servicoEnviar.finalizado.connect(self._estadoFinalizado)

        self._configurarGui()

        self._btnEnviar.enterPressed.connect(self._selecionarArquivoEnviar)
        self._btnReceber.enterPressed.connect(self._selecionarArquivoReceber)
        self._btnCancelar.enterPressed.connect(self.cancelar)

    def _configurarGui(self):
        p = PainelBotoesConsole()
        self._btnEnviar = p.addButton("Enviar")
        self._btnEnviar.setEnabled(self._usuario != None)
        self._btnReceber = p.addButton("Receber")
        self._btnReceber.setEnabled(False)
        self._btnCancelar = p.addButton("Cancelar")
        self._btnCancelar.setVisible(False)

        layoutInformacao = VLayoutConsole()
        self._lblInformacao = LabelConsole()
        layoutInformacao.addTela(50, self._lblInformacao)

        layout = VLayoutConsole()
        self._barraPorcentagem = ProgressBarConsole()
        self._barraPorcentagem.setVisible(False)
        layout.addTela(50, self._barraPorcentagem, "^")

        self.addTela(p)
        self.addTela(layoutInformacao)
        self.addTela(layout)

    def _alterarInformacao(self, texto):
        self._lblInformacao.setTexto(texto)

    def _estadoCancelado(self):
        self.arquivoCancelado.emit()
        self._alterarInformacao("Cancelado")
        QTimer.singleShot(2000, lambda: self._estadoInicial())
        
    def _estadoFinalizado(self):
        self.arquivoFinalizado.emit()
        self._alterarInformacao("Finalizado")
        QTimer.singleShot(2000, lambda: self._estadoInicial())

    def _estadoInicial(self):
        self._alterarPorcentagem(0)
        self._lblInformacao.setTexto("")
        self._btnEnviar.setEnabled(True)
        self._btnReceber.setEnabled(False)
        self._btnCancelar.setVisible(False)
        self._barraPorcentagem.setVisible(False)

    def _recebendoArquivo(self, de, nomeArquivo):
        self._alterarInformacao("Receber -> {0} de {1}".format(nomeArquivo, de))
        self._barraPorcentagem.setVisible(True)
        self._btnEnviar.setEnabled(False)
        self._btnReceber.setEnabled(True)
        self._btnCancelar.setVisible(True)
        
    def _alterarPorcentagem(self, valor):
        self._barraPorcentagem.setPorcentagem(valor)

    def trabalhando(self):
        return self._servicoEnviar.estaEnviandoArquivo() or self._servicoReceber.estaRecebendoArquivo()

    def setUsuario(self, usuario):
        temp = self._usuario
        self._usuario = usuario
        self._servicoEnviar.setPara(self._usuario.getIP())
        
        if not temp:
            self._estadoInicial()

    def cancelar(self):
        if self._servicoEnviar.estaEnviandoArquivo():
            self._servicoEnviar.cancelar()
        elif self._servicoReceber.estaRecebendoArquivo():
            self._servicoReceber.cancelar()

        self._estadoCancelado()

    def _selecionarArquivoEnviar(self):
        m = MenuAbrirArquivoConsole()
        p = PopupConsole(m)
        m.arquivoSelecionado.connect(lambda arq: p.close())
        m.arquivoSelecionado.connect(self.enviarArquivo)
        p.show()

    def enviarArquivo(self, path):
        self._servicoEnviar.enviarArquivo(path, self._usuario.getIP())
        self._alterarInformacao('Enviando '+QFileInfo(path).fileName())
        self._barraPorcentagem.setVisible(True)
        
    def _selecionarArquivoReceber(self):
        m = MenuSalvarArquivoConsole()
        p = PopupConsole(m)
        m.arquivoSelecionado.connect(lambda arq: p.close())
        m.arquivoSelecionado.connect(self.receberArquivo)
        p.show()

    def receberArquivo(self, path):
        self._servicoReceber.aceitarArquivo(path)
        
