#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal

from engineConsole.telas import LabelConsole, ListaTituloConsole
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario


class ItemUsuario(LabelConsole):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        
        self._numConversasNaoVisualizadas = 0

        self.setUsuario(usuario)

    def setUsuario(self, usuario):
        self._usuario = usuario
        self.atualizarTexto()
    
    def getUsuario(self):
        return self._usuario

    def setNumConversasNaoVisualizadas(self, num):
        self._numConversasNaoVisualizadas = num
        self.atualizarTexto()

    def atualizarTexto(self):
        texto = "{0} - {1}".format(self._usuario.getNome(), self._usuario.getIP())
        if self._numConversasNaoVisualizadas > 0:
            texto += " ({0})".format(self._numConversasNaoVisualizadas)
        
        self.setTexto(texto)
    

class TelaUsuarios(ListaTituloConsole):
    usuarioSelecionado = pyqtSignal(Usuario)
    def __init__(self, servico, parent=None):
        super().__init__(titulo=LabelConsole("Usuários", LabelConsole.CENTER), parent=parent)

        self._servico = servico

        self._servico.dadosUsuarioAtualizado.connect(self._atualizarDadosUsuario)
        self.itemSelecionado.connect(self._emitirUsuarioSelecionado)

    def _emitirUsuarioSelecionado(self, item):
        self.usuarioSelecionado.emit(item.getUsuario())

    def addUsuario(self, usuario):
        self.addItem(ItemUsuario(usuario))
        
    def atualizarNumConversasNaoVisualizadas(self, usuario, num):
        self.getItemUsuario(usuario).setNumConversasNaoVisualizadas(num)

    def _atualizarDadosUsuario(self, usuario):
        us = self.getItemUsuario(usuario)
        if not us:
            self.addUsuario(usuario)
        else:
            us.setUsuario(usuario)
        
    def getItemUsuario(self, usuario):
        for i in range(self.quantItens()):
            us = self.getTela(i)
            if us.getUsuario().getIP() == usuario.getIP():
                return us
