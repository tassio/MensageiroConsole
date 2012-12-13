# -*- coding: utf-8 -*-
from engineConsole.buttonConsole import ButtonConsole
from engineConsole.listaConsole import ListaTituloConsole
from engineConsole.labelConsole import LabelConsole
from engineConsole.popupConsole import PopupConsole
from mensageiroCore.servicos.informacao.informacaoMensageiro import Status



class TelaConexao(ButtonConsole):
    def __init__(self, servico, parent=None):
        super().__init__(parent)

        self._servico = servico
        self._servico.conectado.connect(self.atualizarConexao)

        self.enterPressed.connect(self._abrirStatusPopup)
        self._atualizarTexto()
        
    def atualizarConexao(self, con):
        self._atualizarTexto()

    def _atualizarTexto(self):
        status = self._servico.getStatus() if self._servico.estaConectado() else Status(Status.OFFLINE)
        self.setTexto(str(status))

    def _abrirStatusPopup(self):
        if not self._servico.estaConectado():
            return
        
        l = ListaTituloConsole(titulo=LabelConsole("STATUS", LabelConsole.CENTER))
        for i in Status.STATUS:
            l.addItem(LabelConsole(i))
            if i == str(self._servico.getStatus()):
                l.setIndexSelecionado(l.quantItens()-1)

        popup = PopupConsole(l)
        popup.show()
        
        l.itemSelecionado.connect(lambda status: self._mudarStatus(status.getTexto()))
        l.itemSelecionado.connect(lambda status: popup.close())

    def _mudarStatus(self, status):
        self._servico.setStatus(Status.getInstance(status))
        self._atualizarTexto()
