# -*- coding: utf-8 -*-

from PyQt4.QtCore import QTimer, pyqtSignal, pyqtSlot

from engineConsole.labelConsole import LabelConsole
from engineConsole.editConsole import EditConsole, TextEditConsole
from engineConsole.base.engine import EngineConsole
from engineConsole.painelConsole import PainelConsole
from engineConsole.tabTelaConsole import StackedWidgetConsole
from engineConsole.spacerConsole import SpacerConsole

from networkService.servicos.servicoConversa import ServicoConversa
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario


NOME_DEFAULT = "<SEM NOME>"


class TelaSituacao(LabelConsole):
    def __init__(self, usuario, parent=None):
        super().__init__(parent=parent)

        self._usuario = usuario

    def setUsuario(self, usuario):
        self._usuario = usuario
        self.update()

    def getUsuario(self):
        return self._usuario

    def setSituacao(self, sit):
        if sit == TelaEditEnviar.VAZIO:
            self.setTexto('')
        else:
            self.setTexto("{0} está {1}...".format(self._usuario.getNome(), TelaEditEnviar.SITUACOES[int(sit)]))


class TelaEditEnviar(EditConsole):
    VAZIO = "0"
    DIGITANDO = "1"
    APAGANDO = "2"
    SITUACOES = ["","digitando","apagando"]
    
    situacaoModificada = pyqtSignal(str)
    textoDigitado = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._situacao = TelaEditEnviar.VAZIO

        self.enterPressed.connect(self.enviarTexto)

    def _modificarSituacao(self, sit):
        if self._situacao != sit:
            self._situacao = sit
            self.situacaoModificada.emit(sit)

    def _analisarSituacao(self):
        if len(self.getTexto()) == 0:
            self._modificarSituacao(TelaEditEnviar.VAZIO)

    def clear(self):
        self.setTexto('')
        self._modificarSituacao(TelaEditEnviar.VAZIO)

    def enviarTexto(self):
        texto = self.getTexto().strip(' ')
        if texto:
            self.textoDigitado.emit(texto)
            self.clear()

    def onKey(self, key):
        numChars = len(self.getTexto())
        
        super().onKey(key)
        
        if numChars > 0 and len(self.getTexto()) == 0 and key != EngineConsole.ENTER:
            self._modificarSituacao(TelaEditEnviar.APAGANDO)
            QTimer.singleShot(2000, lambda: self._analisarSituacao())
        elif numChars == 0 and len(self.getTexto()) > 0:
            self._modificarSituacao(TelaEditEnviar.DIGITANDO)

    def desenhoTela(self, tam):
        if self.getTexto() == '' and not self.hasFocus():
            return "DIGITE AQUI UMA MENSAGEM"
        else:
            return super().desenhoTela(tam)
            

class TelaEditReceber(TextEditConsole):
    def __init__(self, parent=None):
        super().__init__(6, parent=parent)
        
        self.setReadOnly(True)

    def receberTexto(self, nome, texto):
        self.appendTexto('{0} diz: {1}\n'.format(nome, texto))


class TelaConversaUsuario(PainelConsole):
    conversasNaoVisualizadas = pyqtSignal(Usuario, int)
    def __init__(self, servico, usuario, parent=None):
        super().__init__(parent)
        self._configurarGui()
        
        self._numConversasNaoVisualizadas = 0

        self._servico = servico
        self._usuario = None
        self.setUsuario(usuario)

        self._servico.informacaoTipoValorRecebida.connect(self._receberSituacao)
        self._servico.conversaRecebida.connect(self._receberConversa)
        self._editEnviar.situacaoModificada.connect(self._enviarSituacao)
        self._editEnviar.textoDigitado.connect(self._enviarConversa)

    def _configurarGui(self):
        self._lblUsuario = LabelConsole(parent=self)
        self._editReceber = TelaEditReceber(parent=self)
        self._lblSituacao = TelaSituacao(None,parent=self)
        self._editEnviar = TelaEditEnviar(parent=self)

        self.addTela(self._lblUsuario)
        self.addTela(self._editReceber)
        self.addTela(self._lblSituacao)
        self.addTela(self._editEnviar)

    def atualizarUsuario(self, usuario):
        if self._usuario.getIP() == usuario.getIP():
            self.setUsuario(usuario)

    def setUsuario(self, usuario):
        if not self._usuario or self._usuario.getNome() != usuario.getNome():
            nomeAntigo = self._usuario and self._usuario.getNome() or NOME_DEFAULT
            self._editReceber.setTexto(self._editReceber.getTexto().replace(nomeAntigo, usuario.getNome()))

        self._usuario = usuario
        self._servico.setPara(self._usuario.getIP())
        self._lblSituacao.setUsuario(usuario)
        self._lblUsuario.setTexto("{0} - {1} - {2}".format(usuario.getNome(), usuario.getStatus(), usuario.getIP()))

    def getUsuario(self):
        return self._usuario

    def _receberSituacao(self, de, tipo, valor):
        if tipo == ServicoConversa.INFORMACAO and de == self._usuario.getIP():
            self._lblSituacao.setSituacao(valor['informacao'])
            
    def atualizarNumConversasNaoVisualizadas(self, num):
        self._numConversasNaoVisualizadas = num
        self.conversasNaoVisualizadas.emit(self._usuario, self._numConversasNaoVisualizadas)

    def _receberConversa(self, de, inf):
        if de == self._usuario.getIP():
            self._editReceber.receberTexto(self._usuario.getNome(), inf)
            
            # Emitindo sinal para mostrar as conversas não visualizadas pelo usuário
            if not self.isVisible():
                self.atualizarNumConversasNaoVisualizadas(self._numConversasNaoVisualizadas + 1)

    def receberTexto(self, texto):
        self._editReceber.receberTexto(self._usuario.getNome(), texto)

    def _enviarSituacao(self, sit):
        self._servico.enviarInformacaoConversa(sit)

    def _enviarConversa(self, conv):
        self._servico.enviarConversa(conv)
        self._editReceber.receberTexto(self._servico.getNome(), conv)


class TelaConversa(PainelConsole):
    conversasNaoVisualizadas = pyqtSignal(Usuario, int)
    def __init__(self, servico, parent=None):
        super().__init__(parent)
        self._configurarGui()

        self._servico = servico
        self._servico.dadosUsuarioAtualizado.connect(self.atualizarUsuario)
        self._servico.conversaRecebida.connect(self._receberConversa)

    def _receberConversa(self, de, inf):
        usuario = Usuario(nome=NOME_DEFAULT, ip=de)
        if not self.temConversaUsuario(usuario):
            telaConversaUsuario = TelaConversaUsuario(self._servico, usuario)
            telaConversaUsuario.conversasNaoVisualizadas.connect(self._emitirConversasNaoVisualizadas)
            telaConversaUsuario.receberTexto(inf)
            self._stackedLayout.addTela(telaConversaUsuario)

    def _configurarGui(self):
        self._stackedLayout = StackedWidgetConsole()
        self.addTela(self._stackedLayout)
        
        #Tela inicial
        self._mostrarTelaInicial()

    def _mostrarTelaInicial(self):
        painel = PainelConsole()
        painel.addTela(SpacerConsole(2))
        painel.addTela(LabelConsole("<- Selecione o Usuário"))
        self._stackedLayout.addTela(painel)
        
    @pyqtSlot(Usuario, int)
    def _emitirConversasNaoVisualizadas(self, usuario, num):
        self.conversasNaoVisualizadas.emit(usuario, num)

    def atualizarUsuario(self, usuario):
        ind = self.indexTelaConversa(usuario)
        if ind != -1:
            self._stackedLayout.getChild(ind).atualizarUsuario(usuario)

    def setUsuario(self, usuario):
        ind = self.indexTelaConversa(usuario)
        if ind == -1:
            t = TelaConversaUsuario(self._servico, usuario)
            t.conversasNaoVisualizadas.connect(self._emitirConversasNaoVisualizadas)
            self._stackedLayout.addTela(t)
            ind = self._stackedLayout.numTelas()-1
        else:
            self.atualizarUsuario(usuario)
            
        self._stackedLayout.setVisivel(ind)
        self._stackedLayout.getChild(ind).atualizarNumConversasNaoVisualizadas(0)

    def indexTelaConversa(self, usuario):
        for i in range(1, self._stackedLayout.numTelas()):
            if self._stackedLayout.getChild(i).getUsuario().getIP() == usuario.getIP():
                return i

        return -1

    def temConversaUsuario(self, usuario):
        return self.indexTelaConversa(usuario) != -1
