#-*- coding: utf-8 -*-
from engineConsole.editConsole import EditConsole
from engineConsole.base.engine import Engine
from engineConsole.scrollConsole import ScrollBarConsole


class TextEditConsole(EditConsole):
    def __init__(self, texto='', desenharBorda=True, numMaxLinhas=6, readOnly=False, parent=None):
        super().__init__(texto, readOnly, parent)
        self._tamanho = 80
        self._desenharBorda = desenharBorda
        self._numMaxLinhas = numMaxLinhas

    def acceptFocus(self):
        return True

    def setNumMaxLinhas(self, num):
        self._numMaxLinhas = max(1, num)

    def getNumMaxLinhas(self):
        return self._numMaxLinhas

    def numCaracteresAteLinha(self, linha):
        return sum(map(lambda t: len(t)+1, self._textoTelaAjustado().split('\n')[:linha]))

    def indColunaAtual(self):
        return self.getPosCursor() - self.numCaracteresAteLinha(self.indLinhaAtual())

    def numColunas(self, linha):
        return len(self.getLinha(linha))-1

    def getLinha(self, i):
        if 0 <= i < self.numLinhas():
            return self._textoTelaAjustado().split('\n')[i]

    def getLinhaAtual(self):
        return self.getLinha(self.linhaAtual())

    def indLinhaAtual(self):
        return self._ajustarTexto(self.getTexto()[:self.getPosCursor()+1]).count('\n')

    def numLinhas(self):
        #Ajustar para quando houver uma linha no final sem texto
        return self._textoTelaAjustado().count('\n')+1

    def setLinhaColuna(self, linha, coluna):
        if linha >= 0 and linha < self.numLinhas():
            coluna = min(self.numColunas(linha)+1, coluna)
            self.setPosCursor(self.numCaracteresAteLinha(linha)+coluna)

    def onDirecional(self, direc):
        linha = self.indLinhaAtual()
        coluna = self.indColunaAtual()
        if direc == Engine.UP:
            self.setLinhaColuna(linha - 1, coluna)              
        elif direc == Engine.DOWN:
            self.setLinhaColuna(linha + 1, coluna)
            
        super().onDirecional(direc)

    def _linhasVisiveis(self, mostrarCursor=True):
        texto = self._textoTelaAjustadoComCursor() if mostrarCursor else self._textoTelaAjustado()
            
        if self.numLinhas() <= self._numMaxLinhas:
            return texto

        linha = self.indLinhaAtual()
        dif = int(self._numMaxLinhas / 2)
        texto = texto.split('\n')
        
        if linha + dif >= self.numLinhas():
            return '\n'.join(texto[max(0,self.numLinhas()-self._numMaxLinhas):])
        elif linha - dif < 0:
            return '\n'.join(texto[:self._numMaxLinhas])
        else:
            return '\n'.join(texto[linha - dif: linha + dif])

    def onEnter(self):
        self.addLetraOnCursor('\n')
        super().onEnter()

    def _textoTelaAjustado(self):
        return self._ajustarTexto(self.getTexto())

    def _textoTelaAjustadoComCursor(self):
        return self._ajustarTexto(self.getTextoComCursor())

    def _ajustarTexto(self, texto):
        n = []
        tam = self._tamanho if not self._desenharBorda else self._tamanho - 2
        for linha in texto.split('\n'):
            for i in range(0, len(linha), tam): 
                n.append(linha[i:min(len(linha), i+tam)])
        return '\n'.join(n)

    def desenhoTela(self, tam):
        self._tamanho = tam
        
        texto = self._linhasVisiveis(self.hasFocus())
        texto += '\n'*(self._numMaxLinhas - texto.count('\n'))
        if self._desenharBorda:
            texto = self._colocarBorda(texto, tam)
            
        return texto


class TextEditScrollConsole(TextEditConsole):
    def __init__(self, texto='', numMaxLinhas=10, readOnly=False, parent=None):
        super().__init__(texto, numMaxLinhas=numMaxLinhas, readOnly=readOnly, parent=parent)

        self._scrollBar = ScrollBarConsole(numMaxLinhas+1, 0, orientacao=ScrollBarConsole.VERTICAL)
        self._scrollBar.valorScrollModificado.connect(self._modificarLinhaAtual)
        self.posCursorAlterado.connect(lambda pos: self._alterarScrollBar())

    def focusNextChild(self):
        if self._scrollBar.hasFocus():
            return False

        if self.hasFocus():
            self._scrollBar.setFocus()
        else:
            self.setFocus()
        return True
    
    def focusPreviousChild(self):
        if self.hasFocus():
            return False

        if self._scrollBar.hasFocus():
            self.setFocus()
        else:
            self._scrollBar.setFocus()
        return True

    def indexChildActive(self):
        if self.hasFocus():
            return 0
        elif self._scrollBar.hasFocus():
            return 1
        else:
            return -1

    def _modificarLinhaAtual(self, valor):
        self.setLinhaColuna(int(self.getNumMaxLinhas() / 2)+valor, self.indColunaAtual())

    def _alterarScrollBar(self):
        self._scrollBar.setAteValor(max(0, self.numLinhas()-self.getNumMaxLinhas()))
        self._scrollBar.setValorAtual(self.indLinhaAtual()-int(self.getNumMaxLinhas() / 2))

    def desenhoTela(self, tam):
        s = ''
        scroll = ''
        for i in self._scrollBar.desenhoTelaConsole(tam).split('\n'):
            scroll += "{0}|\n".format(i)
        scroll = "-|\n{0}-|".format(scroll).split('\n')
        
        tela = super().desenhoTela(tam-3).split('\n')
        for i in range(len(tela)):
            s += "{0}{1}\n".format(tela[i], scroll[i])

        if s.endswith('\n'):
            s = s[:len(s)-1]

        return s
