#-*- coding: utf-8 -*-
from PyQt4.QtCore import QFileInfo

from engineConsole.painelConsole import PainelConsole
from engineConsole.tabTelaConsole import TabTelaConsole
from engineConsole.spacerConsole import SpacerConsole
from engineConsole.editConsole import TextEditConsole
from engineConsole.menuDiretorioConsole import MenuAbrirArquivoConsole,\
    MenuSalvarArquivoConsole
from engineConsole.popupConsole import PopupConsole
from engineConsole.buttonConsole import PainelBotoesConsole


class EditorDeTextoConsole(PainelConsole):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._configurarGui()
        self._arquivos = []

        self._btnNovo.enterPressed.connect(self._novoArquivo)
        self._btnAbrir.enterPressed.connect(self._abrirArquivo)
        self._btnSalvar.enterPressed.connect(self._salvarArquivo)
        self._btnSalvarComo.enterPressed.connect(self._salvarComoArquivo)
        self._btnFechar.enterPressed.connect(self._fecharArquivo)
        self._btnFecharOutros.enterPressed.connect(self._fecharArquivosNaoVisiveis)

    def _configurarGui(self):
        p = PainelBotoesConsole()
        self._btnNovo = p.addButton("Novo")
        self._btnAbrir = p.addButton("Abrir...")
        self._btnSalvar = p.addButton("Salvar")
        self._btnSalvarComo = p.addButton("Salvar como...")
        self._btnFechar = p.addButton("Fechar")
        self._btnFecharOutros = p.addButton("Fechar outros")
        
        self._tabArquivos = TabTelaConsole()

        self.addTela(p)
        self.addTela(SpacerConsole(1))
        self.addTela(self._tabArquivos)

    def _novoArquivo(self):
        self._tabArquivos.addTela("SEM NOME", TextEditConsole(numLinhas=12))
        self._arquivos.append(None)

    def _abrirArquivo(self):
        m = MenuAbrirArquivoConsole()
        p = PopupConsole(m)
        m.arquivoSelecionado.connect(lambda arq: p.close())
        m.arquivoSelecionado.connect(self.abrirArquivo)
        p.show()

    def abrirArquivo(self, arq):
        if QFileInfo(arq).exists():
            with open(arq, 'r') as arquivo:
                textoArquivo = ''.join(arquivo.readlines())
                
        self._tabArquivos.addTela(QFileInfo(arq).fileName(), TextEditConsole(texto=textoArquivo,numLinhas=12))
        self._arquivos.append(arq)

    def _salvarArquivo(self):
        if not self._tabArquivos.temSelecionado():
            return
        
        if self._arquivos[self._tabArquivos.getSelecionado()] == None:
            self._salvarComoArquivo()
        else:
            arq = self._arquivos[self._tabArquivos.getSelecionado()]
            self.salvarArquivo(arq)
            
    def _salvarComoArquivo(self):
        if not self._tabArquivos.temSelecionado():
            return
        
        m = MenuSalvarArquivoConsole()
        p = PopupConsole(m)
        m.arquivoSelecionado.connect(lambda arq: p.close())
        m.arquivoSelecionado.connect(self.salvarArquivo)
        p.show()

    def salvarArquivo(self, arq):
        with open(arq, 'w') as arquivo:
            arquivo.write(self._tabArquivos.telaVisivel().getTexto())
            
        self._tabArquivos.modificarTitulo(self._tabArquivos.getSelecionado(), QFileInfo(arq).fileName())

    def _fecharArquivo(self):
        if self._tabArquivos.temSelecionado():
            self._arquivos.pop(self._tabArquivos.getSelecionado())
            self._tabArquivos.removeTelaVisivel()

    def _fecharArquivosNaoVisiveis(self):
        if self._tabArquivos.temSelecionado():
            self._tabArquivos.removeTelasNaoVisiveis()


if __name__ == '__main__':
    from engineConsole.base.baseApplication import CApplication

    cApp = CApplication()
    a = EditorDeTextoConsole()
    a.show()
    cApp.exec_()
